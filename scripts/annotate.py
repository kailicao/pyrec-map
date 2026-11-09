#!/usr/bin/env python3
"""Add type annotations to the Python translation, from YREC's Fortran declarations, and KC's blank lines around
each function's docstring.

    python3 scripts/annotate.py ../yrec/src ../pyrec/pyrec [--dry-run]

For each function that translates a Fortran unit (getopac() for GETOPAC in getopac.f), each argument's type comes
from the unit's declarations (REAL*8 and REAL: float; INTEGER: int; LOGICAL: bool; CHARACTER: str), or from
Fortran's implicit types when it has none (I–N integer, else real). An argument is an array, `np.ndarray`, when
the Python indexes it (an array declared with one element and used as a scalar is a Python scalar, by pyrec's
conventions). The return annotation comes from the function's `return` statements, when every one of them
returns the same names: their types, as a tuple in order. What the script cannot settle (a returned expression,
returns that differ) is left without an annotation and listed, for a person to finish. Functions that already
carry annotations, and private helpers (a leading underscore), are left as they are.

Docstrings: a blank line before a multi-line docstring's closing quotes, and one after the docstring (KC, Nov 9,
2026). Nothing else in the files changes.
"""
import ast, pathlib, re, sys

TYPES = [(r"REAL\s*\*\s*8|DOUBLE\s*PRECISION|REAL\s*\*\s*4|REAL", "float"), (r"INTEGER(\s*\*\s*\d+)?", "int"),
         (r"LOGICAL(\s*\*\s*\d+)?", "bool"), (r"CHARACTER(\s*\*\s*(\(\s*\*\s*\)|\d+))?", "str")]
UNIT = re.compile(r"^\s*(?:(?:REAL\s*\*\s*8|DOUBLE\s*PRECISION|REAL|INTEGER(?:\s*\*\s*\d+)?|LOGICAL(?:\s*\*\s*\d+)?)\s+)?"
                  r"(SUBROUTINE|FUNCTION)\s+([A-Z_]\w*)\s*(?:\((.*?)\))?", re.I)


def statements(path):
    """The Fortran file's statements, continuation lines joined, comments and strings left out: [(line, text)]."""
    out = []
    for i, raw in enumerate(path.read_text(errors="replace").splitlines(), 1):
        if not raw.strip() or raw[:1] in "cC*!dD" or len(raw) <= 6:
            continue
        text = re.sub(r"'[^']*'", "''", raw[6:132]).split("!", 1)[0]
        if raw[5] not in " 0" and out:
            out[-1] = (out[-1][0], out[-1][1] + " " + text.strip())
        elif text.strip():
            out.append((i, text.strip()))
    return out


def split_top(s):
    """Split at commas outside parentheses."""
    parts, depth, cur = [], 0, ""
    for ch in s:
        depth += {"(": 1, ")": -1}.get(ch, 0)
        if ch == "," and depth == 0:
            parts.append(cur)
            cur = ""
        else:
            cur += ch
    return parts + [cur]


def units(path):
    """{unit name (lower): {"args": [names], "kind": "subroutine"/"function", "type": {name: type},
    "dims": {name: its dimensions, "(3)"}, "implicit": bool}}."""
    out, cur = {}, None
    for _, s in statements(path):
        u = s.upper()
        m = UNIT.match(u)
        if m and not u.startswith("END"):
            cur = {"args": [a.strip() for a in (m.group(3) or "").split(",") if a.strip() and a.strip() != "*"],
                   "kind": m.group(1).lower(), "type": {}, "dims": {}, "implicit": True, "name": m.group(2)}
            for pat, ty in TYPES:
                if re.match(r"\s*(" + pat + r")\s+FUNCTION", u):
                    cur["type"][m.group(2)] = ty
            out[m.group(2).lower()] = cur
            continue
        if cur is None:
            continue
        if re.match(r"END\s*(SUBROUTINE|FUNCTION)?\s*\w*$", u) and not re.match(r"END\s*(DO|IF)", u):
            cur = None
            continue
        if re.match(r"IMPLICIT\s+NONE", u):
            cur["implicit"] = False
            continue
        m = re.match(r"DIMENSION\s+(.*)$", u)
        if m:
            for ent in split_top(m.group(1)):
                cur["dims"][ent.split("(")[0].strip()] = ent[ent.find("("):].replace(" ", "")
            continue
        for pat, ty in TYPES:
            m = re.match(r"(" + pat + r")\s*(,[^:]*)?(::)?\s*(.*)$", u)
            if m and not re.match(r"(" + pat + r")\s*FUNCTION", u):
                attrs = m.group(m.lastindex - 2) or ""
                for ent in split_top(m.group(m.lastindex)):
                    name = ent.split("(")[0].split("=")[0].strip()
                    if re.fullmatch(r"[A-Z_]\w*", name):
                        cur["type"][name] = ty
                        lhs = ent.split("=")[0]
                        if "(" in lhs:
                            cur["dims"][name] = lhs[lhs.find("("):].replace(" ", "")
                        elif "DIMENSION" in attrs:
                            cur["dims"][name] = attrs[attrs.find("("):].replace(" ", "")
                break
    return out


def ftype(unit, name):
    name = name.upper()
    if name in unit["type"]:
        return unit["type"][name]
    if name in ("ALT1", "ALT2"):
        return "bool"
    return ("int" if name[:1] in "IJKLMN" else "float") if True else None


def is_array(fn, unit, name):
    """An array in Python: indexed there, or declared with more than one element (an array declared with one
    element and used as a scalar is a Python scalar, by pyrec's conventions)."""
    return indexed(fn, name) or unit["dims"].get(name.upper(), "(1)") not in ("(1)", "")


def indexed(fn, name):
    return any(isinstance(n, ast.Subscript) and isinstance(n.value, ast.Name) and n.value.id == name
               for n in ast.walk(fn))


def own_returns(fn):
    out, stack = [], list(fn.body)
    while stack:
        n = stack.pop()
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda, ast.ClassDef)):
            continue
        if isinstance(n, ast.Return):
            out.append(n)
        stack.extend(ast.iter_child_nodes(n))
    return out


def ann_for(fn, unit, pnames):
    """The parameters' annotations and the return annotation (None when it cannot be settled)."""
    def ty_of_name(nm):
        if nm in ("alt1", "alt2"):
            return "bool"
        if nm in pnames:
            return pnames[nm]
        return "np.ndarray" if is_array(fn, unit, nm) else ftype(unit, nm)
    rets = own_returns(fn)
    shapes = set()
    for r in rets:
        v = r.value
        if v is None or (isinstance(v, ast.Constant) and v.value is None):
            shapes.add("None")
        elif isinstance(v, ast.Tuple) and all(isinstance(e, ast.Name) for e in v.elts):
            shapes.add("tuple[" + ", ".join(ty_of_name(e.id) for e in v.elts) + "]")
        elif isinstance(v, ast.Name):
            shapes.add(ty_of_name(v.id))
        elif isinstance(v, ast.Constant) and isinstance(v.value, bool):
            shapes.add("bool")
        else:
            shapes.add("?")
    if not rets:
        shapes = {"None"}
    if unit["kind"] == "function" and shapes and all(s == "?" for s in shapes):
        shapes = {ftype(unit, unit["name"])}
    ret = shapes.pop() if len(shapes) == 1 and "?" not in shapes else None
    return ret


def format_def(indent, name, params, ret, width=120):
    """The def line, wrapped at commas (inside its parentheses or the return's brackets) to fit the width,
    continuation lines aligned after the opening parenthesis."""
    one = f"{indent}def {name}(" + ", ".join(params) + ")" + (f" -> {ret}" if ret else "") + ":"
    if len(one) <= width:
        return [one]
    pad = " " * (len(indent) + len(f"def {name}("))
    pieces = re.split(r"(?<=, )", one)
    lines, cur = [], ""
    for piece in pieces:
        if cur and len(cur) + len(piece.rstrip()) > width:
            lines.append(cur.rstrip())
            cur = pad
        cur += piece
    lines.append(cur.rstrip())
    return lines


def process(py, ftn, dry):
    src = py.read_text()
    tree = ast.parse(src)
    lines = src.split("\n")
    us = units(ftn) if ftn.exists() else {}
    edits, unsettled, uses_np, n_fn = [], [], False, 0
    for fn in [n for n in tree.body if isinstance(n, ast.FunctionDef)]:
        doc = ast.get_docstring(fn, clean=False) is not None
        if doc:  # KC's blank lines around the docstring
            d = fn.body[0]
            if d.end_lineno > d.lineno and lines[d.end_lineno - 1].strip() == '"""' and lines[d.end_lineno - 2].strip():
                edits.append(("insert", d.end_lineno - 1, ""))
            if len(fn.body) > 1 and fn.body[1].lineno == d.end_lineno + 1:
                edits.append(("insert", d.end_lineno, ""))
        unit = us.get(fn.name)
        if fn.name.startswith("_") or not unit or fn.returns or any(a.annotation for a in fn.args.args):
            continue
        if fn.args.vararg or fn.args.kwarg or fn.args.kwonlyargs or fn.decorator_list:
            continue
        n_fn += 1
        pnames, params = {}, []
        defaults = [None] * (len(fn.args.args) - len(fn.args.defaults)) + list(fn.args.defaults)
        for a, dflt in zip(fn.args.args, defaults):
            nm = a.arg
            ty = "np.ndarray" if is_array(fn, unit, nm) else ftype(unit, nm)
            uses_np |= ty == "np.ndarray"
            pnames[nm] = ty
            params.append(f"{nm}: {ty}" + (f" = {ast.unparse(dflt)}" if dflt is not None else ""))
        ret = ann_for(fn, unit, pnames)
        uses_np |= bool(ret and "np.ndarray" in ret)
        if ret is None:
            unsettled.append(fn.name)
        body_start = fn.body[0].lineno
        hdr = [k for k in range(fn.lineno, body_start) if lines[k - 1].rstrip().endswith(":")]
        if not hdr:
            continue
        indent = lines[fn.lineno - 1][:len(lines[fn.lineno - 1]) - len(lines[fn.lineno - 1].lstrip())]
        trailing = re.search(r":\s*(#.*)?$", lines[hdr[0] - 1]).group(1)
        new = format_def(indent, fn.name, params, ret)
        if trailing:
            new[-1] += "  " + trailing
        edits.append(("replace", fn.lineno - 1, hdr[0], new))
    if uses_np and not re.search(r"^import numpy as np$", src, re.M):
        first = next((k for k, ln in enumerate(lines) if ln.startswith(("import ", "from "))), None)
        if first is not None:
            last_plain = max(k for k, ln in enumerate(lines) if ln.startswith("import ") or k == first)
            edits.append(("insert", last_plain + 1, "import numpy as np"))
        else:  # no imports yet: after the module's docstring
            after = tree.body[0].end_lineno if tree.body and isinstance(tree.body[0], ast.Expr) else 0
            edits.append(("insert", after, "\nimport numpy as np"))
    for e in sorted(edits, key=lambda e: e[1], reverse=True):
        if e[0] == "insert":
            lines.insert(e[1], e[2])
        else:
            lines[e[1]:e[2]] = e[3]
    out = "\n".join(lines)
    if out != src and not dry:
        ast.parse(out)
        py.write_text(out)
    return n_fn, unsettled


def main(src, pkg, dry=False):
    total, left = 0, []
    for py in sorted(pathlib.Path(pkg).glob("*.py")):
        n, uns = process(py, pathlib.Path(src) / (py.stem + ".f"), dry)
        total += n
        left += [f"{py.name}: {u}" for u in uns]
    print(f"{total} functions annotated; {len(left)} without a return annotation, to finish by hand:")
    for x in left:
        print("  " + x)


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if a != "--dry-run"]
    main(*args[:2], dry="--dry-run" in sys.argv)
