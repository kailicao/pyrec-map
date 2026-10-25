## Explanation

**Purpose.** This file interpolates the electron thermal conductivity in the table of A. Y. Potekhin (`condall.d`; Potekhin, Baiko, Haensel and Yakovlev 1999, A&A 346, 345, and Potekhin 1999, A&A 351, 787, per its header), for one ion charge $Z_\mathrm{ion}$, temperature and density. It is Potekhin's published routine (version 23.05.99), with small changes for YREC.

**How it fits.**
- **Inputs:** the arguments `Zion`, `TLG` ($\log T$), `RLG` ($\log\rho$); the table, read from unit `IcondOpacP` (`/MISCOPAC/`) at the first call. [[parmin.f#PARMIN|PARMIN]] sets the unit (75) and opens the file ("MHP 8/25: file opening moved to parmin").
- **Who calls it:** [[condopacpint.f#CONDOPACPINT|CONDOPACPINT]], three times per point (for H, He and a metal of charge 8).
- **What it calls:** [[#HUNT|HUNT]] and [[#CINTERP3|CINTERP3]], both in this file.
- **Outputs:** `CK` = $\log_{10} K$ (the conductivity, cgs), `DRK` = $\partial\log K/\partial\log\rho$, `DTK` = $\partial\log K/\partial\log T$.

**The method.** The table has 15 values of $\log Z_\mathrm{ion}$, 19 of $\log T$ and 64 of $\log\rho$; in the files of `input/opacity/conductive/potekhin/` (`condall.d`, `condall06.d`) they span $Z_\mathrm{ion}$ = 1 to 60, $3 \le \log T \le 9$ (steps of 1/3) and $-6 \le \log\rho \le 9.75$ (steps of 0.25).
1. Locate the point in each grid with HUNT; outside the table the run stops (`CONINTER: … out of range`).
2. Cubic interpolation in $\log\rho$ at 4 temperatures and 2 charges (8 calls to CINTERP3), giving $\log K$ and its derivative in $\log\rho$.
3. Linear interpolation in $\log Z_\mathrm{ion}$.
4. Cubic interpolation in $\log T$, of $\log K$ (giving also $\partial\log K/\partial\log T$) and of $\partial\log K/\partial\log\rho$.

**Design.** The table is kept in local `SAVE`d arrays, read once (`KRUN = 12345` marks it read). The array sizes must match the file. The error branch for $T$ prints the $Z$ grid before stopping, a debugging leftover.

**KC's changes.** 2025-05-30: the integer divisions `MAXZ/2+1` etc. rewritten as `INT(MAXZ/2.)+1` to silence the compiler warning `-Winteger-division`; the result is the same.

## Questions for the experts

1. **Stopping at the table's upper edges.** Any point outside the table stops the run. [[condopacpint.f#CONDOPACPINT|CONDOPACPINT]] guards the call with limits equal to the table's edges ($3 \le \log T \le 9$, $\log\rho \le 9.75$, inclusive). But HUNT returns $N$ for a value equal to the last grid value, so a point at exactly $\log T = 9$ or $\log\rho = 9.75$ passes the guard and stops the run. Rare, but should the guards be strict, or the last interval accepted?

### CONDOPACP

Interpolates $\log K$ and its derivatives in Potekhin's conductivity table: cubic in $\log\rho$ and $\log T$, linear in $\log Z_\mathrm{ion}$. Reads the table at the first call.

### CINTERP3

Interpolation on the interval $[z_0, z_1]$ from 4 tabulated points: a cubic Hermite polynomial whose end slopes are weighted means of the neighboring secant slopes,
$$v'_0 = \frac{(v_1 - v_0)/h^2 + (v_0 - v_-)/h_-^2}{1/h + 1/h_-},$$
and likewise $v'_1$; quadratic at the table's first and last intervals. Returns the value, the first and the second derivative.

### HUNT

Numerical Recipes' `HUNT`: finds $j$ with $x_j \le x < x_{j+1}$ in a monotonic table, starting from the previous index and doubling the step before bisecting. Returns 0 or $N$ outside the table, and $N$ also for a value equal to the last one.
