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

## P0C-03 · 2026-08-12 — product question before visual-proof replacement

- **Question:** What must a replacement GIF let a reviewer see without trusting
  terminal typing or a prose claim?
- **Answer:** It must show the real `player-1100.xp` L2-L4 composition, with
  armor owned by L3 and helmet owned by L4, alongside the focused body region,
  angle-specific cells, and atlas UV panel. It must also show at least two
  meaningful inspection states (not merely the launch command or an idle frame)
  while keeping the standalone read-only boundary visible.

## P0C-03 · 2026-08-12 — first armored GIF capture was unreadable at README scale

- The real VHS capture reached the alternate-screen inspector and executed the
  intended armor/helmet navigation, but its 1800×1080 canvas reduced the
  terminal labels and source-layer evidence to an unreadable size when viewed
  as README media.
- This is a visual-proof failure, not a product failure: the capture does not
  yet meet the question's “let a reviewer see” criterion. The successor keeps
  the same launcher and interactive states while using a tighter canvas that
  still fits the three-panel UV/body surface and all-angle grid.

## P0C-03 · 2026-08-12 — readable armored inspector recording verified

- `docs/armored-inspector.gif` is generated from the committed VHS recipe with
  the real interactive launcher running behind an initial capture hide. The
  GIF begins on the alternate-screen inspector, not a typed startup command.
- Decoded visual inspection confirms the composed sprite/UV surface, armor's
  all-angle `source L3` grid, and helmet's all-angle `source L4` grid after
  angle navigation. The recipe uses only view navigation and quit.
- The automated contract validates that exact recipe shape, renders the same
  L3/L4 states from packaged evidence, parses the GIF image blocks, and proves
  that it contains multiple distinct visual frames. This supports **Verified**
  for the artifact/recipe regression surface; human product acceptance remains
  a separate gate.

## P0C-03 · 2026-08-12 — reviewer found five GIF-proof defects before merge

- **Semantic artifact proof was weak:** the contract counted encoded LZW image
  payload differences. Those byte differences prove neither decoded/composited
  visual states nor the specific armored source ownership shown to a reviewer.
- **Recipe proof was under-specified:** it checked only a few substrings rather
  than parsing the command/Enter/Wait/Show order, exact transitions, quit,
  capture dimensions, or an upper artifact-size limit.
- **Ownership legend was distributed:** the composed screen names
  `player-1100` and L2-L4 composition, while individual grids identify L3 or
  L4. A persistent label must make `L2 base + L3 armor + L4 helmet` legible
  without relying on crop or inference.
- **Claims were not precise enough:** README and this log called the GIF
  “decoded” and “verified” without identifying the exact checked frames,
  visual fingerprints, and reproducibility conditions.
- **Reproducibility lacked a version condition:** the recipe named VHS but did
  not record the generator version or define what visual differences are
  tolerated on regeneration.

The successor must fix all five proof defects in the staged GIF, tape, README,
failure log, and contract only; it must not alter the product viewer.

## P0C-03 · 2026-08-12 — persistent-label render first failed at font resolution

- The intended no-crop lower-canvas ownership label did not render because this
  ImageMagick build cannot resolve the requested `Menlo` font through Freetype.
  The command exited before replacing `docs/armored-inspector.gif`; no visual
  proof claim is made from it.
- The successor must query an installed named font, record it in the recipe,
  and re-run the same lower-canvas label operation. It must then decode the
  final GIF in the standard-library contract rather than depending on the
  image tool used for production inspection.

## P0C-03 · 2026-08-12 — second persistent-label render proved Freetype absent

- Supplying an explicit system-font path also failed: this ImageMagick build
  has no Freetype delegate, so no font path can render annotation text. Again,
  the command exited before replacing the staged GIF.
- The successor may use a bounded image-library overlay only to render the
  fixed ownership caption into the already-captured frames. Product-state
  capture remains VHS-driven, and all committed artifact verification must
  remain dependency-free in `tests/test_contract.py`.

## P0C-03 · 2026-08-12 — first Pillow caption encode lost intermediate state fidelity

- Pillow successfully rendered the persistent lower caption, but its optimized
  delta-frame output did not preserve all intermediate redraw states when
  re-opened: the helmet transition contained a partial frame and a later full
  frame did not correspond to the expected navigation state. The artifact is
  rejected despite keeping the requested dimensions and label.
- The successor must regenerate the unmodified VHS capture, composite every
  decoded frame, burn in the label, and save full frames without delta
  optimization. File size may grow within a documented bound; state fidelity is
  the governing requirement.

## P0C-03 · 2026-08-12 — reviewer-proof remediation passes the bounded artifact gate

- The committed proof artifact is GIF89a, 1320×720, 9 fully composited frames,
  and 660871 bytes. Its exact SHA-256 is
  `bc7f3d5cfdeead4a992890172e9d8c2fbd18ef2ca1f898e35c1e0ee75705af19`.
- `docs/armored-inspector.tape` records VHS 0.11.0 and the exact hidden-launch
  sequence: real launcher, Enter, `Wait+Screen`, Show, armor grid, helmet grid,
  changed angle, and quit. `vhs validate` accepts that recipe.
- The committed artifact carries a persistent lower-canvas label—outside the
  terminal product surface—naming `player-1100.xp | L2 base + L3 armor + L4
  helmet`. It preserves the uncropped composed sprite/UV view and makes the
  fixed ownership fact visible in every reviewed frame.
- The current contract dependency-freely parses GIF blocks, LZW-decodes and
  composites frames, then binds the exact binary plus four semantic frame and
  caption-band hashes: composed UV/body, L3 armor grid, L4 helmet grid, and
  L4 changed-angle grid. This supersedes the earlier weaker “multiple encoded
  payloads” proof claim.
- Reproducibility condition: only VHS 0.11.0's recorded interactive route is
  treated as the capture recipe. A different renderer may rasterize differently;
  do not update the committed byte/state hashes without a manual re-audit of all
  four named frames and intentional review of the changed artifact.

## P0C-03 · 2026-08-12 — contact-sheet audit rejects post-quit shell frame

- A full contact-sheet audit found that the final GIF frame returns to the shell
  after `q`. It visibly shows `./run-inspector.sh` and lacks the persistent
  `player-1100.xp | L2 base + L3 armor + L4 helmet` caption.
- This invalidates the prior frame-count/hash proof: selected semantic frames
  passed, but the artifact as a whole still contains a hidden-command boundary
  violation. Do not submit that GIF.
- The successor must issue `Hide` before quit, regenerate, and prove that every
  decoded/composited frame has the product caption and no frame exposes the
  launcher or shell surface.

## P0C-03 · 2026-08-12 — hidden-quit successor passes all-frame product audit

- `Hide` now precedes `q` in the VHS recipe, so the interactive inspector exits
  cleanly while recording stops before shell restoration. The regenerated
  artifact is GIF89a, 1320×720, 8 composited frames, and 661449 bytes with
  SHA-256 `c230fd945a973ef8d48d789a5e076138c8898619dc7eecb7205e5040e802a5ba`.
- The contact sheet was inspected across all eight frames. Each is a captioned
  inspector state; none is a shell or launch-command surface. The prior
  nine-frame hash and artifact claim are superseded and remain rejected history.
- The dependency-free contract now hashes every fully composited product frame
  and every 1320×50 caption crop, in addition to the four semantic states. This
  makes a post-quit shell or missing caption a test failure rather than a
  selected-frame blind spot.

## P0C-03 · 2026-08-12 — review rejects non-idempotent raw-tape overwrite path

- The VHS tape still writes directly to `docs/armored-inspector.gif`, but the
  accepted artifact also requires an out-of-band Pillow caption pass. Re-running
  the tape therefore overwrites a valid captioned proof with an uncaptioned raw
  capture before any verification can stop it.
- This is a reproducibility and idempotency defect, not a rendering defect. The
  successor needs a committed single regeneration command: VHS writes only a
  temporary raw artifact; a pinned recording-only Pillow step captions a
  temporary final; the all-frame product contract verifies it; only then may an
  atomic replace publish `docs/armored-inspector.gif`.

## P0C-03 · 2026-08-12 — first raw-intermediate tape path did not parse

- VHS 0.11.0 rejected the unquoted absolute `Output /tmp/...` path as separate
  tape tokens, so no raw capture or captioned candidate was produced and the
  committed GIF was untouched.
- The successor keeps the same `/tmp` destination but quotes it according to
  the tape grammar, then validates the recipe before relying on the new pipeline.

## P0C-03 · 2026-08-12 — first atomic regeneration rejected nonreproducible bytes

- The new pipeline wrote only `/tmp` raw output, captioned a temporary candidate,
  and correctly refused to replace the accepted GIF because its SHA-256 differed
  from the committed baseline. The atomic guard therefore preserved the prior
  accepted artifact.
- Exact output bytes are not yet reproducible across two valid VHS captures.
  The successor must compare decoded all-frame and caption evidence, identify
  whether the difference is temporal/container-only or perceptual, and make the
  publish gate honest: exact hash only if repeatable, otherwise a documented
  semantic/perceptual contract with manual-review requirements for new bytes.

## P0C-03 · 2026-08-12 — first semantic-metric probe did not execute

- The first comparison command used GNU-only `find -printf` on macOS and loaded
  the decoder module without registering it in `sys.modules`; the dataclass
  import consequently failed before it could inspect either GIF.
- It produced no artifact judgment and did not touch the accepted proof. The
  successor uses the committed regenerator's module-loading pattern and
  portable file discovery before defining the visual gate.

## P0C-03 · 2026-08-12 — first coarse-fingerprint serialization was invalid

- The follow-up comparison established that matching capture states differ in
  no more than 6 of 660 coarse luminance cells, but its first digest attempt
  serialized 0–25500 luminance values directly as bytes and failed range
  validation before producing reference fingerprints.
- The evidence supports a bounded perceptual gate, but this failed serializer
  is not used. The successor normalizes each cell to an 8-bit luminance bin,
  records the resulting decoded-frame fingerprints, and keeps the accepted GIF
  untouched until that contract passes.

## P0C-03 · 2026-08-12 — byte-identical VHS regeneration was falsified

- Two consecutive valid VHS captures followed the same recipe but were not
  byte- or pixel-identical. Matching product states retained approximately
  93–98% RGB-channel equality, and their complete contact sheets were visually
  equivalent. Exact VHS bytes are therefore not an honest reproducibility gate.
- The accepted artifact remained untouched while that hypothesis was tested.
  Exact hashes continue to detect later changes to a committed GIF, while a
  regeneration must instead pass bounded decoded visual similarity for every
  frame, all four required semantic states, and the persistent caption.

## P0C-03 · 2026-08-12 — atomic semantic regeneration path executed

- The committed tape now writes only
  `/tmp/p0c03-armored-inspector.raw.gif`. The executable regenerator requires
  VHS 0.11.0 and recording-only Pillow 12.1.0, captions a temporary candidate,
  rejects frames outside the accepted inspector surface, maps all four required
  states by a bounded coarse-luminance comparison, and verifies every caption
  band before publishing.
- A full execution produced a 1320×720, five-frame, 422997-byte GIF with
  SHA-256 `20fe289dfefbf7447a6a0e8b2919f26f4eae4143aef4c68d6d2cc07038e744ae`.
  The five-frame contact sheet contains only captioned product screens:
  composed UV/body, L3 armor grid, L4 helmet UV/body, L4 helmet grid, and the
  changed-angle L4 grid. No launcher or restored shell is present.
- The regenerator published the GIF and
  `docs/armored-inspector.contract.json`; the latter binds the exact binary,
  every decoded/composited frame, every caption crop, and the four semantic
  frame indices. The complete suite then passed 12 of 12 tests. VHS timing is
  allowed to vary only inside the semantic/perceptual gate; personal visual
  acceptance remains separate.

## P0C-03 · 2026-08-12 — clean-copy regeneration caught a transient redraw frame

- Final review copied the exact staged tree to a clean temporary directory and
  ran the pinned regenerator. VHS completed, but the candidate contained six
  frames and one was an incomplete armor-grid redraw. Its closest coarse-
  luminance difference from any accepted complete state was 6.876, above the
  2.0 product-frame limit; the other five frames differed by only 0.02–0.03.
- The guard correctly preserved the accepted artifact, but this falsifies the
  claim that the current single command reliably completes. The successor must
  discard transient redraw frames before publication, still require every
  retained frame to match the accepted product surface, and still prove all
  four complete semantic states are present. Repeated clean executions, not one
  lucky capture, are required before closure.

## P0C-03 · 2026-08-12 — final review broke the first perceptual gate

- Executable counterexamples proved that the first 33×20 luminance matcher was
  not state- or color-faithful. It accepted a candidate with no changed-angle
  frame by assigning the helmet grid and changed-angle requirements to the same
  frame; it also accepted a candidate without the composed view by mapping that
  requirement to the helmet-body view.
- A fully grayscale copy of every accepted frame also passed. Luminance alone
  cannot prove the colored base/armor/helmet composition, and semantic indices
  must be distinct and ordered in the recipe's actual state sequence.
- Tests inspected regenerator source strings but did not execute the verifier
  against these counterexamples. The successor needs per-channel RGB matching,
  distinct ordered state assignment, and executable missing-state/grayscale
  rejection tests.
- The first pair publish also replaced the GIF before its receipt. An injected
  failure on the second replace could leave the tracked proof mismatched. The
  successor needs a recoverable two-file publish with an injected-failure test
  proving both originals are restored.

## P0C-03 · 2026-08-12 — strengthened regeneration survives repeated execution

- The successor filters incomplete redraw frames, then uses a per-channel RGB
  33×20 comparison with a 0.5 mean-absolute-difference ceiling. The four
  semantic states must map to distinct, ordered frames. Executable adversarial
  tests now reject candidates missing the composed or changed-angle state and
  reject a fully grayscale copy of the accepted frames.
- GIF and receipt publication now keeps recoverable backups of both owners. An
  injected failure on the receipt replace restores both original files; the
  test verifies their exact bytes after rollback.
- Two consecutive full pinned regeneration commands completed, each followed
  by the complete suite. Both retained five complete captioned product states;
  the artifact bytes differed as expected from VHS timing, while all RGB,
  semantic-order, caption, and exact-receipt checks passed. The final run is
  1320×720, five frames, 447689 bytes, SHA-256
  `d274143ad212fe3c226c8f3790de0d949e8a664e567af460d3534b7281360be5`.
- Final contact-sheet inspection confirms composed UV/body, L3 armor grid, L4
  helmet UV/body, L4 helmet grid, and changed-angle L4 grid; every frame retains
  the player-1100/L2/L3/L4 caption and none exposes a shell. The suite passes 14
  of 14 tests. Personal visual acceptance remains blank.

## P0C-03 · 2026-08-12 — first recording-test CI cache had no dependency owner

- Final re-review found that `actions/setup-python@v5` enabled pip caching while
  the repository has only `requirements-test.txt`. Without an explicit
  `cache-dependency-path`, setup-python searches its default requirements or
  project metadata patterns and can fail before the test dependency install.
- The workflow must bind the cache to `requirements-test.txt`; passing local
  tests cannot substitute for a clean GitHub Actions setup path.
