#!/usr/bin/env python3
"""Compile each of YREC's Fortran files with gfortran's warnings on, and save the warnings for the site.

    python3 scripts/fortran_warnings.py ../yrec/src yrec-map/warnings.json

Compiling only: nothing is linked or run. The modules (*_mod.f) are compiled first, in as many passes as their
USE statements need, into a temporary folder; then every file is compiled against them with the developers'
flags (their Makefile's GNU_BASE_FFLAGS) plus -Wextra and -O2 (which gfortran needs to find values that may
be used before they are set). The output, {file: [[line, column, message], ...]}, is read by codemap.py
(--warnings) and shown, folded, under each routine's page.
"""
import json, pathlib, re, subprocess, sys, tempfile

FLAGS = ["-ffixed-line-length-132", "-Wall", "-Wextra", "-cpp", "-O2", "-DGIT_HASH='0'"]
WARN = re.compile(r"^(?P<file>[^:\n]+\.f):(?P<line>\d+):(?P<col>\d+):\s*\n(?P<body>(?:.*\n)*?)Warning: (?P<msg>.*)$", re.M)


def compile_one(src, tmp):
    r = subprocess.run(["gfortran", *FLAGS, "-J", tmp, "-I", tmp, "-c", str(src), "-o", f"{tmp}/{src.stem}.o"],
                       capture_output=True, text=True)
    return r.returncode, r.stderr


def main(src_dir, out_path):
    src_dir = pathlib.Path(src_dir)
    files = sorted(src_dir.glob("*.f"))
    mods = [f for f in files if f.name.endswith("_mod.f")]
    found = {}
    with tempfile.TemporaryDirectory() as tmp:
        todo = mods[:]
        while todo:  # modules that USE other modules compile once those exist
            left = []
            for f in todo:
                code, err = compile_one(f, tmp)
                (left.append(f) if code else found.__setitem__(f.name, err))
            if len(left) == len(todo):
                sys.exit("modules that do not compile: " + ", ".join(f.name for f in left))
            todo = left
        for f in files:
            if f.name not in found:
                code, err = compile_one(f, tmp)
                if code:
                    print(f"{f.name}: does not compile", file=sys.stderr)
                found[f.name] = err
    out = {}
    for name, err in found.items():
        items = []
        for m in WARN.finditer(err):
            if pathlib.Path(m.group("file")).name == name:
                items.append([int(m.group("line")), int(m.group("col")), m.group("msg").strip()])
        if items:
            out[name] = sorted(set(map(tuple, items)))
    pathlib.Path(out_path).write_text(json.dumps(out, indent=0) + "\n")
    print(f"{sum(len(v) for v in out.values())} warnings in {len(out)} of {len(files)} files")


if __name__ == "__main__":
    main(*sys.argv[1:3])
