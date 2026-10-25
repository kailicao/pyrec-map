## Explanation

**Purpose.** Reads the chemical composition block of one MHD equation-of-state table: the number of species, their atomic weights, abundances and abundance fractions, and a mean molecular weight.

**How it fits.**
- **Input:** an unformatted (binary) record on unit `IR`, opened by the caller.
- **Who calls it:** [[mhdst1.f#MHDST1|`MHDST1`]], three times, once for each of the three MHD tables it reads (`IIDX` = 1, 2, 3), filling the arrays `ATWT/ABUN/ABFRCS/GASMU`, `ATWD/ABUD/ABFRCD/GASXD` and `ATWU/ABUU/ABFRCU/GASXU`.
- **Output:** the arguments `NCHEM`, `ATWT`, `ABUN`, `ABFRCS`, `GASMU`.
- **COMMON:** it declares `/CCOUT2/` (debug and output flags, shared with the MHD routines such as [[mhdst.f#MHDST|`MHDST`]] and [[mhdpx.f#MHDPX|`MHDPX`]], and with [[wrtout.f#WRTOUT|`WRTOUT`]] and others), but uses none of its variables.

**The method.** One `READ` of `NCHEM` followed by `NCHEM` triples (weight, abundance, fraction), then `GASMU`. If the table holds more species than the arrays were dimensioned for (`NCHEM0 < NCHEM`), the program stops. Note that the read itself has already written past the arrays' ends by then.

**Design.** The formatted read and the error message are commented out, so the check stops the run without any message.

## Questions for the experts

1. **Silent stop, after the overflow.** In `RABU`, the check `NCHEM0.LT.NCHEM` comes after the `READ` that fills `ATWT(1:NCHEM)` and the others, so an oversized table first writes beyond the arrays, then stops with no message (format 9009 is commented out). Should the count be read first and the message restored?
2. **Unused COMMON.** `/CCOUT2/` is declared but not used. Leftover from the commented-out error print?
