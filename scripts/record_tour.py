#!/usr/bin/env python3
"""Record a captioned GIF walkthrough of either viewer, without VHS.

Runs the real viewer in a pseudo-terminal, presses the keys from a storyboard,
renders the terminal screen with Pillow, and writes an animated GIF with a
caption bar naming the key and what it shows.

    python3 scripts/record_tour.py inspector docs/recordings/uv-map-inspector-tour.gif
    python3 scripts/record_tour.py viewer    docs/recordings/source-layer-viewer-tour.gif

Recording-only dependencies: Pillow and pyte (see docs/requirements-recording.txt).
"""

from __future__ import annotations

import argparse
import fcntl
import os
import pty
import re
import select
import signal
import struct
import sys
import termios
import textwrap
import time
from pathlib import Path

import pyte
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
FONT_CANDIDATES = [
    ("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
     "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"),
    ("/System/Library/Fonts/Menlo.ttc", "/System/Library/Fonts/Menlo.ttc"),
    ("C:/Windows/Fonts/consola.ttf", "C:/Windows/Fonts/consolab.ttf"),
]
FONT_PATH, FONT_BOLD_PATH = next(
    (pair for pair in FONT_CANDIDATES if Path(pair[0]).exists()),
    FONT_CANDIDATES[0],
)

BG = (24, 24, 32)
FG = (220, 220, 228)
CAPTION_BG = (40, 42, 56)
INSET_BG = (32, 33, 44)
INSET_W = 380
KEY_BG = (250, 200, 80)
KEY_FG = (20, 20, 20)

ANSI_NAMES = {
    "black": (0, 0, 0), "red": (205, 49, 49), "green": (13, 188, 121),
    "brown": (229, 229, 16), "yellow": (229, 229, 16), "blue": (36, 114, 200),
    "magenta": (188, 63, 188), "cyan": (17, 168, 205), "white": (229, 229, 229),
    "brightblack": (102, 102, 102), "brightred": (241, 76, 76),
    "brightgreen": (35, 209, 139), "brightbrown": (245, 245, 67),
    "brightyellow": (245, 245, 67), "brightblue": (59, 142, 234),
    "brightmagenta": (214, 112, 214), "brightcyan": (41, 184, 219),
    "brightwhite": (255, 255, 255),
}

# Storyboards: (keys to send, seconds to hold, caption). Keys are sent, then
# the screen is sampled for the hold time so autoplay animation is captured.
DOWN, RIGHT = "\x1b[B", "\x1b[C"


# --- Reading the live screen: where the sprite box is, and what state it shows.

def inspector_zoom(lines: list[str]):
    """Sprite box in the inspector: rows under the 0123456 column header."""
    for y, line in enumerate(lines[:30]):
        m = re.search(r"0123\d*", line[:30])
        if m:
            h = 0
            while y + 1 + h < len(lines) and re.match(r"\|\s+\d{2}\s", lines[y + 1 + h]):
                h += 1
            return (m.start(), y + 1, m.end() - m.start(), h)
    return None


def inspector_label(lines: list[str]) -> list[str]:
    text = "\n".join(lines)
    m = re.search(r"angle (\d+)\s+anim (\d+) frame (\d+)/(\d+)\s+cursor \((\d+),(\d+)\) region=(\S+)", text)
    focus = re.search(r"Region(?: grid)?: (\w+)", text)
    if not m:
        return []
    angle, anim, frame, frames, cx, cy, region = m.groups()
    return [
        f"angle {int(angle) + 1} of 8",
        f"animation {anim}  frame {int(frame) + 1} of {frames}",
        f"focused region: {focus.group(1) if focus else '-'}",
        f"cursor ({cx},{cy}): {region}",
    ]


def viewer_zoom(lines: list[str]):
    """Sprite box in the source-layer viewer: rows between its title and the evidence block."""
    start = next((y for y, l in enumerate(lines) if l.startswith("-- DISPLAY-ONLY") or re.match(r"-- \S+-L\d+ ", l)), None)
    end = next((y for y, l in enumerate(lines) if l.startswith("-- IMMUTABLE")), None)
    if start is None or end is None or end <= start + 1:
        return None
    return (0, start + 1, 16, end - start - 2)


def viewer_label(lines: list[str]) -> list[str]:
    head = " ".join(lines[:2])
    m = re.search(r":: (\S+) ==\s+XP (\d+)/(\d+)\s+layer (\d+)/\d+\s+angle (\d+)\s+projection \d+\s+frame (\d+)\s+view=(\w+)", head)
    if not m:
        return []
    stem, xp, xps, layer, angle, frame, view = m.groups()
    hand = next((l.strip() for l in lines if l.startswith("hand[")), "")
    hm = re.match(r"hand\[(\w+)\]: '?(.*?)'?$", hand)
    out = [
        f"{stem}  L{int(layer) - 1}",
        f"angle {int(angle) + 1}   frame {int(frame) + 1}",
        f"view: {view.lower()}",
    ]
    if hm and hm.group(1) != "not_applicable_engine_metadata":
        out.append(f"hand: {hm.group(1)}")
        out += ["  " + part for part in textwrap.wrap(hm.group(2).strip(), 24)[:5]]
    elif hm:
        out.append("engine metadata layer")
    return out


INSPECTOR = {
    "cmd": ["./run-inspector.sh"],
    "size": (126, 40),
    "ready": "Standalone inspector is read-only",
    "zoom": inspector_zoom,
    "label": inspector_label,
    "steps": [
        ("", 3.5, "player-1100 (armour + helmet). Left: sprite. Middle: one body region. Right: UV map of atlas coordinates"),
        (RIGHT, 0.5, "→  move the cursor: the UV map highlights its atlas cell; the label names its region"),
        (RIGHT, 0.5, "→  move the cursor: the UV map highlights its atlas cell; the label names its region"),
        (RIGHT, 1.2, "→  move the cursor: the UV map highlights its atlas cell; the label names its region"),
    ]
    + [(DOWN, 1.0, "↓  walk the cursor down the body: helmet, face, armour")] * 6
    + [("r", 1.3, "r  cycle the focused body region")] * 8
    + [
        ("p", 7.0, "p  autoplay: the sprite turns through all 8 angles"),
        ("p", 0.4, "p  autoplay off"),
        ("s", 0.8, "s  switch to the walk animation"),
    ]
    + ([(".", 0.18, ".  walk cycle, frame by frame")] * 8 + [("d", 0.3, "d  turn to the next angle")]) * 8
    + [
        ("g", 4.5, "g  region grid: the armour region in every angle (columns) and frame (rows)"),
        ("r", 3.5, "r  same grid for the next region"),
        ("g", 1.5, "g  back to the UV map"),
    ],
}

VIEWER = {
    "cmd": ["./run-viewer.sh", "--source-key", "player-1100-L3"],
    "size": (150, 68),
    "ready": "SOURCE LAYER CONTRACT VIEWER",
    "zoom": viewer_zoom,
    "label": viewer_label,
    # Before recording: single-frame detail view, selected layer shown inside
    # the full sprite stack. Autoplay stays on, so frames keep animating.
    "setup": ["g", "c"],
    "steps": [
        ("", 5.0, "player-1100 L3 (armour) in the finished sprite, animating. Below: hand label, cell-role grid, layer table"),
        ("x", 7.0, "x  autoplay axis: now turning through the angles"),
        ("x", 3.0, "x  back to playing the animation frames"),
        ("c", 3.5, "c  isolated: only this layer's cells"),
        ("c", 1.5, "c  back to the full stack"),
        ("]", 4.5, "]  next layer: L4 helmet, with its own hand label and reviewed cell roles"),
        ("v", 2.5, "v  hide this layer from the finished sprite"),
        ("v", 1.5, "v  show it again"),
        ("[", 0.6, "[  previous layer"),
        ("[", 5.0, "[  L2 base body. Hand label: reject. The note records what is actually drawn here"),
    ]
    + [("}", 0.12, "}  browse through the 115 sprites")] * 49
    + [
        ("]", 0.4, "]  step past the L0/L1 engine metadata layers"),
        ("]", 6.0, "wolfie-0110 L2: hand label partial. The mount layer also carries the rider's torso and shield"),
        ("x", 6.0, "x  turn the wolf through its angles"),
        ("x", 2.0, "x  back to animation frames"),
        ("}", 0.4, "}  next sprite"),
        ("]", 0.3, "]  skip metadata layers"),
        ("]", 6.0, "wolfie-0111 L2: another partial, with its own hand note"),
    ],
}

STORYBOARDS = {"inspector": INSPECTOR, "viewer": VIEWER}


def colour(value: str, default: tuple[int, int, int]) -> tuple[int, int, int]:
    if value == "default":
        return default
    if value in ANSI_NAMES:
        return ANSI_NAMES[value]
    if len(value) == 6:
        try:
            return tuple(int(value[i:i + 2], 16) for i in (0, 2, 4))  # type: ignore[return-value]
        except ValueError:
            pass
    return default


class Renderer:
    def __init__(self, cols: int, rows: int, font_size: int = 14) -> None:
        self.cols, self.rows = cols, rows
        self.font = ImageFont.truetype(FONT_PATH, font_size)
        self.bold = ImageFont.truetype(FONT_BOLD_PATH, font_size)
        self.cap_font = ImageFont.truetype(FONT_BOLD_PATH, font_size + 1)
        left, top, right, bottom = self.font.getbbox("M")
        self.cw = int(round(self.font.getlength("M")))
        self.ch = int(font_size * 1.25)
        self.pad = 12
        self.cap_h = self.ch + 18
        self.term_w = cols * self.cw + 2 * self.pad
        self.inset_w = INSET_W
        self.width = self.term_w + self.inset_w
        self.height = rows * self.ch + 2 * self.pad + self.cap_h
        self.label_font = ImageFont.truetype(FONT_BOLD_PATH, font_size + 6)
        self.title_font = ImageFont.truetype(FONT_BOLD_PATH, font_size + 1)

    def render(
        self,
        screen: pyte.Screen,
        caption: str,
        zoom: tuple[int, int, int, int] | None = None,
        label: list[str] | None = None,
    ) -> Image.Image:
        img = Image.new("RGB", (self.width, self.height), BG)
        d = ImageDraw.Draw(img)
        for y in range(self.rows):
            line = screen.buffer[y]
            for x in range(self.cols):
                ch = line[x]
                fg = colour(ch.fg, FG)
                bg = colour(ch.bg, BG)
                if ch.reverse:
                    fg, bg = bg, fg
                x0 = self.pad + x * self.cw
                y0 = self.pad + y * self.ch
                x1, y1 = x0 + self.cw, y0 + self.ch
                if bg != BG:
                    d.rectangle([x0, y0, x1 - 1, y1 - 1], fill=bg)
                c = ch.data
                if c == " " or not c:
                    continue
                # Draw block elements as exact rectangles so sprites have no seams.
                if c == "█":
                    d.rectangle([x0, y0, x1 - 1, y1 - 1], fill=fg)
                elif c == "▀":
                    d.rectangle([x0, y0, x1 - 1, y0 + self.ch // 2 - 1], fill=fg)
                elif c == "▄":
                    d.rectangle([x0, y0 + self.ch // 2, x1 - 1, y1 - 1], fill=fg)
                elif c == "▌":
                    d.rectangle([x0, y0, x0 + self.cw // 2 - 1, y1 - 1], fill=fg)
                elif c == "▐":
                    d.rectangle([x0 + self.cw // 2, y0, x1 - 1, y1 - 1], fill=fg)
                else:
                    d.text((x0, y0 + 1), c, font=self.bold if ch.bold else self.font, fill=fg)
        self._draw_inset(img, d, zoom, label or [])
        # Caption bar: key chip + description.
        cy = self.height - self.cap_h
        d.rectangle([0, cy, self.width, self.height], fill=CAPTION_BG)
        key, _, text = caption.partition("  ")
        tx = self.pad
        if text and len(key) <= 3:
            kw = int(self.cap_font.getlength(key)) + 16
            d.rounded_rectangle([tx, cy + 7, tx + kw, cy + self.cap_h - 7], radius=5, fill=KEY_BG)
            d.text((tx + 8, cy + 9), key, font=self.cap_font, fill=KEY_FG)
            tx += kw + 12
        else:
            text = caption
        d.text((tx, cy + 9), text, font=self.cap_font, fill=(240, 240, 245))
        return img


    def _draw_inset(self, img, d, zoom, label) -> None:
        """Right-hand panel: the sprite box enlarged, with a live state label."""
        x0 = self.term_w
        d.rectangle([x0, 0, self.width, self.height - self.cap_h], fill=INSET_BG)
        d.text((x0 + 20, 16), "SPRITE BOX (live)", font=self.title_font, fill=(170, 170, 190))
        if zoom is None:
            return
        cx, cy, cw, chh = zoom
        crop = img.crop((
            self.pad + cx * self.cw, self.pad + cy * self.ch,
            self.pad + (cx + cw) * self.cw, self.pad + (cy + chh) * self.ch,
        ))
        avail_w = self.inset_w - 40
        avail_h = self.height - self.cap_h - 60 - 34 * (len(label) + 1)
        scale = max(1, min(avail_w // max(1, crop.width), avail_h // max(1, crop.height), 6))
        big = crop.resize((crop.width * scale, crop.height * scale), Image.Resampling.NEAREST)
        bx = x0 + (self.inset_w - big.width) // 2
        by = 48
        d.rectangle([bx - 3, by - 3, bx + big.width + 2, by + big.height + 2], outline=(90, 90, 120), width=2)
        img.paste(big, (bx, by))
        ty = by + big.height + 22
        for i, line in enumerate(label):
            colour_ = (250, 200, 80) if i == 0 else (235, 235, 245)
            d.text((x0 + 20, ty), line, font=self.label_font, fill=colour_)
            ty += 34


class Session:
    def __init__(self, cmd: list[str], cols: int, rows: int) -> None:
        self.screen = pyte.Screen(cols, rows)
        self.stream = pyte.ByteStream(self.screen)
        env = dict(os.environ, TERM="xterm-256color", COLUMNS=str(cols), LINES=str(rows))
        pid, fd = pty.fork()
        if pid == 0:
            os.chdir(ROOT)
            os.execvpe(cmd[0], cmd, env)
        fcntl.ioctl(fd, termios.TIOCSWINSZ, struct.pack("HHHH", rows, cols, 0, 0))
        self.pid, self.fd = pid, fd

    def pump(self, seconds: float) -> None:
        end = time.monotonic() + seconds
        while True:
            remaining = end - time.monotonic()
            if remaining <= 0:
                return
            ready, _, _ = select.select([self.fd], [], [], remaining)
            if ready:
                try:
                    data = os.read(self.fd, 65536)
                except OSError:
                    return
                if not data:
                    return
                self.stream.feed(data)

    def settle(self, quiet: float = 0.05, limit: float = 0.5) -> None:
        """Keep reading until output pauses, so a frame is never captured mid-redraw."""
        end = time.monotonic() + limit
        while time.monotonic() < end:
            ready, _, _ = select.select([self.fd], [], [], quiet)
            if not ready:
                return
            try:
                data = os.read(self.fd, 65536)
            except OSError:
                return
            if not data:
                return
            self.stream.feed(data)

    def text(self) -> str:
        return "\n".join(self.screen.display)

    def send(self, keys: str) -> None:
        os.write(self.fd, keys.encode())

    def close(self) -> None:
        try:
            self.send("q")
            self.pump(0.5)
        finally:
            try:
                os.kill(self.pid, signal.SIGTERM)
            except ProcessLookupError:
                pass
            os.waitpid(self.pid, 0)


def record(board: dict, out: Path, sample: float = 0.1) -> None:
    cols, rows = board["size"]
    sess = Session(board["cmd"], cols, rows)
    rend = Renderer(cols, rows)
    deadline = time.monotonic() + 20
    while board["ready"] not in sess.text():
        if time.monotonic() > deadline:
            sess.close()
            raise SystemExit(f"viewer never showed {board['ready']!r}")
        sess.pump(0.2)
    sess.pump(0.8)
    for keys in board.get("setup", []):
        sess.send(keys)
        sess.pump(0.6)

    frames: list[Image.Image] = []
    durations: list[int] = []
    for keys, hold, caption in board["steps"]:
        if keys:
            sess.send(keys)
        t = 0.0
        while t < hold - 1e-6:
            step = min(sample, hold - t)
            sess.pump(step)
            sess.settle()
            t += step
            lines = sess.screen.display
            img = rend.render(sess.screen, caption, board["zoom"](lines), board["label"](lines))
            ms = int(round(step * 1000))
            if frames and img.tobytes() == frames[-1].tobytes():
                durations[-1] += ms
            else:
                frames.append(img)
                durations.append(ms)
    sess.close()
    durations[-1] += 1500  # pause before the loop restarts

    out.parent.mkdir(parents=True, exist_ok=True)
    # One shared palette (built from a sample of frames) so unchanged pixels keep
    # the same index and the GIF stores only what changed between frames.
    picks = frames[:: max(1, len(frames) // 12)][:12]
    sheet = Image.new("RGB", (frames[0].width, frames[0].height * len(picks)))
    for i, f in enumerate(picks):
        sheet.paste(f, (0, i * f.height))
    palette = sheet.quantize(colors=255, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
    pal = [f.quantize(palette=palette, dither=Image.Dither.NONE) for f in frames]
    pal[0].save(out, save_all=True, append_images=pal[1:], duration=durations, loop=0, optimize=True, disposal=1)
    print(f"{out}: {len(frames)} frames, {sum(durations) / 1000:.1f}s, {out.stat().st_size / 1e6:.2f} MB")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("which", choices=sorted(STORYBOARDS))
    ap.add_argument("out", type=Path)
    args = ap.parse_args()
    record(STORYBOARDS[args.which], args.out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
