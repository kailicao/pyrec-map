#!/bin/bash
# bugcheck_tree.sh DIR: a scratch copy of YREC's src/ for checking suspected bugs, in DIR/src: the clone's sources, the
# counting routine (bugcheck_probe.f, its counts written by CALL PROBE_DUMP before main.f's final STOP), and the null
# change behind -DNOISE (nearly every opacity times 1 + 1e-10, before getopac.f's last RETURN). Add counting lines and
# #ifdef FIX_<stem>_<n> fixes to the copy, never to the clone; build one executable per set of macros with
#   make clean; make -j4 REPO_HASH=check GNU_BASE_FFLAGS="-ffixed-line-length-132 -Wall -cpp -J. -DGIT_HASH=\"'check'\" [-D...]"
# (an empty REPO_HASH stops the run at its first write), and run each with bugcheck_run.sh.
Y=${YREC:-$(cd "$(dirname "$0")/../../yrec" && pwd)}
S=$(cd "$(dirname "$0")" && pwd)
mkdir -p "$1" && rm -rf "$1/src" && cp -r "$Y/src" "$1/src" && cp "$S/bugcheck_probe.f" "$1/src/" || exit 9
python3 - "$1/src" <<'EOF'
import sys
d = sys.argv[1]
s = open(f"{d}/getopac.f").read().split("\n")
i = max(k for k, l in enumerate(s) if l.strip() == "RETURN"); assert s[i + 1].strip() == "END"
s[i:i] = ["C PROBE NOISE (a null change, to measure the noise floor)", "#ifdef NOISE", "      O = O*(1.0D0+1.0D-10)",
          "      OL = DLOG10(O)", "#endif"]
open(f"{d}/getopac.f", "w").write("\n".join(s))
m = open(f"{d}/main.f").read().split("\n")
i = max(k for k, l in enumerate(m) if l.strip() == "STOP"); assert m[i + 1].strip() == "END"
m[i:i] = ["C PROBE dump", "      CALL PROBE_DUMP"]
open(f"{d}/main.f", "w").write("\n".join(m))
EOF
