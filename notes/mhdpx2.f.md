## Explanation

**Purpose.** `MHDPX2` interpolates one MHD table, chosen by the index `ITBL`, at $(\log P, \log T)$, and stores the result in one row of `VAROUT` (rows 1–3 for the ZAMS tables A, B, C, whatever the sign of `ITBL`; row `ITBL`, 4–8, for the centre tables), together with the table's hydrogen abundance in `XCOMP`.

**How it fits.** Called only by [[mhdpx1.f#MHDPX1|`MHDPX1`]]. Calls [[intpt.f#INTPT|`INTPT`]] (the interpolation) and [[zero.f#ZERO|`ZERO`]] (clears the work vector). It reads the tables from COMMON: the ZAMS tables `TAB1A`, `TAB2A`, `TAB1B`, `TAB2B`, `TAB1C`, `TAB2C` (lower and upper parts, 20 variables) with their compositions `CHEA`, `CHEB`, `CHEC`; the centre tables `TABX1`–`TABX5` (25 variables) with `CHE1`–`CHE5`. All are filled by [[mhdst.f#MHDST|`MHDST`]] and shared only with it.

**The method.** By the comment's nomenclature: `ITBL` = −1, −2, −3 are the lower parts of tables A, B, C and +1, +2, +3 their upper parts (stored in the same output rows 1–3); 4 to 8 are the centre tables 1–5. Each branch calls `INTPT` on its table and copies the result; `XCOMP(row)` = the table's $X$ (`ABFRC…(1)`).

**KC's changes.** 2025-05-30: DO loops rewritten to end on `CONTINUE` (no change in behaviour intended).

## Questions for the experts

1. **Zeros on failure.** `VARO` is zeroed before `INTPT`; when `INTPT` returns early (pressure above the table), the row gets zeros (e.g. $\log\rho = 0$) without any warning.
2. **Repetitive code.** Nine nearly identical branches; passing the table as an argument would shorten it.

### MHDPX2

Interpolates one chosen MHD table at $(\log P, \log T)$ with `INTPT` (above).
