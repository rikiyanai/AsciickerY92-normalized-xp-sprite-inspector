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

## P0C-03 · 2026-08-12 — generic repository name hid the Asciicker Y9-2 owner

- `normalized-xp-sprite-inspector` named the data format and tool but not the
  Asciicker Y9-2 product whose normalized player sprite and layer contract it
  inspects. The user selected `AsciickerY92-normalized-xp-sprite-inspector` as
  the standalone repository identity.
- README naming is corrected first; local-directory and private GitHub rename
  remain one coordinated publication step so remotes and parent records cannot
  point at different names.

## P0C-03 · 2026-08-12 — rename state and README surface corrected

- The local checkout, GitHub repository, and `origin` now all use
  `AsciickerY92-normalized-xp-sprite-inspector`. The earlier "remain one
  coordinated publication step" sentence is stale history, not current state.
- The README keeps the product GIF and source/provenance pointer, but removes
  front-page failure-log bookkeeping. The failure log remains the durable audit
  surface for rejected and revoked claims.

## P0C-03 · 2026-08-31 — animation-proof and evidence-index successor started

- Requirement: the public proof must show the real normalized XP/body viewer
  moving through adjacent animation frames while retaining explicit region and
  angle navigation; the repository must also expose its packaged XP, anchor,
  and review evidence without copying frozen inputs.
- Current owners are `scripts/xp_uv_body_viewer.py`,
  `docs/armored-inspector.tape`,
  `scripts/regenerate_armored_inspector_gif.py`, and the existing contract
  JSON. The stale owners are the README's five-state wording and the absence of
  a dedicated historical-evidence index.
- The successor is limited to documentation, recording recipe, recording
  assembly/contract, tests, and provenance indexes. It does not change the
  viewer's read-only authority or packaged XP bytes.
- This attempt is **Implemented** only until the new recipe, decoded GIF, full
  test suite, link checks, and bounded visual inspection pass.

## P0C-03 · 2026-08-31 — first animation-state filter rejected adaptive-palette grouping

- The first successor implementation grouped captioned GIF frames by encoded
  frame hashes. Pillow's per-frame adaptive palettes changed those bytes even
  when the decoded terminal canvas was the same, so the expected nine stable
  capture runs were reported as zero.
- The command exited before publication and preserved the prior accepted GIF.
  The falsifier was a decoded coarse-RGB run probe over the raw VHS artifact,
  which recovered the expected nine stable state runs.
- The successor moved stable-state selection before captioning and now groups
  decoded raw canvases by their visible coarse-RGB fingerprint.

## P0C-03 · 2026-08-31 — seven-state animation walkthrough verified

- The canonical VHS route now reaches the real animation group with `s`, steps
  through three adjacent frames with `.`, then records the armor grid, helmet
  grid, and changed-angle state. The launcher remains hidden until the viewer
  title is rendered, and `Hide` remains before quit.
- The regenerator selected seven stable raw canvases, captioned them, rejected
  missing or duplicate semantic states, and atomically published the GIF and
  contract. The accepted artifact is 1320×720, 7 frames, 652461 bytes, and
  SHA-256 `df3207e0b4f9edf920b44db3581e8607313061ddc31913305e45d2a74ca2a397`.
- Contract semantic states are composed UV/body, L3 armor grid, animation
  frames 1–3, L4 helmet grid, and L4 changed-angle grid. The contact sheet and
  representative frame previews show the ownership caption on every frame and
  no shell surface.
- `python3 -m unittest discover -s tests -v` passes 16 of 16 tests. The highest
  supported stage is **Verified** for the automated recording contract and
  bounded visual proof; personal acceptance remains separate.
- Prepared About description: “Read-only Asciicker Y9-2 normalized REXPaint XP
  sprite inspector for reviewed body regions, layer ownership, UV coordinates,
  and animation frames.”

## P0C-03 · 2026-08-31 — seven-state GIF and one-fixture corpus claim rejected by operator

- Operator correction: the previous status overstated the README/GIF update.
  The requirement was not merely to link a GIF. The GIF script must regenerate
  a faster, broader walkthrough that shows real frame progression, and the repo
  must make the packaged XP corpus viewable rather than hiding behind one
  focused fixture.
- The successor expands `assets/sprites/` to the full 115 packaged XP files,
  updates `docs/historical-evidence/manifest.json` to bind every XP hash, keeps
  hand-entered labels and review notes tracked through
  `docs/research/ascii/semantic_maps/layer_evidence_cards.jsonl`, changes the
  GIF generator to an eight-state 0.18-second sequence, and adds an every-XP
  raw-layer dump regression.
- This entry rejects the earlier seven-state completion claim until the
  regenerated GIF is opened in Finder, tests pass, the diff is reviewed, and a
  new commit is pushed.

## P0C-03 · 2026-08-31 — eight-state faster inspector GIF and full XP corpus verified

- The corrected repository state packages all 115 XP inputs under
  `assets/sprites/`, updates `docs/historical-evidence/manifest.json` with each
  XP path and SHA-256, and keeps the hand-entered anchors/review cards under
  `docs/research/ascii/semantic_maps/` as the historical evidence owner.
- The regenerated `docs/armored-inspector.gif` shows eight semantic viewer
  states: composed UV/body, L3 armor grid, animation group, two adjacent
  animation frames, projection change, L4 helmet grid, and L4 helmet
  angle/frame change. The artifact is 1320×720, 8 frames, 764,261 bytes,
  SHA-256
  `ba8748e6d86485edd82a959938612a910a2e40abc982dba47def5693c7ad6d7c`,
  with an 18-centisecond delay per frame.
- Verification performed in-session: `./scripts/regenerate_armored_inspector_gif.py`
  completed, `python3 -m unittest discover -s tests -v` passed 17/17, the
  every-XP raw-layer dump regression exercised all 115 packaged files, the GIF
  was revealed in Finder with `open -R`, and a bounded contact-sheet preview
  was visually inspected.
- Highest supported stage: **Verified** for regenerated GIF behavior, full
  packaged XP viewability, and hand-labeled evidence reachability. Operator
  acceptance remains separate.


---

# Source-layer viewer development history (imported unchanged)

# Failure Log

## P0C-05 / FL-4162 · 2026-08-11 — standalone read-only extraction

- Pinned parser-only source to pipeline-v3 commit `7fdecabf...`.
- Resolved exactly 115 XP inputs from the frozen shard manifest.
- Excluded mutation-capable XP core, recorder, queue, comparison, compiler, and
  anchor surfaces.
- One-screen output was tested; headed recording and user acceptance remained
  pending.

## P0C-05 / FL-4162 · 2026-08-12 — standalone provenance and recording completed

- Replaced the live absolute Desktop provenance path with a non-resolving
  historical-source label while preserving its source hash.
- Added a real terminal recording linked from the README and a regression test
  for the path boundary.
- Automated execution is verified; user acceptance remains separate.

## P0C-05 / FL-4162 · 2026-08-12 — acceptance re-audit revoked visual proof

- Intended product: a readable, read-only Source Layer Contract Viewer over the
  exact 115-XP / 573-layer frozen corpus.
- Direct execution still validates the corpus and reaches the intended viewer.
  The product implementation was not replaced by a different proxy.
- The deleted GIF used a 1440x900 terminal at 13px and changed grid, stack, and
  highlight modes without making those transitions legible at README scale.
- Highest supported stage: **Executed with automated contract verification**;
  visual verification and user acceptance are open.
- The rejected `.tape` recipe was deleted because its fixed 13px capture would
  recreate the same illegible proof; readability must be designed before recapture.

## P0C-05 / FL-4162 · 2026-08-12 — raw armored-layer search over-returned ledger data

- Re-establishing the recording surface correctly selected the five-layer
  `player-1100` asset: L2 body, L3 armor, and L4 helmet expose the contract
  composition more clearly than the default metadata layer.
- A broad `rg` across the full-cell JSONL shards also matched the enormous
  coordinate-decision record and over-returned hundreds of kilobytes before the
  output guard truncated it. Only the bounded source-review rows are usable
  evidence from that attempt.
- Further inspection must query exact indexed fields or exercise the viewer
  read model; raw full-ledger lines are not an acceptable diagnostic or visual
  proof surface.

## P0C-05 / FL-4162 · 2026-08-12 — first compact-surface test command discovered zero tests

- Running `python3 -m unittest -v` from the repository root reported
  `Ran 0 tests`; this layout does not make the `tests/` directory an
  implicit unittest module.
- The result proves nothing and is not counted. Verification must use explicit
  discovery with `python3 -m unittest discover -s tests -v`, then inspect the
  compact armored surface separately.

## P0C-05 / FL-4162 · 2026-08-12 — first GIF contact-sheet inspection over-returned

- The valid VHS run produced a 1000×700, 10.84-second, 271-frame GIF, and a
  bounded 960×1344 JPEG contact sheet sampled its state changes.
- The first image-view call nevertheless attempted to return the full 73 KB
  contact sheet inline and was blocked by the context guard. No readability
  judgment is attached to that rejected payload.
- The guard supplied a smaller preview path; visual acceptance must inspect that
  recovered preview and, if necessary, narrower individual frame crops before
  linking the GIF from the README.
- Follow-up: a representative frame scaled to the intended 800-pixel README
  width still triggered the same inline-output guard at 33 KB. Its separately
  recovered preview path, not the blocked response, is the next inspection
  surface.

## P0C-05 / FL-4162 · 2026-08-12 — first compact GIF still scrolled the header away

- The recovered 800-pixel frame preview showed real armor/helmet state changes
  and readable contract text, but the long selected-role panel title made the
  final, selected, and animation panels exceed VHS's actual terminal columns.
  They stacked vertically and pushed the product identity/corpus header out of
  the viewport.
- That GIF is rejected and moved recoverably to Trash. The compact-only panel
  title and header must be shortened while retaining the full normalized role
  in the frozen-contract summary; the three visual panels must then remain on
  one row for the entire recording.

## P0C-05 / FL-4162 · 2026-08-12 — second GIF frame still exceeded inline image budget

- After the responsive correction, a representative 700-pixel frame was
  intentionally compressed to 20 KB for bounded inspection. The image-view
  adapter still refused to return those bytes inline and supplied a smaller
  recovered preview instead.
- This is another inspection-transport failure, not a recording verdict. Only
  the recovered preview may be used to judge whether the header, three panels,
  contract summary, and controls coexist legibly.

## P0C-05 / FL-4162 · 2026-08-12 — responsive armored recording accepted as verification

- The second real VHS run keeps the product/corpus header, final sprite,
  selected raw layer, three-frame animation window, frozen composition,
  assigned-cell count, authority boundary, and controls on one 1000×700 screen.
- The recovered frame preview was readable even at 400×280; the README presents
  it at up to twice that size. It visibly shows the full armored composite,
  isolated helmet/armor contribution, moving active frame, layer selection, and
  hide/show state rather than command entry.
- Accepted artifact:
  `docs/recordings/source-layer-contract-viewer.gif`, 10.84 seconds, 271
  frames, 439,037 bytes, SHA-256
  `bc6fbc3d97ace9fb161282150880632724a436d4780994815c95622bda61dc25`.
- Highest proven stage is **Verified**. The user's personal judgment of the
  published GIF remains an explicit acceptance step.

## P0C-05 / FL-4162 · 2026-08-12 — GIF opening frame exposed command entry

- Direct inspection of GIF frame 0 showed the `./run-viewer.sh` launch command,
  even though the product surface itself was readable in later frames. This does
  not meet the explicit visual-proof boundary: the recording must demonstrate
  the viewer, not terminal typing.
- The VHS shell now `exec`s the compact armored viewer before capture begins;
  the GIF must be regenerated and its opening plus state-change frames inspected
  before it is again considered verified.

## P0C-05 / FL-4162 · 2026-08-12 — VHS rejects an argument-bearing shell setting

- VHS 0.11.0 rejected `Set Shell "zsh -c 'exec …'"` with `invalid shell`; its
  `Shell` setting accepts only an executable path, so this route cannot remove
  the launch command from the opening frame.
- The pre-existing GIF remains intact. The revised recipe instead keeps capture
  hidden until `Wait+Screen /SOURCE LAYER CONTRACT VIEWER/` confirms the product
  surface is rendered; that supported VHS primitive must be exercised before a
  replacement artifact is written.

## P0C-05 / FL-4162 · 2026-08-12 — no-typing recapture verified

- VHS 0.11.0 validated and rendered the revised recipe. The opening frame now
  begins on the full `player-1100` compact contract surface; later sampled
  frames visibly cover selected-layer change, helmet hide/restore, and angle
  change while retaining the final sprite, three adjacent frames, composition,
  assigned cells, and read-only authority.
- Replaced accepted artifact:
  `docs/recordings/source-layer-contract-viewer.gif`, 10.84 seconds, 271
  frames, 450,625 bytes, SHA-256
  `37a300a37b64091e8cabf77d7790681fbbb4aac71fee5dbc045e14642c84ed19`.
- Highest proven stage remains **Verified**; personal acceptance is still a
  separate user judgment.

## P0C-05 / FL-4162 · 2026-08-12 — review follow-up: angle state escaped rendered bounds

- Native code review found that repeated `.` advanced `ViewerState.angle`
  without updating it to the actual atlas row range. Rendering clamps its local
  angle, so the displayed state could disagree with the rendered frame (for
  example, an 11th displayed angle on an 8-angle atlas).
- The interaction path must wrap the state itself against the selected layer's
  real frame geometry, with boundary tests for both directions.

## P0C-05 / FL-4162 · 2026-08-12 — review follow-up: XP byte hash was not checked on load

- The contract ledger declares `source_xp.sha256`, but `xp_for_key` selected and
  parsed an XP path without comparing the loaded asset's bytes to that source of
  truth. A substituted same-name asset could therefore be rendered.
- Load must fail on a hash mismatch, and the test suite must independently
  validate every one of the 115 frozen XP asset hashes.

## P0C-05 / FL-4162 · 2026-08-12 — review follow-up: GIF proof test was header-only

- The existing regression only checked `GIF89a` and README linkage. It did not
  protect the 1000×700 capture geometry, the layer/hide/restore/angle sequence,
  or the hidden-until-rendered capture boundary that prevents terminal-command
  startup frames.
- The proof test must assert each of those recipe and artifact invariants.

## P0C-05 / FL-4162 · 2026-08-12 — review follow-up: provenance omitted local extension identity

- `docs/provenance.md` described the original root adjustment but not the
  substantive local compact-mode viewer extension. That leaves the current
  standalone product's read-only recording surface insufficiently traceable.
- Provenance must distinguish exact copied frozen inputs from the standalone
  viewer extension and name its maintained read-only contract role.

## P0C-05 / FL-4162 · 2026-08-12 — second review follow-up: GIF checks did not bind decoded evidence

- The strengthened recording test inspected GIF dimensions and the VHS recipe,
  but it still inferred startup and interaction states from tape text alone. A
  blank or unrelated 1000×700 GIF could pass those assertions.
- The accepted binary must be decoded in the dependency-free test suite and
  sampled visual state digests pinned to the opening and interaction frames.

## P0C-05 / FL-4162 · 2026-08-12 — second review follow-up: asset-hash failure leaked a traceback

- XP byte validation now raises `ContractDataError`, but the initial
  `compose_screen` call in interactive mode lies outside `main`'s controlled
  error boundary. A corrupted asset could therefore print a traceback instead
  of the viewer's bounded `FAIL:` response.
- Main must cover the whole initial render/interactive path, and a subprocess
  regression must prove corrupt-asset CLI failure is non-zero, concise, and
  traceback-free.

## P0C-05 / FL-4162 · 2026-08-12 — accepted GIF contained transient redraw frames

- The accepted 1000×700 GIF had 271 decoded frames even though it was intended
  to prove only five stable viewer states. The regression bound frames 0, 60,
  115, 170, and 225, leaving 266 frames unchecked.
- Full-sequence inspection found that the unbound frames include partial
  terminal redraws between interactions. Those frames are not a fully rendered
  product state, so the prior visual-proof acceptance is revoked.
- Successor requirement: reproducibly capture five or six complete terminal
  screenshots, assemble only those full canvases into the GIF, and decode,
  composite, and hash every resulting frame. Every frame must retain the product
  title, 115-XP / 573-layer totals, assigned/unresolved count, and `READ-ONLY`.

## P0C-05 / FL-4162 · 2026-08-12 — first held-state capture recipe failed path parsing

- VHS 0.11.0 rejected all five absolute `Screenshot` targets because the
  generated recipe supplied those paths as unquoted tokens. No replacement GIF
  was written, and the prior artifact remained untouched.
- The parser's screenshot operand is a string path. The successor quotes each
  generated absolute path, then re-runs the same five-state capture pipeline.

## P0C-05 / FL-4162 · 2026-08-12 — second held-state capture lost post-screenshot input

- Quoted screenshot paths succeeded for the first two states, but the `v` sent
  immediately after the second browser screenshot did not reach the interactive
  viewer. VHS timed out waiting for `HIDDEN-FROM-STACK`; its last screen still
  showed the helmet as `INCLUDED`.
- No replacement GIF was written. The successor adds a short uncaptured settle
  interval after each screenshot before sending the next interactive key. These
  waits cannot create animation frames because VHS is producing PNG stills, not
  the final GIF.

## P0C-05 / FL-4162 · 2026-08-12 — third held-state capture duplicated two stale states

- The five-frame GIF decoded successfully, but full-frame hashes proved frames
  0/1 were identical and frames 2/3 were identical. `Wait+Screen /L4/`
  prematurely matched the old L3 screen's composition row, while the restored
  screen was captured before the browser paint completed.
- That GIF is rejected. The successor waits for the header-specific L4 state
  and inserts an uncaptured paint-settle interval between every successful
  screen match and PNG screenshot. The final GIF still contains only the five
  PNG states, never the waits or terminal redraws.

## P0C-05 / FL-4162 · 2026-08-12 — fourth held-state capture used a wrapped restore match

- The header-specific L4 wait and screenshot settle succeeded through the
  hidden state. The restore wait then timed out because the terminal extractor
  wraps `player_helmet_regular` between `helm` and `et_regular`; the visible
  restored screen itself correctly reported `INCLUDED`.
- No replacement GIF was written. The successor matches the unwrapped header
  token `INCLUDED`, which is absent from the preceding hidden-state header, and
  retains the post-match paint-settle interval before capture.

## P0C-05 / FL-4162 · 2026-08-12 — five complete held states replaced redraw video

- `scripts/build-recording.sh` now uses VHS only to capture five complete PNG
  states, then ImageMagick assembles those stills into the final GIF. A repeated
  build produced the same binary SHA-256, so the pipeline is reproducible on the
  verified toolchain.
- Accepted artifact: 1000×700, 5 full-canvas frames, 1.80 seconds per state,
  517,740 bytes, SHA-256
  `2d41e4b2c64a784567180d9a3ed1aea2936fa5e40ac24acb112c5e1a7409cafb`.
- All five frames were decoded and composited by the dependency-free regression.
  Their RGB SHA-256 values are `fef8a80b…`, `a0fc1112…`, `1126d563…`,
  `a0fc1112…`, and `aacf57df…`; the repeated helmet/restored hash is expected
  because restoration returns to the selected-helmet visual state.
- A vertical contact sheet of every frame was inspected. Each frame visibly
  retains the viewer title and `READ-ONLY`, 115-XP / 573-layer frozen totals,
  selected layer, composition, assigned/unresolved count, and authority. The
  states are L3 armor, L4 helmet, helmet hidden, helmet restored, and L4 frame 2
  at angle 2. No frame contains shell input or a partial terminal redraw.
- Verification: 11/11 unit tests pass; VHS recipe validation, shell syntax,
  scoped secret/path scan, and `git diff --check` pass. Highest proven stage is
  **Verified**; personal acceptance remains separate.

## P0C-05 / FL-4162 · 2026-08-12 — repository name omitted Asciicker Y9.2 identity

- `source-layer-contract-viewer` described the tool category but not the frozen
  game/source lineage that gives its 115-XP / 573-layer contract meaning.
- The requested standalone identity is
  `AsciickerY92-source-layer-contract-viewer`. Before renaming, the source was
  confirmed private on `main`, the exact target name was confirmed absent, and
  the local origin still pointed at the source repository.

## P0C-05 / FL-4162 · 2026-08-12 — first local rename command used the parent directory

- The GitHub rename succeeded, but the combined local origin/directory command
  ran `git remote set-url` from the projects directory, which is not a
  repository.
  It stopped at that first command, so neither the local origin nor directory
  had changed.
- The successor runs `git remote set-url` inside the checkout, verifies it, and
  only then moves the exact checkout path to the already-proven absent target.

## P0C-05 / FL-4162 · 2026-08-12 — Asciicker Y9.2 repository identity applied

- The private GitHub repository is now exactly
  `rikiyanai/AsciickerY92-source-layer-contract-viewer`, still private with
  default branch `main`.
- Local origin fetch/push URLs now use that exact repository, and the checkout
  directory has the same exact repository name. The old local path is absent.
  No commit or push was performed as part of the rename.
## P0C-05 · 2026-08-12 — first renamed-repository push correctly rejected concurrent README work

- Push of local visual-proof commit `3a8f055` was rejected as non-fast-forward.
  The renamed private remote had advanced through user-authored `586d2ad` and
  `b6dfcd3`, which identify the viewer as an Asciicker Y9-2 REXPaint XP surface
  and adjust its opening description.
- No force push or overwrite is permitted. The successor must preserve those
  user-authored README changes, integrate the stable-frame proof on top, rerun
  every contract, and push only a fast-forward history.

## P0C-05 · 2026-08-12 — concurrent Asciicker Y9-2 README identity preserved

- The local proof history was rebased onto user commits `586d2ad` and
  `b6dfcd3`. The README keeps their Asciicker Y9-2 REXPaint `.xp` ownership and
  applies the exact requested repository title together with the five stable
  read-only product states.

## P0C-05 · 2026-08-12 — README provenance sentence overfocused on visibility

- The README linked the correct provenance document, but described it as the
  private-visibility boundary. The front page should explain the product and
  visual proof; repository visibility belongs in audit evidence and GitHub
  metadata.
- The successor keeps the provenance link and reproducible GIF recipe, but
  removes redundant private-visibility wording from README prose.

## P0C-05 / FL-4162 · 2026-08-31 — animation-proof and evidence-index successor started

- Requirement: the public proof must show the real source-layer viewer moving
  through adjacent animation frames at a useful pace while retaining layer,
  projection, angle, hide/show, and read-only contract evidence; the repository
  must expose every packaged XP input and source-owned review evidence without
  mutating the frozen corpus.
- Current owners are `scripts/source_layer_contract_viewer.py`,
  `docs/recordings/source-layer-contract-viewer.tape`,
  `scripts/build-recording.sh`, and the existing recording regression. The
  stale owners are the README's five-state/1.80-second wording and the absence
  of a dedicated historical-evidence index.
- The successor is limited to documentation, recording recipe/assembly, tests,
  provenance indexes, and the failure log. It does not change the parser,
  contract ledger, review decisions, or XP bytes.
- This attempt is **Implemented** only until the new recipe, decoded GIF, full
  test suite, link checks, and bounded visual inspection pass.

## P0C-05 / FL-4162 · 2026-08-31 — seven-state animation walkthrough verified

- The canonical VHS route now captures armor frames 1–3 before changing raw
  layer, hiding/restoring the helmet, and changing angle/frame. The launcher is
  hidden until the viewer title renders, and the build assembles only the seven
  held full-canvas screenshots.
- The accepted artifact is 1000×700, 7 frames, 726754 bytes, and SHA-256
  `1a0f7946a326e679da3bfa6bb055855e3e0c1427a0e61472f29ad3893cb02f9f`. Every
  frame uses a 55-centisecond delay and decodes to a complete viewer canvas.
- The contact sheet and representative first/last frame previews retain the
  viewer title, 115-XP / 573-layer totals, selected layer, three-frame
  animation panel, frozen composition, assigned-cell count, and read-only
  authority. No command entry or partial redraw is present.
- `python3 -m unittest discover -s tests -v` passes 12 of 12 tests. The highest
  supported stage is **Verified** for the automated recording contract and
  bounded visual proof; personal acceptance remains separate.
- Prepared About description: “Read-only FL-4162 source-layer contract viewer
  over 115 reviewed Asciicker Y9-2 REXPaint XP sprites with layer ownership,
  animation frames, and frozen provenance.”

## P0C-05 / FL-4162 · 2026-08-31 — seven-state GIF claim rejected by operator

- Operator correction: the previous seven-state GIF was not accepted as the
  requested update. It linked a GIF and showed limited frame stepping, but it
  did not show enough of the viewer or the broader XP/layer navigation.
- The corrected requirement is stricter: update the capture script, regenerate
  the committed GIF, show more viewer surfaces, show real frame progression at
  a faster review pace, keep all 115 XP files and 573 raw layers reachable, keep
  hand-labeled/review evidence tracked in `docs/historical-evidence/`, open the
  regenerated GIF in Finder, and verify the binary by decoded frame/timing
  checks before pushing.
- This entry rejects the earlier completion claim. The successor owns
  `docs/recordings/source-layer-contract-viewer.tape`,
  `scripts/build-recording.sh`, README recording text, tests, and the
  regenerated `docs/recordings/source-layer-contract-viewer.gif`.

## P0C-05 / FL-4162 · 2026-08-31 — thirteen-state faster source-layer GIF verified

- The corrected VHS recipe now captures thirteen held viewer states instead of
  seven. The sequence shows armor animation frame progression, angle and
  projection changes, helmet hide/restore, L0/L1/L2 raw-layer inspection, and a
  transition to the next XP stem while retaining the 115-XP / 573-layer corpus
  totals on the viewer surface.
- The regenerated `docs/recordings/source-layer-contract-viewer.gif` is
  1000×700, 13 frames, 1,434,477 bytes, SHA-256
  `6b9f198bdf3b30657fb8c775ac5ecb2abd9c8095165913a99adf5c5ae8b10d6b`,
  with an 18-centisecond delay per frame.
- Verification performed in-session: `./scripts/build-recording.sh` completed,
  `python3 -m unittest discover -s tests -v` passed 12/12, decoded frame-hash
  and timing checks matched the test contract, the GIF was revealed in Finder
  with `open -R`, and a bounded contact-sheet preview was visually inspected.
- Highest supported stage: **Verified** for regenerated GIF behavior, test
  coverage, and corpus reachability. Operator acceptance remains separate.

## Consolidation · 2026-10-01 — source parser collided with retired proxy filename

- The initial combined suite ran 29 tests: 28 passed and the normalized
  `test_rejected_generic_proxy_is_absent` guard failed because the imported
  source parser occupied `scripts/xp_read_model.py`. The separate two
  consolidation regressions passed. No commit, push or repository deletion
  followed that failed run.
- The source parser is renamed to `source_layer_xp_read_model.py` with its
  bytes unchanged; the source viewer imports that explicit name. The existing
  normalized absence guard remains unchanged. This preserves the new
  source-layer view without reinstating the rejected generic viewer.
- Re-run every normalized, source-layer and consolidation test before
  publication. Falsifier: any missing input, altered XP byte, broken
  launcher, revived generic proxy or failing test prevents deletion.
