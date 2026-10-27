## Explanation

**Purpose.** The one-time setup of a run's physics: it sets the physical constants used everywhere, then reads (or has read) every table the run needs: opacities, the Fermi–Dirac tables for the degenerate equation of state, the model-atmosphere pressure tables for the surface boundary condition, the OPAL 2006 equation-of-state tables, and the SCV equation-of-state tables.

**How it fits.**
- **Who calls it:** the main program ([[main.f|`main.f`]]), once, after [[parmin.f#PARMIN|`PARMIN`]] has read the namelists. Since "MHP 8/25", the file names are passed as arguments rather than through COMMON.
- **What it calls:** [[hra.f#HRA|`HRA`]] (a fit to the Harvard Reference Atmosphere's $T(\tau)$; here $\log_{10} T$ at $\tau = 2/3$, stored as `HRAS`), [[setupopac.f#SETUPOPAC|`SETUPOPAC`]] (all opacity tables), [[alfilein.f#ALFILEIN|`ALFILEIN`]] (Allard atmospheres, when `KTTAU` = 4), and [[esac06.f#SETEOS06|`SETEOS06`]] (the OPAL 2006 EOS table, when `LOPALE06`; it was read on the first call to `ESAC06` before).
- **Inputs, through modules:** the switches `KTTAU`, `LSCV`, `LOPALE06` from [[nmlpar_mod.f|`NMLPAR_MOD`]]; the unit numbers (`IFERMI`, `IOATM`, `ISCVH`, `ISCVHE`, `ISCVZ`, `ISHORT`) from [[iounits_mod.f|`IOUNITS_MOD`]]; `XENV` from [[comp_mod.f|`COMP_MOD`]], passed on to `SETUPOPAC`.
- **Outputs, through modules:** the constants in [[constants_mod.f|`CONSTANTS_MOD`]] (read by nearly every physics routine); the Debye–Hückel constant `CDH` and charges `DHNUE` ([[debhu_mod.f|`DEBHU_MOD`]], used by [[eqstat.f#EQSTAT|`EQSTAT`]] and others); the Fermi tables `DVAL`, `ETAT8`, `DTABLE`, `IDEN` ([[ccr_mod.f|`CCR_MOD`]], used by [[eqrelv.f#EQRELV|`EQRELV`]]); `HRAS` ([[atmos_mod.f|`ATMOS_MOD`]]); the atmosphere tables `ATMPL`, `ATMTL`, `ATMGL`, `ATMZ` ([[atmos2_mod.f|`ATMOS2_MOD`]]) or `ATMPLC`… ([[atmos2c_mod.f|`ATMOS2C_MOD`]]) and their usable ranges `IMIN`, `IMINMAX`, `IMIN2`, `IMINMAX2` ([[fac_mod.f|`FAC_MOD`]]), used by [[surfp.f#SURFP|`SURFP`]] and [[kcsurfp.f#KCSURFP|`KCSURFP`]]; and the SCV tables `TLOGX`, `NPTSX`, `TABLEX`, `TABLEY`, `TABLEZ` ([[scveos_mod.f|`SCVEOS_MOD`]]), which [[setscv.f#SETSCV|`SETSCV`]] later combines.

**The method.**
1. **Constants** (cgs): $\ln 10$, $M_\odot = 1.9891\times10^{33}$ g, $M_\mathrm{bol,\odot} = 4.79$, a year of $3.1558\times10^7$ s, $c$, $\sigma$, $a/3 = 4\sigma/(3c)$ (`CA3`), $R = 8.31451\times10^7$ (`CGAS`), $\log G = -7.17571$, $m_e$, $k$, $h$, and the combinations
   $$\texttt{CMKH} = \log_{10}\frac{(2\pi m_e k)^{3/2}}{h^3},\qquad \texttt{CDELRL} = -\log_{10}\Bigl(\tfrac{4\pi}{3}\cdot 16\,\sigma\Bigr),\qquad \texttt{CDH} = -\frac{e^3}{3}\sqrt{\frac{\pi}{k\,m_H^3}},$$
   with $m_H = 1/N_A$ g; `CMIXL3` $= 16\sqrt2\,\sigma$. $L_\odot$ and $R_\odot$ are taken from `CONSTANTS_MOD` as already set (initialized there, and in the `PHYSICS` namelist).
2. **Opacity tables** through `SETUPOPAC`.
3. **Fermi–Dirac tables:** 43 values of the density variable `DVAL` and of `ETAT8`, then 860 records of `DTABLE(1..5, I, J)`; the index `IDEN(1..261)` maps a density bin in steps of 0.05 to the table row. A non-increasing `DVAL` stops the run.
4. **Atmosphere pressure tables** (`KTTAU` = 3, 4: 57 $\log T_\mathrm{eff}$ × 11 $\log g$; `KTTAU` = 5: Kurucz/Castelli 2004, 76 × 11, "JNT 6/14"). Missing entries are $-999$; for each temperature, the code records the range of gravities with valid pressures ("G Somers 5/15").
5. **OPAL 2006 EOS tables** (`LOPALE06`): `SETEOS06`. Independent of the SCV tables; a run may use both.
6. **SCV tables** (`LSCV`): for each of 63 temperatures, `NPTSX(I)` rows of 11 quantities for hydrogen and helium, and 13 for metals (the metal table is stored in reverse order of pressure; "computed using the Prather equation of state in the old Yale code").

**Changed since `rp_1`.** COMMON blocks to modules, `IMPLICIT NONE`; the arguments for the removed options dropped (the MHD equation of state, with its call to `MHDTBL`, and the OPAL92, Kurucz 1990, LAOL89 and Alexander 1995 opacity tables: the file names `FKUR`, `FKUR2`, `FLAOL`, `FLAOL2`, `FLLDAT`, `FMHD1`–`FMHD8`, `FOPAL2`, `OPECALEX` and the LAOL mix `V`); the OPAL 2006 EOS table now read here, by `SETEOS06`.

## Questions for the experts

1. **A wrong bound for the Kurucz/Castelli tables (apparent bug).** In the `KTTAU` = 5 branch, a temperature with no valid pressure sets `IMIN2(J) = NG`; the grid there has `NGC` gravities. Both are 11 today, so there is no effect, but the line was copied from the branch above. Use `NGC`.
2. **Fermi table indices read from the file.** `READ(IFERMI,160) (I,J,(DTABLE(K,I,J),K=1,5),NCARDS=1,860)` reads `I` and `J` from each record and uses them as subscripts at once. A bad record writes anywhere in `DTABLE`. Is the file format guaranteed, or should the indices be checked?
3. **"SHOULD BE INT(DVAL,ETC.)".** A comment (MHP 10/02) says the monotonicity test should compare `INT` values, but the line is commented out. Is the current test right?
4. **Constants of different vintages.** $G$, $\sigma$, $k$, $h$, $m_e$ are 1986 CODATA values, $M_\odot$ is set here, but $L_\odot$ and $R_\odot$ come from elsewhere (initialized in `CONSTANTS_MOD`, and in the namelist). `CSECYR` is $3.1558\times10^7$ s, while `RATES` says it uses the sidereal year. Should the constants be updated together?
