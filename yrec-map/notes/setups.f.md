## Explanation

**Purpose.** The one-time setup of a run's physics: it sets the physical constants used everywhere, then reads (or has read) every table the run needs: opacities, the Fermi–Dirac tables for the degenerate equation of state, the model-atmosphere pressure tables for the surface boundary condition, the OPAL 2006 equation-of-state tables, and the SCV equation-of-state tables.

**How it fits.**
- **Who calls it:** the main program ([`main.f`](main.f.md)), once, after [`PARMIN`](https://github.com/yreclab/yrec/blob/7be4133/src/parmin.f#L16-L1489) has read the namelists. Since "MHP 8/25," the file names are passed as arguments rather than through COMMON.
- **What it calls:** [`HRA`](hra.f.md#hra) (a fit to the Harvard Reference Atmosphere's $`T(\tau)`$; here $`\log_{10} T`$ at $`\tau = 2/3`$, stored as `HRAS`), [`SETUPOPAC`](https://github.com/yreclab/yrec/blob/7be4133/src/setupopac.f#L14-L95) (all opacity tables), [`ALFILEIN`](alfilein.f.md#alfilein) (Allard atmospheres, when `KTTAU` = 4), and [`SETEOS06`](esac06.f.md#seteos06) (the OPAL 2006 EOS table, when `LOPALE06`; it was read on the first call to `ESAC06` before).
- **Inputs, through modules:** the switches `KTTAU`, `LSCV`, `LOPALE06` from [`NMLPAR_MOD`](nmlpar_mod.f.md); the unit numbers (`IFERMI`, `IOATM`, `ISCVH`, `ISCVHE`, `ISCVZ`, `ISHORT`) from [`IOUNITS_MOD`](iounits_mod.f.md); `XENV` from [`COMP_MOD`](comp_mod.f.md), passed on to `SETUPOPAC`.
- **Outputs, through modules:** the constants in [`CONSTANTS_MOD`](constants_mod.f.md) (read by nearly every physics routine); the Debye–Hückel constant `CDH` and charges `DHNUE` ([`DEBHU_MOD`](debhu_mod.f.md), used by [`EQSTAT`](eqstat.f.md#eqstat) and others); the Fermi tables `DVAL`, `ETAT8`, `DTABLE`, `IDEN` ([`CCR_MOD`](ccr_mod.f.md), used by [`EQRELV`](eqrelv.f.md#eqrelv)); `HRAS` ([`ATMOS_MOD`](atmos_mod.f.md)); the atmosphere tables `ATMPL`, `ATMTL`, `ATMGL`, `ATMZ` ([`ATMOS2_MOD`](atmos2_mod.f.md)) or `ATMPLC`… ([`ATMOS2C_MOD`](atmos2c_mod.f.md)) and their usable ranges `IMIN`, `IMINMAX`, `IMIN2`, `IMINMAX2` ([`FAC_MOD`](fac_mod.f.md)), used by [`SURFP`](surfp.f.md#surfp) and [`KCSURFP`](kcsurfp.f.md#kcsurfp); and the SCV tables `TLOGX`, `NPTSX`, `TABLEX`, `TABLEY`, `TABLEZ` ([`SCVEOS_MOD`](scveos_mod.f.md)), which [`SETSCV`](https://github.com/yreclab/yrec/blob/7be4133/src/setscv.f#L4-L255) later combines.

**The method.**
1. **Constants** (cgs): $`\ln 10`$, $`M_\odot = 1.9891\times10^{33}\,\mathrm{g}`$, $`M_\mathrm{bol,\odot} = 4.79`$, a year of $`3.1558\times10^7\,\mathrm{s}`$, $`c`$, $`\sigma`$, $`a/3 = 4\sigma/(3c)`$ (`CA3`), $`R = 8.31451\times10^7`$ (`CGAS`), $`\log G = -7.17571`$, $`m_e`$, $`k`$, $`h`$, and the combinations
   
   $$\displaystyle \texttt{CMKH} = \log\_{10}\frac{(2\pi m\_e k)^{3/2}}{h^3},\qquad \texttt{CDELRL} = -\log\_{10}\Bigl(\tfrac{4\pi}{3}\cdot 16\\,\sigma\Bigr),\qquad \texttt{CDH} = -\frac{e^3}{3}\sqrt{\frac{\pi}{k\\,m\_H^3}},$$
   
   with $`m_H = 1/N_A\,\mathrm{g}`$; `CMIXL3` $`= 16\sqrt2\,\sigma`$, the constant in the coefficient $`A_1`$ of the mixing-length cubic $`A_3V^3 + V^2 + A_1V - 1 = 0`$ that [`TPGRAD`](tpgrad.f.md#tpgrad) solves for the convective efficiency. $`M_\mathrm{bol,\odot}`$ (`CMBOL`) gives the model's bolometric magnitude, $`M_\mathrm{bol} = 4.79 - 2.5\log(L/L_\odot)`$, in [`WRTOUT`](wrtout.f.md#wrtout). $`L_\odot`$ and $`R_\odot`$ are taken from `CONSTANTS_MOD` as already set (initialized there, and in the `PHYSICS` namelist).

    > **Question** ([line 141](https://github.com/yreclab/yrec/blob/7be4133/src/setups.f#L141), [line 148](https://github.com/yreclab/yrec/blob/7be4133/src/setups.f#L148), [lines 156–172](https://github.com/yreclab/yrec/blob/7be4133/src/setups.f#L156-L172)). **Constants of different vintages.** $`G`$, $`\sigma`$, $`k`$, $`h`$, $`m_e`$ are 1986 CODATA values, $`M_\odot`$ is set here, but $`L_\odot`$ and $`R_\odot`$ come from elsewhere (initialized in `CONSTANTS_MOD`, and in the namelist). `CSECYR` is $`3.1558\times10^7\,\mathrm{s}`$, while `RATES` says it uses the sidereal year ([rates.f, line 657](https://github.com/yreclab/yrec/blob/7be4133/src/rates.f#L657)). Should the constants be updated together?

    > **Question** ([line 146](https://github.com/yreclab/yrec/blob/7be4133/src/setups.f#L146)). **$`M_\mathrm{bol,\odot} = 4.79`$.** With $`L_\odot`$ = `CLSUN` = $`3.8515\times10^{33}\,\mathrm{erg\,s^{-1}}`$, the IAU 2015 zero point ($`M_\mathrm{bol} = 0`$ at $`3.0128\times10^{35}\,\mathrm{erg\,s^{-1}}`$) gives $`M_\mathrm{bol,\odot} = 4.73`$, and the IAU nominal value is 4.74; `CMBOL` = 4.79 is fixed here, apart from `CLSUN`, which the namelist can change. Which zero point do the bolometric magnitudes written by WRTOUT follow, and should `CMBOL` be derived from `CLSUN`?

2. **Opacity tables** through `SETUPOPAC`.
3. **Fermi–Dirac tables:** 43 values of the density variable `DVAL` and of `ETAT8`, then 860 records of `DTABLE(1..5, I, J)`; the index `IDEN(1..261)` maps a density bin in steps of 0.05 to the table row. A non-increasing `DVAL` stops the run (exit status 3, an input error).

    **The Fermi table's indices are safe in the shipped file.** `READ(IFERMI,160) (I,J,(DTABLE(K,I,J),K=1,5),NCARDS=1,860)` ([line 221](https://github.com/yreclab/yrec/blob/7be4133/src/setups.f#L221)) reads `I` and `J` from each record and uses them as subscripts at once, so a bad record would write anywhere in `DTABLE(5,43,20)` ([ccr_mod.f, line 26](https://github.com/yreclab/yrec/blob/7be4133/src/ccr_mod.f#L26)); but the 860 records of `input/eos/yale/FERMI.TAB` have 860 distinct pairs, with `I` from 1 to 43 and `J` from 1 to 20 (checked from the file, Nov 10, 2026), so a check of the indices would guard only a user's own table.

    **The real-valued monotonicity test is the right one.** A comment (MHP 10/02) says the test should compare `INT` values, but the line that does is commented out ([lines 227–229](https://github.com/yreclab/yrec/blob/7be4133/src/setups.f#L227-L229)). The active test is right for the shipped table. In `FERMI.TAB`, `DVAL` is strictly increasing but not spaced by whole numbers ($`-16`$, $`-15`$, …, $`-12`$, $`-11.5`$, …), so an `INT` test would stop the run at 29 of its 41 checks (checked from the file, Nov 10, 2026), and the comment can go.

4. **Atmosphere pressure tables** (`KTTAU` = 3, 4: 57 $`\log T_\mathrm{eff}`$ $`\times`$ 11 $`\log g`$; `KTTAU` = 5: Kurucz/Castelli 2004, $`76 \times 11`$, "JNT 6/14"). Missing entries are $`-999`$; for each temperature, the code records the range of gravities with valid pressures ("G Somers 5/15"; for `KTTAU` = 5, bug 1).
5. **OPAL 2006 EOS tables** (`LOPALE06`): `SETEOS06`. Independent of the SCV tables; a run may use both.
6. **SCV tables** (`LSCV`): for each of 63 temperatures, `NPTSX(I)` rows of 11 quantities for hydrogen and helium, and 13 for metals (the metal table is stored in reverse order of pressure; "computed using the Prather equation of state in the old Yale code").

**From YREC's documentation.** [Control Options](https://yrec.readthedocs.io/en/latest/namelist_control.html) (Input files) and [Microphysics in YREC](https://yrec.readthedocs.io/en/latest/microphysics.html): `FFERMI` is the table of Fermi integrals for partial (and relativistic) degeneracy, required for every run; `FSCVH`, `FSCVHE`, `FSCVZ` the SCV EOS tables for H, He and metals (the last generated with YREC's own EOS, for consistency); `FATM` the Kurucz or Kurucz/Castelli atmosphere table; `FALLARD` the Allard atmospheres (solar $`Z`$ only). [Physics Options](https://yrec.readthedocs.io/en/latest/namelist_physics.html) (Constants): the code works in cgs but writes solar units, with `CLSUN` and `CRSUN` as $`L_\odot`$ and $`R_\odot`$.

**Changed since `rp_1`.** COMMON blocks to modules, `IMPLICIT NONE`; the arguments for the removed options dropped (the MHD equation of state, with its call to `MHDTBL`, and the OPAL92, Kurucz 1990 (the code's name; probably the opacities of Kurucz [1991](https://ui.adsabs.harvard.edu/abs/1991ASIC..341..441K), “New Opacity Calculations”), LAOL89 and Alexander 1995 (the code's name for the tables of Alexander & Ferguson [1994](https://ui.adsabs.harvard.edu/abs/1994ApJ...437..879A)) opacity tables: the file names `FKUR`, `FKUR2`, `FLAOL`, `FLAOL2`, `FLLDAT`, `FMHD1`–`FMHD8`, `FOPAL2`, `OPECALEX` and the LAOL mix `V`); the OPAL 2006 EOS table now read here, by `SETEOS06`.

**Changed since `a8a5950`.** The stop on a bad Fermi table now exits with status 3, the code for input errors (`KNOWN_ISSUES.md`, issue 38).

## Bugs, by priority

1. **(never occurred)** **A wrong bound for the Kurucz/Castelli tables.** ([line 355](https://github.com/yreclab/yrec/blob/7be4133/src/setups.f#L355); [lines 59–60](https://github.com/yreclab/yrec/blob/7be4133/src/setups.f#L59-L60)) In the `KTTAU` = 5 branch, a temperature with no valid pressure sets `IMIN2(J) = NG`, the number of gravities of the other grid (`KTTAU` = 3, 4); this grid has `NGC`. The line was copied from the branch above ([line 298](https://github.com/yreclab/yrec/blob/7be4133/src/setups.f#L298)). Both are 11 today, so there is no effect; it would matter if the Kurucz/Castelli grid gained gravities.

    **A possible fix:**

    ```diff
    --- a/src/setups.f
    +++ b/src/setups.f
    @@ -352,7 +352,9 @@
     C          if all of the P values at a given T are -999, set IMIN
     C          to the number of gravity terms. in responce, the code
     C          should break when trying to find surface P.
    -           IF(.NOT.LCATCH) IMIN2(J) = NG
    +C 11/09/26 KC via Claude
    +C code changed to use this grid's number of gravities, NGC.
    +           IF(.NOT.LCATCH) IMIN2(J) = NGC
             END DO
     C END JNT 6/14
           ENDIF
    ```

    **Checked by running YREC** (Nov 9, 2026; a line added at each suspected path counted how often it was taken, the outputs otherwise unchanged): YREC's cases do not use `KTTAU` = 5, so `testsuite/Test_solarGS98_kurucz` was run with `KTTAU` = 5 and `FATM` = `atmos/CastelliKurucz/atmk2004p00.tab`, as `input/atmos/CastelliKurucz/README` asks ("You NEED TO CHANGE KTTAU to 5"). The loop ran for all 76 temperatures, and each had a valid pressure, so the line never assigned `NG`; with `NG` = `NGC` = 11 it would change nothing anyway. The fix was not run, and the item stays fragile code. The line is a copy of [line 298](https://github.com/yreclab/yrec/blob/7be4133/src/setups.f#L298); no comment says otherwise.
