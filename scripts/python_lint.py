#!/usr/bin/env python3
"""Lint the Python translation with ruff, and save its findings for the site.

    python3 scripts/python_lint.py ../pyrec yrec-map/ruff.json

Runs `ruff check` with pyrec's own settings (its pyproject.toml) and writes {file name: [[line, column,
"CODE message"], ...]}, which codemap.py (--twin-warnings) marks on the Python's lines and lists, folded, on
each page. Nothing is changed in pyrec.
"""
import json, pathlib, subprocess, sys


def main(repo, out_path):
    r = subprocess.run(["ruff", "check", "--no-cache", "--output-format", "json", "pyrec"], cwd=repo,
                       capture_output=True, text=True)
    out = {}
    for f in json.loads(r.stdout or "[]"):
        name = pathlib.Path(f["filename"]).name
        out.setdefault(name, []).append([f["location"]["row"], f["location"]["column"], f"{f['code']} {f['message']}"])
    for v in out.values():
        v.sort()
    pathlib.Path(out_path).write_text(json.dumps(out, indent=0, sort_keys=True) + "\n")
    print(f"{sum(len(v) for v in out.values())} findings in {len(out)} files")


if __name__ == "__main__":
    main(*sys.argv[1:3])
