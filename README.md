# Normalized XP Sprite Inspector

Private standalone repository reserved for the read-only normalized-XP sprite
UV/body inspector (P0C-03).

## Current state

Repository ownership is established, but source extraction is intentionally
blocked. The current `xp_uv_body_viewer.py` spans the Y9-2 and pipeline-v3
checkouts and still embeds anchor/semantic-map mutation modes. Copying that file
wholesale would violate this repository's read-only product boundary.

The extraction must retain only:

- raw XP layer/frame/angle browsing;
- exact noninteractive JSON dumps;
- parser-only XP helpers;
- selected `player-nude.xp` demo data.

It must exclude decision capture, anchor editing, batch assignment operations,
semantic-map saves, compilers, runtime code, and unrelated sprites.

This repository is private. It is not yet runnable or user accepted.
