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
