## Explanation

**Purpose.** This file interpolates the electron thermal conductivity in the table of A. Y. Potekhin (`condall.d`; Potekhin, Baiko, Haensel and Yakovlev 1999, A&A 346, 345, and Potekhin 1999, A&A 351, 787, per its header), for one ion charge $Z_\mathrm{ion}$, temperature and density. It is Potekhin's published routine (version 23.05.99), with small changes for YREC.

**How it fits.**
- **Inputs:** the arguments `Zion`, `TLG` ($\log T$), `RLG` ($\log\rho$); the table, read from unit `IcondOpacP` ([[iounits_mod.f#IOUNITS_MOD|`IOUNITS_MOD`]]) at the first call. [[parmin.f#PARMIN|PARMIN]] sets the unit (75) and opens the file ("MHP 8/25: file opening moved to parmin").
- **Who calls it:** [[condopacpint.f#CONDOPACPINT|CONDOPACPINT]], three times per point (for H, He and a metal of charge 8).
- **What it calls:** [[#HUNT|HUNT]] and [[#CINTERP3|CINTERP3]], both in this file.
- **Outputs:** `CK` = $\log_{10} K$ (the conductivity, cgs), `DRK` = $\partial\log K/\partial\log\rho$, `DTK` = $\partial\log K/\partial\log T$.

**The method.** The table has 15 values of $\log Z_\mathrm{ion}$, 19 of $\log T$ and 64 of $\log\rho$; in the files of `input/opacity/conductive/potekhin/` (`condall.d`, `condall06.d`) they span $Z_\mathrm{ion}$ = 1 to 60, $3 \le \log T \le 9$ (steps of 1/3) and $-6 \le \log\rho \le 9.75$ (steps of 0.25).
1. Locate the point in each grid with HUNT; outside the table the run stops (`CONINTER: … out of range`).
2. Cubic interpolation in $\log\rho$ at 4 temperatures and 2 charges (8 calls to CINTERP3), giving $\log K$ and its derivative in $\log\rho$.
3. Linear interpolation in $\log Z_\mathrm{ion}$.
4. Cubic interpolation in $\log T$, of $\log K$ (giving also $\partial\log K/\partial\log T$) and of $\partial\log K/\partial\log\rho$.

**Design.** The table is kept in local `SAVE`d arrays, read once (`KRUN = 12345` marks it read). The array sizes must match the file. The error branch for $T$ prints the $Z$ grid before stopping, a debugging leftover.

**From YREC's documentation.** [Physics Options](https://yrec.readthedocs.io/en/latest/namelist_physics.html): `LCONDOPACP` uses the updated conductive opacity tables, whose path is `FcondOpacP` ([Control Options](https://yrec.readthedocs.io/en/latest/namelist_control.html)).

**Changed since `rp_1`.** Declarations only: `/MISCOPAC/` to `IOUNITS_MOD`, `IMPLICIT NONE` in all three units.

## Bugs, by priority

1. **(never occurred)** **A point on the table's last temperature or density stops the run.** ([[#L99-L109]]) `HUNT` returns `N` for a value equal to the last grid value ([[#L269-L276]]), and the tests after it treat `N` as out of range, so the run stops ("CONINTER: T out of range," "CONINTER: rho out of range"). [[condopacpint.f#CONDOPACPINT|`CONDOPACPINT`]] guards its calls with limits that include the table's upper edges, $\log T \le 9$ and $\log\rho \le 9.75$ ([[condopacpint.f#L54]]), so a point at exactly $\log T = 9$ or $\log\rho = 9.75$ passes the guard and stops the run. Only with `LcondOpacP` (off by default, set in all 51 decks of the test suite and recommended by the user guide), and only at exactly these values, so rare.

    **A possible fix:**

    ```diff
    --- a/src/condopacp.f
    +++ b/src/condopacp.f
    @@ -96,7 +96,11 @@
           ZLG=dlog10(Zion)
           call HUNT(AZ,MAXZ,ZLG,IZ)
           if (IZ.eq.0.or.IZ.eq.MAXZ) stop'CONINTER: Z out of range'
    +C 11/09/26 KC via Claude
    +C code changed to accept a point on the table's last temperature or
    +C density, which HUNT returns as JLO = N, in the last interval.
           call HUNT(AT,MAXT,TLG,IT)
    +      IF(IT.EQ.MAXT.AND.TLG.LE.AT(MAXT)) IT=MAXT-1
     
     C      if (IT.eq.0.or.IT.eq.MAXT) stop'CONINTER: T out of range'
           if (IT.eq.0.or.IT.eq.MAXT) then
    @@ -106,6 +110,7 @@
           endif
     
           call HUNT(AR,MAXR,RLG,IR)
    +      IF(IR.EQ.MAXR.AND.RLG.LE.AR(MAXR)) IR=MAXR-1
           if (IR.eq.0.or.IR.eq.MAXR) stop'CONINTER: rho out of range'
           ITM=max0(1,IT-1)
           ITP=min0(MAXT,IT+2)
    ```

    **Checked by running YREC** (Nov 9, 2026; a line added at each suspected path counted how often it was taken, the outputs otherwise unchanged): 34 runs, 26 of YREC's cases (from a 0.04 $M_\odot$ brown dwarf and the solar models to 9 $M_\odot$, rotation, and helium burning) and 8 made-up ones (each one of YREC's cases with a few settings changed), of which one stopped in its first second. The table lookup ran in all 33 others, from 0.18 million to 223 million times a run, at $\log T$ = 3 to 8.40 and $\log\rho$ = −6 to 7.45. No point fell on the table's last temperature or density, and no run stopped here, so the fix was not run. What would reach it: a point at exactly $\log T = 9$ or $\log\rho = 9.75$, beyond the conditions of every run. Intent: none found; the temperature stop was rewritten to print the indices ([[#L101-L106]]), keeping the test.

### CONDOPACP

Interpolates $\log K$ and its derivatives in Potekhin's conductivity table: cubic in $\log\rho$ and $\log T$, linear in $\log Z_\mathrm{ion}$. Reads the table at the first call.

### CINTERP3

Interpolation on the interval $[z_0, z_1]$ from 4 tabulated points: a cubic Hermite polynomial whose end slopes are weighted means of the neighboring secant slopes,
$$v'_0 = \frac{(v_1 - v_0)/h^2 + (v_0 - v_-)/h_-^2}{1/h + 1/h_-},$$
and likewise $v'_1$; quadratic at the table's first and last intervals. Returns the value, the first and the second derivative.

### HUNT

Numerical Recipes' `HUNT`: finds $j$ with $x_j \le x < x_{j+1}$ in a monotonic table, starting from the previous index and doubling the step before bisecting. Returns 0 or $N$ outside the table, and $N$ also for a value equal to the last one.
