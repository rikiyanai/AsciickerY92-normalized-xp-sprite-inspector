Require python3

Set Shell "zsh"
Set FontSize 18
Set Width 1000
Set Height 700
Set Padding 14
Set TypingSpeed 1ms
Set Theme "Catppuccin Mocha"

Hide
Type "./run-viewer.sh --source-key player-1100-L3 --compact" Enter
Wait+Screen /SOURCE LAYER CONTRACT VIEWER/
Type " "
Wait+Screen /frame 1/
Show
Sleep 160ms
Screenshot "@@BUILD_DIR@@/01-armor-selected.png"
Sleep 160ms

# Advance through the three real animation frames before changing layer.
Type "n"
Wait+Screen /frame 2/
Sleep 160ms
Screenshot "@@BUILD_DIR@@/02-animation-frame-2.png"
Sleep 160ms
Type "n"
Wait+Screen /frame 3/
Sleep 160ms
Screenshot "@@BUILD_DIR@@/03-animation-frame-3.png"
Sleep 160ms

Type "."
Wait+Screen /angle 2/
Sleep 160ms
Screenshot "@@BUILD_DIR@@/04-armor-angle-2.png"
Sleep 160ms

Type "r"
Wait+Screen /projection 2/
Sleep 160ms
Screenshot "@@BUILD_DIR@@/05-armor-projection-2.png"
Sleep 160ms

Type "]"
Wait+Screen /player-1100 · L4 · frame/
Sleep 160ms
Screenshot "@@BUILD_DIR@@/06-helmet-selected.png"
Sleep 160ms
Type "v"
Wait+Screen /HIDDEN-FROM-STACK/
Sleep 160ms
Screenshot "@@BUILD_DIR@@/07-helmet-hidden.png"
Sleep 160ms
Type "v"
Wait+Screen /INCLUDED/
Sleep 160ms
Screenshot "@@BUILD_DIR@@/08-helmet-restored.png"
Sleep 160ms
Type "]"
Wait+Screen /L0/
Sleep 160ms
Screenshot "@@BUILD_DIR@@/09-layer-l0-metadata.png"
Sleep 160ms
Type "]"
Wait+Screen /L1/
Sleep 160ms
Screenshot "@@BUILD_DIR@@/10-layer-l1-metadata.png"
Sleep 160ms
Type "]"
Wait+Screen /L2/
Sleep 160ms
Screenshot "@@BUILD_DIR@@/11-layer-l2-body.png"
Sleep 160ms
Type "."
Type "n"
Wait+Screen /frame 2 · angle 2/
Sleep 160ms
Screenshot "@@BUILD_DIR@@/12-angle-and-frame-changed.png"
Sleep 160ms
Type "}"
Wait+Screen /SOURCE LAYER CONTRACT VIEWER/
Sleep 160ms
Screenshot "@@BUILD_DIR@@/13-next-xp-stem.png"
Sleep 160ms

Hide
Type "q"
