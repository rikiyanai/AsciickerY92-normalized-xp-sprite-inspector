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
Sleep 2s
Type "g"
Sleep 2s

# Return to the full UV/body view, then advance from armor to helmet.
Type "g"
Type "r"
Sleep 2s

# The helmet's all-angle grid reveals its distinct L4 source ownership.
Type "g"
Sleep 2s
Type "d"
Sleep 2s
# Quit cleanly without recording the restored shell prompt or launch command.
Hide
Type "q"
