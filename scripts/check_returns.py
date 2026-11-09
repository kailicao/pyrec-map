#!/usr/bin/env python3
"""Check the Python translation's calls against the routines they call: what each call unpacks against what the
routine returns, and how many arguments it passes against the routine's signature.

    python3 scripts/check_returns.py ../pyrec/pyrec [--csv out.csv]

Returns: for each function, its returns are the sizes of its `return` statements (a tuple's length, 1 for a single
value, 0 for a bare `return` or none; returns of nested functions are not counted, except through `return
helper(...)`, which takes the helper's sizes). For each call to a function of the package, the call's use is the
number of names it unpacks (`a, b = f(...)`: 2; `a = f(...)`: 1; a bare `f(...)`: 0). A mismatch is a call whose use
differs from every size its callee returns, or a callee whose returns differ among themselves.

Arguments: each call to a routine of the package (the function named as its file, `getopac()` in getopac.py)
passes at least its required arguments and at most all of them. Nothing is run.
"""
import ast, csv, pathlib, sys


def returns_of(fn):
    nested = {n.name: n for n in ast.walk(fn) if isinstance(n, ast.FunctionDef) and n is not fn}
    sizes = set()
    stack = list(fn.body)
    while stack:
        node = stack.pop()
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda, ast.ClassDef)):
            continue  # nested functions' returns are their own
        if isinstance(node, ast.Return):
            v = node.value
            if v is None:
                sizes.add(0)
            elif (isinstance(v, ast.Call) and isinstance(v.func, ast.Name) and v.func.id in nested):
                sizes |= returns_of(nested[v.func.id])  # `return _out()`: the helper's tuple
            else:  # an explicit `return None` is one value (iounits_mod.read at end of file)
                sizes.add(len(v.elts) if isinstance(v, ast.Tuple) else 1)
        stack.extend(ast.iter_child_nodes(node))
    return sizes or {0}


def main():
    root = pathlib.Path(sys.argv[1])
    funcs, calls = {}, []
    for p in sorted(root.glob("*.py")):
        tree = ast.parse(p.read_text())
        imported = {}
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.module and node.module.startswith("pyrec."):
                for a in node.names:
                    imported[a.asname or a.name] = (node.module.split(".", 1)[1], a.name)
        for node in tree.body:
            if isinstance(node, ast.FunctionDef) and not node.name.startswith("_"):
                funcs[(p.stem, node.name)] = returns_of(node)
        for node in ast.walk(tree):
            if isinstance(node, (ast.Assign, ast.Expr)) and isinstance(node.value, ast.Call):
                f = node.value.func
                if isinstance(f, ast.Name) and f.id in imported:
                    target = imported[f.id]
                elif isinstance(f, ast.Attribute) and isinstance(f.value, ast.Name):
                    target = (f.value.id, f.attr)  # module.function
                else:
                    continue
                if isinstance(node, ast.Expr):
                    used = 0
                else:
                    t = node.targets[0]
                    used = len(t.elts) if isinstance(t, ast.Tuple) else 1
                calls.append((p.stem, node.lineno, target, used))
    rows = []
    for (mod, name), sizes in sorted(funcs.items()):
        if len(sizes) > 1:
            rows.append(("callee", f"{mod}.py", "", f"{name}", "returns differ: " + ", ".join(map(str, sorted(sizes)))))
    missing = set()
    for caller, line, target, used in calls:
        if target not in funcs:
            if target[0] in {p.stem for p in root.glob("*.py")}:
                missing.add(target)
            continue
        sizes = funcs[target]
        if used not in sizes:
            kind = "drops" if used == 0 else "call"  # a bare call drops what the routine sets: right only if the caller never reads it
            rows.append((kind, f"{caller}.py", line, f"{target[0]}.{target[1]}", f"unpacks {used}, returns {'/'.join(map(str, sorted(sizes)))}"))
    for m in sorted(missing):
        rows.append(("call", "", "", f"{m[0]}.{m[1]}", "no such function in that file"))
    if "--csv" in sys.argv:
        with open(sys.argv[sys.argv.index("--csv") + 1], "w", newline="") as f:
            csv.writer(f).writerows([("kind", "file", "line", "function", "problem")] + rows)
    print(f"{len(funcs)} functions, {len(calls)} calls to the package; {len(rows)} problems")
    for r in rows[:40]:
        print("  ", *r)
    check_arguments(root)


def check_arguments(root):
    """Each call to a routine of the package against the routine's signature (the function named as its file)."""
    defs = {}
    for f in root.glob("*.py"):
        for n in ast.parse(f.read_text()).body:
            if isinstance(n, ast.FunctionDef) and n.name == f.stem:
                a = n.args
                defs[n.name] = (len(a.args) - len(a.defaults), len(a.args), a.vararg is not None)
    bad = []
    for f in sorted(root.glob("*.py")):
        t = ast.parse(f.read_text())
        imp = {a.asname or a.name: a.name for n in ast.walk(t)
               if isinstance(n, ast.ImportFrom) and n.module and n.module.startswith("pyrec.") for a in n.names}
        for n in ast.walk(t):
            if (isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and imp.get(n.func.id) in defs
                    and not any(isinstance(x, ast.Starred) for x in n.args)):
                lo, hi, var = defs[imp[n.func.id]]
                k = len(n.args) + len(n.keywords)
                if k < lo or (k > hi and not var):
                    bad.append((f.name, n.lineno, imp[n.func.id], k, lo, hi))
    print(f"{len(defs)} routines; {len(bad)} calls with the wrong number of arguments")
    for name, line, callee, k, lo, hi in bad:
        print(f"   {name}:{line} {callee}: {k} arguments, takes {lo}" + ("" if lo == hi else f" to {hi}"))


if __name__ == "__main__":
    main()
