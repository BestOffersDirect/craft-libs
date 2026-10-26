"""Regenerate crates/crw/src/tables.rs from the frozen tables in crates/crw/clean-room/logs/table_sel{0,1,2}.json.

Run from anywhere: `python crates/crw/clean-room/tools/gen_tables.py`. The JSON files are the
derivation's frozen data (06-crw-format.md section 3); this script only renders them as Rust
constants, keeping the file's doc comment. It was a local tool during the derivation in LightCraft
(plan/crw/model/gen_tables.py) and moved here so the tables stay reproducible.
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
TABLES = ROOT / "crates/crw/src/tables.rs"
LOGS = ROOT / "crates/crw/clean-room/logs"

TAIL = """
/// The tables for DecoderTable selector 0, 1 or 2.
pub(crate) fn tables(selector: u32) -> Option<SelTables> {
    match selector {
        0 => Some(SelTables { first: FIRST_0, main: MAIN_0 }),
        1 => Some(SelTables { first: FIRST_1, main: MAIN_1 }),
        2 => Some(SelTables { first: FIRST_2, main: MAIN_2 }),
        _ => None,
    }
}
"""


def main():
    head = TABLES.read_text(encoding="utf-8").split("#[rustfmt::skip]")[0]
    out = [head.rstrip("\n") + "\n"]
    for sel in (0, 1, 2):
        spec = json.loads((LOGS / f"table_sel{sel}.json").read_text(encoding="utf-8"))
        for part, name in (("first", "FIRST"), ("main", "MAIN")):
            rows = sorted(spec[part].items(), key=lambda kv: (len(kv[0]), kv[0]))
            out.append("#[rustfmt::skip]")
            out.append(f"const {name}_{sel}: &[(u16, u8, u8, u8)] = &[")
            line = []
            for code, (r, s) in rows:
                line.append(f"(0b{code}, {len(code)}, {r}, {s}),")
                if len(line) == 6:
                    out.append("    " + " ".join(line))
                    line = []
            if line:
                out.append("    " + " ".join(line))
            out.append("];")
    TABLES.write_text("\n".join(out) + TAIL, encoding="utf-8", newline="\n")
    print(f"generated {TABLES.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
