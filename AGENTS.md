# AGENTS.md

Shared Rust libraries for the Craft Apps (LightCraft, PhotoCraft, PdfCraft, VectorCraft, FilmCraft,
DesignCraft, WordCraft and the others). The shared standards live in
[craftrules](https://github.com/storytold/craftrules) (`../../craftrules` on a dev machine): read its
`AGENTS.md`, then `standards/never-crash.md`, `standards/engineering.md` and `standards/licensing.md`.

## Start every session here

1. Read this file, then the `README.md` of each crate you touch (its boundaries, origin and tests).
2. A crate that derives or reads a format (`jpeg`, `media`, `crw`, …) follows
   [`docs/clean-room.md`](docs/clean-room.md); a crate with a `clean-room/` folder keeps that record
   intact (its `README.md` says what is frozen and how a change is reopened).
3. Check `git status`, `git worktree list` and unmerged branches before starting anything new; commit
   small and often.

## Rules

- **Never crash.** Every crate's `lib.rs` starts with
  `#![deny(clippy::unwrap_used, clippy::expect_used, clippy::panic, clippy::unimplemented, clippy::todo, clippy::unreachable)]`.
  No `unsafe` (the workspace forbids it). Input-derived numbers are hostile: `get()` instead of
  indexing for offsets that come from a file, checked or saturating arithmetic for lengths and
  counts, bounded recursion (depth limits or budgets), allocations capped by a `Limits` the caller
  can lower. Every crash fix lands with a regression test that panicked before it.
- **New crates** go in `crates/<name>`, named `craft-<name>`, inherit the workspace package fields
  and lints, and are listed in `[workspace.dependencies]`, in the root `README.md` (one entry per
  library) and in a workflow of their own (`.github/workflows/<name>.yml`: fmt, clippy with
  `-D warnings`, tests on Linux, Windows and macOS, and a `wasm32-unknown-unknown` check for a
  crate that an app's web build can use).
- **No app code.** A crate here must be useful to more than one app and must not depend on any app.
  App policy (colour models, UI, settings, command handling) stays in the apps; the crate's README
  states its boundaries and, when the code came from an app, its origin (repository, paths,
  revision) and what changed in the move. `NOTICE` → *Source provenance* records the same.
- **Clean-room.** Format code is written only from published specifications, prose documentation,
  usable sample files and black-box observation of reference binaries; never from GPL/LGPL/AGPL/CDDL
  sources or Adobe material, in any form. The process and the record a crate keeps are in
  [`docs/clean-room.md`](docs/clean-room.md). If you have seen something you should not have, stop
  and say so.
- **Assets and samples.** Nothing enters the repository without a row in `ATTRIBUTION.md` (path,
  author, source, licence) and a licence text where one is required (`licenses/`). Sample media is
  never committed: tests fetch pinned, SHA-256-verified, licence-checked files outside the checkout
  (`scripts/fetch-*.py`) and skip cleanly when they are absent. No Adobe assets of any kind, including
  Adobe's open-licensed fonts; fonts come from craft-fonts.
- **Time goes through `chrono`** (workspace dependency). Never hand-roll UTC/calendar conversion (days-to-date algorithms, leap-year math); a crate owns only its output format string. The one exception is range extension: past the years chrono can represent, shift the date by whole 400-year Gregorian cycles (146,097 days, after which the calendar repeats), let chrono compute the month and day, and add the cycles back to the year (splitting seconds into hours, minutes and seconds is plain arithmetic). A library that reads a timestamp from a file hands it on as Unix seconds and lets the app convert.
- **Tests.** Unit and property tests next to the code; every feature has a test that would fail
  without it; decoders have a hostile-input sweep (truncations, byte mutations, proptest) and, for
  real files, a digest-pinned sample test. A test that cannot run (no sample files, no GPU) prints
  why it skipped and passes, unless a `*_REQUIRE_*` variable (set in CI) turns the skip into a
  failure.
- **Before merging:** `cargo fmt --check`, `cargo clippy --workspace --all-targets -- -D warnings`,
  `cargo test --workspace`. Each crate's workflow runs the same for that crate on every PR.
- **Commits:** one change per commit, only green states, messages that say what and why. Apps
  consume a crate by git revision (`craft-<name> = { git = "https://github.com/storytold/craft-libs", rev = "<commit>" }`),
  so a merged commit is an API contract: note breaking changes in the crate's README.
