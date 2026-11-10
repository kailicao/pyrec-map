#!/bin/bash
# bugcheck_run.sh EXE NML1 NML2 OUTDIR: run one YREC case for checking suspected bugs, with the clone's inputs; the
# outputs, probe.log (the counting lines), stdout.txt, and status.txt ("exit N seconds S") go to OUTDIR.
# The start models are a private tree of links to the clone's (OUTDIR/start): a start model the case writes (an
# F...= "{YREC_START}/..." other than FFIRST, such as FLAST) is a real, writable copy there, so no run writes into
# the clone and no run reads another run's output (Nov 10, 2026: TAMS cases had overwritten the clone's start models,
# from which other cases start). Keep OUTDIR's path short: YREC's file names hold 256 characters.
# The clone is ../yrec beside this repository (the project folder's layout), or $YREC if set.
Y=${YREC:-$(cd "$(dirname "$0")/../../yrec" && pwd)}
mkdir -p "$4" && cd "$4" || exit 9
[ -d start ] && chmod -R u+w start; rm -rf start && cp -rs "$Y/startmodels" start && find start -type d -exec chmod u+w {} + || exit 8
for f in $(grep -hoE '^[[:space:]]*F[A-Z0-9]*[[:space:]]*=[[:space:]]*"\{YREC_START\}/[^"]*"' "$2" "$3" | grep -v '^[[:space:]]*FFIRST' \
           | sed -E 's/.*\{YREC_START\}\/([^"]*)".*/\1/'); do
  [ -L "start/$f" ] && cp --remove-destination "$(readlink "start/$f")" "start/$f" && chmod u+w "start/$f"   # this case writes it
  mkdir -p "start/$(dirname "$f")"
done
export YREC_INPUT=$Y/input YREC_START=$PWD/start YREC_OUTPUT=$PWD YREC_PROBE=$PWD/probe.log
s=$(date +%s); "$1" "$2" "$3" > stdout.txt 2>&1; e=$?
echo "exit $e seconds $(( $(date +%s) - s ))" > status.txt
chmod -R u+w start; rm -rf start
