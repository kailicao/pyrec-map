"""bug_list.py: keep bugs/bugs.json in step with the pages' suspected bugs, and check the bug page against them.

Each bug's marker, title, and cited lines come from its page's notes ("## Bugs, by priority" in yrec-map/notes/);
its status ("**Checked by KC** (date)." at the start of the item, else unconfirmed) also comes from the page;
its one-line result ("runs") is kept in bugs.json itself, the only place it lives. The script
rewrites bugs.json (new bugs get an empty "runs" to fill in) and reports where bugs/notes/index.md disagrees: a
bug that changes results or output missing from the page, or listed under another kind. Run from the repository:
    python3 scripts/bug_list.py"""
import json, re, sys
from pathlib import Path

PROBLEMS = []
NOTES, PAGE, JS = Path("yrec-map/notes"), Path("bugs/notes/index.md"), Path("bugs/bugs.json")
SITE, GH = "https://kailicao.github.io/pyrec-map/yrec-map/", "https://github.com/yreclab/yrec/blob/7be4133/src/"
ON_PAGE = {"changes results, large", "changes results, small", "stops the run", "wrong output"}
ITEM = re.compile(r"(?ms)^(\d+)\. \*\*\(([a-z][a-z ,]+[a-z])\)\*\*\s+(.*?)(?=^\d+\. \*\*\(|\Z)")


def bugs():
    for p in sorted(NOTES.glob("*.md")):
        s = p.read_text(encoding="utf-8")
        if "## Bugs, by priority" not in s:
            continue
        sec = s.split("## Bugs, by priority", 1)[1]
        sec = sec[:re.search(r"(?m)^#", sec).start()] if re.search(r"(?m)^#", sec) else sec  # up to the next heading
        for m in ITEM.finditer(sec):
            body = m.group(3)
            if not re.search(r"\*\*Checked by (?:running YREC|reading the code)\*\*", body):
                PROBLEMS.append(f"{p.stem}#{m.group(1)}: no run passage inside the item (a paragraph moved out of it?)")
            kc = re.match(r"\*\*Checked by KC\*\* \(([^)]*)\)\.\s*", body)  # the status, on the bug's own page
            if kc:
                body = body[kc.end():]
            t = re.match(r"\*\*(.*?)\*\*", body)
            rest = body[t.end():] if t else body
            groups = re.findall(r"\(((?:\[\[[^\]]*\]\][,;]?\s*)+)\)", rest[:600])
            links = next((re.findall(r"\[\[([^\]]*)\]\]", g) for g in groups if "#L" in g), [])
            code = []
            for l in links:
                c = re.match(r"([\w.]*)#(L\d+(?:-L\d+)?)", l)
                if c:
                    code.append(GH + (c.group(1) or p.stem) + "#" + c.group(2))
            title = re.sub(r"\[\[(?:[^\]|#]*#)?([^\]|]*)\]\]", r"\1", t.group(1) if t else "").replace("`", "").rstrip(".")
            yield {"file": p.stem, "number": int(m.group(1)), "result": m.group(2), "title": title,
                   "status": f"checked by KC ({kc.group(1)})" if kc else "unconfirmed",
                   "write_up": f"{SITE}{p.stem}.html#b{m.group(1)}", "code": code}


old = {f"{b['file']}#{b['number']}": b for b in json.loads(JS.read_text())["bugs"]} if JS.exists() else {}
out, problems = [], PROBLEMS
for b in bugs():
    k = f"{b['file']}#{b['number']}"
    o = old.get(k, {})
    b["runs"] = o.get("runs", "")
    if not b["runs"]:
        problems.append(f"{k}: no 'runs' line in bugs.json")
    out.append({key: b[key] for key in ("file", "number", "result", "status", "title", "runs", "write_up", "code")})
head = json.loads(JS.read_text()) if JS.exists() else {}
head = {k: v for k, v in head.items() if k != "bugs"}
JS.write_text(json.dumps({**head, "bugs": out}, indent=1, ensure_ascii=False), encoding="utf-8")

page = PAGE.read_text(encoding="utf-8")
listed = {}
for line in page.split("\n"):  # an entry or a table row: its kind (the table's are wrong output), and KC's mark anywhere in it
    m = re.match(r"(?:- \*\*\(([a-z ,]+)\)\*\* )?(?:\*\*Checked by KC\*\* \([^)]*\)\. )?\*{0,2}\|? ?"
                 r"\[`([\w.]+)` bug (\d+)\]\(\.\./yrec-map/[\w.]+\.html#b\d+\)", line)
    if m:
        listed[f"{m.group(2)}#{m.group(3)}"] = (m.group(1) or "wrong output", "**Checked by KC**" in line)
for b in out:
    k = f"{b['file']}#{b['number']}"
    if b["result"] in ON_PAGE and k not in listed:
        problems.append(f"{k} ({b['result']}): not on the bug page")
    elif k in listed and listed[k][0] != b["result"]:
        problems.append(f"{k}: the bug page says {listed[k][0]}, its page {b['result']}")
    elif k in listed and listed[k][1] != b["status"].startswith("checked"):
        problems.append(f"{k}: the bug page and its page disagree on Checked by KC")
for k in listed:
    if k not in {f"{b['file']}#{b['number']}" for b in out if b["result"] in ON_PAGE}:
        problems.append(f"{k}: on the bug page, but its page marks it otherwise")
print(f"{len(out)} bugs in bugs.json; {len(listed)} on the bug page; {len(problems)} problems")
print("\n".join(problems))
sys.exit(1 if problems else 0)
