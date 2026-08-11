# Failure Log

## P0C-03 · 2026-08-11 — repository created; unsafe extraction refused

- The private repository and product boundary were created.
- The parent `xp_uv_body_viewer.py` combined read-only browsing with mutation
  surfaces, so it was not copied wholesale.

## P0C-03 · 2026-08-12 — read-only extraction implemented

- Reused the parser-only XP read model and wrote a standalone terminal viewer
  with no serialization authority.
- Added exact JSON output, no-write tests, a real terminal recording, and
  package-relative sample data.
- The product is runnable and locally verified; user acceptance remains a
  separate gate.

## P0C-03 · 2026-08-12 — acceptance re-audit found a product substitution

- Intended product: a standalone normalized-XP UV/body inspector with a
  judgeable relationship between sprite content and the UV/body inspection
  surface, while retaining no mutation authority.
- Observed result: the executable shows a 7x9 glyph frame and generic
  layer/animation/frame/angle counters. It contains no UV/body model, labels,
  mapping, or inspection evidence.
- The deleted GIF accurately showed the proxy, but therefore did not prove the
  intended product.
- Highest supported stage: **Implemented and Executed proxy only**. The intended
  UV/body inspector is not Implemented, Verified, or Accepted.
- The rejected `.tape` recipe was deleted because it could only recreate proof
  of the proxy; the intended UV/body outcome must be defined before recapture.

## P0C-03 · 2026-08-12 — first real-viewer hardening patch did not apply

- The actual upstream viewer and its bounded dependencies were copied for the
  replacement attempt, but the first hardening patch expected a batch-function
  docstring that differs from the inspected source. `apply_patch` rejected the
  whole edit; the copied files remained byte-identical to their source owners.
- No read-only or product-completion claim is made from that failed patch. The
  successor is split into source-exact, individually verifiable hunks.

## P0C-03 · 2026-08-12 — first extracted-viewer execution failed dependency resolution

- `./run-inspector.sh --once` failed before rendering because the imported
  helper set resolved to `None` and `_require_y9_helpers()` rejected execution.
- This run supplies no UV/body evidence. The successor inspects each packaged
  import directly before changing the dependency boundary.

## P0C-03 · 2026-08-12 — actual UV/body surface replaced the proxy

- Product question answered before implementation: this repository must let an
  operator inspect how a reviewed normalized-XP sprite frame, semantic body
  regions, and atlas UV coordinates relate to one another. A generic frame
  preview cannot satisfy that requirement.
- Copied the real `xp_uv_body_viewer.py`, its bounded parser/semantic helpers,
  `player-0100.xp`, its anchor map, and evidence cards from their recorded source
  owners. `./run-inspector.sh --once` then rendered the real sprite, focused
  region, angle-region grid, and UV-coordinate panels.
- The upstream viewer also contains authoring, save, decision-capture, and batch
  mutation behavior. The standalone replacement adds fail-closed guards and
  blocks the corresponding interactive keys. Those guards must be tested
  directly; ordinary navigation alone is not proof that the repository is
  read-only.
- The old generic adapter, parser copy, and `player-nude.xp` demo are deleted so
  there is only one executable product owner.
- Current highest stage before the successor test run: **Executed**. Verification
  and any new visual proof remain open until the real surface and all mutation
  guards pass together.

## P0C-03 · 2026-08-12 — first replacement contract run failed two over-exact assertions

- `python3 -m unittest discover -s tests -v` passed direct save rejection,
  review-decision rejection, batch-mutation rejection, and proxy-removal checks,
  but failed 2 of 5 tests.
- The non-TTY assertion expected `interactive mode requires a TTY`; the real
  anchor-review surface reports `anchor review requires a TTY`.
- The screen assertion expected only the sprite basename and uppercase
  `READ-ONLY`; the source-owned anchor correctly displays its recorded relative
  reference path and the screen says `Standalone inspector is read-only`.
- The rendered output did contain the actual sprite panel, focused
  `subcell_fill` region, atlas UV map, region list, and mutation-blocking text.
  The successor relaxes only the two brittle string assumptions and re-runs the
  complete contract; this failed run is not counted as verification.

## P0C-03 · 2026-08-12 — default fixture changed to prove the layered contract

- User acceptance feedback required an armored sprite that visibly exercises
  more layers. The prior `player-0100.xp` fixture has four layers but exposes
  only one reviewed overlay above its L2 base.
- Replaced it with `player-1100.xp` and its matching
  `player-1100-anchors.json`. This normalized fixture has five layers and
  recorded regions for L2 base, L3 armor, and L4 helmet.
- The inspection screen now composes L2-L4 in ordinal engine order, starts on
  the armor region, labels the composed range, and makes the all-angle region
  grid read the focused region's recorded source layer. This change targets the
  observable product requirement; layer count alone is not treated as proof.

## P0C-03 · 2026-08-12 — dormant write implementations removed

- The first fail-closed extraction still retained unreachable upstream anchor
  save and batch-write implementations after immediate guards. It also retained
  the generic dump mode's `--out` file writer. Runtime guard tests proved those
  specific entry points were blocked, but dead disk-mutation code was an
  unnecessary authority and audit ambiguity.
- Removed the temporary-file/replace implementations and the `--out` option.
  JSON dump mode now writes only to stdout. Added a source-level absence check
  for the removed disk-write primitives in addition to runtime rejection tests.
- This is a hardening correction, not a retroactive claim that the earlier
  guarded version had passed the stronger no-write-source condition.

## P0C-03 · 2026-08-12 — armored UV/body replacement contract passes

- `python3 -m py_compile scripts/xp_uv_body_viewer.py` passes.
- `python3 -m unittest discover -s tests -v` passes 8 of 8 tests against
  the actual `player-1100.xp` UV/body surface, L2-L4 composition, recorded
  L3/L4 armor and helmet ownership, protected input hashes, direct save and
  decision rejection, batch rejection, removed output-file authority, and
  deleted proxy artifacts.
- Highest directly supported stage: **Verified** for the automated standalone
  read-only contract. Personal visual/GIF acceptance remains open; no GIF is
  manufactured from this test result.

## P0C-03 · 2026-08-12 — first combined pre-commit audit command did not run

- The shell rejected the combined diff/status/secret-scan command with
  `parse error near ')'` because the regular expression's nested quote escaping
  was malformed. None of that command's checks are credited.
- The successor runs structural checks and secret patterns as separate commands
  with shell-safe quoting before any commit or push.

## P0C-03 · 2026-08-12 — first replacement commit blocked by copied CRLF source

- `git diff --cached --check` rejected the commit before Git created it because
  every line of copied upstream `scripts/pipeline/sprite_errors.py` retained a
  carriage return and was reported as trailing whitespace.
- No commit or push occurred. The successor normalizes line endings in that one
  dependency, reruns compile and all product contracts, then repeats the staged
  diff check.
