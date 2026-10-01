#!/bin/sh
set -eu

repo_root=$(CDPATH= cd -- "$(dirname "$0")/.." && pwd)
tape_template="$repo_root/docs/recordings/source-layer-contract-viewer.tape"
gif_path="$repo_root/docs/recordings/source-layer-contract-viewer.gif"
build_dir=$(mktemp -d "${TMPDIR:-/tmp}/source-layer-contract-viewer.XXXXXX")

cleanup() {
    rm -f -- \
        "$build_dir/01-armor-selected.png" \
        "$build_dir/02-animation-frame-2.png" \
        "$build_dir/03-animation-frame-3.png" \
        "$build_dir/04-armor-angle-2.png" \
        "$build_dir/05-armor-projection-2.png" \
        "$build_dir/06-helmet-selected.png" \
        "$build_dir/07-helmet-hidden.png" \
        "$build_dir/08-helmet-restored.png" \
        "$build_dir/09-layer-l0-metadata.png" \
        "$build_dir/10-layer-l1-metadata.png" \
        "$build_dir/11-layer-l2-body.png" \
        "$build_dir/12-angle-and-frame-changed.png" \
        "$build_dir/13-next-xp-stem.png" \
        "$build_dir/capture.tape" \
        "$build_dir/source-layer-contract-viewer.gif"
    rmdir "$build_dir" 2>/dev/null || true
}
trap cleanup EXIT HUP INT TERM

command -v vhs >/dev/null 2>&1 || {
    echo "FAIL: vhs is required" >&2
    exit 2
}
command -v magick >/dev/null 2>&1 || {
    echo "FAIL: ImageMagick is required" >&2
    exit 2
}

sed "s|@@BUILD_DIR@@|$build_dir|g" "$tape_template" > "$build_dir/capture.tape"
(cd "$repo_root" && vhs "$build_dir/capture.tape")

set -- \
    "$build_dir/01-armor-selected.png" \
    "$build_dir/02-animation-frame-2.png" \
    "$build_dir/03-animation-frame-3.png" \
    "$build_dir/04-armor-angle-2.png" \
    "$build_dir/05-armor-projection-2.png" \
    "$build_dir/06-helmet-selected.png" \
    "$build_dir/07-helmet-hidden.png" \
    "$build_dir/08-helmet-restored.png" \
    "$build_dir/09-layer-l0-metadata.png" \
    "$build_dir/10-layer-l1-metadata.png" \
    "$build_dir/11-layer-l2-body.png" \
    "$build_dir/12-angle-and-frame-changed.png" \
    "$build_dir/13-next-xp-stem.png"
for frame_path do
    test -s "$frame_path" || {
        echo "FAIL: missing captured state: $frame_path" >&2
        exit 2
    }
done

magick -delay 18 "$@" -loop 0 "$build_dir/source-layer-contract-viewer.gif"
mv -f -- "$build_dir/source-layer-contract-viewer.gif" "$gif_path"
magick identify "$gif_path"
