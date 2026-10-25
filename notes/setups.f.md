## Explanation

**Purpose.** The one-time setup of a run's physics: it sets the physical constants used everywhere, then reads (or has read) every table the run needs: opacities, the MHD equation of state, the Fermi–Dirac tables for the degenerate equation of state, the model-atmosphere pressure tables for the surface boundary condition, and the SCV equation-of-state tables.

**How it fits.**
- **Who calls it:** the main program ([[main.f|`main.f`]]), once, after [[parmin.f#PARMIN|`PARMIN`]] has read the namelists. Since "MHP 8/25", the file names are passed as arguments rather than through COMMON.
- **What it calls:** [[hra.f#HRA|`HRA`]] (a fit to the Harvard Reference Atmosphere's $T(\tau)$; here $\log_{10} T$ at $\tau = 2/3$, stored as `HRAS`), [[setupopac.f#SETUPOPAC|`SETUPOPAC`]] (all opacity tables), [[mhdtbl.f#MHDTBL|`MHDTBL`]] (MHD tables, when `LMHD`), and [[alfilein.f#ALFILEIN|`ALFILEIN`]] (Allard atmospheres, when `KTTAU` = 4).
- **Outputs, through COMMON:** the constants in `/CONST/`, `/CONST1/`, `/CONST2/`, `/CONST3/` (read by nearly every physics routine); the Debye–Hückel constant `CDH` and charges `DHNUE` (`/DEBHU/`, used by [[eqstat.f#EQSTAT|`EQSTAT`]] and others); the Fermi tables `DVAL`, `ETAT8`, `DTABLE`, `IDEN` (`/CCR/`, used by [[eqrelv.f#EQRELV|`EQRELV`]]); the atmosphere tables `ATMPL`, `ATMTL`, `ATMGL`, `ATMZ` (`/ATMOS2/`) or `ATMPLC`… (`/ATMOS2C/`) and their usable ranges `IMIN`, `IMINMAX`, `IMIN2`, `IMINMAX2` (`/FAC/`), used by [[surfp.f#SURFP|`SURFP`]] and [[kcsurfp.f#KCSURFP|`KCSURFP`]]; and the SCV tables `TLOGX`, `NPTSX`, `TABLEX`, `TABLEY`, `TABLEZ` (`/SCVEOS/`), which [[setscv.f#SETSCV|`SETSCV`]] later combines. The argument `V` (the Cox–Stewart mix of the LAOL tables) is passed back from `SETUPOPAC`.

**The method.**
1. **Constants** (cgs): $\ln 10$, $M_\odot = 1.9891\times10^{33}$ g, $M_\mathrm{bol,\odot} = 4.79$, a year of $3.1558\times10^7$ s, $c$, $\sigma$, $a/3 = 4\sigma/(3c)$ (`CA3`), $R = 8.31451\times10^7$ (`CGAS`), $\log G = -7.17571$, $m_e$, $k$, $h$, and the combinations
   $$\texttt{CMKH} = \log_{10}\frac{(2\pi m_e k)^{3/2}}{h^3},\qquad \texttt{CDELRL} = -\log_{10}\Bigl(\tfrac{4\pi}{3}\cdot 16\,\sigma\Bigr),\qquad \texttt{CDH} = -\frac{e^3}{3}\sqrt{\frac{\pi}{k\,m_H^3}},$$
   with $m_H = 1/N_A$ g; `CMIXL3` $= 16\sqrt2\,\sigma$. $L_\odot$ and $R_\odot$ are taken from `/CONST/` as already set.
2. **Opacity and MHD tables** through the routines above.
3. **Fermi–Dirac tables:** 43 values of the density variable `DVAL` and of `ETAT8`, then 860 records of `DTABLE(1..5, I, J)`; the index `IDEN(1..261)` maps a density bin in steps of 0.05 to the table row. A non-increasing `DVAL` stops the run.
4. **Atmosphere pressure tables** (`KTTAU` = 3, 4: 57 $\log T_\mathrm{eff}$ × 11 $\log g$; `KTTAU` = 5: Kurucz/Castelli 2004, 76 × 11, "JNT 6/14"). Missing entries are $-999$; for each temperature, the code records the range of gravities with valid pressures ("G Somers 5/15").
5. **SCV tables** (`LSCV`): for each of 63 temperatures, `NPTSX(I)` rows of 11 quantities for hydrogen and helium, and 13 for metals (the metal table is stored in reverse order of pressure; "computed using the Prather equation of state in the old Yale code").

## Questions for the experts

1. **A wrong bound for the Kurucz/Castelli tables (apparent bug).** In the `KTTAU` = 5 branch, a temperature with no valid pressure sets `IMIN2(J) = NG`; the grid there has `NGC` gravities. Both are 11 today, so there is no effect, but the line was copied from the branch above. Use `NGC`.
2. **Fermi table indices read from the file.** `READ(IFERMI,160) (I,J,(DTABLE(K,I,J),K=1,5),NCARDS=1,860)` reads `I` and `J` from each record and uses them as subscripts at once. A bad record writes anywhere in `DTABLE`. Is the file format guaranteed, or should the indices be checked?
3. **"SHOULD BE INT(DVAL,ETC.)".** A comment (MHP 10/02) says the monotonicity test should compare `INT` values, but the line is commented out. Is the current test right?
4. **Constants of different vintages.** $G$, $\sigma$, $k$, $h$, $m_e$ are 1986 CODATA values, $M_\odot$ is set here, but $L_\odot$ and $R_\odot$ come from elsewhere (the namelist, probably). `CSECYR` is $3.1558\times10^7$ s, while `RATES` says it uses the sidereal year. Should the constants be updated together?
