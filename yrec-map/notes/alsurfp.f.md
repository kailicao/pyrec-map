## Explanation

**Purpose.** This file gives the outer boundary condition from the Allard model atmospheres: for a star's $\log T_\mathrm{eff}$ and $\log g$, it returns the pressure (and temperature) at which the interior is joined to the atmosphere. By default it returns $\log P$ at the point where $T = T_\mathrm{eff}$; with the option `LALTPTau100`, $\log P$ and $\log T$ at $\tau = 100$.

**How it fits.**
- **Inputs:** the arguments `TEFFL` ($\log T_\mathrm{eff}$), `GL` ($\log g$) and `LPRT` (print to the model file); the table in `ALATM01_MOD` from [[alfilein.f#ALFILEIN|ALFILEIN]] and its limits in `ALATM02_MOD` from [[altabinit.f#ALTABINIT|ALTABINIT]]; the option `LALTPTau100` in `NMLPAR_MOD`, set in [[parmin.f#PARMIN|PARMIN]].
- **Who calls it:** [[envint.f#ENVINT|ENVINT]] (the envelope integration, for the surface boundary condition) and [[massloss.f#MASSLOSS|MASSLOSS]].
- **What it calls:** [[locate.f#LOCATE|LOCATE]] (bisection in a table) and [[polint.f#POLINT|POLINT]] (polynomial interpolation through 4 points).
- **Outputs:** `AP` ($\log P$) and `AT` ($\log T$) in `ATMPRT_MOD`, shared with ENVINT, [[surfp.f#SURFP|SURFP]], [[kcsurfp.f#KCSURFP|KCSURFP]], [[qatm.f#QATM|QATM]] and MASSLOSS; the flag `LAlFail`, which tells the caller that the point is outside the table. Its comment says the caller should then switch to a gray (`KTTAU = 0`) or Kurucz (`KTTAU = 3`) atmosphere.
- **What the callers do on failure:** [[envint.f#ENVINT|ENVINT]] switches to a gray atmosphere (`KTTAU = 0`, `LTTAU = .TRUE.`); [[massloss.f#MASSLOSS|MASSLOSS]] (marked "experimental code … llp 06/15/2009") tests `LAlFail` and skips the accreted matter's entropy, so the previous lookup's `AT`, `AP` are not used ([[massloss.f#L182-L191]]; settled from the code, Nov 9, 2026).
- **Text output:** a line to `ISHORT` at every call, and to `ISTOR` as well when `LPRT` is true.

**The method.**
1. If $\log T_\mathrm{eff} \ge t_\mathrm{max}$, or $\log g$ is outside the overall range (`GLXmin`, `GLXmax`), set `LAlFail` and return. If $\log T_\mathrm{eff} \le t_\mathrm{min}$, stop the run.

    > **Question** ([[#L149-L195]]). **Asymmetric failure.** Above the table in $T_\mathrm{eff}$ the caller is told to switch atmospheres; below it the run stops. Is a cool star leaving the table meant to end the run?

2. Find 4 rows in $\log T_\mathrm{eff}$ around the point, shifted to stay inside the table. In each row, find 4 valid columns in $\log g$ around the point; if $\log g$ is outside that row's allowed range, set `LAlFail` and return. The header says this range extends one column's width beyond the table on each side ([[#L13-L16]]); [[altabinit.f#ALTABINIT|ALTABINIT]] sets four widths below ([[altabinit.f#q1]]).
3. In each row $i$, interpolate in $\log g$ with the polynomial through the 4 points:
$$y_i(g) = \sum_{k=1}^{4} y(t_i, g_k) \prod_{l \ne k} \frac{g - g_l}{g_k - g_l},$$
for $y = \log P_\mathrm{eff}$, $\log P_{100}$ and $\log T_{100}$.
4. Interpolate the 4 row values in $\log T_\mathrm{eff}$ the same way. Without the $\tau = 100$ option, `AP` is $\log P$ at $T = T_\mathrm{eff}$ and `AT` $= \log T_\mathrm{eff}$; with it, `AP` $= \log P_{100}$ and `AT` $= \log T_{100}$.

Since rows can have different valid columns, each row uses its own 4 values of $\log g$: the grid need not be rectangular.

**Design.** The routine stops the program below the table in $T_\mathrm{eff}$ but only flags the other failures; the stop is a bare `STOP`, exit status 0 ([[#L312-L319]]; `KNOWN_ISSUES.md`, issue 38, open). It writes to `ISHORT` on every call, which can make the short output long.

> **Question** ([[#L290-L304]]; [[#L31]]; [[#L79]]). **A message on every call.** When `LPRT` is false, the routine still writes two lines to `ISHORT` at every call. Was this meant for debugging only? The header also says the print goes to `ISHORT` and `IMODPT`, and that a point outside the table ends the program; the code writes the print to `ISTOR`, and stops only below the table. Should the header be corrected?

**Changed since `rp_1`.** Declarations only: COMMON blocks to modules (`/ALATM01/`, `/ALATM02/`, `/ATMPRT/`; `LALTPTau100` from `/ALATM03/` to `NMLPAR_MOD`, `/LUOUT/` to `IOUNITS_MOD`; the unused `/ALATM04/` dropped), `IMPLICIT NONE`.

### ALSURFP

Two-dimensional 4×4 Lagrange interpolation (in $\log g$, then in $\log T_\mathrm{eff}$) in the Allard table; returns $\log P$ and $\log T$ at the fitting point in `ATMPRT_MOD`, or sets `LAlFail` outside the table.
