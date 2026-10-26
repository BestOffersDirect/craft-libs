# Canon CRW clean-room derivation record

Everything that establishes how `craft-crw` decodes a CRW, in the order it happened. The record was
produced in LightCraft (`clean-room/crw/`, branch `clean-room-crw-format-decode`, revision
`70c755e42a65661401142819278d51b0c5977f7f`) between 2026-10-12 and 2026-10-25 and moved here
**verbatim** when the decoder became this shared crate. The documents are the evidence: they are
not rewritten after the fact, so paths they mention are LightCraft's paths of that time (the
mapping is below), and `00-starting-assumptions.md` is committed once and never edited.

## Documents

| File | What it is |
|---|---|
| [`00-starting-assumptions.md`](00-starting-assumptions.md) | What the author believed before consulting any source; every item marked unverified. Immutable. |
| [`01-plan.md`](01-plan.md) | The derivation plan, the corpus (public CC0 files with hashes; private files by name, size and hash), the maintainer's decisions (§7) and approval. |
| [`sources.md`](sources.md) | Every URL opened and search run, with the time, what was asked and what was taken. The rules in force are at its top. |
| [`02-container.md`](02-container.md) | CIFF heap parsing from Canon's specification and ExifTool's prose pages, each fact cited. |
| [`03-payload-layout.md`](03-payload-layout.md) | The RawData payload partition established by statistics alone (no decoding): low-bits plane, 514-byte header, ff00-stuffed stream, tail. |
| [`04-derivation-log.md`](04-derivation-log.md) | The entropy-coding derivation, experiment by experiment, against the black-box reference. |
| [`06-crw-format.md`](06-crw-format.md) | **The frozen format** (revision 2) and its reopening rule. The decoder implements this document. |
| [`07-verification.md`](07-verification.md) | Full-frame exact comparison against the reference, zero tuning: 28 of 29 files, then 1,516 of 1,516 D60 files. |
| [`08-color.md`](08-color.md) | CFA phase, active area, black and white levels, white-balance records, orientation and time: what the decoder reports beyond the samples. §3's colour matrices concern LightCraft (below). |
| [`09-private-corpus.md`](09-private-corpus.md) | The maintainer's EOS D60 files and controlled captures (grey card, lens cap, white-balance presets) and what each set established. |
| [`10-chart-calibration.md`](10-chart-calibration.md) | EOS D60 colour matrices from ColorChecker captures. This is LightCraft's colour work (`crates/raw/src/chart_table.rs` there), kept here because it is part of the same record and uses the same captures. |

There is no `05-geometry-colour.md`: the plan named it, and the material went into `08-color.md`.

## Scripts and logs

- `ciff_dump.py`, `p1_payload.py`, `p1b_markers.py`, `p1c_lowbits_bounds.py`, `p2_oracle_lsb.py`:
  the planning and payload-statistics scripts (standard library only; run them with `python -I`).
  Their public outputs are in `logs/` (`structure-*.txt`, `p1*.txt`, `verification-sweep.txt`).
- `logs/table_sel{0,1,2}.json`: **the frozen code tables**, the source of truth that
  `tools/gen_tables.py` renders into `../src/tables.rs`. `table_sel0_d60class.json` is the
  revision-1 selector-0 table, kept for the record.
- `logs/private-corpus.tsv`, `logs/chart-captures.tsv`: names, sizes and SHA-256 of the
  maintainer's own files. No image content, metadata or thumbnails are recorded anywhere here.
- `logs/private/` (gitignored): per-file dumps of the private files, which can hold personal
  metadata. Local only.

## What stayed local

- The Python reference model and probe harness (`plan/crw/model/` in LightCraft, gitignored),
  by the maintainer's decision #4. Its findings are all in `04-derivation-log.md`.
- The reference decoder: LibRaw 0.22.2, official pre-built Windows binaries installed by the
  maintainer; only `unprocessed_raw.exe` was ever run, as a black box. The source tree shipped
  alongside it was never opened, read or searched.
- Canon's CIFF specification PDF (copyrighted; archive URL and SHA-256 in `sources.md`).
- The reference TIFFs (`<name>.crw.tiff`) the verification compared against; `CRAFT_CRW_ORACLE`
  points the test at a local copy.

## Path mapping (LightCraft at the time → craft-libs)

| In the documents | Now |
|---|---|
| `clean-room/crw/…` | `crates/crw/clean-room/…` |
| `crates/raw/src/vendor/crw.rs` | `crates/crw/src/lib.rs` |
| `crates/raw/src/vendor/crw_tables.rs` | `crates/crw/src/tables.rs` |
| `crates/raw/tests/crw_oracle.rs` | `crates/crw/tests/samples.rs` (`CRAFT_CRW_ORACLE`, formerly `LIGHTCRAFT_CRW_ORACLE`) |
| `white_from_data` (LightCraft's shared estimate) | `saturation_plateau` in `crates/crw/src/lib.rs` |
| `xtask/src/main.rs` `RAW_SAMPLES` (corpus URLs) | `crates/crw/tests/samples.json` + `scripts/fetch-crw-samples.py` |
| `plan/crw/model/gen_tables.py` | `crates/crw/clean-room/tools/gen_tables.py` |
| `docs/arw6-compression.md` (the house model for a derivation) | LightCraft's document; the method is summarised in `docs/clean-room.md` of this repository |
| `crates/raw/src/chart_table.rs`, `spectral_table.rs`, `camera_preview`, `assets/camera-profiles/` | LightCraft (colour stays in the app) |

## Rules that were in force

From `sources.md` and `01-plan.md`: no raw-decoder source may be opened, fetched, searched inside
or requested (dcraw, LibRaw, rawspeed, rawloader/rawler, dnglab, darktable, RawTherapee,
libopenraw, ExifTool's Perl code, including licence headers, comments and mirrors). Allowed:
published format documentation in prose, published standards, the sample files, and a reference
decoder's binary run as a black box with every probe logged. No tuning after the freeze: a
mismatch reopens the derivation explicitly, with its cause and a new freeze commit recorded
(`06-crw-format.md`, revision 2, is the one reopening). The general standard this followed is
[`docs/clean-room.md`](../../../docs/clean-room.md).
