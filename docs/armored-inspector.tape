# Capture engine: VHS 0.11.0. The launcher is deliberately hidden so the GIF
# begins on the alternate-screen inspector rather than terminal typing.
#
# This tape writes only a raw /tmp artifact. The committed captioned proof is
# owned by scripts/regenerate_armored_inspector_gif.py, which verifies it before
# atomically replacing docs/armored-inspector.gif.
Output "/tmp/p0c03-armored-inspector.raw.gif"
Set FontSize 18
Set Width 1320
Set Height 720
Set Theme "Dracula"
Set TypingSpeed 1ms

Hide
Type "./run-inspector.sh"
Enter
Wait+Screen /Anchor review: player-1100-anchors.json/
Show

# Default focus is the reviewed armor overlay: source L3 in the next state.
Sleep 1s
Type "g"
Sleep 1s

# Return to the full UV/body view, enter the reviewed eight-frame animation,
# then play three adjacent frames with the viewer's real frame-navigation
# control before moving from armor to helmet.
Type "g"
Sleep 1s
Type "s"
Sleep 1s
Type "."
Sleep 1s
Type "."
Sleep 1s
Type "r"
Sleep 1s

# The helmet's all-angle grid reveals its distinct L4 source ownership.
Type "g"
Sleep 1s
Type "d"
Sleep 1s
# Quit cleanly without recording the restored shell prompt or launch command.
Hide
Type "q"
