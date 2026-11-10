# Glossary

Every variable declared in one of YREC's 85 modules (898 in all), under its current name in lower case, as pyrec writes it. Some of YREC's names are not intuitive, and their history explains why: many are short, from the days of Fortran 77, and their types are implied by the first letter (`a`–`h` and `o`–`z` real, `i`–`n` integer, `l` logical). They are kept and explained here rather than renamed (Kaili Cao, Oct 31, 2026); every file page lists the variables its source uses, linked to their entries. The physics is written in the YREC paper's symbols (the overview's Notation); "log" is base 10 unless stated. Where neither the code nor YREC's documentation says what a variable holds, or its units, the entry says what is known and asks, in italics (42 entries). The constants and the input/output units come first, then the namelist modules, then the other modules in alphabetical order. An array's dimensions follow its meaning in parentheses, as in `(JSON)`, where `json` is the maximum number of shells.

## CONSTANTS_MOD

The physical and mathematical constants (solar units, $\ln 10$, $\pi$, $G$, $\sigma$, the gas constant, and their logarithms), all `REAL*8` and, apart from `CAVOG`, set at run time.

- **`c4pi`**: $4\pi$; set in [[setups.f#SETUPS|`SETUPS`]].
- **`c4pi3l`**: $\log_{10}(4\pi/3)$; set in [[setups.f#SETUPS|`SETUPS`]]. *Name:* C, 4 PI over 3, Log.
- **`c4pil`**: $\log_{10} 4\pi$; set in [[setups.f#SETUPS|`SETUPS`]]. *Name:* C, 4 PI, Log.
- **`ca3`**: $a/3 = 4\sigma/3c$, the radiation constant over three, in erg cm⁻³ K⁻⁴; set in [[setups.f#SETUPS|`SETUPS`]].
- **`ca3l`**: $\log_{10}(a/3)$; set in [[setups.f#SETUPS|`SETUPS`]] but never read.
- **`cavog`**: Avogadro's number, defined as $1/m_u$ with $m_u = 1.6605402\times10^{-24}$ g, in g⁻¹; a `PARAMETER`; read by [[engeb.f#ENGEB|`ENGEB`]] and [[deutrate.f#DEUTRATE|`DEUTRATE`]] in the deuterium-burning rate. *Name:* C, AVOGadro.
- **`cc13`**: $1/3$; set in [[setups.f#SETUPS|`SETUPS`]] (and earlier, to the same value, in [[parmin.f#PARMIN|`PARMIN`]]). *Name:* C, 1 over 3.
- **`cc23`**: $2/3$; set in [[setups.f#SETUPS|`SETUPS`]] (and in [[parmin.f#PARMIN|`PARMIN`]]).
- **`cdelrl`**: $-\log_{10}(4\pi/3) - \log_{10}\sigma - \log_{10}16$, the constant of the radiative gradient $\nabla_\mathrm{rad}$; set in [[setups.f#SETUPS|`SETUPS`]]. *Name:* C, DEL R ($\nabla_\mathrm{rad}$), Log.
- **`cgas`**: the molar gas constant $\mathcal{R}$, 8.314510D7 erg mol⁻¹ K⁻¹; set in [[setups.f#SETUPS|`SETUPS`]].
- **`cgl`**: $\log_{10} G$ (−7.17571, for $G = 6.67259\times10^{-8}$ cgs); set in [[setups.f#SETUPS|`SETUPS`]]. *Name:* C, G, Log.
- **`cln`**: $\ln 10$; set in [[setups.f#SETUPS|`SETUPS`]] (and earlier in [[parmin.f#PARMIN|`PARMIN`]]); read by 68 files. *Name:* C, LN.
- **`clndp`**: $\ln 10$, the value `CLN` is copied from; set in [[setups.f#SETUPS|`SETUPS`]].
- **`clni`**: $1/\ln 10$; set in [[setups.f#SETUPS|`SETUPS`]]. *Name:* C, LN Inverse.
- **`clnsun`**: $\ln 10/L_\odot$, in erg⁻¹ s; set in [[setups.f#SETUPS|`SETUPS`]].
- **`clsun`**: the solar luminosity $L_\odot$, in erg s⁻¹ (default 3.8515D33); in the `PHYSICS` namelist, so a run can change it. *Name:* C for constant, L for luminosity, SUN.
- **`clsunl`**: $\log_{10} L_\odot$; set in [[setups.f#SETUPS|`SETUPS`]].
- **`cmbol`**: the Sun's bolometric magnitude, 4.79; set in [[setups.f#SETUPS|`SETUPS`]]. *Name:* C, M BOLometric.
- **`cmixl2`**: $1/3$, a constant of the mixing-length theory; set in [[setups.f#SETUPS|`SETUPS`]].
- **`cmixl3`**: $16\sqrt2\,\sigma$, a constant of the mixing-length theory, in erg cm⁻² s⁻¹ K⁻⁴; set in [[setups.f#SETUPS|`SETUPS`]].
- **`cmkh`**: $\log_{10}[(2\pi m_e)^{3/2}k^{5/2}/h^3]$, for the Saha equation (cgs); set in [[setups.f#SETUPS|`SETUPS`]]. *Name:* C, $m_e$, $k$, $h$.
- **`cmkhn`**: set and read nowhere.
- **`cmsun`**: the solar mass $M_\odot$, 1.9891D33 g; set in [[setups.f#SETUPS|`SETUPS`]].
- **`cmsunl`**: $\log_{10} M_\odot$; set in [[setups.f#SETUPS|`SETUPS`]] but never read.
- **`cpi`**: $\pi$; set in [[setups.f#SETUPS|`SETUPS`]].
- **`crsun`**: the solar radius $R_\odot$, in cm (default 6.9598D10); in the `PHYSICS` namelist, so a run can change it. *Name:* C, R for radius, SUN.
- **`crsunl`**: $\log_{10} R_\odot$; set in [[setups.f#SETUPS|`SETUPS`]].
- **`csecyr`**: seconds per year, 3.1558D7 s yr⁻¹; set in [[setups.f#SETUPS|`SETUPS`]]. *Name:* C, SEConds per YeaR.
- **`csig`**: the Stefan–Boltzmann constant $\sigma$, 5.67051D-5 erg cm⁻² s⁻¹ K⁻⁴; set in [[setups.f#SETUPS|`SETUPS`]]. *Name:* C, SIGma.
- **`csigl`**: $\log_{10}\sigma$; set in [[setups.f#SETUPS|`SETUPS`]].
- **`c_2`**: $c_2 = 0.0506$, the constant of the centrifugal term in the Matt et al. wind law; set in [[parmin.f#PARMIN|`PARMIN`]], read by [[mwind.f#MWIND|`MWIND`]] and [[mcowind.f#MCOWIND|`MCOWIND`]].

## IOUNITS_MOD

The Fortran logical unit numbers of every input and output file, all `INTEGER*4`, assigned in [[parmin.f#PARMIN|`PARMIN`]] (fixed in the code, not inputs).

- **`ialex06`**: unit 90, the low-temperature opacities of Ferguson et al. (2005), called ALEX06 in the code, read by [[readalex06.f#READALEX06|`READALEX06`]]. *Name:* I for unit, ALEXander 2006.
- **`iclcd`**: unit 91, the acoustic-depth output; assigned only with `LACOUT`.
- **`icondopacp`**: unit 75, the Potekhin conductive opacities, read by [[condopacp.f#CONDOPACP|`CONDOPACP`]]; declared `IcondOpacP`. *Name:* I, CONDuctive OPACities, Potekhin.
- **`idebug`**: unit 18, reserved for debugging output.
- **`ifermi`**: unit 15, the Fermi–Dirac tables, read by [[setups.f#SETUPS|`SETUPS`]].
- **`ifirst`**: unit 12, the starting model.
- **`ijlast`**: the unit to which [[wrtout.f#WRTOUT|`WRTOUT`]] writes the model with `LJLAST` (acoustic-depth output), but assigned nowhere; the branch never runs, since `LACOUT` cannot be turned on.
- **`ilast`**: unit 11, the last model.
- **`iliv95`**: unit 48, the OPAL95 opacity table, read by [[ll95tbl.f#LL95TBL|`LL95TBL`]].
- **`imilne`**: unit 21, Milne's invariant variables, written by [[wrtmil.f#WRTMIL|`WRTMIL`]].
- **`imodpt`**: unit 22, the shell-by-shell output of models.
- **`ioatm`**: unit 38, the Kurucz model atmospheres, read by [[setups.f#SETUPS|`SETUPS`]].
- **`ioatma`**: unit 66, the Allard model atmospheres, read by [[alfilein.f#ALFILEIN|`ALFILEIN`]].
- **`iopale`**: unit 49, the OPAL 2006 equation of state, read by [[readcoeos06.f#READCOEOS06|`READCOEOS06`]].
- **`iopatm`**: unit 26, the atmosphere for a pulsation code (also opened by [[pdist.f#PDIST|`PDIST`]]).
- **`iopenv`**: unit 25, the envelope for a pulsation code.
- **`iopmod`**: unit 24, the interior model for a pulsation code.
- **`iopurez`**: unit 62, the pure-metal ("pure Z," $Z = 1$) LAOL89 opacity table, read by [[rdzlaol.f#RDZLAOL|`RDZLAOL`]] (PARMIN's comment calls it "pure CN").
- **`iowr`**: unit 6, the status output (the screen); the [[main.f#(file level)|main program]] sets it to 9 before calling PARMIN, which overwrites it.
- **`irun`**: unit 13, the `PHYSICS` namelist, read by PARMIN.
- **`iscvh`**: unit 72, the hydrogen table of the SCV equation of state, read by [[setups.f#SETUPS|`SETUPS`]].
- **`iscvhe`**: unit 73, the helium table of the SCV equation of state, read by SETUPS.
- **`iscvz`**: unit 74, the metals table of the SCV equation of state, read by SETUPS.
- **`ishort`**: unit 20, all diagnostic information, the `.short` file.
- **`isnu`**: unit 33, the solar neutrino fluxes. *Name:* I, SNU (the solar neutrino unit).
- **`isound`**: unit 500, the sound-speed profile, written by [[wrtmod.f#WRTMOD|`WRTMOD`]] with `LSOUND`.
- **`istand`**: unit 14, the `CONTROL` namelist, read by PARMIN.
- **`istor`**: unit 23, the saved models, usable as starting models.
- **`itrack`**: unit 19, the evolutionary track.

## NMLBYPASS_MOD

The namelist variables that serve only to set other quantities, or are kept for later development, read by [[parmin.f#PARMIN|`PARMIN`]] and [[remap.f#REMAP|`REMAP`]] but by no physics routine; all are in the `PHYSICS` namelist unless an entry says `CONTROL`.

- **`flag_dw`**: with `LNEWVARS`, copied by [[remap.f#REMAP|`REMAP`]] into `HPTTOL(12)` ([[nmlpar_mod.f#NMLPAR_MOD|`NMLPAR_MOD`]]): the largest spacing in $\log\Omega$ between shells, rotating models only (REMAP's comment), or, as the documentation puts it, the threshold for preserving $\Omega$ discontinuities; in dex, default 0.10. *Name:* the difference in $\Omega$ (W) at which a shell boundary is flagged.
- **`flag_dx`**: with `LNEWVARS`, copied into `HPTTOL(3)`: the difference in $X$ between neighbouring shells above which their boundary is flagged, to avoid numerical diffusion; default 0.05. *Name:* the X difference (DX) that flags a boundary.
- **`flag_dz`**: with `LNEWVARS`, copied into `HPTTOL(4)`: the same for $Z$; default 0.05.
- **`fo`**: default 1.0; written to the `.short` file only, in [[parmin.f#PARMIN|`PARMIN`]]'s summary line, labelled "COUPLING"; read nowhere else. *What it once controlled is not stated: what does "FO" stand for?*
- **`isetiso`**: in `CONTROL`, integer, default 0: whether to impose the isotope ratios and light-element abundances on the starting model; with 1, PARMIN checks the mixture named by `AISO` (`'L21'`, or `'CUS'` for the custom values) and [[starin.f#STARIN|`STARIN`]] applies it. *The documentation gives 2 for the custom mixture, while the code tests only `ISETISO = 1` and takes the custom one from `AISO = 'CUS'`: does 2 still do anything?* *Name:* SET ISOtopes.
- **`isetmix`**: in `CONTROL`, integer, default 0: whether to impose a CNO mixture on the starting model; with 1, PARMIN takes the preset named by `AMIX` (`GS98`, `AAG21`, `M22P`, `M22M`) or, for `'CUS'`, the fractions `FRAC_C`, `FRAC_N`, `FRAC_O`, and STARIN applies them. *The documentation gives 2 for the custom mixture, while the code tests only `ISETMIX = 1` and takes the custom one from `AMIX = 'CUS'`: does 2 still do anything?* *Name:* SET MIXture.
- **`lenvg`**: logical, default `.FALSE.`; read nowhere (the documentation: "Not used. Outer-layer structure calculation after convergence"); it came from the former `COMMON/ENVGEN/`.
- **`lnewnuc`**: logical, default `.FALSE.`; with it, [[remap.f#REMAP|`REMAP`]] derives the rate factors `SSTANDARD` ([[nmlpar_mod.f#NMLPAR_MOD|`NMLPAR_MOD`]]) and `QS0E`, `QQS0EE`, `FC12`, `FO16` ([[cross_mod.f#CROSS_MOD|`CROSS_MOD`]]) from the S-factors `S0_*`, `S0P_*`, `S0PP_*`. *Name:* L for logical, NEW NUClear cross-section format (the documentation).
- **`lnewvars`**: logical, default `.FALSE.`; with it, [[remap.f#REMAP|`REMAP`]] copies the `TOL_*`, `FLAG_*` and `TIME_*` variables and `LSTRUCT_TIME` into `HPTTOL`, `ATIME`, `LPTIME`, `DTWIND` and `DTDIF`. *Name:* NEW VARiable names for the tolerances (the documentation).
- **`lstruct_time`**: logical, default `.FALSE.`; with `LNEWVARS`, copied into `LPTIME`: limit the time step by the changes of $T$, $P$, $r$, $L$ at any shell (`TIME_DT`, `TIME_DP`, `TIME_DR`, `TIME_DL`), used on the pre-main sequence only, and switched off once $\epsilon_\mathrm{grav}$ turns negative near the ZAMS (the documentation). *Name:* STRUCTural changes limit the TIME step.
- **`lxbe91`**: logical, default `.FALSE.`; with it, [[parmin.f#PARMIN|`PARMIN`]] sets the factor `SBE91` = `XSBE91`/1.1 for the p(⁹Be,γ) cross section. *Name:* L, cross section (X) of Be9, channel 1.
- **`lxbe92`**: logical, default `.FALSE.`; with it, PARMIN sets `SBE92` = `XSBE92`/1.5D4 for p(⁹Be,d) (the documentation labels it a p+⁶Li channel, a slip).
- **`lxbe93`**: logical, default `.FALSE.`; with it, PARMIN sets `SBE93` = `XSBE93`/1.5D4 for p(⁹Be,α) (the documentation labels it a p+⁶Li channel, a slip).
- **`lxli6`**: logical, default `.FALSE.`; with it, PARMIN sets `SLI6` = `XSLI6`/5.5D3 for the p+⁶Li cross section.
- **`lxli7`**: logical, default `.FALSE.`; with it, PARMIN sets `SLI7` = `XSLI7`/52 for the p+⁷Li cross section.
- **`npenv`**: in `CONTROL`, integer, no default; [[parmin.f#PARMIN|`PARMIN`]] sets it to 9999 when not positive, as it does `NPOINT` and `NPRTMOD`; read nowhere else. *What it counts is not stated: an interval between envelope printouts, as its name suggests?*
- **`pmma`**: the index $a$ of the Matt et al. wind law (`LMWIND`): the mass-loss rate scales as $\Omega^a$ (through $L_X/L_\mathrm{bol}$); default 2.0, reset by `AWIND` ('K97' and 'V13': 2); [[parmin.f#PARMIN|`PARMIN`]] derives from it the exponent `EXW`. Used as given only with `AWIND = 'CUS'`.
- **`pmmb`**: the index $b$ of the wind law: the field strength scales as $(\Omega R^c)^b$; default 1.0 ('K97' and 'V13': 1); enters `EXW`.
- **`pmmc`**: the index $c$ of the wind law (the power of $R$ in the field strength's $(\Omega R^c)^b$); default 2.0 ('K97': 2, 'V13': 0); enters `EXR`.
- **`pmmd`**: the index $d$ of the wind law: the field strength scales as $\tau_\mathrm{cz}^d$, and $d$ also switches the centrifugal and photospheric-pressure terms; default 0.0 ('K97': 0, 'V13': 1); enters `EXPR`, `EXCEN`.
- **`pmmjd`**: the normalization of $\dot J$ in the wind law, default 1.32D30; [[parmin.f#PARMIN|`PARMIN`]] sets `CONSTFACTOR` = `FK`·`PMMJD`/`PMMSOLW`$^{a_\Omega}$. *Units not stated: the solar $\dot J$ in g cm² s⁻²?*
- **`pmmm`**: the index $m$ of the wind law (the power of the field strength, $B^{4m}$, and of $\dot M^{1-2m}$ in $\dot J$); default 0.5 ('K97': `ALFA`/3, 'V13': 0.22); enters `EXW`, `EXR`, `EXM`, `EXL`, `EXPR`, `EXCEN`.
- **`pmmmd`**: default 1.27D12; read nowhere. *What it holds is not stated: the solar mass-loss rate $\dot M_\odot$, in g s⁻¹?*
- **`r14_15`**: in `CONTROL`, the ¹⁴N/¹⁵N ratio, default 411.9 (Lodders 2021); [[parmin.f#PARMIN|`PARMIN`]] only checks that a custom value is not negative; a placeholder, ¹⁵N is not followed (the documentation). *Name:* Ratio of 14 to 15.
- **`r16_17`**: in `CONTROL`, the ¹⁶O/¹⁷O ratio, default 471.4; checked like `R14_15`; a placeholder, ¹⁷O is not followed. *The default is close to the solar ¹⁶O/¹⁸O ratio, while `R16_18`'s 2693.0 is close to ¹⁶O/¹⁷O: are the two defaults swapped ([[starin.f#b3|`STARIN`'s suspected bug 3]])?*
- **`s0_1_1`**: $S_0$ of p+p, in keV b, default 4.01D-22 (Solar Fusion II); with `LNEWNUC`, [[remap.f#REMAP|`REMAP`]] sets `SSTANDARD(1)` to its ratio to the reference 4.07D-22. *Name:* S0, then the reacting nuclei by mass number (1 for p, 3 for ³He, 12 for ¹²C, …).
- **`s0_1_12`**: $S_0$ of p+¹²C, keV b, default 1.34; gives `SSTANDARD(4)` (reference 1.45).
- **`s0_1_13`**: $S_0$ of p+¹³C, keV b, default 7.6; gives `SSTANDARD(5)` (reference 5.5).
- **`s0_1_14`**: $S_0$ of p+¹⁴N, keV b, default 1.66; gives `SSTANDARD(6)` (reference 3.32).
- **`s0_1_15_c12alp`**: $S_0$ of ¹⁵N(p,α)¹²C, keV b, default 7.3D4; with `LNEWNUC`, sets `FC12` (its ratio to 6.75D4), one side of the N15+p branching. *Name:* p+15 giving C12 + ALPha.
- **`s0_1_15_o16`**: $S_0$ of ¹⁵N(p,γ)¹⁶O, keV b, default 36; sets `FO16` (its ratio to 64), the other side of the branching. *Name:* p+15 giving O16.
- **`s0_1_16`**: $S_0$ of p+¹⁶O, keV b, default 10.6; gives `SSTANDARD(7)` (reference 9.4).
- **`s0_1_be7e`**: the proportionality constant of ⁷Be+e⁻ capture (in its linear term, REMAP's comment), default 1.7709D-10; gives `SSTANDARD(15)` (reference 1.752D-10). *Units not stated: which units does it take?* *Name:* Be7 + Electron.
- **`s0_1_be7p`**: $S_0$ of p+⁷Be, keV b, default 0.0208; gives `SSTANDARD(16)` (reference 0.0243). *Name:* Be7 + P.
- **`s0_3_3`**: $S_0$ of ³He+³He, keV b, default 5.21D3; gives `SSTANDARD(2)` (reference 5.15D3).
- **`s0_3_4`**: $S_0$ of ³He+⁴He, keV b, default 0.56; gives `SSTANDARD(3)` (reference 0.54).
- **`s0_hep`**: $S_0$ of the hep reaction (³He+p), keV b, default 8.6D-20; gives `SSTANDARD(17)` (reference 8.0D-20).
- **`s0_pep`**: the pep rate's proportionality constant relative to p+p (REMAP's comment), default 3.5734D-6; gives `SSTANDARD(14)` (reference 3.4848D-6). *Units not stated: which units does it take?*
- **`s0p_1_1`**: $S'$ of p+p, the first derivative of $S$ in energy, in b, default 4.49D-24; with `LNEWNUC`, [[remap.f#REMAP|`REMAP`]] sets `QS0E(1)` to $(S'/S_0)$ over that of Adelberger et al. (1998). *Name:* S0 Prime.
- **`s0p_1_12`**: $S'$ of p+¹²C, b, default 2.6D-3; gives `QS0E(4)`.
- **`s0p_1_13`**: $S'$ of p+¹³C, b, default -7.83D-3; gives `QS0E(5)`.
- **`s0p_1_14`**: $S'$ of p+¹⁴N, b, default -3.3D-3; gives `QS0E(6)`.
- **`s0p_1_16`**: $S'$ of p+¹⁶O, b, default -5.4D-2; gives `QS0E(7)`.
- **`s0p_1_be7p`**: $S'$ of p+⁷Be, b, default -3.12D-5; gives `QS0E(8)`.
- **`s0p_3_3`**: $S'$ of ³He+³He, b, default -4.9; gives `QS0E(2)`.
- **`s0p_3_4`**: $S'$ of ³He+⁴He, b, default -3.6D-4; gives `QS0E(3)`.
- **`s0pp_1_12`**: $S''$ of p+¹²C, the second derivative of $S$ in energy, default 8.3D-5; with `LNEWNUC`, REMAP sets `QQS0EE(4)` to $(S''/S_0)$ over that of Adelberger et al. (1998). *Units not stated: b keV⁻¹?* *Name:* S0 double Prime.
- **`s0pp_1_13`**: $S''$ of p+¹³C, default 7.29D-4; gives `QQS0EE(5)`. *Units not stated: b keV⁻¹?*
- **`s0pp_1_16`**: $S''$ of p+¹⁶O, default 0.0; gives `QQS0EE(7)`. *Units not stated: b keV⁻¹?*
- **`s0pp_1_be7p`**: $S''$ of p+⁷Be, default -2.288D-7; gives `QQS0EE(8)`. *Units not stated: b keV⁻¹?*
- **`time_core_min`**: with `LNEWVARS`, copied into `ATIME(1)`: the smallest central abundance ($X$ or $Y$) for which the core-burning time-step criteria apply; default 1.0D-3.
- **`time_dl`**: with `LNEWVARS`, copied into `ATIME(11)`: the largest change of $L$ at any shell in a step (pre-main sequence, `LSTRUCT_TIME`); [[ptime.f#PTIME|`PTIME`]] compares the fractional change of $L$ with `TIME_DL`·ln 10, so in dex; default 2.0D-2.
- **`time_dp`**: copied into `ATIME(9)`: the largest change of $\log P$ at any shell in a step (pre-main sequence), dex; default 4.0D-2.
- **`time_dr`**: copied into `ATIME(10)`: the largest change of $\log r$ at any shell in a step (pre-main sequence), dex; default 2.0D-2.
- **`time_dt`**: copied into `ATIME(8)`: the largest change of $\log T$ at any shell in a step (pre-main sequence), dex; default 2.0D-2.
- **`time_dw_global`**: with `LNEWVARS`, copied into `DTWIND`: the largest fractional change of $\Omega$ at any shell per model step ([[wtime.f#WTIME|`WTIME`]]); default 8.0D-2.
- **`time_dw_mix`**: copied into `DTDIF`: the largest fractional change of $\Omega$ per rotational-mixing substep ([[getw.f#GETW|`GETW`]]); default 8.0D-2.
- **`time_dx_core_frac`**: copied into `ATIME(3)`: the largest fraction of the central $X$ burned in a step (core hydrogen burning); default 0.5.
- **`time_dx_core_tot`**: copied into `ATIME(2)`: the largest absolute change of the central $X$ in a step; default 2.0D-2.
- **`time_dx_shell`**: copied into `ATIME(7)`: the largest fraction of $X$ burned in the hydrogen shell in a step; default 0.1.
- **`time_dx_total`**: copied into `ATIME(6)`: the largest mass of hydrogen burned in a step, in $M_\odot$; default 1.5D-3.
- **`time_dy_core_frac`**: copied into `ATIME(5)`: the largest fraction of the central $Y$ burned in a step (core helium burning); default 0.5.
- **`time_dy_core_tot`**: copied into `ATIME(4)`: the largest absolute change of the central $Y$ in a step; default 2.0D-2.
- **`time_dy_shell`**: copied into `ATIME(12)`: the largest fraction of $Y$ burned in the helium shell in a step; default 0.1.
- **`time_dy_total`**: copied into `ATIME(14)`: the largest mass of helium burned in a step, in $M_\odot$; default 1.5D-3.
- **`time_max_dt_frac`**: copied into `ATIME(13)`: the largest factor by which the time step may change from one model to the next; default 1.5. *Name:* the MAXimum DT FRACtion (an older comment writes `TIME_MAX_DT_FAC`).
- **`tol_czbase_fine_width`**: with `LNEWVARS`, copied into `HPTTOL(7)`: the width, in $\log P$, of the finely zoned region at the base of the convective envelope; default 0.0 (none; the documentation suggests 0.4 for red giants). *Name:* TOLerance, Convection Zone BASE.
- **`tol_dl_max`**: copied into `HPTTOL(9)`: the largest spacing in $L/L_\mathrm{surf}$ between shells; default 0.02.
- **`tol_dm_max`**: copied into `HPTTOL(2)`: the largest spacing in $\log m$ between shells; default 0.08.
- **`tol_dm_min`**: copied into `HPTTOL(1)`: the smallest spacing in $\log m$ between shells (REMAP's comment; the documentation: in mass, important for the thin outer fitting points); default 1.0D-8.
- **`tol_dp_core_max`**: copied into `HPTTOL(11)`: the largest spacing in $\log P$ between shells in the radiative interior; default 0.05.
- **`tol_dp_czbase_max`**: copied into `HPTTOL(10)`: the largest spacing in $\log P$ near the base of the convective envelope; default 0.05.
- **`tol_dp_env_max`**: copied into `HPTTOL(8)`: the largest spacing in $\log P$ in the convective envelope; default 0.05.
- **`tol_dx_max`**: copied into `HPTTOL(5)`: the largest spacing in $X$ between shells, usually disabled (default 1.0; the documentation calls it legacy).
- **`tol_dz_max`**: copied into `HPTTOL(6)`: the largest spacing in $Z$ between shells, usually disabled (default 1.0).
- **`xb10_ini`**: in `CONTROL`, the initial ¹⁰B mass fraction, default 1.002D-9 (Lodders 2021); [[parmin.f#PARMIN|`PARMIN`]] only checks a custom value (not negative, and the light elements' sum below 1); a placeholder, B is not followed. *Name:* X (mass fraction) of B10, INItial.
- **`xb11_ini`**: in `CONTROL`, the initial ¹¹B mass fraction, default 4.405D-9; checked like `XB10_INI`; a placeholder.
- **`xsbe91`**: the p(⁹Be,γ) cross section, keV b, default 1.1; used with `LXBE91`. *Name:* X-Section of Be9, channel 1.
- **`xsbe92`**: the p(⁹Be,d) cross section, keV b, default 1.5D4; used with `LXBE92`.
- **`xsbe93`**: the p(⁹Be,α) cross section, keV b, default 1.5D4; used with `LXBE93`.
- **`xsli6`**: the p+⁶Li cross section, keV b, default 5.5D3; used with `LXLI6`. *Name:* X-Section of Li6.
- **`xsli7`**: the p+⁷Li cross section, keV b, default 52; used with `LXLI7`.
- **`zxmix`**: in `CONTROL`, $Z/X$ of the CNO mixture, default 0.02292 (GS98); [[parmin.f#PARMIN|`PARMIN`]] sets it from the preset named by `AMIX` (with `ISETMIX = 1`); otherwise only written to the `.short` file in the `DERIVED` namelist. *Name:* Z/X of the MIXture.

## NMLPAR_MOD

The run's settings that the physics routines read: the members of the `CONTROL` and `PHYSICS` namelists, read by [[parmin.f#PARMIN|`PARMIN`]], and a few quantities PARMIN derives from them (written in its output-only `DERIVED` namelist). An entry is in `PHYSICS` unless it says `CONTROL` or derived; a default is the module's initializer.

- **`abstol`**: the absolute convergence criterion for abundance changes in the burning network, [[kemcom.f#KEMCOM|`KEMCOM`]]; default 1.0D-5. *Name:* ABSolute TOLerance.
- **`acfpft`**: the fractional accuracy of the rotational distortion (the departure from spherical symmetry, "cubed" per the documentation), for [[shape.f#SHAPE|`SHAPE`]]; default 1.0D-36; [[checkj.f#CHECKJ|`CHECKJ`]] raises it temporarily to at least `DJOK`$\times10^{-2}$. *Name:* ACcuracy of the distortion factors FP, FT ($f_P$, $f_T$).
- **`alatm_alpha`**: the $\alpha$-enhancement asked of the Allard atmosphere tables (`KTTAU = 4`), read by [[alfilein.f#ALFILEIN|`ALFILEIN`]]; no initializer, but PARMIN sets it to 0 before reading the namelist. *Name:* ALlard ATMosphere. *Units not stated: [α/Fe] in dex?*
- **`alatm_feh`**: the [Fe/H] asked of the Allard atmosphere tables, read by [[alfilein.f#ALFILEIN|`ALFILEIN`]]; no initializer, but PARMIN sets it to 0 before reading the namelist. *Name:* ALlard ATMosphere, Fe/H.
- **`alphac`**: $\alpha_c$, the step overshoot of convective cores, in units of $H_p$ (with `LOVSTC`); default 0.0D0; read by [[oversh.f#OVERSH|`OVERSH`]].
- **`alphae`**: $\alpha_e$, the overshoot below convective envelopes, in units of $H_p$ (with `LOVSTE`); default 0.0D0; read by [[oversh.f#OVERSH|`OVERSH`]], [[hpoint.f#HPOINT|`HPOINT`]], [[getw.f#GETW|`GETW`]] and the [[main.f#(file level)|main program]].
- **`alpham`**: $\alpha_m$, the overshoot above and below intermediate convection zones, in units of $H_p$ (with `LOVSTM`); default 0.0; read by [[oversh.f#OVERSH|`OVERSH`]].
- **`atime`**: `(14)`, the time-step limits: (1) the central $X$ (or $Y$) below which shell rather than core criteria apply; (2), (3) the largest absolute and fractional $\Delta X$ per step in core hydrogen burning; (4), (5) the same for $Y$ in core helium burning; (6), (7) the hydrogen burned per step after the main sequence, in total and as a fraction in the shell; (8)–(11) the largest local changes of $T$, $P$, $R$, $L$ per step (pre-main sequence); (12), (14) the same as (7), (6) for helium shells; (13) the largest factor by which the step may grow. Default (1.0D-3, 2.0D-2, 5.0D-1, 2.0D-2, 3.0D-1, 1.5D-3, 1.0D-1, 2.0D-2, 4.0D-2, 2.0D-2, 2.0D-2, 0.25D0, 1.5D0, 0.25D0); [[remap.f#REMAP|`REMAP`]] overwrites it from the `TIME_…` inputs with `LNEWVARS`; read by [[htimer.f#HTIMER|`HTIMER`]]'s criteria and [[findsh.f#FINDSH|`FINDSH`]].
- **`atmbeg`**: the initial step in $\log\tau$ of the atmosphere integration in [[envint.f#ENVINT|`ENVINT`]]; default 1.0D-1; set to `ATMSTP` (and restored) by [[calcad.f#CALCAD|`CALCAD`]], [[stitch.f#STITCH|`STITCH`]] and [[wrtmod.f#WRTMOD|`WRTMOD`]].
- **`atmd0`**: the starting density at $\tau = 0$ of the atmosphere integration in [[envint.f#ENVINT|`ENVINT`]], in g cm$^{-3}$ and not a logarithm (ENVINT takes $\log P = \log[(\mathcal{R}\rho + aT^3/3)T]$ from it, and divides it by 10 to retry when the start passes the end); default 1.0D-10. The documentation calls it the log of the density.
- **`atmerr`**: the tolerance of the atmosphere integration in [[envint.f#ENVINT|`ENVINT`]]; default 3.0D-4. *Name:* ATMosphere ERRor.
- **`atmmax`**: the largest step in $\log\tau$ of the atmosphere integration; default 5.0D-1; set to `ATMSTP` (and restored) by [[calcad.f#CALCAD|`CALCAD`]], [[stitch.f#STITCH|`STITCH`]] and [[wrtmod.f#WRTMOD|`WRTMOD`]].
- **`atmmin`**: the smallest step in $\log\tau$ of the atmosphere integration; default 1.0D-1; set to `ATMSTP` (and restored) by the same three routines.
- **`atmstp`**: the fixed step in $\log\tau$ that [[calcad.f#CALCAD|`CALCAD`]], [[stitch.f#STITCH|`STITCH`]] and [[wrtmod.f#WRTMOD|`WRTMOD`]] give the atmosphere integration (as `ATMBEG`, `ATMMIN`, `ATMMAX`) when they integrate for output; default 0.5. *Name:* ATMosphere STeP.
- **`betac`**: with `LOVMAX`, the largest core overshoot as a fraction of the core's physical size; default 0.15D0; read by [[oversh.f#OVERSH|`OVERSH`]].
- **`calsolage`**: in `CONTROL`, the solar age for the solar calibration, in yr; default 4.57D9; read by [[setcal.f#SETCAL|`SETCAL`]] (the documentation calls it a tolerance). *Name:* CALibration, SOLar AGE.
- **`calsolzx`**: in `CONTROL`, the target surface $(Z/X)_\odot$ of the solar calibration (with `LCALSOLZX`); default 0.02292D0 (GS98); read by [[chkcal.f#CHKCAL|`CHKCAL`]].
- **`cmin`**: the smallest abundance the burning network follows, [[kemcom.f#KEMCOM|`KEMCOM`]]; default 1.0D-20.
- **`cmixla`**: in `CONTROL`, `(50)`, the mixing length $\alpha$ for each run (kind card): the main program sets `CMIXL = CMIXLA(NK)`; no initializer, and PARMIN stops the run if an entry it uses is not positive; [[setcal.f#SETCAL|`SETCAL`]], [[chkcal.f#CHKCAL|`CHKCAL`]] and [[setscal.f#SETSCAL|`SETSCAL`]] fill it during calibrations. *Name:* `CMIXL` for each run.
- **`codm`**: a constant diffusion coefficient for angular-momentum transport, added to the velocity times radius in [[codiff.f#CODIFF|`CODIFF`]], so in cm$^2$ s$^{-1}$ (with `LCODM`); default 2.5D4; also read by [[seculr.f#SECULR|`SECULR`]]. The documentation: 9e4 matches the solar core's rotation.
- **`compacc`**: `(15)`, the composition of accreted material, as mass fractions of the 15 species of `HCOMP` ($X$, $Y$, $Z$, ³He, the CNO isotopes, D, ⁶Li, ⁷Li, ⁹Be); default (0.71668d0, 0.265721d0, 0.01757d0, …); read by [[mdot.f#MDOT|`MDOT`]], [[mix.f#MIX|`MIX`]], [[dburn.f#DBURN|`DBURN`]], `DBURNM` and [[liburn.f#LIBURN|`LIBURN`]]. *Name:* COMPosition of ACCreted matter.
- **`constfactor`**: derived (with `LROT`), the constant $K$ of the wind law, set in PARMIN: `FK`$\cdot 2.036\times10^{33}\cdot(1.452\times10^9)^{\mathtt{ALFA}}$ for the old law, `FK`$\cdot$`PMMJD`$/$`PMMSOLW`$^{\mathtt{EXW}}$ for Matt et al.'s (`LMWIND`); read by [[wind.f#WIND|`WIND`]], [[cowind.f#COWIND|`COWIND`]], [[mwind.f#MWIND|`MWIND`]] and [[mcowind.f#MCOWIND|`MCOWIND`]].
- **`creim`**: $\eta$ of the Reimers mass loss (with `LREIMER`), $\dot M = \eta L/(gR)$ in [[massloss.f#MASSLOSS|`MASSLOSS`]]; default -4.0D-13. *Name:* C, REIMers. *Units unclear: MASSLOSS evaluates $L/(gR)$ in cgs (g s$^{-1}$) and MDOT reads the result as $M_\odot$ yr$^{-1}$, while the default is Reimers' coefficient for solar units; which is meant?*
- **`cstdiffmix`**: with `LTHOUL` and `LDIFZ`, a factor on the metals' settling coefficient $D_1$ in [[setup_grsett.f#SETUP_GRSETT|`SETUP_GRSETT`]], added in 10/09 to "mimic mixing to reduce settling"; default 1.0.
- **`cstmixing`**: with `LTHOUL`, a factor on the helium settling coefficients `COD1`, `COD2` in [[setup_grsett.f#SETUP_GRSETT|`SETUP_GRSETT`]], for the same purpose; default 1.0.
- **`djok`**: the tolerance of the rotational mixing (angular momentum) in [[checkj.f#CHECKJ|`CHECKJ`]] and [[dadcoeft.f#DADCOEFT|`DADCOEFT`]]; default 1.0D-4.
- **`dmdt0`**: the constant mass-loss rate $\dot M$, in $M_\odot$ yr$^{-1}$, negative for loss and positive for accretion (with `LMDOT`); default -1.0D-14; read by [[massloss.f#MASSLOSS|`MASSLOSS`]], [[coefft.f#COEFFT|`COEFFT`]], [[mix.f#MIX|`MIX`]], [[dburn.f#DBURN|`DBURN`]] and [[liburn.f#LIBURN|`LIBURN`]]. *Name:* DM/DT.
- **`dpenv`**: experimental: full mixing from the centre to this fractional mass depth (the documentation); default 1.0D0; read by [[mix.f#MIX|`MIX`]].
- **`dt_gs`**: settling is done in substeps of at most `DT_GS` times the settling time (the documentation: when the global step is below `DT_GS` $\tau$ at the base of the convection zone); default 0.1D0; read by [[mix.f#MIX|`MIX`]] and [[rotmix.f#ROTMIX|`ROTMIX`]]. *Name:* $\Delta t$, Gravitational Settling.
- **`dtdif`**: the largest $\Delta\Omega/\Omega$ per mixing substep: [[getw.f#GETW|`GETW`]] divides the step into substeps of at most `DTDIF`; default 1.0D-2; [[remap.f#REMAP|`REMAP`]] overwrites it from `TIME_DW_MIX` with `LNEWVARS`.
- **`dtwind`**: the largest $\Delta\Omega/\Omega$ per model ([[wtime.f#WTIME|`WTIME`]]'s comment, which gives 0.08 as the default); default 1.0D1; [[remap.f#REMAP|`REMAP`]] overwrites it from `TIME_DW_GLOBAL` (0.08) with `LNEWVARS`; also read by [[getw.f#GETW|`GETW`]].
- **`end_dcen`**: in `CONTROL`, `(50)`, the central deuterium mass fraction at which a run stops (the documentation: 2.75D-5 and 2.75D-7 for the start and end of the deuterium birthline); default 0.0, no stop; the [[main.f#(file level)|main program]] negates an entry the starting model already passes, which disables it.
- **`end_xcen`**: in `CONTROL`, `(50)`, the central $X$ at which a run stops (the documentation: 0.714620 at the ZAMS, 0.0001 at the TAMS); default 0.0, no stop; read by the [[main.f#(file level)|main program]]. *When the starting model's $X$ is already below it, main.f (line 438) sets `END_DCEN(NK)` to `-END_XCEN(NK)` rather than negating `END_XCEN(NK)`: a slip?*
- **`end_ycen`**: in `CONTROL`, `(50)`, the central $Y$ at which a run stops (the documentation: 0.9700 at the ZAHB, 0.0001 at the TAHB); default 0.0, no stop; the [[main.f#(file level)|main program]] negates an entry the starting model already passes.
- **`endage`**: in `CONTROL`, `(50)`, the age at which a run stops, in yr; default 0.0; [[htimer.f#HTIMER|`HTIMER`]] shortens the last step to reach it; set during calibrations by [[setcal.f#SETCAL|`SETCAL`]], [[setscal.f#SETSCAL|`SETSCAL`]] and [[chkscal.f#CHKSCAL|`CHKSCAL`]].
- **`envbeg`**: the initial step in $\log P$ of the envelope integration in [[envint.f#ENVINT|`ENVINT`]]; default 1.0D-1; changed by [[calcad.f#CALCAD|`CALCAD`]], [[stitch.f#STITCH|`STITCH`]], [[wrtmod.f#WRTMOD|`WRTMOD`]], [[getnewenv.f#GETNEWENV|`GETNEWENV`]] and [[starin.f#STARIN|`STARIN`]].
- **`enverr`**: the tolerance of the envelope integration in [[envint.f#ENVINT|`ENVINT`]]; default 3.0D-4.
- **`envmax`**: the largest step in $\log P$ of the envelope integration; default 5.0D-1; changed by the routines listed under `ENVBEG`.
- **`envmin`**: the smallest step in $\log P$ of the envelope integration; default 1.0D-1; changed by the routines listed under `ENVBEG`.
- **`envstp`**: the fixed step in $\log P$ that [[calcad.f#CALCAD|`CALCAD`]], [[stitch.f#STITCH|`STITCH`]] and [[wrtmod.f#WRTMOD|`WRTMOD`]] give the envelope integration when they integrate for output; default 0.5. *Name:* ENVelope STeP.
- **`etadh0`**: the lower limit of the Debye–Hückel parameter (with `LDH`), in [[eqrelv.f#EQRELV|`EQRELV`]]; default -1.0D0. *Name:* $\eta$, Debye–Hückel.
- **`etadh1`**: the upper limit of the Debye–Hückel parameter; default 1.0D0; read by [[eqrelv.f#EQRELV|`EQRELV`]].
- **`excen`**: derived (Matt et al.'s law), the exponent $n$ of the centrifugal factor $F_\mathrm{cen}$, `PMMM`$\cdot$`PMMD`; read by [[mwind.f#MWIND|`MWIND`]] and [[mcowind.f#MCOWIND|`MCOWIND`]]. *Name:* EXponent, CENtrifugal.
- **`exl`**: derived (Matt et al.'s law), the exponent of $L$ in the torque, $1 - 2$`PMMM`; read by [[amcalc.f#AMCALC|`AMCALC`]]. *Name:* EXponent of L.
- **`exm`**: derived, the exponent of $M$ in the torque: $-$`ALFA`$/3$ for the old law, $-$`PMMM` for Matt et al.'s; read by [[amcalc.f#AMCALC|`AMCALC`]], [[wind.f#WIND|`WIND`]] and [[cowind.f#COWIND|`COWIND`]]. *Name:* EXponent of M.
- **`exmd`**: derived (old law only), the exponent of $\dot M$ in the torque, $1 - 2$`ALFA`$/3$; read by [[wind.f#WIND|`WIND`]] and [[cowind.f#COWIND|`COWIND`]]. *Name:* EXponent of MDot (PARMIN's comment).
- **`expr`**: derived (Matt et al.'s law), the exponent of the photospheric pressure, $2$`PMMM`$\cdot$`PMMD`; read by [[amcalc.f#AMCALC|`AMCALC`]]. *Name:* EXponent of P.
- **`exr`**: derived, the exponent of $R$ in the torque: $2 -$ `ALFA` for the old law, $2 + 5$`PMMM`$- 4$`PMMM`$\cdot$`PMMC` for Matt et al.'s; read by [[amcalc.f#AMCALC|`AMCALC`]], [[wind.f#WIND|`WIND`]] and [[cowind.f#COWIND|`COWIND`]]. *Name:* EXponent of R.
- **`extau`**: derived (Matt et al.'s law), the exponent of $\tau_\mathrm{cz}$ in [[amcalc.f#AMCALC|`AMCALC`]], set to 0 since the $\tau_\mathrm{cz}$ term moved to MWIND and MCOWIND (G. Somers 8/17). *Name:* EXponent of TAU.
- **`exw`**: derived, the exponent of $\Omega$ in the torque: $1 + 4$`ALFA`$/3$ for the old law, $1 + a - 2am + 4mb$ (from `PMMA`, `PMMM`, `PMMB`) for Matt et al.'s; read by [[wind.f#WIND|`WIND`]], [[cowind.f#COWIND|`COWIND`]], [[mwind.f#MWIND|`MWIND`]], [[mcowind.f#MCOWIND|`MCOWIND`]] and [[dadcoeft.f#DADCOEFT|`DADCOEFT`]]. *Name:* EXponent of W ($\Omega$).
- **`fc`**: $f_c$, the efficiency of rotational mixing of composition relative to angular-momentum transport; default 1.0D0; read by [[codiff.f#CODIFF|`CODIFF`]], [[dadcoeft.f#DADCOEFT|`DADCOEFT`]], [[vcirc.f#VCIRC|`VCIRC`]] and [[getfc.f#GETFC|`GETFC`]].
- **`fcore`**: with `LCORE`, the factor in mass by which the central fitting point is moved inward (the documentation); default 1.0; [[starin.f#STARIN|`STARIN`]] rounds it to a whole number of mesh steps, `FCORE` = `MCORE`$\cdot$`HPTTOL(2)`.
- **`fcorr0`**: the factor on the Henyey corrections at the first iteration; default 0.8D0; the main program starts `FCORR` at $|$`FCORR0`$| -$ `FCORRI`, and [[crrect.f#CRRECT|`CRRECT`]] raises it by `FCORRI` at each iteration, up to 1, when `FCORR0` > 0. *Name:* FCORR, the correction factor, initial.
- **`fcorri`**: the increment of that factor at each iteration; default 0.1D0; read by [[crrect.f#CRRECT|`CRRECT`]] and the main program. *Name:* FCORR, increment.
- **`fczdmdt`**: with mass loss, the step limit $\Delta t \le$ `FCZDMDT`$\cdot M_\mathrm{cz}/|\dot M|$ in [[mdot.f#MDOT|`MDOT`]]; default 0.1D0. *Name:* F, Convection Zone, DM/DT.
- **`fes`**: the factor on the meridional (Eddington–Sweet) circulation velocity $v_\mathrm{ES}$ in [[vcirc.f#VCIRC|`VCIRC`]]; default 1.0D0. *Name:* F, Eddington–Sweet.
- **`fesc`**: the weight of $v_\mathrm{ES}$ in the mixing of composition only, $f_{c,\mathrm{ES}}$, in [[codiff.f#CODIFF|`CODIFF`]], [[dadcoeft.f#DADCOEFT|`DADCOEFT`]] and [[vcirc.f#VCIRC|`VCIRC`]]; default 1.0D0.
- **`fgry`**: the factor on helium's settling coefficients (the documentation: 0.75 without rotational mixing); default 1.0D0; read by [[setup_grsett.f#SETUP_GRSETT|`SETUP_GRSETT`]] and `MICRODIFF_COD`. *Name:* F, GRavitational settling, Y.
- **`fgrz`**: the factor on the metals' settling coefficients; default 1.0D0; read by the same routines.
- **`fgsf`**: the factor on the velocity of the Goldreich–Schubert–Fricke instability, $v_\mathrm{GSF}$, in [[vcirc.f#VCIRC|`VCIRC`]]; default 1.0D0.
- **`fgsfc`**: the weight of $v_\mathrm{GSF}$ in the mixing of composition only, in [[codiff.f#CODIFF|`CODIFF`]], [[dadcoeft.f#DADCOEFT|`DADCOEFT`]] and [[vcirc.f#VCIRC|`VCIRC`]]; default 1.0D0.
- **`fmu`**: $f_\mu$, the scale of the "fictitious $\mu$ currents" of Kippenhahn & Möllenhoff (with `IMU = 3`) in [[vcirc.f#VCIRC|`VCIRC`]]; default 1.0D0. *Name:* F, $\mu$.
- **`frac_c`**: in `CONTROL` (and derived), the fraction of the metals' mass in carbon, for the custom CNO mixture (`ISETMIX = 1`, `AMIX = 'CUS'`); default 0.172148D0 (GS98); PARMIN replaces it from a preset `AMIX`, and [[starin.f#STARIN|`STARIN`]] applies it with `LMIXTURE`.
- **`frac_n`**: the same for nitrogen; default 0.050426D0.
- **`frac_o`**: the same for oxygen; default 0.468195D0.
- **`fss`**: the factor on the shear velocity $v_\mathrm{SS}$ in [[vcirc.f#VCIRC|`VCIRC`]]; default 1.0D0.
- **`fssc`**: the weight of $v_\mathrm{SS}$ in the mixing of composition only, in [[codiff.f#CODIFF|`CODIFF`]] and [[dadcoeft.f#DADCOEFT|`DADCOEFT`]]; default 1.0D0.
- **`ftotdmdt`**: with mass loss, the step limit $\Delta t \le$ `FTOTDMDT`$\cdot M/|\dot M|$ in [[mdot.f#MDOT|`MDOT`]]; default 1.0D-2. *Name:* F, TOTal mass, DM/DT.
- **`fw`**: $f_w$, a global factor on the diffusion coefficients of angular-momentum transport; default 1.0D0; read by [[codiff.f#CODIFF|`CODIFF`]], [[dadcoeft.f#DADCOEFT|`DADCOEFT`]] and [[rotgrid.f#ROTGRID|`ROTGRID`]].
- **`grtol`**: the tolerance on the abundance changes of the settling solver; default 1.0D-8; read by [[grsett.f#GRSETT|`GRSETT`]] and [[microdiff_run.f#MICRODIFF_RUN|`MICRODIFF_RUN`]]. *Name:* GRavitational settling TOLerance.
- **`hpttol`**: `(12)`, the mesh tolerances: (1) the smallest mass spacing; (2) the largest spacing in $\log m$; (3), (4) the smallest jumps in $X$, $Z$ kept as discontinuities; (5), (6) the legacy spacing in $X$, $Z$; (7) the width of the finely zoned region at the base of the convection zone; (8) the largest $\Delta\log P$ in the outer convection zone; (9) the largest spacing in $L/L_\mathrm{surf}$; (10), (11) the largest $\Delta\log P$ at the base of the surface convection zone and below it; (12) the smallest jump in $\Omega$ kept as a discontinuity. Default (1.0D-8, 8.0D-2, 5.0D-2, 5.0D-2, 1.0D0, 1.0D0, 0.0D0, 5.0D-2, 2.0D-2, 5.0D-2, 5.0D-2, 1.0D-1); [[remap.f#REMAP|`REMAP`]] overwrites it from the `TOL_…` and `FLAG_…` inputs with `LNEWVARS`; read by [[hpoint.f#HPOINT|`HPOINT`]], [[getgrid.f#GETGRID|`GETGRID`]], `MIXGRID`, [[rotgrid.f#ROTGRID|`ROTGRID`]], [[getnewenv.f#GETNEWENV|`GETNEWENV`]] and [[starin.f#STARIN|`STARIN`]]. *Name:* the tolerances of `HPOINT`, the rezoning.
- **`htoler`**: `(5,2)`, the Henyey tolerances, read by [[crrect.f#CRRECT|`CRRECT`]]: `HTOLER(1..4,1)` the convergence limits on the largest correction to $\log P$, $\log T$, $\log R$ and $L/L_\mathrm{tot}$; `HTOLER(1..4,2)` the corrections above which the run is abandoned as diverging; `HTOLER(5,1)`, `(5,2)` the agreement of analytic and numerical derivatives for P and R, and for T and L, beyond which an iteration is skipped (the documentation). Default (6.0D-5, 4.5D-5, 3.0D-5, 9.0D-5, 3.0D-5; 9.0D-1, 5.0D-1, 5.0D-1, 2.0D0, 2.5D-6). *Name:* Henyey TOLERance.
- **`ies`**: the circulation formula in [[vcirc.f#VCIRC|`VCIRC`]]: 2 for Kippenhahn & Möllenhoff (1974), any other value for Zahn (1991); default 1. *Name:* I for a choice, Eddington–Sweet.
- **`igsf`**: the stability condition for the GSF (and ABCD) instabilities in [[vcirc.f#VCIRC|`VCIRC`]]: 1 none (recommended), 2 the angular-velocity gradient against viscosity and thermal diffusion, 0 that plus a mean-molecular-weight condition; default 1.
- **`ilambda`**: the formula for the Coulomb logarithm $\ln\Lambda$ in the collision integrals of settling (the documentation: 4, recommended, the constant 2.2); default 1; PARMIN sets 4 with `LDIFLI`; read by [[setup_grsett.f#SETUP_GRSETT|`SETUP_GRSETT`]]; also in `DERIVED`.
- **`impjmod`**: the rotation profile imposed on the radiative interior below the surface convection zone ("impose J model," PARMIN's comment): 0 none, 1 solid-body rotation, 2 a solid-body core decoupled from the convection zone, 3 a solid-body core coupled at its base; default 0; PARMIN sets 1 with `LSOLID` (and `LROT`); read by [[seculr.f#SECULR|`SECULR`]], [[wczimp.f#WCZIMP|`WCZIMP`]], [[getw.f#GETW|`GETW`]] and [[midmod.f#MIDMOD|`MIDMOD`]].
- **`imu`**: the treatment of $\mu$ gradients in [[vcirc.f#VCIRC|`VCIRC`]]: 3 for the $\mu$ currents of Kippenhahn & Möllenhoff (1974), any other value for the factor of Zahn & Maeder (1998); default 1.
- **`inewcp`**: derived (with `LNEWCP`), the row of `HCOMP` of the species named by `ANEWCP` (its position in PARMIN's list plus 3); read by [[rscale.f#RSCALE|`RSCALE`]].
- **`ipver`**: in `CONTROL`, the format of the pulsation output; default 1; read by [[wrtmod.f#WRTMOD|`WRTMOD`]] and [[envint.f#ENVINT|`ENVINT`]]. *Name:* Pulsation VERsion.
- **`itdif1`**: the number of passes between the structure and the rotational mixing (1 = none; 2 recommended for rotational mixing); default 1; the [[main.f#(file level)|main program]] sets it to 1 when `LROT` is false.
- **`itdif2`**: the number of iterations between nuclear burning and rotational mixing (1 = none); default 1; read by [[seculr.f#SECULR|`SECULR`]], [[checkc.f#CHECKC|`CHECKC`]], [[checkj.f#CHECKJ|`CHECKJ`]] and [[dadcoeft.f#DADCOEFT|`DADCOEFT`]].
- **`itfp1`**: the number of iterations between the equipotential shape and the effective radius (the structural effects of rotation), in [[shape.f#SHAPE|`SHAPE`]]; default 5.
- **`itfp2`**: the number of iterations for the effective radius at a given shape parameter, in [[shape.f#SHAPE|`SHAPE`]]; default 20.
- **`itrver`**: in `CONTROL`, the format of the `.track` file (the documentation strongly recommends 0, one line per model); default 1; read by [[wrthead.f#WRTHEAD|`WRTHEAD`]] and [[wrtout.f#WRTOUT|`WRTOUT`]]. *Name:* TRack VERsion.
- **`kemmax`**: the largest number of substeps of the abundance integration in [[kemcom.f#KEMCOM|`KEMCOM`]]; default 50.
- **`kttau`**: the atmosphere: 0 Eddington gray, 1 Krishna Swamy, 2 the `HRA` $T$–$\tau$ relation, 3 Kurucz, 4 Allard, 5 Castelli–Kurucz 2004; default 0; [[surfbc.f#SURFBC|`SURFBC`]] switches it to 0 beyond the tables' limits and back to `KTTAU0`, and the [[main.f#(file level)|main program]] restores it at each calibration cycle. *Name:* $T(\tau)$, the relation.
- **`kttau0`**: derived, `KTTAU` as read, set by PARMIN; [[surfbc.f#SURFBC|`SURFBC`]] returns to it.
- **`l_zerodt_prems`**: in `CONTROL`, with it a rescale card (`KINDRN` = 2) is a true zero-time-step rescale for a pre-main-sequence model too, which otherwise (with $\log T_c$ < 6.6) is aged as a failsafe; default `.FALSE.`; read by the [[main.f#(file level)|main program]]. *Name:* ZERO DT (time step), PRE-Main Sequence.
- **`ladov`**: experimental adiabatic overshoot; default `.FALSE.`; read by [[tpgrad.f#TPGRAD|`TPGRAD`]]. *Name:* ADiabatic OVershoot.
- **`lalex06`**: in `CONTROL`, use the molecular opacities of Ferguson et al. (2005) (recommended); default `.FALSE.`, but [[getopac.f#GETOPAC|`GETOPAC`]] stops the run without them; read by GETOPAC and [[setupopac.f#SETUPOPAC|`SETUPOPAC`]].
- **`laltptau100`**: with the Allard tables, take $\log P$ and $\log T$ at $\tau = 100$ instead of at $T = T_\mathrm{eff}$; no initializer, but PARMIN sets it false before reading the namelist; read by [[alsurfp.f#ALSURFP|`ALSURFP`]]. *Name:* ALlard, T and P at Tau 100.
- **`lbscale`**: with Matt et al.'s law and `LROSSBY`, scale the field as well: $\Omega$ and $\Omega_\mathrm{sat}$ multiplied by $\tau/\tau_\odot$; default `.FALSE.`; PARMIN sets it false for `AWIND = 'K97'` and true for `'V13'`; read by [[mwind.f#MWIND|`MWIND`]] and [[mcowind.f#MCOWIND|`MCOWIND`]]. *Name:* B (the field) SCALEd.
- **`lcalcenv`**: whether [[envint.f#ENVINT|`ENVINT`]] goes on past the atmosphere and keeps the envelope's structure; default `.TRUE.`, but [[gettau.f#GETTAU|`GETTAU`]] sets it at each call (true when $\log P_\mathrm{base} - \log P_\mathrm{surf} < 1$ or without `LNEWTCZ`). *Name:* CALCulate the ENVelope.
- **`lcals`**: in `CONTROL`, calibrate the Sun: adjust $Y$ and $\alpha$ to match $R_\odot$ and $L_\odot$ at the solar age; default `.FALSE.`; read by the [[main.f#(file level)|main program]]. *Name:* CALibrate the Sun.
- **`lcalsolzx`**: in `CONTROL`, also match the surface $Z/X$ to `CALSOLZX` in the solar calibration (otherwise $Z$ is held fixed); default `.FALSE.`; read by [[chkcal.f#CHKCAL|`CHKCAL`]].
- **`lcalst`**: in `CONTROL`, calibrate a star of given $L$ and $T_\mathrm{eff}$ or $R$ ([[setscal.f#SETSCAL|`SETSCAL`]], [[chkscal.f#CHKSCAL|`CHKSCAL`]]); default `.FALSE.`; read by the [[main.f#(file level)|main program]]; not in the documentation. *Name:* CALibrate a STar.
- **`lcodm`**: add the constant coefficient `CODM` to the angular-momentum diffusion; default `.FALSE.`; read by [[codiff.f#CODIFF|`CODIFF`]] and [[seculr.f#SECULR|`SECULR`]].
- **`lcondopacp`**: use the conductive opacities of Potekhin (the updated tables, opened by PARMIN); default `.FALSE.`; read by [[getopac.f#GETOPAC|`GETOPAC`]]. *Name:* CONDuctive OPACities, Potekhin (PARMIN's comment).
- **`lcore`**: move the central fitting point inward by `FCORE` in mass, with a Taylor expansion, on runs that start from the stored model; default `.FALSE.`; read by [[starin.f#STARIN|`STARIN`]].
- **`lcorr`**: in `CONTROL`, write the details of convergence to the `.short` file; default `.TRUE.`; read by [[crrect.f#CRRECT|`CRRECT`]]. *Name:* CORRections.
- **`ldebug`**: in `CONTROL`, debug output: PARMIN opens the debug file, and [[hpoint.f#HPOINT|`HPOINT`]] writes a table of the old and new points every `NPOINT` models; default `.FALSE.`.
- **`ldh`**: the Debye–Hückel correction in the Yale equation of state; default `.FALSE.`; read by [[eqrelv.f#EQRELV|`EQRELV`]]'s callers and passed on through many routines ([[physic.f#PHYSIC|`PHYSIC`]], [[coefft.f#COEFFT|`COEFFT`]], [[crrect.f#CRRECT|`CRRECT`]], …). *Name:* Debye–Hückel.
- **`ldifad`**: experimental: treat meridional circulation as diffusion plus advection; default `.FALSE.`; read by [[seculr.f#SECULR|`SECULR`]], [[setupv.f#SETUPV|`SETUPV`]], [[vcirc.f#VCIRC|`VCIRC`]], [[rotgrid.f#ROTGRID|`ROTGRID`]], [[dcoeft.f#DCOEFT|`DCOEFT`]] and [[checkj.f#CHECKJ|`CHECKJ`]]. *Name:* DIFfusion and ADvection.
- **`ldifli`**: settling of the light species; default `.FALSE.`; PARMIN then turns on `LNEWDIF`, `LDIFY`, `LDIFZ`, `LTHOUL`, turns off `LTHOULFIT` and sets `ILAMBDA` = 4; read by the `MICRODIFF` routines.
- **`ldify`**: gravitational settling of helium; default `.FALSE.`; PARMIN turns it on with `LDIFZ` or `LDIFLI`, and [[mix.f#MIX|`MIX`]] and [[rotmix.f#ROTMIX|`ROTMIX`]] turn it off once the central $X$ < `XMIN`; also in `DERIVED`.
- **`ldifz`**: gravitational settling of the metals; default `.FALSE.`; PARMIN then turns on `LDIFY` and `LTHOUL`; it also makes [[setupopac.f#SETUPOPAC|`SETUPOPAC`]] load a second opacity table; also in `DERIVED`.
- **`ldisk`**: disk locking; default `.FALSE.`; read by [[seculr.f#SECULR|`SECULR`]], [[getw.f#GETW|`GETW`]], [[solid.f#SOLID|`SOLID`]] and [[mdot.f#MDOT|`MDOT`]].
- **`lexcom`**: follow the extended composition, 15 species (with D, ⁶Li, ⁷Li, ⁹Be) instead of 11; default `.FALSE.`; read by 17 routines. *Name:* EXtended COMposition.
- **`lfirst`**: in `CONTROL`, `(50)`, per run: true to start from the stored starting model (`FFIRST`), false to continue from the previous run's last model; default `.TRUE.`; PARMIN forces `LFIRST(1)` true, and [[setcal.f#SETCAL|`SETCAL`]] and [[setscal.f#SETSCAL|`SETSCAL`]] fill it; read by [[starin.f#STARIN|`STARIN`]] and [[wrthead.f#WRTHEAD|`WRTHEAD`]].
- **`linstb`**: rotationally induced mixing and hydrodynamic angular-momentum transport; default `.FALSE.`. *Name:* INSTaBilities.
- **`lisotope`**: derived, true when PARMIN accepts an isotope and light-element mixture (`ISETISO` = 1 with `AISO = 'L21'` or a valid `'CUS'`); [[starin.f#STARIN|`STARIN`]] then applies `R12_13`, `R16_18` and the `X…_INI`.
- **`ljdot0`**: angular-momentum loss by the wind; default `.TRUE.`. *Name:* $\dot J$.
- **`lkuthe`**: settings for the helium flash: [[crrect.f#CRRECT|`CRRECT`]] sets its correction factor from the largest correction (0.8 or 1), the main program stores the starting model, and [[wrtout.f#WRTOUT|`WRTOUT`]] changes its output; default `.FALSE.`.
- **`lmdot`**: the experimental mass-loss and accretion module; default `.FALSE.`; [[mdot.f#MDOT|`MDOT`]] turns it off when accretion with `LDISK` reaches the disk's lifetime; also read by [[massloss.f#MASSLOSS|`MASSLOSS`]], [[coefft.f#COEFFT|`COEFFT`]], [[mix.f#MIX|`MIX`]] and the burning routines. *Name:* $\dot M$.
- **`lmilne`**: in `CONTROL`, write the Milne (homology) invariants with [[wrtmil.f#WRTMIL|`WRTMIL`]] (PARMIN opens the file); default `.FALSE.`; alone it writes nothing: [[putstore.f#PUTSTORE|`PUTSTORE`]] calls WRTMIL only with `LSTATM` or `LSTENV`, [[wrtout.f#WRTOUT|`WRTOUT`]] only in its pulsation branch.
- **`lmixture`**: derived, true when PARMIN accepts a CNO mixture (`ISETMIX` = 1); [[starin.f#STARIN|`STARIN`]] then applies `FRAC_C`, `FRAC_N`, `FRAC_O`.
- **`lmwind`**: use the wind law of Matt et al. (2012), as adapted by van Saders & Pinsonneault (2013), in [[mwind.f#MWIND|`MWIND`]] and [[mcowind.f#MCOWIND|`MCOWIND`]], instead of the old law; default `.FALSE.`. *Name:* Matt WIND.
- **`lnew0`**: compute a new surface boundary condition at each model (needed with rotation); default `.FALSE.`; PARMIN sets it with `LROT`; read by the [[main.f#(file level)|main program]]; also in `DERIVED`.
- **`lnewcp`**: set one species (named by `ANEWCP`) to `XNEWCP` everywhere, in [[rscale.f#RSCALE|`RSCALE`]] (main sequence only); default `.FALSE.`; PARMIN turns it off if `ANEWCP` is not recognized.
- **`lnewdif`**: the updated settling routines (a legacy option); default `.FALSE.`; PARMIN sets it with `LDIFLI`; read by [[mix.f#MIX|`MIX`]] and [[rotmix.f#ROTMIX|`ROTMIX`]]; also in `DERIVED`. *Name:* NEW DIFfusion.
- **`lnews`**: extrapolate the changes of the previous step for the first guess of the next; default `.FALSE.`; read by the [[main.f#(file level)|main program]].
- **`lnewtcz`**: compute $\tau_\mathrm{cz}$ by the new method in [[gettau.f#GETTAU|`GETTAU`]] rather than in [[envint.f#ENVINT|`ENVINT`]]; default `.TRUE.`. *Name:* NEW $\tau_\mathrm{cz}$.
- **`lnoj`**: no angular-momentum transport by the rotational mixing: [[codiff.f#CODIFF|`CODIFF`]] zeroes its coefficient, [[vcirc.f#VCIRC|`VCIRC`]] zeroes the velocities where $L(r)/L$ < 0.99, and [[seculr.f#SECULR|`SECULR`]] counts the step as converged; default `.FALSE.`. *Name:* NO J.
- **`lnulos1`**: the neutrino losses of Itoh et al. (1996), in [[engeb.f#ENGEB|`ENGEB`]] (a legacy option); default `.FALSE.`. *Name:* NeUtrino LOSses.
- **`lnumderiv`**: numerical rather than analytic derivatives of the equation of state (very slow); default `.FALSE.`; read by [[eqstat.f#EQSTAT|`EQSTAT`]].
- **`lopal95`**: in `CONTROL`, the atomic opacities in the OP/OPAL format (recommended); no initializer; read by [[getopac.f#GETOPAC|`GETOPAC`]], [[setupopac.f#SETUPOPAC|`SETUPOPAC`]] and `SURFOPAC`.
- **`lopale06`**: the OPAL 2006 equation of state (PARMIN opens the table); default `.FALSE.`; read by [[eqstat2.f#EQSTAT2|`EQSTAT2`]], [[setups.f#SETUPS|`SETUPS`]] and [[calcad.f#CALCAD|`CALCAD`]].
- **`lovmax`**: with `LOVSTC`, limit core overshoot by `BETAC`, against pathologies for small cores; default `.TRUE.` (since `7be4133`); read by [[oversh.f#OVERSH|`OVERSH`]].
- **`lovstc`**: core overshoot (mixing only, unless `LADOV`); default `.FALSE.`; PARMIN stops the run if it is set with `LSEMIC`. *Name:* OVerShooT, Core.
- **`lovste`**: envelope overshoot; default `.FALSE.`. *Name:* OVerShooT, Envelope.
- **`lovstm`**: overshoot of intermediate convection zones (not recommended); default `.FALSE.`. *Name:* OVerShooT, Middle.
- **`lpout`**: in `CONTROL`, call [[pdist.f#PDIST|`PDIST`]] after each model, which opens the pulsation files whenever the track has moved by more than `POMAX`; default `.FALSE.`.
- **`lptime`**: limit the step by structural changes (`PTIME`, with `ATIME(8)`–`(11)`); default `.TRUE.`; [[remap.f#REMAP|`REMAP`]] sets it from `LSTRUCT_TIME` with `LNEWVARS`; [[htimer.f#HTIMER|`HTIMER`]] turns it off for the rest of the job once $\log T_c$ > 7.1 and $L_\mathrm{grav}$ < 0; the main program restores it at each calibration cycle.
- **`lpulse`**: in `CONTROL`, pulsation output (PARMIN opens the files); default `.FALSE.`; the [[main.f#(file level)|main program]] turns it on for chosen models and restores it, and [[pdist.f#PDIST|`PDIST`]] turns it off.
- **`lpurez`**: in `CONTROL`, load the pure-$Y$/$Z$ opacity table (`FPUREZ`), which [[getopac.f#GETOPAC|`GETOPAC`]] needs for $Z$ > 0.1 at $\log T$ > 7 (helium-burning cores); default `.FALSE.`; also read by [[setupopac.f#SETUPOPAC|`SETUPOPAC`]]. *Name:* PURE Z.
- **`lreimer`**: Reimers mass loss with `CREIM`, in [[massloss.f#MASSLOSS|`MASSLOSS`]]; default `.FALSE.`.
- **`lrel`**: derived (with `LNEWCP`): `XNEWCP` is on the astronomers' logarithmic scale, unless `ATMP = 'ABS'`; read by [[rscale.f#RSCALE|`RSCALE`]]. *Name:* RELative.
- **`lrossby`**: scale the wind's saturation with the Rossby number, $\Omega_\mathrm{sat} = \Omega_\mathrm{max}\tau_\odot/\tau$; default `.TRUE.`; read by [[amcalc.f#AMCALC|`AMCALC`]], [[mwind.f#MWIND|`MWIND`]], [[mcowind.f#MCOWIND|`MCOWIND`]] and [[dadcoeft.f#DADCOEFT|`DADCOEFT`]].
- **`lrot`**: rotation; default `.FALSE.`; read by about 20 routines. *Name:* ROTation.
- **`lrwsh`**: in `CONTROL`, rewind the `.short` file before each model, so that it keeps only the last model's details; default `.FALSE.`; read by the [[main.f#(file level)|main program]]. *Name:* ReWind SHort.
- **`lscv`**: use the SCV equation of state where it is valid and OPAL is not; default `.FALSE.`; read by [[eqstat2.f#EQSTAT2|`EQSTAT2`]], [[setups.f#SETUPS|`SETUPS`]] and [[starin.f#STARIN|`STARIN`]].
- **`lsdepth`**: decrease the starspots' contrast with depth, assuming a constant field; default `.FALSE.`; read by [[tpgrad.f#TPGRAD|`TPGRAD`]]. *Name:* Spot DEPTH.
- **`lsemic`**: semiconvection; default `.FALSE.`; PARMIN stops the run if it is set with any overshoot; read by [[mix.f#MIX|`MIX`]]. *Name:* SEMIConvection.
- **`lsenv0a`**: in `CONTROL`, `(50)`, per run: move the outer fitting point to `SENV0A`; default `.FALSE.`; the [[main.f#(file level)|main program]] copies it to `LSENV0` ([[cenv_mod.f#CENV_MOD|`CENV_MOD`]]); filled by [[setcal.f#SETCAL|`SETCAL`]] and [[setscal.f#SETSCAL|`SETSCAL`]].
- **`lsnu`**: compute the solar neutrino fluxes (PARMIN opens `FSNU`); default `.FALSE.`; read by [[engeb.f#ENGEB|`ENGEB`]], [[coefft.f#COEFFT|`COEFFT`]], [[wrtout.f#WRTOUT|`WRTOUT`]] and the main program.
- **`lsolid`**: solid-body rotation everywhere; default `.FALSE.`; PARMIN sets `IMPJMOD` = 1 with it; read by [[seculr.f#SECULR|`SECULR`]], [[wczimp.f#WCZIMP|`WCZIMP`]], [[getw.f#GETW|`GETW`]] and [[midmod.f#MIDMOD|`MIDMOD`]].
- **`lsolwind`**: mass loss scaled to the solar wind (the documentation: not implemented); default `.FALSE.`; in [[mdot.f#MDOT|`MDOT`]] its branch is inert, since its three constants are zero.
- **`lstatm`**: in `CONTROL`, add the atmosphere to the stored models; no initializer; [[envint.f#ENVINT|`ENVINT`]] sets it false with `LSTCH`; read by [[putstore.f#PUTSTORE|`PUTSTORE`]], [[stitch.f#STITCH|`STITCH`]] and [[wrtmod.f#WRTMOD|`WRTMOD`]]. *Name:* STore ATMosphere.
- **`lstch`**: in `CONTROL`, write the interior, envelope and atmosphere in one stitched format (recommended); default `.FALSE.`; read by [[putstore.f#PUTSTORE|`PUTSTORE`]] and [[envint.f#ENVINT|`ENVINT`]].
- **`lstenv`**: in `CONTROL`, add the envelope to the stored models; no initializer; read by [[putstore.f#PUTSTORE|`PUTSTORE`]], [[stitch.f#STITCH|`STITCH`]], [[wrtmod.f#WRTMOD|`WRTMOD`]] and [[envint.f#ENVINT|`ENVINT`]]. *Name:* STore ENVelope.
- **`lstmod`**: in `CONTROL`, the documentation: "Set the same as LSTORE. May be redundant"; no initializer; [[putstore.f#PUTSTORE|`PUTSTORE`]] only writes it in the `.store` file's header.
- **`lstore`**: in `CONTROL`, store model structures in the `.store` file; default `.FALSE.`; read by [[putstore.f#PUTSTORE|`PUTSTORE`]], [[wrtout.f#WRTOUT|`WRTOUT`]], [[wrtmod.f#WRTMOD|`WRTMOD`]] and the main program.
- **`lstpch`**: in `CONTROL`, with `LSTORE`, store the final model of a run; default `.FALSE.`; read by the [[main.f#(file level)|main program]].
- **`lstphys`**: in `CONTROL`, add the microphysics ($\epsilon$, $\kappa$, …) to the stored models; no initializer; read by [[putstore.f#PUTSTORE|`PUTSTORE`]]. *Name:* STore PHYSics.
- **`lstrot`**: in `CONTROL`, add the rotation data to the stored models; no initializer; read by [[putstore.f#PUTSTORE|`PUTSTORE`]]. *Name:* STore ROTation.
- **`lteff`**: in `CONTROL`, with `LCALST`, give the star's $T_\mathrm{eff}$ (`STEFF`) rather than its radius (`SR`); [[setscal.f#SETSCAL|`SETSCAL`]] computes the other; default `.FALSE.`.
- **`lthoul`**: the settling coefficients of Thoul et al.; default `.FALSE.`; PARMIN sets it with `LDIFZ` or `LDIFLI`; read by [[setup_grsett.f#SETUP_GRSETT|`SETUP_GRSETT`]]; also in `DERIVED`.
- **`lthoulfit`**: with `LTHOUL`, the published fit instead of the full solution (not recommended); default `.FALSE.`; PARMIN turns it off with `LDIFLI`; also in `DERIVED`.
- **`ltrack`**: in `CONTROL`, write the global properties to the `.track` file; default `.TRUE.`; read by [[wrthead.f#WRTHEAD|`WRTHEAD`]] and [[wrtout.f#WRTOUT|`WRTOUT`]].
- **`ltrist`**: limit the step by the envelope triangle ([[entime.f#ENTIME|`ENTIME`]], when `LPTIME` is off; the documentation: during the Hertzsprung gap); default `.FALSE.`; read by [[htimer.f#HTIMER|`HTIMER`]]. *Name:* TRIangle.
- **`lttau`**: derived, true while [[surfbc.f#SURFBC|`SURFBC`]] has switched to the gray atmosphere; PARMIN sets it false.
- **`lvfc`**: a variable $f_c$ (Zahn 1991), from [[getfc.f#GETFC|`GETFC`]]; default `.FALSE.`; read by [[codiff.f#CODIFF|`CODIFF`]] and [[seculr.f#SECULR|`SECULR`]]. *Name:* Variable FC.
- **`lwnew`**: start the model in solid-body rotation at `WNEW`, in [[starin.f#STARIN|`STARIN`]]; default `.FALSE.`.
- **`lzramp`**: in `CONTROL`, a ramp in $Z$ in [[rscale.f#RSCALE|`RSCALE`]] (from `RSCLZC` at the centre to the surface $Z$); it also makes [[setupopac.f#SETUPOPAC|`SETUPOPAC`]] load a second opacity table; default `.FALSE.`. *Name:* Z RAMP.
- **`mcore`**: with `LCORE`, the number of mesh points [[starin.f#STARIN|`STARIN`]] adds below the central fitting point, $\lfloor\log_{10}\mathtt{FCORE}/\mathtt{HPTTOL(2)}\rfloor + 1$, set there; default 0 (the documentation lists it as unused).
- **`niter1`**: the iterations before the surface boundary condition is checked (level 1 of the main program); default 2.
- **`niter2`**: the iterations after that check, with the start-of-step burning rates (level 2); default 20.
- **`niter3`**: the iterations between the structure and the nuclear burning rates (level 3; 0 when convergence is difficult); default 2.
- **`niter4`**: the iterations between the structure, rotation and rotational mixing (level 4; 0 without rotation); default 0; read by the [[main.f#(file level)|main program]].
- **`niter_gs`**: the largest number of iterations of the settling solver; default 10; read by [[grsett.f#GRSETT|`GRSETT`]] and [[microdiff_run.f#MICRODIFF_RUN|`MICRODIFF_RUN`]].
- **`nmodls`**: in `CONTROL`, `(50)`, the number of models after which a run stops; default 0; filled by [[setcal.f#SETCAL|`SETCAL`]] and [[setscal.f#SETSCAL|`SETSCAL`]]. *Name:* Number of MODeLS.
- **`npoint`**: in `CONTROL`, every how many models [[hpoint.f#HPOINT|`HPOINT`]] writes its debug table (with `LDEBUG`); default 1; PARMIN sets 9999 when it is not positive.
- **`nprtmod`**: in `CONTROL`, write a detailed structure every `NPRTMOD` models ([[wrtout.f#WRTOUT|`WRTOUT`]]); default 1; PARMIN sets 9999 when it is not positive. *Name:* PRinT every N MODels.
- **`nprtpt`**: in `CONTROL`, write every `NPRTPT`-th shell; default 1; PARMIN sets 9999 when it is not positive; read by [[pindex.f#PINDEX|`PINDEX`]], [[wrtmil.f#WRTMIL|`WRTMIL`]] and [[checkj.f#CHECKJ|`CHECKJ`]]. *Name:* PRinT every N PoinTs.
- **`numrun`**: in `CONTROL`, the number of runs (kind cards); default 1; [[setcal.f#SETCAL|`SETCAL`]] sets 48, [[setscal.f#SETSCAL|`SETSCAL`]] 50. *Name:* NUMber of RUNs.
- **`optol`**: the composition tolerance of the opacities: [[getopac.f#GETOPAC|`GETOPAC`]] leaves the 2-D table at the surface composition when $X$ or $Z$ differs from it by more than this; default 1.0D-8. *Name:* OPacity TOLerance.
- **`pdisk`**: the angular velocity at which disk locking holds the star, in rad s$^{-1}$; default 7.2722D-6 (a 10-day period); read by [[solid.f#SOLID|`SOLID`]]. The documentation calls it a period.
- **`pmmsolp`**: $\log P$ at $T_\mathrm{eff}$ in the solar model, for the field's calibration (cgs); default 4.9304D0; read by [[amcalc.f#AMCALC|`AMCALC`]]. *Name:* SOLar P.
- **`pmmsoltau`**: the Sun's convective overturn time $\tau_\odot$, in s; default 9.4805D5; read by [[amcalc.f#AMCALC|`AMCALC`]], [[mwind.f#MWIND|`MWIND`]], [[mcowind.f#MCOWIND|`MCOWIND`]] and [[dadcoeft.f#DADCOEFT|`DADCOEFT`]].
- **`pmmsolw`**: the Sun's angular velocity $\Omega_\odot$, in rad s$^{-1}$; default 2.836D-6; read by [[mwind.f#MWIND|`MWIND`]] and [[mcowind.f#MCOWIND|`MCOWIND`]], and by PARMIN for `CONSTFACTOR` and `WMAX`.
- **`poa`**: in `CONTROL`, the weight $a$ of $\Delta\log L$ in [[pdist.f#PDIST|`PDIST`]]'s distance along the track; default 1.0D0.
- **`pob`**: in `CONTROL`, the weight $b$ of $\Delta\log T_\mathrm{eff}$; default 10.0D0.
- **`poc`**: in `CONTROL`, the weight $c$ of the change of age, in Gyr; default 0.0D0.
- **`pomax`**: in `CONTROL`, the squared distance $\ell^2$ along the track at which [[pdist.f#PDIST|`PDIST`]] writes pulsation files; default 0.1D0.
- **`r12_13`**: in `CONTROL`, the ¹²C/¹³C ratio applied by [[starin.f#STARIN|`STARIN`]] with `LISOTOPE`; default 88.27D0.
- **`r16_18`**: in `CONTROL`, the ¹⁶O/¹⁸O ratio applied by [[starin.f#STARIN|`STARIN`]] with `LISOTOPE` (it splits `HCOMP(9)` and `HCOMP(11)`); default 2693.0D0. *The default is near the documentation's ¹⁶O/¹⁷O (2644), while its ¹⁶O/¹⁸O is 468.2 and `R16_17` defaults to 471.4: are the two defaults swapped?*
- **`rcrit`**: the critical Reynolds number $R_\mathrm{crit}$ of the secular shear instability in [[vcirc.f#VCIRC|`VCIRC`]]; default 1.0D3.
- **`reltol`**: the relative convergence criterion for abundance changes in [[kemcom.f#KEMCOM|`KEMCOM`]]; default 1.0D-4. *Name:* RELative TOLerance.
- **`rsclzc`**: in `CONTROL`, `(50)`, with `LZRAMP`, the central $Z_c$ of the ramp; default -1.0D0 (off); read by [[rscale.f#RSCALE|`RSCALE`]]; filled by [[setcal.f#SETCAL|`SETCAL`]] and [[setscal.f#SETSCAL|`SETSCAL`]]. *Name:* ReSCaLe Z, Centre.
- **`rsclzm1`**: in `CONTROL`, `(50)`, the mass fraction $m/M$ below which $Z = Z_c$; default -1.0D0.
- **`rsclzm2`**: in `CONTROL`, `(50)`, the mass fraction above which $Z$ is the surface value (linear between); default -1.0D0.
- **`sbe91`**: the factor on the reference cross section of ⁹Be(p,γ)¹⁰B (1.1 keV b), in [[lirate88.f#LIRATE88|`LIRATE88`]]; default 1.0D0; PARMIN sets `XSBE91`/1.1 with `LXBE91`; also in `DERIVED`.
- **`sbe92`**: the same for ⁹Be(p,d)2⁴He (reference 15,000 keV b); default 1.0D0; from `XSBE92` with `LXBE92`.
- **`sbe93`**: the same for ⁹Be(p,α)⁶Li (reference 15,000 keV b); default 1.0D0; from `XSBE93` with `LXBE93`.
- **`senv0a`**: in `CONTROL`, `(50)`, with `LSENV0A`, the outer fitting point as $\log_{10}(m_\mathrm{fit}/M)$; default 1.26D-4; the main program copies it to `SENV0`, which [[starin.f#STARIN|`STARIN`]] makes negative and at most $-10^{-12}$.
- **`setdt`**: in `CONTROL`, `(50)`, a fixed time step for the run, in yr, used by [[htimer.f#HTIMER|`HTIMER`]]; default 0.0; filled by [[setcal.f#SETCAL|`SETCAL`]] and [[setscal.f#SETSCAL|`SETSCAL`]]. *Name:* SET DT.
- **`sli6`**: the factor on the reference cross section of ⁶Li + p (5.5 MeV b), in [[lirate88.f#LIRATE88|`LIRATE88`]]; default 1.0D0; PARMIN sets `XSLI6`/5.5D3 with `LXLI6`; also in `DERIVED`.
- **`sli7`**: the same for ⁷Li + p (52 keV b); default 1.0D0; from `XSLI7` with `LXLI7`.
- **`spotf`**: the starspot filling factor (0.25, active main-sequence stars); default 0.00; read by [[surfbc.f#SURFBC|`SURFBC`]], [[gettau.f#GETTAU|`GETTAU`]], [[tpgrad.f#TPGRAD|`TPGRAD`]], [[starin.f#STARIN|`STARIN`]] and others. *Name:* SPOT Filling.
- **`spotx`**: the starspot temperature contrast (0.85 typical of sunspots); default 1.00; read by the same routines.
- **`sr`**: in `CONTROL`, with `LCALST`, the star's radius $R_*/R_\odot$; no initializer; [[setscal.f#SETSCAL|`SETSCAL`]] computes it from `XLS` and `STEFF` with `LTEFF`; read by [[chkscal.f#CHKSCAL|`CHKSCAL`]]. *Name:* Star's R.
- **`sstandard`**: `(17)`, factors on the reference zero-energy S-factors of [[engeb.f#ENGEB|`ENGEB`]] and [[rates.f#RATES|`RATES`]]: (1) p+p, (2) ³He+³He, (3) ³He+⁴He, (4)–(7) p + ¹²C, ¹³C, ¹⁴N, ¹⁶O, (8), (10)–(12) resonant helium-burning reactions, (9), (13) unused, (14) pep, (15) ⁷Be + e, (16) ⁷Be + p, (17) hep; default (0.9828D0, 1.0485D0, 0.9815D0, 0.9241D0, 1.3818D0, 1.0542D0, 1.0D0 ×8, 1.0108D0, 0.7819D0, 0.2875D0); [[remap.f#REMAP|`REMAP`]] replaces it with `LNEWNUC` (1–7 and 14–17 from the `S0_…` inputs, the rest 1).
- **`steff`**: in `CONTROL`, with `LCALST` and `LTEFF`, the star's $T_\mathrm{eff}$, in K; no initializer; [[setscal.f#SETSCAL|`SETSCAL`]] computes it from `XLS` and `SR` otherwise. *Name:* Star's TEFF.
- **`tcut`**: `(5)`, thresholds in $\log T$: (1) below which all burning rates are zero; (2), (3) the equilibrium pp chains and CN cycle in [[eqburn.f#EQBURN|`EQBURN`]] (the documentation calls them unused); (4) the $\alpha$ captures in [[engeb.f#ENGEB|`ENGEB`]] and [[rates.f#RATES|`RATES`]]; (5) the neutrino losses in ENGEB; default (6.5D0, 6.5D0, 6.82D0, 7.7D0, 7.5D0).
- **`tdisk`**: the disk's lifetime, in Gyr (the documentation: 1e-4 to 1e-2 recommended); default 0.0D0; read by [[seculr.f#SECULR|`SECULR`]], [[getw.f#GETW|`GETW`]], [[solid.f#SOLID|`SOLID`]] and [[mdot.f#MDOT|`MDOT`]].
- **`tenv0`**: the lowest $\log T$ of the envelope integration: [[hpoint.f#HPOINT|`HPOINT`]] drops outer points cooler than it, and [[envint.f#ENVINT|`ENVINT`]] stores the envelope at $(\mathtt{TENV0}+\mathtt{TENV1})/2$; default 3.0D0.
- **`tenv1`**: the highest $\log T$ of the envelope integration: HPOINT adds a point from the stored envelope when the outer point is hotter; default 9.0D0.
- **`tgcut`**: the $\log T$ above which convection is taken as adiabatic, in [[tpgrad.f#TPGRAD|`TPGRAD`]]; default 6.9D0.
- **`tmolmax`**: the $\log T$ above which only the atomic opacities are used, in [[getopac.f#GETOPAC|`GETOPAC`]] (a ramp from `TMOLMIN`); default 4.1D0. *Name:* T, MOLecular, MAXimum.
- **`tmolmin`**: the $\log T$ below which only the molecular opacities are used; default 4.0D0.
- **`toll`**: the tolerance on $\log L/L_\odot$ of the solar calibration, in [[chkcal.f#CHKCAL|`CHKCAL`]]; in `CONTROL`; default 1.0D-5. *Name:* TOLerance on L.
- **`tollaol`**: the margin of extrapolation (as $\ln$ `TOLLAOL`) in the pure-metal (LAOL format) opacity table, [[gtpurz.f#GTPURZ|`GTPURZ`]]; default 10.0. *Name:* TOLerance, LAOL tables.
- **`tolr`**: in `CONTROL`, the tolerance on $\log R/R_\odot$ of the solar calibration; default 1.0D-4. *Name:* TOLerance on R.
- **`tolz`**: in `CONTROL`, the tolerance on $\log(Z/X)$ of the solar calibration (with `LCALSOLZX`); default 1.0D-3. *Name:* TOLerance on Z.
- **`tridl`**: the size of the envelope triangle in $\log L$, between its lower pair and its upper point; default 8.0D-2; read by [[surfbc.f#SURFBC|`SURFBC`]] and [[entime.f#ENTIME|`ENTIME`]]. *Name:* TRIangle, D L.
- **`tridt`**: the spacing of the triangle's lower pair in $\log T_\mathrm{eff}$; default 1.0D-2; read by the same routines. *Name:* TRIangle, D T.
- **`tscut`**: the $\log T$ above which the default equation of state takes the gas as fully ionized ([[eqstat2.f#EQSTAT2|`EQSTAT2`]] calls [[eqrelv.f#EQRELV|`EQRELV`]] alone); default 6.0D0.
- **`vnew`**: `(12)`, the relative mass fractions of 12 elements of the envelope's mixture (G&N93), from which [[starin.f#STARIN|`STARIN`]] computes the number fractions at the first run; default (0.001999D0, 0.003238D0, …).
- **`walpcz`**: the exponent of $\Omega \propto r^{\mathtt{WALPCZ}}$ in the convection zone (0 solid body, $-2$ uniform specific angular momentum); default 0.0D0; PARMIN clamps it to $[-2, 0]$ with `LROT`; read by [[wczimp.f#WCZIMP|`WCZIMP`]], [[momi.f#MOMI|`MOMI`]], [[mdot.f#MDOT|`MDOT`]] and [[getnewenv.f#GETNEWENV|`GETNEWENV`]]. *Name:* W ($\Omega$), CZ.
- **`weakscreening`**: the largest weak-screening parameter $U_\mathrm{weak}$ for which [[engeb.f#ENGEB|`ENGEB`]] and [[rates.f#RATES|`RATES`]] use weak screening (above 1: always); default 0.03D0.
- **`wmax`**: the saturation angular velocity of the wind, $\Omega_\mathrm{sat}$, in rad s$^{-1}$; default 3.0D-4; PARMIN replaces it by `WMAX_SUN`$\cdot$`PMMSOLW` when `WMAX_SUN` < 1000; read by [[wind.f#WIND|`WIND`]], [[cowind.f#COWIND|`COWIND`]], [[mwind.f#MWIND|`MWIND`]], [[mcowind.f#MCOWIND|`MCOWIND`]] and [[dadcoeft.f#DADCOEFT|`DADCOEFT`]]; also in `DERIVED`.
- **`wnew`**: with `LWNEW`, the angular velocity of the solid-body start, in rad s$^{-1}$ ([[starin.f#STARIN|`STARIN`]] sets $\Omega$ to it); default 0.0D0; [[wind.f#WIND|`WIND`]] and [[mwind.f#MWIND|`MWIND`]] overwrite it with the latest surface $\Omega$ (MWIND's page asks about this).
- **`xbe9_ini`**: in `CONTROL`, the initial ⁹Be mass fraction applied by [[starin.f#STARIN|`STARIN`]] with `LISOTOPE`; default 1.595D-10.
- **`xenv0a`**: in `CONTROL`, `(50)`, the envelope $X$ of each run, a label: the main program copies it to `XENV0` for the output headers, while the composition comes from the model or its rescaling; no initializer; filled by [[setcal.f#SETCAL|`SETCAL`]], [[chkcal.f#CHKCAL|`CHKCAL`]], [[setscal.f#SETSCAL|`SETSCAL`]] and [[chkscal.f#CHKSCAL|`CHKSCAL`]]. *Name:* `XENV0` for each run.
- **`xh2_ini`**: in `CONTROL`, the initial deuterium mass fraction applied with `LISOTOPE`; default 2.781D-5.
- **`xhe3_ini`**: in `CONTROL`, the initial ³He mass fraction; default 3.461D-5.
- **`xli6_ini`**: in `CONTROL`, the initial ⁶Li mass fraction; default 7.187D-10.
- **`xli7_ini`**: in `CONTROL`, the initial ⁷Li mass fraction; default 1.025D-8.
- **`xls`**: in `CONTROL`, with `LCALST`, the star's luminosity $L_*/L_\odot$; no initializer; read by [[setscal.f#SETSCAL|`SETSCAL`]] and [[chkscal.f#CHKSCAL|`CHKSCAL`]].
- **`xlstol`**: in `CONTROL`, the tolerance on $L/L_\odot$ (linear) of that calibration; no initializer; read by [[chkscal.f#CHKSCAL|`CHKSCAL`]].
- **`xmin`**: settling stops once the central $X$ < `XMIN` ([[mix.f#MIX|`MIX`]] and [[rotmix.f#ROTMIX|`ROTMIX`]] turn `LDIFY` off), and [[setup_grsett.f#SETUP_GRSETT|`SETUP_GRSETT`]] starts above a convective core where $X$ > `XMIN`; default 1.0D-3.
- **`xnewcp`**: with `LNEWCP`, the value given to one species: a mass fraction, or with `LREL` $\log\epsilon$ on the astronomers' scale, $X = 10^{\mathtt{XNEWCP}-12}X_\mathrm{surf}$; default 1.3D1; [[rscale.f#RSCALE|`RSCALE`]] overwrites it with the converted mass fraction.
- **`ymin`**: settling of helium needs some shell with $Y$ > `YMIN` (the documentation: off once surface $Y$ < `YMIN`); default 1.0D-3; read by [[mix.f#MIX|`MIX`]], [[rotmix.f#ROTMIX|`ROTMIX`]], [[setup_grsett.f#SETUP_GRSETT|`SETUP_GRSETT`]] and `MICRODIFF_SETUP`.
- **`zenv0a`**: in `CONTROL`, `(50)`, the envelope $Z$ of each run, a label like `XENV0A`; no initializer; filled by [[setcal.f#SETCAL|`SETCAL`]], [[chkcal.f#CHKCAL|`CHKCAL`]] and [[setscal.f#SETSCAL|`SETSCAL`]]. *Name:* `ZENV0` for each run.
- **`zopal951`**: in `CONTROL`, the $Z$ of a surface-mixture opacity table generated at the start (faster for models without diffusion); no initializer; read by `LL95TBL`.

## ACDPTH_MOD

The acoustic-depth output: the results of [[calcad.f#CALCAD|`CALCAD`]] and the switches that decide at which ages it runs (it never runs, since `lacout` cannot be turned on).

- **`acatmd`**: an array `(JSON)`, set and read nowhere. *What it was meant to hold is not stated: the atmosphere's density for the acoustic depth?*
- **`acatmp`**: an array `(JSON)`, set and read nowhere. *What it was meant to hold is not stated: the atmosphere's pressure?*
- **`acatmr`**: an array `(JSON)`, set and read nowhere. *What it was meant to hold is not stated: the atmosphere's radius?*
- **`acatmt`**: an array `(JSON)`, set and read nowhere. *What it was meant to hold is not stated: the atmosphere's temperature?*
- **`ageout`**: `(5)`, the ages at which to write the acoustic-depth output, in Gyr (initial values 0.5, 1, 5, 10, 20); read by the [[main.f#(file level)|main program]].
- **`deladj`**: $\nabla_\mathrm{ad}$ at each point, `(JSON)`, from the OPAL 2006 or SCV equation of state; set and read by [[calcad.f#CALCAD|`CALCAD`]]. *Name:* DEL (gradient), AD (adiabatic).
- **`lacout`**: the master switch of the acoustic-depth output, `.FALSE.`; in no namelist and set nowhere, so it stays off. *Name:* L (logical), AC (acoustic), OUT (output).
- **`ladon`**: true while `lacout` is on; set by the [[main.f#(file level)|main program]], read by [[getopal95.f#GETOPAL95|`GETOPAL95`]] (four-point interpolation) and [[wrtout.f#WRTOUT|`WRTOUT`]].
- **`laoly`**: a logical, set and read nowhere. *What it was meant to switch is not stated.*
- **`lclcd`**: write the `CALCAD` files at this step (initially `.FALSE.`); set by the [[main.f#(file level)|main program]] at the ages `ageout`, read by `CALCAD` and [[envint.f#ENVINT|`ENVINT`]]. *Name:* L (logical), CLCD for CALCAD.
- **`ljlast`**: true on the step just before an age in `ageout` (initially `.FALSE.`); set by the [[main.f#(file level)|main program]], read by [[wrtout.f#WRTOUT|`WRTOUT`]].
- **`ljwrt`**: keeps the output on for the step after an age in `ageout` (initially `.FALSE.`); set and read by the [[main.f#(file level)|main program]].
- **`tatmos`**: the acoustic depth of the atmosphere; always 0, since its computation in [[calcad.f#CALCAD|`CALCAD`]] is commented out; written by [[wrtout.f#WRTOUT|`WRTOUT`]].
- **`tauczn`**: the acoustic depth of the base of the convection zone over the sound travel time from surface to centre, `tcz`/`tnorm` (dimensionless); set by [[calcad.f#CALCAD|`CALCAD`]], reset to 0 by [[wrtout.f#WRTOUT|`WRTOUT`]] without a convective envelope. *Name:* TAU (acoustic depth), CZ, N (normalized).
- **`tauhe`**: set to 0 by [[calcad.f#CALCAD|`CALCAD`]] and written by [[wrtout.f#WRTOUT|`WRTOUT`]]; never computed. *What it holds is not stated: the acoustic depth of the helium ionization zone?*
- **`tcz`**: the acoustic depth of the base of the convection zone, in s; set by [[calcad.f#CALCAD|`CALCAD`]].
- **`tnorm`**: the sound travel time from the surface to the centre, in s; set by [[calcad.f#CALCAD|`CALCAD`]]. *Name:* T (time), NORM (the normalization of `tauczn`).
- **`whe`**: set to 0 by [[calcad.f#CALCAD|`CALCAD`]] and written by [[wrtout.f#WRTOUT|`WRTOUT`]]; never computed. *What it holds is not stated: the width of the helium ionization zone?*

## AEOS06_MOD

The OPAL 2006 equation-of-state tables and their grids.

- **`dfs`**: the inverse spacings of the $T_6$ grid, `(NT)`, `dfs(i)` $= 1/(\mathtt{t6a}(i) - \mathtt{t6a}(i-1))$; set by [[readcoeos06.f#READCOEOS06|`READCOEOS06`]], read by [[esac06.f#ESAC06|`ESAC06`]] and [[t6rinteos06.f#T6RINTEOS06|`T6RINTEOS06`]].
- **`dfsr`**: the inverse spacings of the density grid `rho`, `(NR)`; set by `READCOEOS06`, read by `ESAC06` and `T6RINTEOS06`.
- **`dfsx`**: the inverse spacings of the $X$ grid `xa`, `(MX)`; set by `READCOEOS06`, read by `ESAC06`.
- **`esk`**: one table quantity interpolated in $X$ on the $(T_6, \rho)$ grid, `(NT,NR)`; set by [[esac06.f#ESAC06|`ESAC06`]], read by it and [[t6rinteos06.f#T6RINTEOS06|`T6RINTEOS06`]].
- **`esk2`**: the second, overlapping quadratic interpolation in $X$ that `ESAC06` blends into `esk`, `(NT,NR)`; set by `ESAC06`, read by it and `T6RINTEOS06`.
- **`mf`**: the index of the first of the $X$ tables used in the interpolation; set in [[esac06.f#ESAC06|`ESAC06`]].
- **`midx`**: the index over the five $X$ tables, used as a loop counter in [[readcoeos06.f#READCOEOS06|`READCOEOS06`]] and [[esac06.f#ESAC06|`ESAC06`]] (renamed from `M`). *Name:* M, INDEX.
- **`mv`**: the number of quantities in each table, 10 (a private `PARAMETER`).
- **`mx`**: the number of $X$ values, 5 (a private `PARAMETER`).
- **`nr`**: the number of densities in the grid, 169 (a private `PARAMETER`).
- **`nt`**: the number of temperatures in the grid, 197 (a private `PARAMETER`).
- **`rho`**: the density grid, in g cm$^{-3}$, not a logarithm (from $10^{-14}$ to $10^7$), `(NR)`; set by [[readcoeos06.f#READCOEOS06|`READCOEOS06`]], read by `ESAC06`, [[rhoofp06.f#RHOOFP06|`RHOOFP06`]], [[eqbound06.f#EQBOUND06|`EQBOUND06`]] and `T6RINTEOS06`.
- **`t6a`**: the temperature grid $T_6 = T/10^6$ K, not a logarithm (from 100 down to 0.002), `(NT)`; set by `READCOEOS06`. *Name:* T6, A (auxiliary array, ESAC06's comments).
- **`t6list`**: $T_6$ at each density and temperature of the table, `(NR,NT)`; set by `READCOEOS06`, read by `ESAC06` and `RHOOFP06`.
- **`xa`**: the five $X$ values of the tables, 0, 0.2, 0.4, 0.6, 0.8 (a `DATA` statement), `(MX)`; read by [[esac06.f#ESAC06|`ESAC06`]] and [[rhoofp06.f#RHOOFP06|`RHOOFP06`]].
- **`xz`**: the tables: for each $X$ in `xa`, ten quantities (pressure in megabar, energy, entropy, their derivatives, ...; ESAC06's comments) on the $(T_6, \rho)$ grid, `(MX,MV,NT,NR)`; read in by [[readcoeos06.f#READCOEOS06|`READCOEOS06`]], read by `ESAC06` and `RHOOFP06`.

## ALATM01_MOD

The Allard model-atmosphere table, read by [[alfilein.f#ALFILEIN|`ALFILEIN`]] and interpolated by the other Allard routines.

- **`alphas`**: the $\alpha$-element enhancements found in the table file, `(NGA)`; set and used only within [[alfilein.f#ALFILEIN|`ALFILEIN`]] to choose the table.
- **`fehs`**: the metallicities [Fe/H] found in the table file, `(NGA)`; set and used only within `ALFILEIN`.
- **`gls`**: the table's $\log g$ grid, `(NGA)`; set by [[alfilein.f#ALFILEIN|`ALFILEIN`]], read by [[altabinit.f#ALTABINIT|`ALTABINIT`]], [[alprint.f#ALPRINT|`ALPRINT`]] and [[alsurfp.f#ALSURFP|`ALSURFP`]]. *Name:* G, L (log), S (plural).
- **`loldnextgen`**: the table file is in the old NextGen format; set by `ALFILEIN` and read nowhere else.
- **`nalpha`**: the number of values in `alphas`; set by `ALFILEIN`.
- **`nfeh`**: the number of values in `fehs`; set by `ALFILEIN`.
- **`nga`**: the size of the $\log g$ dimension, 25 (a private `PARAMETER`).
- **`ngl`**: the number of $\log g$ values in `gls`; set by `ALFILEIN`.
- **`nta`**: the size of the $\log T_\mathrm{eff}$ dimension, 250 (a private `PARAMETER`).
- **`nteff`**: the number of $\log T_\mathrm{eff}$ values in `teffls`; set by `ALFILEIN`.
- **`p100ls`**: $\log P$ at $\tau = 100$, `(NTA,NGA)` (for the option `LALTPTau100`); set by `ALFILEIN`.
- **`pls`**: $\log P$ where $T = T_\mathrm{eff}$, `(NTA,NGA)`; set by `ALFILEIN`, interpolated by [[alsurfp.f#ALSURFP|`ALSURFP`]].
- **`t100ls`**: $\log T$ at $\tau = 100$, `(NTA,NGA)` (for `LALTPTau100`); set by `ALFILEIN`.
- **`teffls`**: the table's $\log T_\mathrm{eff}$ grid, `(NTA)`; set by `ALFILEIN`.

## ALATM02_MOD

The valid range of the Allard table, set by [[altabinit.f#ALTABINIT|`ALTABINIT`]].

- **`glmax`**: for each $\log T_\mathrm{eff}$ row, the largest valid $\log g$, `(NTA)`; set by [[altabinit.f#ALTABINIT|`ALTABINIT`]], read by [[alsurfp.f#ALSURFP|`ALSURFP`]] and [[alprint.f#ALPRINT|`ALPRINT`]].
- **`glmin`**: for each row, the smallest valid $\log g$, `(NTA)`; set by `ALTABINIT`.
- **`glxmax`**: the largest $\log g$ over all rows; set by `ALTABINIT`.
- **`glxmin`**: the smallest $\log g$ over all rows; set by `ALTABINIT`.
- **`iglmax`**: for each row, the last valid column of the $\log g$ grid, `(NTA)`; set by `ALTABINIT`.
- **`iglmin`**: for each row, the first valid column, `(NTA)`; set by `ALTABINIT`.
- **`nta`**: the size of the $\log T_\mathrm{eff}$ dimension, 250 (a private `PARAMETER`).
- **`tefflmax`**: the largest valid $\log T_\mathrm{eff}$; set by [[altabinit.f#ALTABINIT|`ALTABINIT`]] (recomputed by [[alprint.f#ALPRINT|`ALPRINT`]]).
- **`tefflmin`**: the smallest valid $\log T_\mathrm{eff}$; set by `ALTABINIT` (recomputed by `ALPRINT`).

## ALATM05_MOD

The Allard table's own first and last $\log T_\mathrm{eff}$.

- **`al_tefflmax`**: the Allard table's largest $\log T_\mathrm{eff}$; set by [[altabinit.f#ALTABINIT|`ALTABINIT`]], read by [[surfbc.f#SURFBC|`SURFBC`]] to switch away from the Allard atmospheres. *Name:* AL (Allard), TEFF, L (log), MAX.
- **`al_tefflmin`**: the Allard table's smallest $\log T_\mathrm{eff}$; set by `ALTABINIT`, read nowhere.

## ALOT06ALL_MOD

All the tables of the low-temperature opacities of Ferguson et al. (2005), called ALEX06 in the code.

- **`captalex06`**: $\log\kappa$ for 143 compositions on the grid of 85 temperatures and 19 values of $R$, `(NUMXZ,NUMT,NUMD)`; read in by [[readalex06.f#READALEX06|`READALEX06`]], interpolated by [[alex06tab.f#ALEX06TAB|`ALEX06TAB`]]. *Name:* CAP (κ), ALEX06.
- **`numd`**: the number of $R$ values, 19 (a private `PARAMETER`).
- **`numt`**: the number of temperatures, 85 (a private `PARAMETER`).
- **`numxz`**: the number of compositions, 143 (a private `PARAMETER`).

## ALOT06_MOD

The ALEX06 low-temperature opacity table for the current composition, with the composition and the starting indices of the search.

- **`capalex06`**: $\log\kappa$ on the $(T, R)$ grid for the composition `xe`, `ze`, `(NUMT,NUMD)`; set by [[alex06tab.f#ALEX06TAB|`ALEX06TAB`]] (first by [[readalex06.f#READALEX06|`READALEX06`]]), read by [[getalex06.f#GETALEX06|`GETALEX06`]]. *Name:* CAP (κ), ALEX06.
- **`id`**: the starting index in $R$ of the search in [[getalex06.f#GETALEX06|`GETALEX06`]], which updates it (initially 10).
- **`it`**: the starting index in $T$ of the search in `GETALEX06`, which updates it (initially 43).
- **`ix`**: the first of the $X$ tables used (initially 4); set by [[alex06tab.f#ALEX06TAB|`ALEX06TAB`]].
- **`numd`**: the number of $R$ values, 19 (a private `PARAMETER`).
- **`numt`**: the number of temperatures, 85 (a private `PARAMETER`).
- **`xe`**: the $X$ of the current table (initially 0); reset by [[getalex06.f#GETALEX06|`GETALEX06`]] when the point's $X$ differs by more than $10^{-8}$.
- **`ze`**: the $Z$ of the current table (initially 0); reset by `GETALEX06` likewise.

## ATMOS2C_MOD

The surface-pressure table used when `KTTAU` is 5, read by [[setups.f#SETUPS|`SETUPS`]] and interpolated by [[kcsurfp.f#KCSURFP|`KCSURFP`]].

- **`atmglc`**: the table's $\log g$ grid, `(NGC)`; set by [[setups.f#SETUPS|`SETUPS`]] from the file `FATM`. *Name:* ATM, G, L (log), C (the `KTTAU` = 5 table).
- **`atmplc`**: $\log P$ at the surface on the $(\log T_\mathrm{eff}, \log g)$ grid, `(NTC,NGC)`; set by `SETUPS`, read by [[kcsurfp.f#KCSURFP|`KCSURFP`]].
- **`atmtlc`**: the table's $\log T_\mathrm{eff}$ grid, `(NTC)`; set by `SETUPS`.
- **`ngc`**: the number of $\log g$ values, 11 (a private `PARAMETER`).
- **`ntc`**: the number of $\log T_\mathrm{eff}$ values, 76 (a private `PARAMETER`).

## ATMOS2_MOD

The (Kurucz) surface-pressure table read when `KTTAU` is 3 or 4, interpolated by [[surfp.f#SURFP|`SURFP`]].

- **`atmgl`**: the table's $\log g$ grid, `(NG)`; set by [[setups.f#SETUPS|`SETUPS`]] from the file `FATM`. *Name:* ATM, G, L (log).
- **`atmpl`**: $\log P$ at the surface on the $(\log T_\mathrm{eff}, \log g)$ grid, `(NT,NG)`; set by `SETUPS`, read by [[surfp.f#SURFP|`SURFP`]].
- **`atmtl`**: the table's $\log T_\mathrm{eff}$ grid, `(NT)`; set by `SETUPS`.
- **`atmz`**: the table's metallicity $Z$ (also stored for the `KTTAU` = 5 table); set by `SETUPS`, read by no routine.
- **`ng`**: the number of $\log g$ values, 11 (a private `PARAMETER`).
- **`nt`**: the number of $\log T_\mathrm{eff}$ values, 57 (a private `PARAMETER`).

## ATMOS_MOD

One number: the $T(\tau)$ relation at $\tau = 2/3$.

- **`hras`**: $\mathrm{HRA}(2/3)$, the value of the $T(\tau)$ relation [[hra.f#HRA|`HRA`]] at $\tau = 2/3$, in $\log T$; set once by [[setups.f#SETUPS|`SETUPS`]], read by [[envint.f#ENVINT|`ENVINT`]] and [[qatm.f#QATM|`QATM`]], so that $T = T_\mathrm{eff}$ at $\tau = 2/3$.

## ATMPRT_MOD

The state at the last point of the atmosphere integration (or the fitting point of a tabulated atmosphere), for the envelope integration and the output.

- **`ad`**: $\log\rho$ at the point; set by [[qatm.f#QATM|`QATM`]] only when the model is stored or written for pulsation (`LSAVE`, `LPUMOD`). *Name:* A (atmosphere), D (density).
- **`afxion`**: the ionization fractions `FXION` from the equation of state, `(3)`: in [[eqsaha.f#EQSAHA|`EQSAHA`]], `SAHAX(7)` and the singly and doubly ionized helium fractions `SAHEX1`, `SAHEX2`; set by `QATM` with `LSAVE` or `LPUMOD`. *Which species `FXION(1)` (`SAHAX(7)`) is, is not stated: hydrogen?*
- **`ao`**: the opacity $\kappa$, in cm$^2$ g$^{-1}$, not a logarithm (`O` from [[getopac.f#GETOPAC|`GETOPAC`]]); set by `QATM` with `LSAVE` or `LPUMOD`.
- **`ap`**: $\log P$ at the point; set by [[qatm.f#QATM|`QATM`]], [[surfp.f#SURFP|`SURFP`]] and [[kcsurfp.f#KCSURFP|`KCSURFP`]]; read by [[envint.f#ENVINT|`ENVINT`]] and [[massloss.f#MASSLOSS|`MASSLOSS`]].
- **`at`**: $\log T$ at the point; set by `QATM`, the table routines and [[alsurfp.f#ALSURFP|`ALSURFP`]]; read by `ENVINT` and `MASSLOSS`.
- **`taul`**: $\log\tau$, the optical depth at the point (named `TAU` until the module); set by [[qatm.f#QATM|`QATM`]].

## ATMSTRUCT_MOD

The structure of the atmosphere, point by point, set by [[envint.f#ENVINT|`ENVINT`]] and read only by [[stitch.f#STITCH|`STITCH`]] for the stitched output of the whole star.

- **`abetas`**: $\beta = P_\mathrm{gas}/P$ at each atmosphere point, `(JSON)`; set by [[envint.f#ENVINT|`ENVINT`]].
- **`adels`**: the three temperature gradients at each point, `(3,JSON)`: $\nabla_\mathrm{rad}$, $\nabla$, $\nabla_\mathrm{ad}$; set by `ENVINT`. *Name:* A (atmosphere), DEL (gradient), S (plural).
- **`afxions`**: the three ionization fractions (as `afxion` in [[atmprt_mod.f#ATMPRT_MOD|`ATMPRT_MOD`]]) at each point, `(3,JSON)`; set by `ENVINT`.
- **`agam1`**: $\Gamma_1$ at each point, `(JSON)`; set by `ENVINT`.
- **`aqdt`**: $Q_{\rho T}$ at each point, `(JSON)`; set by `ENVINT`.
- **`atmocp`**: $c_P$ at each point, `(JSON)`; set by `ENVINT`.
- **`atmod`**: $\log\rho$ at each point, `(JSON)`; set by `ENVINT`.
- **`atmoo`**: the opacity $\kappa$ at each point, not a logarithm, `(JSON)`; set by `ENVINT`.
- **`atmop`**: $\log P$ at each point, `(JSON)`; set by `ENVINT`.
- **`atmor`**: the radial step from the previous atmosphere point, $\Delta r = \Delta\tau/\overline{\rho\kappa}$, in cm, not a logarithm, `(JSON)` (the page calls it $\log r$; [[envint.f#ENVINT|`ENVINT`]] stores `DELTR`, which [[stitch.f#STITCH|`STITCH`]] adds to the envelope's top radius).
- **`atmot`**: $\log T$ at each point, `(JSON)`; set by `ENVINT`.
- **`numatm`**: the number of atmosphere points stored; set by `ENVINT`.

## CCOUT_MOD

One switch for the stitched stored-model output.

- **`lphhd`**: write the header of the stitched stored-model output; set to `LSTCH` by [[parmin.f#PARMIN|`PARMIN`]], turned off by [[putstore.f#PUTSTORE|`PUTSTORE`]] after its first call.

## CCR_MOD

The table of the electron (Fermi–Dirac) equation of state used for partial degeneracy, read by [[setups.f#SETUPS|`SETUPS`]] and used by [[eqrelv.f#EQRELV|`EQRELV`]].

- **`dtable`**: the Fermi table, five quantities at each of 43 density abscissae and 20 temperatures ($\log T$ from 5.0 in steps of 0.2), `(5,43,20)`; read by [[setups.f#SETUPS|`SETUPS`]] from unit `IFERMI`, interpolated by [[eqrelv.f#EQRELV|`EQRELV`]] (the first quantity enters the electron pressure). *Which five quantities, and in what units, is not stated.*
- **`dval`**: the 43 density abscissae, in the variable $\log(\rho\,\mu_e^{-1}) - 1.5\log T$ that `EQRELV` forms, `(43)`; read by `SETUPS`. *Name:* D (density), VAL (values).
- **`etat8`**: the electron degeneracy parameter $\eta$ at each abscissa of `dval`, `(43)`; read by `SETUPS`, interpolated by `EQRELV`.
- **`iden`**: maps a density bin of width 0.05 in `dval` to its table row, `(261)`; built by `SETUPS`, read by `EQRELV`. *Name:* I (index), DEN (density).

## CENT_MOD

The central conditions and the base of the surface convection zone of the last model written, set by [[wrtout.f#WRTOUT|`WRTOUT`]] for the neutrino-flux output of the [[main.f#(file level)|main program]].

- **`czsurf_m`**: the mass of the surface convection zone, in $M_\odot$ (the star's mass when fully convective, 0 without one); set by [[wrtout.f#WRTOUT|`WRTOUT`]]. *Name:* CZ (convection zone), SURF (surface), M (mass).
- **`czsurf_r`**: the radius of the base of the surface convection zone, in $R_\odot$ (0 when fully convective or without one); set by `WRTOUT`.
- **`dcenter`**: the central $\log\rho$; set by `WRTOUT`. *Name:* D (density), CENTER.
- **`pcenter`**: the central $\log P$; set by `WRTOUT`.
- **`tcenter`**: the central $\log T$; set by `WRTOUT`.

## CENV_MOD

The option to move the envelope's fitting point.

- **`lsenv0`**: move the envelope's fitting point to `senv0`; copied from the run's `LSENV0A` by the [[main.f#(file level)|main program]], read by [[starin.f#STARIN|`STARIN`]].
- **`senv0`**: the requested fitting point, $\log(m_\mathrm{fit}/M)$; copied from `SENV0A` by the main program; `STARIN` makes it negative and at most $-10^{-12}$.

## COMP2_MOD

The envelope's helium, completing [[comp_mod.f#COMP_MOD|`COMP_MOD`]].

- **`y3env`**: the envelope's ³He mass fraction $Y_3$; set by [[starin.f#STARIN|`STARIN`]], read by [[physic.f#PHYSIC|`PHYSIC`]] and [[checkc.f#CHECKC|`CHECKC`]].
- **`yenv`**: the envelope's ⁴He mass fraction, $1 - X - Z - Y_3$; set by `STARIN`, read by `PHYSIC` and `CHECKC`.

## COMP_MOD

The composition of the envelope and the star's total and envelope masses.

- **`amuenv`**: the envelope's inverse mean molecular weight per ion, $\mu_\mathrm{ion}^{-1} = \sum_i X_i/A_i$ over twelve species; set in [[starin.f#STARIN|`STARIN`]], corrected for the local $X$, $Z$ by its readers ([[mu.f#MU|`MU`]], [[eqstat2.f#EQSTAT2|`EQSTAT2`]], [[physic.f#PHYSIC|`PHYSIC`]], [[checkc.f#CHECKC|`CHECKC`]]). *Name:* AMU (as in the equation of state), ENV.
- **`fxenv`**: the envelope's number fractions of the twelve species, $(X_i/A_i)/\mathtt{amuenv}$, `(12)`; set in `STARIN`, passed on by `EQSTAT2` to the Saha solver.
- **`senv`**: $\log(m/M)$ at the fitting point between the interior model and the envelope; set in `STARIN`, [[hpoint.f#HPOINT|`HPOINT`]], [[mdot.f#MDOT|`MDOT`]], [[getnewenv.f#GETNEWENV|`GETNEWENV`]] and [[crrect.f#CRRECT|`CRRECT`]], read by [[envint.f#ENVINT|`ENVINT`]].
- **`stotal`**: $\log M$, in g (from `HSTOT`); set in `STARIN`, [[rscale.f#RSCALE|`RSCALE`]] and `MDOT`.
- **`xenv`**: the envelope's $X$; set by [[starin.f#STARIN|`STARIN`]] from `xnew`.
- **`xnew`**: the surface $X$ for which the surface opacity table was last made; set in `STARIN`, [[rscale.f#RSCALE|`RSCALE`]] and [[hpoint.f#HPOINT|`HPOINT`]], read by [[crrect.f#CRRECT|`CRRECT`]] and [[wrtout.f#WRTOUT|`WRTOUT`]].
- **`zenv`**: the envelope's $Z$; set by `STARIN` from `znew`, may be reset by `RSCALE` and [[parmin.f#PARMIN|`PARMIN`]].
- **`zenvm`**: the envelope's $Z$ other than the CNO-cycle elements (STARIN's comment); set in `STARIN`, read by [[mixcz.f#MIXCZ|`MIXCZ`]].
- **`znew`**: the surface $Z$ for which the surface opacity table was last made; set in `STARIN`, `RSCALE` and `HPOINT`.

## CONFAC_MOD

The factors that convert radius, mass, temperature and time between the code's units and those of Bahcall and Loeb (1989) in the diffusion routines, set by [[microdiff_setup.f#MICRODIFF_SETUP|`MICRODIFF_SETUP`]] and [[setup_grsett.f#SETUP_GRSETT|`SETUP_GRSETT`]].

- **`con_mass`**: the mass conversion factor, $10^{-2}\,\mathtt{con\_rad}^3$, the inverse of the mass unit $100\ \mathrm{g\,cm^{-3}} \times R_\odot^3$; set by [[microdiff_setup.f#MICRODIFF_SETUP|`MICRODIFF_SETUP`]] and [[setup_grsett.f#SETUP_GRSETT|`SETUP_GRSETT`]]. *Name:* CON (conversion), MASS.
- **`con_rad`**: the radius conversion factor, $1/R_\odot$ (Bahcall's value), in cm$^{-1}$; set by the same two routines.
- **`con_temp`**: the temperature conversion factor, $10^{-7}$ K$^{-1}$ (the unit $10^7$ K); set by the same two routines.
- **`con_time`**: the time unit, $2.7\times10^{13}$ yr in s, which "includes factor of 2.2 from ln Lambda" (the Coulomb logarithm); set by the same two routines.

## CROSS_MOD

The factors by which the nuclear reaction rates are adjusted for user-changed cross sections, set by [[remap.f#REMAP|`REMAP`]] and read by [[engeb.f#ENGEB|`ENGEB`]] and [[rates.f#RATES|`RATES`]].

- **`fc12`**: the factor on the ¹⁵N(p,α)¹²C branch: 1, or with `LNEWNUC` the ratio of the user's $S_0$ to the reference; set in [[remap.f#REMAP|`REMAP`]].
- **`fo16`**: the factor on the ¹⁵N(p,γ)¹⁶O branch, likewise; set in `REMAP`.
- **`qqs0ee`**: factors on the second-derivative terms ($Q_4$, $Q_5$) of the eight pp and CNO rates, proportional to $S''/S$ relative to the reference, `(8)`; 1 unless `LNEWNUC`; set in `REMAP`.
- **`qs0e`**: factors on the first-derivative terms ($Q_2$, $Q_3$) of the eight rates, proportional to $S'/S$, `(8)`; 1 unless `LNEWNUC`; set in `REMAP`. *Name:* Q, S0 (the S-factor at zero energy).

## CTOL_MOD

The fraction of the Henyey correction applied in the current iteration.

- **`fcorr`**: the fraction of the Henyey correction applied; set by the [[main.f#(file level)|main program]] to $|\mathtt{FCORR0}| - \mathtt{FCORRI}$ at each model's start, raised by `FCORRI` per iteration up to 1 by [[crrect.f#CRRECT|`CRRECT`]], which scales the corrections by it. *Name:* F (fraction), CORR (correction).

## DEBHU_MOD

The inputs of the Debye–Hückel correction to the equation of state, read only by [[eqrelv.f#EQRELV|`EQRELV`]].

- **`cdh`**: the constant $-\sqrt{\pi/(k\,m_H^3)}\,e^3/3$ of the Debye–Hückel pressure, in cgs; set in [[setups.f#SETUPS|`SETUPS`]]. *Name:* C (constant), DH (Debye–Hückel).
- **`dhnue`**: the charges of C, N, O, Ne, Na, Mg, Al, Si, P, S, Cl, Ar, Ca, Ti, Cr, Mn, Fe, Ni, `(18)`; set in `SETUPS`.
- **`xxdh`**: the local $X$, copied from the shell's composition before the equation of state is called by nine routines (such as [[physic.f#PHYSIC|`PHYSIC`]] and [[coefft.f#COEFFT|`COEFFT`]]).
- **`yydh`**: the local $Y$ (³He + ⁴He), copied likewise.
- **`zdh`**: the local abundances of the 18 heavy elements (C = ¹²C + ¹³C, N = ¹⁴N + ¹⁵N, O = ¹⁶O + ¹⁸O from `HCOMP`), `(18)`, copied likewise.
- **`zzdh`**: the local $Z$, copied likewise.

## DEUTER_MOD

The deuterium burning rates, the mass accreted in the step and the base of the surface convection zone.

- **`drate`**: the deuterium burning rate at each shell, `(JSON)`; set by [[deutrate.f#DEUTRATE|`DEUTRATE`]] (zeroed in [[mix.f#MIX|`MIX`]]), read by [[dburn.f#DBURN|`DBURN`]], where the deuterium abundance falls as $\exp(-2\,\mathtt{drate}\,\Delta t)$, and [[midmod.f#MIDMOD|`MIDMOD`]]. *Units not stated: s$^{-1}$, with $\Delta t$ in s?*
- **`drate0`**: the rate at the start of the step, `(JSON)`; copied from `drate` by `DEUTRATE` on the first iteration, remapped by [[hpoint.f#HPOINT|`HPOINT`]].
- **`fmassacc`**: the mass accreted in the step (`DELM`), in g; set by [[mdot.f#MDOT|`MDOT`]], read by `DBURN`, [[dburnm.f#DBURNM|`DBURNM`]] and [[liburn.f#LIBURN|`LIBURN`]]. *Name:* F, MASS, ACC (accreted).
- **`jcz`**: the shell at the base of the surface convection zone (`JENV`); set by the [[main.f#(file level)|main program]] and [[massloss.f#MASSLOSS|`MASSLOSS`]], read by `DEUTRATE` and [[engeb.f#ENGEB|`ENGEB`]]. *Name:* J (shell index), CZ.

## DIFAD2_MOD

The advective and diffusive parts of the meridional circulation velocity at each shell, for the diffusion-plus-advection treatment of angular momentum (`LDIFAD`).

- **`vesa`**: the advective (signed) part, `(JSON)`; set by [[vcirc.f#VCIRC|`VCIRC`]], read by [[rotgrid.f#ROTGRID|`ROTGRID`]] (into `ecod3`) and [[checkj.f#CHECKJ|`CHECKJ`]]. *Units not stated: cm s$^{-1}$, or a coefficient in cm$^2$ s$^{-1}$?* *Name:* VES (the circulation velocity, `VES` in `VCIRC`), A (advective).
- **`vesa0`**: `vesa` from the previous call, `(JSON)`; saved and read by `VCIRC` alone, which averages the two.
- **`vesd`**: the diffusive part, `(JSON)`; set by `VCIRC`, read by `ROTGRID` (into `ecod4`) and `CHECKJ`. *Units not stated: cm$^2$ s$^{-1}$?* *Name:* VES, D (diffusive).
- **`vesd0`**: `vesd` from the previous call, `(JSON)`; saved and read by `VCIRC` alone.

## DIFAD3_MOD

The Zahn-type factors of the diffusion-plus-advection treatment of angular momentum (`LDIFAD`), shared by [[setupv.f#SETUPV|`SETUPV`]], [[vcirc.f#VCIRC|`VCIRC`]] and [[dadcoeft.f#DADCOEFT|`DADCOEFT`]]; all are arrays `(JSON)`.

- **`dgsf`**: $r\,|v_\mathrm{GSF}|$, the radius times the Goldreich–Schubert–Fricke velocity, `(JSON)`; set by [[vcirc.f#VCIRC|`VCIRC`]], read nowhere. *Name:* D (diffusion), GSF.
- **`dss`**: $r\,|v_\mathrm{SS}|$, the radius times the secular-shear velocity, `(JSON)`; set by `VCIRC`, read nowhere. *Name:* D, SS (secular shear).
- **`ecod5`**: a coefficient read by [[dadcoeft.f#DADCOEFT|`DADCOEFT`]] in its band matrix, `(JSON)`; set by no routine, so it keeps its initial value. *What it holds is not stated.*
- **`ecod6`**: likewise, `(JSON)`; read by `DADCOEFT`, set by no routine. *What it holds is not stated.*
- **`egsf`**: the Goldreich–Schubert–Fricke term added to `ecod4` in `DADCOEFT` (rescaled in place there), `(JSON)`; set by no routine. *Units not stated.*
- **`ess`**: the secular-shear term added to `ecod4` in `DADCOEFT` (rescaled in place there), `(JSON)`; set by no routine. *Units not stated.*
- **`ev0`**: a factor of the circulation velocity read by `DADCOEFT`, `(JSON)`; set by no routine (the counterpart of `fv0`). *What it holds is not stated.*
- **`ev1a`**: likewise, the counterpart of `fv1a`, `(JSON)`; read by `DADCOEFT`, set by no routine. *What it holds is not stated.*
- **`ev1b`**: likewise, the counterpart of `fv1b`, `(JSON)`; read by `DADCOEFT`, set by no routine. *What it holds is not stated.*
- **`ev2a`**: likewise, the counterpart of `fv2a`, `(JSON)`; read by `DADCOEFT`, set by no routine. *What it holds is not stated.*
- **`ev2b`**: likewise, the counterpart of `fv2b`, `(JSON)`; read by `DADCOEFT`, set by no routine. *What it holds is not stated.*
- **`facd2`**: a factor set by [[setupv.f#SETUPV|`SETUPV`]], from which `VCIRC` forms `vesd2`, `(JSON)`. *What it holds is not stated.*
- **`facd3`**: likewise, the factor of `vesd3`, `(JSON)`; set by `SETUPV`. *What it holds is not stated.*
- **`fgeom`**: a geometric factor by which `DADCOEFT` multiplies `ecod3` and `ecod4`, `(JSON)`; set by no routine. *What it holds is not stated.*
- **`fv0`**: a factor of the circulation velocity, `(JSON)`; set by `SETUPV`, rescaled by `VCIRC`. *What it holds is not stated.*
- **`fv1a`**: `FES1`/`fv0`, `(JSON)`; set by `SETUPV`, read nowhere. *What it holds is not stated.*
- **`fv1b`**: `FES2`/`fv0`, `(JSON)`; set by `SETUPV`, read nowhere. *What it holds is not stated.*
- **`fv2a`**: a factor set by `SETUPV`, `(JSON)`, read nowhere. *What it holds is not stated.*
- **`fv2b`**: a factor set by `SETUPV` (with the `FACT7` term added), `(JSON)`, read nowhere. *What it holds is not stated.*
- **`vesd2`**: `0.2*facd2*WM`, rescaled by the μ-gradient factor, `(JSON)`; set by `VCIRC`, read nowhere. *What it holds is not stated.*
- **`vesd3`**: `0.2*facd3*WM`, rescaled likewise, `(JSON)`; set by `VCIRC`, read nowhere. *What it holds is not stated.*

## DIFAD_MOD

The advective and diffusive coefficients of angular-momentum transport on the even grid, used with `LDIFAD`.

- **`ecod3`**: the advective coefficient, `(JSON)`; interpolated from `vesa` by [[rotgrid.f#ROTGRID|`ROTGRID`]], recomputed by [[dadcoeft.f#DADCOEFT|`DADCOEFT`]], read by [[dcoeft.f#DCOEFT|`DCOEFT`]] and [[checkj.f#CHECKJ|`CHECKJ`]]. *Units not stated.*
- **`ecod4`**: the diffusive coefficient, with the composition diffusion coefficient added, `(JSON)`; set by `ROTGRID`, recomputed by `DADCOEFT`. *Units not stated: cm$^2$ s$^{-1}$?*

## DIMENSIONS_MOD

The one structural array dimension shared by the whole code.

- **`json`**: the maximum number of shells in a model, 5000 (a `PARAMETER`, used by 144 files).

## DISK_MOD

The star's age, which the rotation routines compare with the disk-locking time.

- **`sage`**: the total age `DAGE`, in Gyr; stored by the [[main.f#(file level)|main program]] after each model, read by [[getw.f#GETW|`GETW`]], [[seculr.f#SECULR|`SECULR`]], [[solid.f#SOLID|`SOLID`]] and [[mdot.f#MDOT|`MDOT`]].

## DPMIX_MOD

The extent of the overshoot region below a convection zone and the index of the shell being computed, read only by [[tpgrad.f#TPGRAD|`TPGRAD`]].

- **`iov1`**: the first shell of the overshoot region (−1 when there is none); set by [[oversh.f#OVERSH|`OVERSH`]]. *Name:* I (index), OV (overshoot), 1 (first).
- **`iov2`**: the last shell of the overshoot region; set by `OVERSH`.
- **`iovim`**: the shell for which the gradient is wanted; set just before the call by [[coefft.f#COEFFT|`COEFFT`]], [[physic.f#PHYSIC|`PHYSIC`]], [[qenv.f#QENV|`QENV`]] and [[starin.f#STARIN|`STARIN`]]; with `LADOV`, `TPGRAD` takes $\nabla = \nabla_\mathrm{ad}$ when `iov1` ≤ `iovim` ≤ `iov2`.

## DWMAX_MOD

The critical rotation gradient for the shear instability at each shell, and its value at the start of the step.

- **`qwrmax`**: the critical $d\Omega/d\ln r$ for the shear instability (Endal and Sofia 1978), $2\sqrt{(\rho/P)(\nabla_\mathrm{ad}-\nabla)\,g^2}$, in s$^{-1}$, at the interface between shells `IM-1` and `IM`; 0 where both shells are convective or the root is not real; `(JSON)`. Set by [[physic.f#PHYSIC|`PHYSIC`]], read only by [[hpoint.f#HPOINT|`HPOINT`]] to copy it.
- **`qwrmx0`**: the start-of-step copy of `qwrmax`, `(JSON)`; made by [[hpoint.f#HPOINT|`HPOINT`]], read nowhere. *Name:* `QWRMAX` shortened to six characters, 0 for the start of the step.

## EEEOS06_MOD

Workspace of the OPAL 2006 equation-of-state interpolation: the table values of the quantity being interpolated, and the $X$ values of the tables.

- **`epl`**: for each $X$ index, the table values of the quantity being interpolated (`XZ(MIDX,IV,IT,IR)` of `AEOS06_MOD`), `(MX,NT,NR)`; copied for each variable `IV` and read in the interpolation by [[esac06.f#ESAC06|`ESAC06`]].
- **`mx`**: the number of $X$ values of the tables, 5; a `PRIVATE` parameter, as in `AEOS06_MOD`.
- **`nr`**: the number of densities of the tables, 169; a `PRIVATE` parameter.
- **`nt`**: the number of temperatures of the tables, 197; a `PRIVATE` parameter.
- **`xx`**: the $X$ values of the five tables, `(MX)`, a copy of `XA` made by [[esac06.f#SETEOS06|`SETEOS06`]]; read by [[esac06.f#ESAC06|`ESAC06`]] and [[readcoeos06.f#READCOEOS06|`READCOEOS06`]].

## EGRIDDER_MOD

The coefficients of the higher-derivative terms of the diffusion-plus-advection treatment of angular momentum (`LDIFAD`).

- **`eqqcod`**: `qqcod` times $\Omega$ (`WM`) at each shell, `(JSON)`; set by [[vcirc.f#VCIRC|`VCIRC`]], read by [[dadcoeft.f#DADCOEFT|`DADCOEFT`]] as the coefficients of its $d^2\Omega/dr^2$ rows.
- **`eqqqcod`**: the coefficients of the $d^3\Omega/dr^3$ rows of [[dadcoeft.f#DADCOEFT|`DADCOEFT`]], `(JSON)`; read there but set by no routine. *Should `VCIRC` fill it from `qqqcod`, as it fills `eqqcod` from `qqcod`?*
- **`qqcod`**: $\tfrac23\,r^4/(G\,m)$ at each interface (`CC23*RM**4/CG/HS3`, cgs), `(JSON)`; set by [[setupv.f#SETUPV|`SETUPV`]], turned into `eqqcod` by [[vcirc.f#VCIRC|`VCIRC`]].
- **`qqqcod`**: $P r^2/(\rho\,G\,m\,\nabla)$ at each shell, the temperature scale height $H_p/\nabla$ (cm; the code's `HTM`, `HTP`), `(JSON)`; set by [[setupv.f#SETUPV|`SETUPV`]], read nowhere.

## EGRID_MOD

The evenly spaced grid on which angular momentum transport and rotational mixing are solved, all set by [[getgrid.f#GETGRID|`GETGRID`]].

- **`chi`**: the grid variable $\chi = \log m/\Delta_m + L/\Delta_L - \log P/\Delta_P$ at each shell of the region (dimensionless; the $\Delta$s are the mesh tolerances `HPTTOL`), `(JSON)`.
- **`dchi`**: the spacing of the even points in $\chi$, $(\chi_\mathrm{last}-\chi_1)/(\mathtt{NTOT}-1)$. *Name:* $\Delta\chi$.
- **`echi`**: $\chi$ at the even points, from `CHI(1)` in steps of `dchi`, `(JSON)`. *Name:* E for the even grid.
- **`es1`**: the mass $m$ (g) at the even points, interpolated in $\log m$ by [[osplin.f#OSPLIN|`OSPLIN`]], `(JSON)`. *Name:* E for the even grid, `HS1` the mass in g.
- **`ntot`**: the number of even points (`INTEGER*4`): the number of shells in the region, but at least 3.

## ENTROP_MOD

The rates of change of the structure variables over the last step, for a better first guess of the next model (`LNEWS`).

- **`hll0`**: the relative change of $L$ over the last step, $2(L-L_\mathrm{old})/(L+L_\mathrm{old})$, per second, `(JSON)`; set by the [[main.f#(file level)|main program]], interpolated by [[hpoint.f#HPOINT|`HPOINT`]] when the grid changes.
- **`hpp0`**: the change of $\log P$ over the last step divided by the step `DELTS` (s$^{-1}$), `(JSON)`; set by the [[main.f#(file level)|main program]], interpolated by [[hpoint.f#HPOINT|`HPOINT`]].
- **`hrr0`**: the change of $\log r$ per second over the last step, `(JSON)`; set by the [[main.f#(file level)|main program]], interpolated by [[hpoint.f#HPOINT|`HPOINT`]].
- **`htt0`**: the change of $\log T$ over the last step divided by `DELTS` (s$^{-1}$), `(JSON)`; set by the [[main.f#(file level)|main program]], interpolated by [[hpoint.f#HPOINT|`HPOINT`]]. The comments call these four "entropy terms," but they are time derivatives of the structure.

## ENVPRT_MOD

The state at the current point of the envelope integration, set by [[qenv.f#QENV|`QENV`]] at each call and stored by [[envint.f#ENVINT|`ENVINT`]].

- **`ebeta`**: $\beta$, the ratio of gas to total pressure. *Name:* E for envelope, BETA.
- **`ed`**: $\log\rho$. *Name:* E for envelope, D for density.
- **`edel`**: the temperature gradients `(3)`: $\nabla_\mathrm{rad}$, $\nabla_\mathrm{ad}$, $\nabla$ (`DELR`, `DELA`, `DEL`).
- **`efxion`**: the ionization fractions `(3)` from the equation of state (H$^+$, He$^+$, He$^{++}$, as [[eqsaha.f#EQSAHA|`EQSAHA`]] orders them).
- **`eo`**: the opacity $\kappa$ (cm$^2$ g$^{-1}$, not a logarithm); set only when `QENV` saves the point (`LSAVE` or `LPUMOD`).
- **`ep`**: $\log P$.
- **`er`**: $\log r$.
- **`es`**: $\log(m/M)$, the mass coordinate relative to the star's mass (`SL - STOTAL`).
- **`et`**: $\log T$.
- **`evel`**: the convective velocity (cm s$^{-1}$; 0 where radiative).

## ENVSTRUCT_MOD

The run of the envelope's structure, point by point, stored by [[envint.f#ENVINT|`ENVINT`]] (point 1 at the bottom after it reverses the order) and shifted by [[getnewenv.f#GETNEWENV|`GETNEWENV`]] and [[starin.f#STARIN|`STARIN`]] when the fitting point moves.

- **`ebetas`**: $\beta$ at each stored point, `(JSON)`. *Name:* `EBETA` stored.
- **`edels`**: the gradients $\nabla_\mathrm{rad}$, $\nabla_\mathrm{ad}$, $\nabla$ at each point, `(3,JSON)`.
- **`efxions`**: the ionization fractions (H$^+$, He$^+$, He$^{++}$) at each point, `(3,JSON)`.
- **`egam1`**: the adiabatic exponent $\Gamma_1$ at each point, `(JSON)`.
- **`envd`**: $\log\rho$ at each point, `(JSON)`.
- **`envl`**: the luminosity $L/L_\odot$ at each point (not a logarithm; the same value throughout the envelope), `(JSON)`.
- **`envo`**: the opacity $\kappa$ (cm$^2$ g$^{-1}$, not a logarithm) at each point, `(JSON)`.
- **`envp`**: $\log P$ at each point, `(JSON)`.
- **`envr`**: $\log r$ at each point, `(JSON)`.
- **`envs`**: $\log(m/M)$ at each point, `(JSON)`.
- **`envt`**: $\log T$ at each point, `(JSON)`.
- **`envx`**: $X$ at each point, `(JSON)`.
- **`envz`**: $Z$ at each point, `(JSON)`.
- **`eqcp`**: $c_P$ (erg g$^{-1}$ K$^{-1}$) at each point, `(JSON)`. *Name:* E for envelope, `QCP`.
- **`eqdt`**: $Q_{\rho T} = (\partial\ln\rho/\partial\ln T)_P$ at each point, `(JSON)`. *Name:* E for envelope, `QDT`.
- **`evels`**: the convective velocity (cm s$^{-1}$) at each point, `(JSON)`.
- **`lcenv`**: whether each point is convective (`EVEL` > 0), `LOGICAL*4`, `(JSON)`. *Name:* L for logical, C for convective, ENV.
- **`numenv`**: the number of stored points (`INTEGER*4`).

## EOS06MISC_MOD

Results and workspace of the OPAL 2006 equation-of-state interpolation: the interpolated quantities, the grid indices of the current point, the tables' compositions, the order of the quantities and the extent of each table row.

- **`eos`**: the ten interpolated quantities `(MV)`: $P$, $E$, $S$, $\partial E/\partial\rho|_T$, $c_V$, $\partial\ln P/\partial\ln\rho$, $\partial\ln P/\partial\ln T$, $\Gamma_1$, $\Gamma_2/(\Gamma_2-1)$, $\Gamma_3-1$; set by [[esac06.f#ESAC06|`ESAC06`]] and corrected for radiation by [[radsub06.f#RADSUB06|`RADSUB06`]].
- **`esact`**: one quantity interpolated in $T_6$ and $\rho$ by [[t6rinteos06.f#T6RINTEOS06|`T6RINTEOS06`]], before `ESAC06` scales it into `eos`.
- **`h`**: workspace `(4)` of [[t6rinteos06.f#T6RINTEOS06|`T6RINTEOS06`]]: the quadratics in $\rho$ at fixed $T$.
- **`index`**: the order in which the quantities are stored, `(10)`, initially 1 to 10 (`INTEGER*4`).
- **`ip`**: the number of temperature points used in the interpolation (`INTEGER*4`); set by [[esac06.f#ESAC06|`ESAC06`]].
- **`iq`**: the number of density points used in the interpolation (`INTEGER*4`); set by [[esac06.f#ESAC06|`ESAC06`]].
- **`iri`**: the inverse of `index`, `(10)` (`INTEGER*4`); set by [[esac06.f#SETEOS06|`SETEOS06`]].
- **`k1`**: the first of the four temperature indices around the point (`INTEGER*4`); set by [[esac06.f#ESAC06|`ESAC06`]], read by [[t6rinteos06.f#T6RINTEOS06|`T6RINTEOS06`]] and [[eqbound06.f#EQBOUND06|`EQBOUND06`]].
- **`k2`**: the second of the four temperature indices around the point (`INTEGER*4`); set by [[esac06.f#ESAC06|`ESAC06`]], read by [[t6rinteos06.f#T6RINTEOS06|`T6RINTEOS06`]] and [[eqbound06.f#EQBOUND06|`EQBOUND06`]].
- **`k3`**: the third of the four temperature indices around the point (`INTEGER*4`); set by [[esac06.f#ESAC06|`ESAC06`]], read by [[t6rinteos06.f#T6RINTEOS06|`T6RINTEOS06`]] and [[eqbound06.f#EQBOUND06|`EQBOUND06`]].
- **`k4`**: the fourth of the four temperature indices around the point (`INTEGER*4`); set by [[esac06.f#ESAC06|`ESAC06`]], read by [[t6rinteos06.f#T6RINTEOS06|`T6RINTEOS06`]] and [[eqbound06.f#EQBOUND06|`EQBOUND06`]].
- **`l1`**: the first of the four density indices around the point (`INTEGER*4` despite the initial letter); set by [[esac06.f#ESAC06|`ESAC06`]], read by `T6RINTEOS06` and `EQBOUND06`.
- **`l2`**: the second of the four density indices around the point (`INTEGER*4` despite the initial letter); set by [[esac06.f#ESAC06|`ESAC06`]], read by `T6RINTEOS06` and `EQBOUND06`.
- **`l3`**: the third of the four density indices around the point (`INTEGER*4` despite the initial letter); set by [[esac06.f#ESAC06|`ESAC06`]], read by `T6RINTEOS06` and `EQBOUND06`.
- **`l4`**: the fourth of the four density indices around the point (`INTEGER*4` despite the initial letter); set by [[esac06.f#ESAC06|`ESAC06`]], read by `T6RINTEOS06` and `EQBOUND06`.
- **`mv`**: the number of interpolated quantities, 10; a `PRIVATE` parameter.
- **`mx`**: the number of $X$ values of the tables, 5; a `PRIVATE` parameter.
- **`nr`**: the number of densities of the tables, 169; a `PRIVATE` parameter.
- **`nra`**: for each temperature, the number of densities in the tables (the tables are not rectangular), `(NT)`, initialized in the module (`INTEGER*4`).
- **`nt`**: the number of temperatures of the tables, 197; a `PRIVATE` parameter.
- **`nta`**: for each density, the number of temperatures in the tables, `(NR)`, initialized in the module (`INTEGER*4`).
- **`q`**: workspace `(4)` of [[t6rinteos06.f#T6RINTEOS06|`T6RINTEOS06`]]: the quadratics in $T$.
- **`xxh`**: set and read nowhere.
- **`zz`**: the $Z$ of each table, `(MX)`, read from the table headers by [[readcoeos06.f#READCOEOS06|`READCOEOS06`]].

## ERRMOM_MOD

The relative tolerance of the iteration for the moment of inertia and the surface rotation rate.

- **`toleri`**: the relative tolerance to which [[solid.f#SOLID|`SOLID`]] matches the convection zone's angular momentum (at most 20 tries); [[checkj.f#CHECKJ|`CHECKJ`]] relaxes it to at least `DJOK`/100 around its call to `GETROT` and then restores it. Its first value is $10^{-12}$ (since `7be4133`; before, nothing gave it one, so it started at zero). *Name:* TOLER for tolerance.

## FAC_MOD

The range of valid gravities at each temperature of the two surface-pressure tables, and the interpolation indices of the last lookup.

- **`imin`**: for each temperature of the surface-pressure table, the lowest gravity index with a valid pressure, `(NT)` (`INTEGER*4`); set by [[setups.f#SETUPS|`SETUPS`]], read by [[surfp.f#SURFP|`SURFP`]].
- **`imin2`**: the same for the 76-temperature (Kurucz/Castelli) table, `(NTC)`; set by [[setups.f#SETUPS|`SETUPS`]], read by [[kcsurfp.f#KCSURFP|`KCSURFP`]].
- **`iminmax`**: for each temperature, the highest gravity index with a valid pressure, `(NT)`; set by [[setups.f#SETUPS|`SETUPS`]], read by [[surfp.f#SURFP|`SURFP`]].
- **`iminmax2`**: the same for the 76-temperature table, `(NTC)`; set by `SETUPS`, read by [[kcsurfp.f#KCSURFP|`KCSURFP`]].
- **`jp`**: the temperature index of the last interpolation (`INTEGER*4`); set by [[surfp.f#SURFP|`SURFP`]] and [[kcsurfp.f#KCSURFP|`KCSURFP`]], read nowhere.
- **`kp`**: the four gravity indices of the last interpolation, `(4)`; set by `SURFP` and `KCSURFP`, read nowhere.
- **`nt`**: the number of temperatures of the surface-pressure table, 57; a `PRIVATE` parameter.
- **`ntc`**: the number of temperatures of the Kurucz/Castelli surface-pressure table, 76; a `PRIVATE` parameter.

## FLUXES_MOD

The solar neutrino fluxes, per gram at the current shell and summed over the star, and the capture rates for the chlorine and gallium experiments.

- **`clsnu`**: the capture rate for the ³⁷Cl experiment, in SNU, $\sum_i f_i\Phi_i$ over the first eight fluxes; set by [[wrtout.f#WRTOUT|`WRTOUT`]]. *Name:* Cl, SNU.
- **`flux`**: the neutrino fluxes at the Earth of the ten reactions (pp, pep, hep, ⁷Be, ⁸B, ¹³N, ¹⁵O, ¹⁷F, and the fictional He3+He3 and He3+He4 fluxes) produced per gram at one shell, `(10)`; set by [[engeb.f#ENGEB|`ENGEB`]]. *Units: ENGEB's comment writes "CM^-2 SEC^-2 PER GM"; is it cm$^{-2}$ s$^{-1}$ per gram?*
- **`fluxtot`**: the fluxes summed over the shells, weighted by the shell masses, `(10)`; built by [[coefft.f#COEFFT|`COEFFT`]] (with `LSNU`) and the [[main.f#(file level)|main program]], written and zeroed by [[wrtout.f#WRTOUT|`WRTOUT`]].
- **`gasnu`**: the capture rate for the ⁷¹Ga experiments, in SNU; set by [[wrtout.f#WRTOUT|`WRTOUT`]]. *Name:* Ga, SNU.

## GALOT06_MOD

The grids of the low-temperature opacities of Ferguson et al. (2005) (ALEX06 in the code), fixed initial values moved from `READALEX06`.

- **`numd`**: the number of $\log R$ values ($R = \rho/T_6^3$), 19; a `PRIVATE` parameter.
- **`numt`**: the number of $\log T$ values, 85; a `PRIVATE` parameter.
- **`numx`**: the number of $X$ values, 9; a `PRIVATE` parameter.
- **`numz`**: the number of $Z$ values, 16; a `PRIVATE` parameter.
- **`r0gr06`**: the $\log R$ grid, −8 to 1 in steps of 0.5, `(NUMD)`. *Name:* R grid, 06 for the 2006 tables.
- **`tgr06`**: the $\log T$ grid, 2.70 to 4.50, `(NUMT)`; read by [[getalex06.f#GETALEX06|`GETALEX06`]] and checked against the tables by [[readalex06.f#READALEX06|`READALEX06`]]. *Name:* T grid, 06.
- **`xxg06`**: the nine $X$ values, 0 to 1, `(NUMX)`; read by [[alex06tab.f#ALEX06TAB|`ALEX06TAB`]].
- **`zzg06`**: the sixteen $Z$ values, 0 to 0.10, `(NUMZ)`; read by [[alex06tab.f#ALEX06TAB|`ALEX06TAB`]].

## GRAVEZ_MOD

The metals ($Z$) on the equally spaced radial grid of the older settling routine [[grsett.f#GRSETT|`GRSETT`]], with their diffusion coefficients, used with `LDIFZ`; the grid's radii are in Bahcall–Loeb units.

- **`ecod1z`**: the settling coefficient of the metals at the grid points, `(JSON)`; set by [[model_to_equal.f#MODEL_TO_EQUAL|`MODEL_TO_EQUAL`]], read by [[lax_wendrof1.f#LAX_WENDROF1|`LAX_WENDROF1`]]. *Units not stated: Bahcall–Loeb units, as the grid?* *Name:* E for the equally spaced grid, `COD1Z`.
- **`ecod1z_h`**: the settling coefficient at the midpoints, `(JSON)`; set by `MODEL_TO_EQUAL`, updated by [[grsett.f#GRSETT|`GRSETT`]] with the half-step abundances, read by [[lax_wendrof2.f#LAX_WENDROF2|`LAX_WENDROF2`]]. *Name:* _H for the midpoints.
- **`ecod2z_h`**: the diffusion coefficient of the metals at the midpoints, `(JSON)`; set by `MODEL_TO_EQUAL`, read nowhere (the metals get only the settling term).
- **`eqcod1z_h`**: the abundance-dependent part of the settling coefficient at the midpoints, `(JSON)`; set by `MODEL_TO_EQUAL`, read by `GRSETT`.
- **`eqcod2z_h`**: the abundance-dependent part of the diffusion coefficient at the midpoints, `(JSON)`; set by `MODEL_TO_EQUAL`, read nowhere.
- **`ez`**: $Z$ at the grid points, `(JSON)`: set by [[model_to_equal.f#MODEL_TO_EQUAL|`MODEL_TO_EQUAL`]], advanced by `LAX_WENDROF2`, turned into the change over the step by `GRSETT`.
- **`ez_h`**: $Z$ at the midpoints, `(JSON)`; set by `MODEL_TO_EQUAL` and [[lax_wendrof1.f#LAX_WENDROF1|`LAX_WENDROF1`]] (the half step), read by `GRSETT`.

## INTPAR_MOD

The settings of the Bulirsch–Stoer integration of the atmosphere and envelope, all in the `PHYSICS` namelist read by [[parmin.f#PARMIN|`PARMIN`]].

- **`imax`**: the largest number of step subdivisions [[bsstep.f#BSSTEP|`BSSTEP`]] tries (`INTEGER*4`, default 11).
- **`nuse`**: the number of points in `BSSTEP`'s extrapolation to zero step, passed to [[ratext.f#RATEXT|`RATEXT`]] (`INTEGER*4`, default 7).
- **`stolr0`**: the relative tolerance of the integration (default 1.0D-3); [[envint.f#ENVINT|`ENVINT`]] uses it as is for the atmosphere and scales it by $|$`SENV`$|$ for the envelope.

## INTVAR_MOD

The structure variables at the interfaces between shells, for the rotation routines, all set by [[setupv.f#SETUPV|`SETUPV`]] by four-point Lagrangian interpolation in radius.

- **`alm`**: the luminosity $L$ (erg s$^{-1}$, not a logarithm) at each interface, `(JSON)`; read also by [[vcirc.f#VCIRC|`VCIRC`]].
- **`delami`**: $\nabla_\mathrm{ad}$ at each interface (from `DELAM`), `(JSON)`.
- **`delmi`**: $\nabla_\mathrm{rad}$ at each interface (from `DELRM`), `(JSON)`.
- **`dm`**: the density $\rho$ (g cm$^{-3}$, not a logarithm) at each interface, `(JSON)`; read also by [[getfc.f#GETFC|`GETFC`]].
- **`epsilm`**: the energy generation rate $\epsilon$ (from `ESUMM`, erg g$^{-1}$ s$^{-1}$) at each interface, `(JSON)`.
- **`hgm`**: the gravity $g$ (cm s$^{-2}$) at each interface, `(JSON)`; read also by `VCIRC`. *Name:* `HG` at the midpoint.
- **`hs3`**: the mass $m$ (g) at each interface, `(JSON)`.
- **`pm`**: the pressure $P$ (not a logarithm) at each interface, `(JSON)`.
- **`qdtmi`**: $Q_{\rho T} = (\partial\ln\rho/\partial\ln T)_P$ at each interface (from `QDTM`), `(JSON)`.
- **`rm`**: the radius $r$ (cm) of the interface between shells `I-1` and `I`, the mean of their radii, `(JSON)`; read also by `VCIRC`, `GETFC` and [[seculr.f#SECULR|`SECULR`]]. *Name:* R at the midpoint.
- **`tm`**: the temperature $T$ (K, not a logarithm) at each interface, `(JSON)`.

## LABEL_MOD

The envelope's $X$ and $Z$ of the current run, used to label the output.

- **`xenv0`**: the envelope's $X$ for run `NK`, from the namelist array `XENV0A`, set by the [[main.f#(file level)|main program]] and by [[rscale.f#RSCALE|`RSCALE`]] when the run rescales the composition; written in the output headers (initial value 0.7D0, overwritten before use).
- **`zenv0`**: the envelope's $Z$ for run `NK`, from `ZENV0A`, set as `xenv0`; written in the output headers (initial value 0.02D0, overwritten before use).

## LIOV_MOD

The overshoot distance below the surface convection zone at the start and end of the step, for light-element burning with overshoot.

- **`pscal0`**: `pscal1` at the start of the step; set by the [[main.f#(file level)|main program]] at the start of a run and copied from `pscal1` by [[getw.f#GETW|`GETW`]] and [[bursmix.f#BURSMIX|`BURSMIX`]]. *Name:* P SCALe (height), 0 for the start of the step.
- **`pscal1`**: the overshoot distance at the end of the step, $\alpha_e$ times $H_p$ at the base of the convection zone (cm), with `LOVSTE` and a convective surface, 0 otherwise; set by [[getw.f#GETW|`GETW`]] and the main program, read by [[liburn.f#LIBURN|`LIBURN`]] and [[liburn2.f#LIBURN2|`LIBURN2`]]. *Name:* P SCALe, 1 for the end of the step.

## LLOT95A_MOD

All the OPAL95 opacity tables as read, with their grids in $\log T$, $\log R$, $X$ and $Z$.

- **`cappa2`**: $\log\kappa$ of every table, `(NUMXZ,NUMT,NUMD)`; read by [[ll95tbl.f#LL95TBL|`LL95TBL`]] (missing entries 9.999), interpolated by [[op95ztab.f#OP95ZTAB|`OP95ZTAB`]], [[op954d.f#OP954D|`OP954D`]] and [[getopal95.f#GETOPAL95|`GETOPAL95`]]. *Name:* kappa.
- **`numd`**: the number of $\log R$ values ($R = \rho/T_6^3$), 19; a `PRIVATE` parameter.
- **`numt`**: the number of $\log T$ values, 70; a `PRIVATE` parameter.
- **`numx`**: the number of $X$ values, 10; a `PRIVATE` parameter.
- **`numxm`**: the number of $X$ tables for each $Z$, `(NUMZ)` (10, but 9, 9, 8 for $Z$ = 0.06, 0.08, 0.1), initialized in the module; read nowhere.
- **`numxz`**: the number of tables, 126; a `PRIVATE` parameter.
- **`numz`**: the number of $Z$ values, 13; a `PRIVATE` parameter.
- **`nz`**: the offset of each $Z$'s tables in `cappa2`'s first index, `(NUMZ)` (0, 10, … , 118), initialized in the module.
- **`r0gr`**: the $\log R$ grid, `(NUMD)`; read from the tables by [[ll95tbl.f#LL95TBL|`LL95TBL`]]. *Name:* R grid.
- **`tgr`**: the $\log T$ grid, `(NUMT)`; read from the tables by `LL95TBL`. *Name:* T grid.
- **`xxg`**: the $X$ values of the tables, 0 to 1, `(NUMX)`, initialized in the module.
- **`zzg`**: the $Z$ values of the tables, 0 to 0.10, `(NUMZ)`, initialized in the module.

## LLOT95E_MOD

The OPAL95 opacity table interpolated to the surface composition (one $X$ and $Z$), and that $X$.

- **`cappae`**: $\log\kappa$ on the ($\log T$, $\log R$) grid at $X$ = `xop95` and $Z$ = `ZTAB`, `(NUMT,NUMD)`; set by [[op95xtab.f#OP95XTAB|`OP95XTAB`]], read by [[op952d.f#OP952D|`OP952D`]].
- **`numd`**: the number of $\log R$ values, 19; a `PRIVATE` parameter.
- **`numt`**: the number of $\log T$ values, 70; a `PRIVATE` parameter.
- **`xop95`**: the $X$ of `cappae`; set by [[op95xtab.f#OP95XTAB|`OP95XTAB`]], read by [[getopal95.f#GETOPAL95|`GETOPAL95`]]. *Name:* X of the OPAL95 table (formerly `XTAB`).

## LLOT95_MOD

The OPAL95 opacity tables interpolated to the current surface $Z$, one for each $X$, and that $Z$.

- **`cappa`**: $\log\kappa$ on the ($X$, $\log T$, $\log R$) grid at $Z$ = `ztab`, `(NUMX,NUMT,NUMD)`; set by [[op95ztab.f#OP95ZTAB|`OP95ZTAB`]], read by [[op95xtab.f#OP95XTAB|`OP95XTAB`]], [[op953d.f#OP953D|`OP953D`]] and [[getopal95.f#GETOPAL95|`GETOPAL95`]]. *Name:* kappa.
- **`numd`**: the number of $\log R$ values, 19; a `PRIVATE` parameter.
- **`numt`**: the number of $\log T$ values, 70; a `PRIVATE` parameter.
- **`numx`**: the number of $X$ values, 10; a `PRIVATE` parameter.
- **`ztab`**: the $Z$ of `cappa`; set by [[op95ztab.f#OP95ZTAB|`OP95ZTAB`]], read by [[getopal95.f#GETOPAL95|`GETOPAL95`]].

## MASSCHG2_MOD

The quantities of the (experimental) thermal response of the convective envelope to accretion.

- **`dlogp`**: the change of $\log P$ that [[mdot.f#MDOT|`MDOT`]] derives from `scen` and applies to the envelope; read also by [[coefft.f#COEFFT|`COEFFT`]]. Zero in practice, since `scen` = 0.
- **`dlogt`**: the change of $\log T$, set and read as `dlogp`; zero in practice.
- **`sacc`**: $(\mathcal R/\mu)(\tfrac32\ln T - \ln\rho)$ (erg g$^{-1}$ K$^{-1}$, an entropy per gram) at the base of the envelope; set by [[massloss.f#MASSLOSS|`MASSLOSS`]], read nowhere.
- **`scen`**: the same quantity mass-averaged over the convective envelope; computed by [[massloss.f#MASSLOSS|`MASSLOSS`]] and then set to 0, read by [[mdot.f#MDOT|`MDOT`]].
- **`smass0`**: the total mass $M/M_\odot$ after the step's mass change; set by [[mdot.f#MDOT|`MDOT`]], read nowhere.

## MDPHY_MOD

Physical quantities at each shell at an intermediate time of the step (weight `FX` between the old and new model), set by [[midmod.f#MIDMOD|`MIDMOD`]] for the rotational-mixing and angular-momentum loop.

- **`amum`**: the mean molecular weight $\mu$, `(JSON)`; set by `MIDMOD`, [[checkc.f#CHECKC|`CHECKC`]] and [[getw.f#GETW|`GETW`]], read by [[setupv.f#SETUPV|`SETUPV`]] and [[vcirc.f#VCIRC|`VCIRC`]].
- **`cpm`**: $c_P$ (erg g$^{-1}$ K$^{-1}$), `(JSON)`.
- **`delam`**: $\nabla_\mathrm{ad}$, `(JSON)`; read also by [[liburn.f#LIBURN|`LIBURN`]] and [[liburn2.f#LIBURN2|`LIBURN2`]].
- **`delm`**: $\nabla$, `(JSON)`; read also by [[rotmix.f#ROTMIX|`ROTMIX`]].
- **`delrm`**: $\nabla_\mathrm{rad}$, `(JSON)`; read also by `LIBURN` and `LIBURN2`.
- **`epsm`**: the energy generation rate `esumm` plus `SEG(6,J)` and `SEG(7,J)` (erg g$^{-1}$ s$^{-1}$), `(JSON)`; read by [[rotgrid.f#ROTGRID|`ROTGRID`]] and [[mixgrid.f#MIXGRID|`MIXGRID`]].
- **`esumm`**: the energy generation rate $\epsilon$ (`SESUM`, erg g$^{-1}$ s$^{-1}$), `(JSON)`.
- **`om`**: the opacity $\kappa$ (cm$^2$ g$^{-1}$, not a logarithm), `(JSON)`.
- **`qdtm`**: $Q_{\rho T} = (\partial\ln\rho/\partial\ln T)_P$, `(JSON)`.
- **`thdifm`**: the thermal diffusivity (cm$^2$ s$^{-1}$), `(JSON)`; read by `VCIRC`.
- **`velm`**: the convective velocity (interpolated, the larger of the two where the shell becomes convective, 0 where it becomes radiative), `(JSON)`; read nowhere.
- **`viscm`**: the viscosity (cm$^2$ s$^{-1}$), `(JSON)`; read by `VCIRC`.

## NEWOPAC_MOD

Two switches of the opacity setup.

- **`l2z`**: whether two opacity tables in $Z$ are needed, `LZRAMP .OR. LDIFZ` (`LOGICAL*4`); set by [[setupopac.f#SETUPOPAC|`SETUPOPAC`]], read by [[getopac.f#GETOPAC|`GETOPAC`]]. *Name:* L for logical, 2 Z (two tables in $Z$).
- **`llaol`**: the switch of the obsolete LAOL opacities (`LOGICAL*4`, initially `.FALSE.`, in no namelist), set nowhere; read by [[starin.f#STARIN|`STARIN`]].

## NEWRAT_MOD

The proton-capture rates of ⁶Li, ⁷Li and ⁹Be at each shell for the current model, all set by [[lirate88.f#LIRATE88|`LIRATE88`]] (with `J` = 1) and read by [[liburn.f#LIBURN|`LIBURN`]] and [[liburn2.f#LIBURN2|`LIBURN2`]].

- **`rbe9`**: the rate per ⁹Be nucleus, $\rho X\,N_A\langle\sigma v\rangle$ summed over ⁹Be(p,γ), (p,d) and (p,α) and scaled by `SBE91`–`SBE93`; zero above the burning region, `(JSON)`. *Units not stated: s$^{-1}$, if the Caughlan–Fowler fits are in cm$^3$ mol$^{-1}$ s$^{-1}$?*
- **`rli6`**: the rate per ⁶Li nucleus of ⁶Li(p,³He)α, $\rho X\,N_A\langle\sigma v\rangle$ scaled by `SLI6`, `(JSON)`. *Units not stated, as for `rbe9`.*
- **`rli7`**: the rate per ⁷Li nucleus of ⁷Li(p,α)α, scaled by `SLI7`, `(JSON)`. *Units not stated, as for `rbe9`.*

## OLDMOD_MOD

The model at the start of the step (the "old" model): structure, composition, effective temperature, and surface luminosity.

- **`hcompp`**: the old composition, mass fractions as in `HCOMP` (1 $X$, 2 $Y$, 3 $Z$, 4–15 the tracked isotopes), `(15,JSON)`; saved by the [[main.f#(file level)|main program]], [[hpoint.f#HPOINT|`HPOINT`]], [[getw.f#GETW|`GETW`]] and [[bursmix.f#BURSMIX|`BURSMIX`]].
- **`hdo`**: the old $\log\rho$, `(JSON)`; `HPOINT` also uses it as scratch. *Name:* `HD` old.
- **`hlo`**: the old $L/L_\odot$ (not a logarithm), `(JSON)`. *Name:* `HL` old.
- **`hpo`**: the old $\log P$, `(JSON)`; saved by the main program, `HPOINT` and [[starin.f#STARIN|`STARIN`]]. *Name:* `HP` old.
- **`hro`**: the old $\log r$, `(JSON)`. *Name:* `HR` old.
- **`hss`**: the old mass coordinates, against which [[hpoint.f#HPOINT|`HPOINT`]] interpolates (and the new grid while it builds it), `(JSON)`. *Units not stated: $\log m$, as `HS`?*
- **`hto`**: the old $\log T$, `(JSON)`. *Name:* `HT` old.
- **`lco`**: the old convective flags (`LOGICAL*4`), `(JSON)`; saved by [[hpoint.f#HPOINT|`HPOINT`]], read by [[midmod.f#MIDMOD|`MIDMOD`]]. *Name:* `LC` old.
- **`hlsuro`**: the old surface luminosity, $L/L_\odot$ (`HL(M)`); saved by the main program, `HPOINT` and `STARIN`, read by [[entime.f#ENTIME|`ENTIME`]] (since `7be4133`, in place of `MO`, the old number of shells). *Name:* `HL` at the SURface, old.
- **`lczo`**: old convective flags (`LOGICAL*4`), `(JSON)`; saved by `HPOINT` (and `STARIN` for the starting model), read by [[crrect.f#CRRECT|`CRRECT`]], which passes them to `GETROT` (since `7be4133`). *What does it flag, as against `lco`?*
- **`tefflo`**: the old $\log T_\mathrm{eff}$; saved by the main program, `HPOINT` and `STARIN`, read by [[entime.f#ENTIME|`ENTIME`]]. *Name:* `TEFFL` old.

## OLDPHY_MOD

Physical quantities of the model at the start of the step, saved by [[hpoint.f#HPOINT|`HPOINT`]] after the remap, which [[midmod.f#MIDMOD|`MIDMOD`]] interpolates against the new model for the rotational-mixing substeps.

- **`amuo`**: the mean molecular weight $\mu$ of a fully ionized gas at the start of the step (dimensionless), `(JSON)`; copied from `HAMU` by [[hpoint.f#HPOINT|`HPOINT`]]; read by `MIDMOD` and [[getw.f#GETW|`GETW`]] (the change of $\mu$ over the step). *Name:* `AMU` + O for old.
- **`cpo`**: $c_P$ at the start of the step, erg g$^{-1}$ K$^{-1}$, `(JSON)`; copied from `CP` by [[hpoint.f#HPOINT|`HPOINT`]]. *Name:* `CP` + O for old.
- **`delao`**: $\nabla_\mathrm{ad}$ at the start of the step, `(JSON)`; copied from `SDEL(3,·)` by [[hpoint.f#HPOINT|`HPOINT`]], which also forms `DDELM` = `DELAO` − `DELO`. *Name:* `DELA` + O for old.
- **`delo`**: $\nabla$ (the actual gradient) at the start of the step, `(JSON)`; copied from `SDEL(2,·)` by [[hpoint.f#HPOINT|`HPOINT`]]. *Name:* `DEL` + O for old.
- **`delro`**: $\nabla_\mathrm{rad}$ at the start of the step, `(JSON)`; copied from `SDEL(1,·)` by [[hpoint.f#HPOINT|`HPOINT`]]. *Name:* `DELR` + O for old.
- **`epso`**: the total energy generation $\epsilon$ at the start of the step, nuclear plus `SEG(6)`, `SEG(7)` (neutrino and gravitational terms), erg g$^{-1}$ s$^{-1}$, `(JSON)`; interpolated onto the new grid by [[hpoint.f#HPOINT|`HPOINT`]] ("MHP 6/00").
- **`esumo`**: the nuclear energy generation `SESUM` at the start of the step, erg g$^{-1}$ s$^{-1}$, `(JSON)`; interpolated onto the new grid by [[hpoint.f#HPOINT|`HPOINT`]]. *Name:* `SESUM` + O for old.
- **`oo`**: the opacity $\kappa$ at the start of the step (not a logarithm), cm$^2$ g$^{-1}$, `(JSON)`; copied from `SO` by [[hpoint.f#HPOINT|`HPOINT`]]. *Name:* `O` (opacity) + O for old.
- **`qdto`**: $\partial\ln\rho/\partial\ln T$ at the start of the step, `(JSON)`; copied from `SQDT` by [[hpoint.f#HPOINT|`HPOINT`]]. *Name:* `QDT` + O for old.
- **`thdifo`**: the radiative diffusivity at the start of the step, cm$^2$ s$^{-1}$, `(JSON)`; copied from `THDIF` by [[hpoint.f#HPOINT|`HPOINT`]]. *Name:* `THDIF` (thermal diffusivity) + O for old.
- **`velo`**: the convective velocity at the start of the step, cm s$^{-1}$, `(JSON)`; copied from `SVEL` by [[hpoint.f#HPOINT|`HPOINT`]]. *Name:* VEL (velocity) + O for old.
- **`visco`**: the viscosity (radiative plus molecular) at the start of the step, cm$^2$ s$^{-1}$, `(JSON)`; copied from `VISC` by [[hpoint.f#HPOINT|`HPOINT`]]. *Name:* `VISC` + O for old.

## OLDRAT_MOD

The proton-capture rates of ⁶Li, ⁷Li and ⁹Be at each shell for the model at the start of the step; the current model's are in [[newrat_mod.f#NEWRAT_MOD|`NEWRAT_MOD`]].

- **`rbe90`**: the ⁹Be proton-capture rate at the start of the step (the Caughlan–Fowler fit times $\rho X$, per second, not a logarithm), `(JSON)`; set by [[lirate88.f#LIRATE88|`LIRATE88`]] (`J` = 2) and copied from `RBE9` by [[getw.f#GETW|`GETW`]] and [[bursmix.f#BURSMIX|`BURSMIX`]]. *Name:* Rate, BE9, 0 for the start.
- **`rli60`**: the ⁶Li proton-capture rate at the start of the step, s$^{-1}$, `(JSON)`; set like `RBE90`. *Name:* Rate, LI6, 0 for the start.
- **`rli70`**: the ⁷Li proton-capture rate at the start of the step, s$^{-1}$, `(JSON)`; set like `RBE90`. *Name:* Rate, LI7, 0 for the start.

## OLDROT2_MOD

The terms of the time derivative of $\theta$ in the Maeder–Zahn (1998) treatment of angular-momentum transport, at the start of the step and during the substeps, at each interface `I` (between shells `I-1` and `I`).

- **`ddelm`**: $\nabla_\mathrm{ad} - \nabla$ at the interface, `(JSON)`; set by [[hpoint.f#HPOINT|`HPOINT`]] from the old model, then overwritten by [[setupv.f#SETUPV|`SETUPV`]] with the $\mu$-gradient term added (not below a floor); read by `SETUPV` and [[vcirc.f#VCIRC|`VCIRC`]].
- **`festime`**: $P/(g\,\Delta\nabla\,\rho)$ at the interface ($\Delta\nabla = \nabla_\mathrm{ad}-\nabla$, floored), `(JSON)`; set by [[setupv.f#SETUPV|`SETUPV`]] (0 where unused) and rescaled by [[vcirc.f#VCIRC|`VCIRC`]] with the $\mu$-gradient factor.
- **`qwrmst`**: $d\Omega/dr$ at the start of the current substep, s$^{-1}$ cm$^{-1}$, `(JSON)`; set by [[getw.f#GETW|`GETW`]]; read nowhere.
- **`qwrst`**: $d\Omega/dr$ of the model at the start of the step, s$^{-1}$ cm$^{-1}$, `(JSON)`; set by [[hpoint.f#HPOINT|`HPOINT`]], copied into `QWRMST` by [[getw.f#GETW|`GETW`]].
- **`thm`**: $r_{i-1}^2 r_i^2/(\sqrt{m_{i-1}m_i}\,G)$ at the interface (the $r^4/(\sqrt m\,G)$ of $\theta$, not a logarithm), `(JSON)`; set by [[setupv.f#SETUPV|`SETUPV`]] ("added for $d\theta/dt$ term from Zahn & Maeder 1998").
- **`thn`**: the $d\theta/dt$ term, `FESTIME`·(`THM`$\,\bar\Omega\,d\Omega/dr$ − `THP`)/$\Delta t$, `(JSON)`; set and read by [[vcirc.f#VCIRC|`VCIRC`]], which adds it to the circulation velocities.
- **`tho`**: $\theta$ = `THM`$\,\bar\Omega\,d\Omega/dr$ of the model at the start of the step, `(JSON)`; set by [[hpoint.f#HPOINT|`HPOINT`]], copied into `THP` by [[getw.f#GETW|`GETW`]] on the first iteration.
- **`thp`**: $\theta$ at the start of the current substep, `(JSON)`; set by [[getw.f#GETW|`GETW`]]; read by [[vcirc.f#VCIRC|`VCIRC`]].
- **`wmst`**: $\Omega$ at the start of the current substep, rad s$^{-1}$, `(JSON)`; set by [[getw.f#GETW|`GETW`]]; read by [[seculr.f#SECULR|`SECULR`]] (the starting surface $\Omega$ for the wind).

## OLDROT_MOD

The rotation of the model at the start of the step, on the new point distribution, saved by [[hpoint.f#HPOINT|`HPOINT`]] ("store the old model structure for use in diffusion").

- **`eta2x`**: the distortion term $\eta_2$ (from Radau's equation) at the start of the step, `(JSON)`; saved and interpolated by [[hpoint.f#HPOINT|`HPOINT`]], which copies it back into `ETA2`.
- **`hgo`**: the mean gravity $\langle g\rangle$ (`HG`) at the start of the step, cm s$^{-2}$, `(JSON)`; saved by [[hpoint.f#HPOINT|`HPOINT`]]; read by [[midmod.f#MIDMOD|`MIDMOD`]] (interpolated to mid-step). *Name:* `HG` + O for old.
- **`hio`**: the moment of inertia $I$ of each shell (`HI`) at the start of the step, g cm$^2$, `(JSON)`; saved by [[hpoint.f#HPOINT|`HPOINT`]]; read nowhere. *Name:* `HI` + O for old.
- **`hjx`**: the specific angular momentum $j$ of each shell (`HJM`, "J/M stored in HJX") at the start of the step, cm$^2$ s$^{-1}$, `(JSON)`; saved and interpolated by [[hpoint.f#HPOINT|`HPOINT`]], which copies it back into `HJM`.
- **`r0x`**: the equivalent radius $r_0$ of each equipotential (`R0`, cm, not a logarithm) at the start of the step, `(JSON)`; saved and interpolated by [[hpoint.f#HPOINT|`HPOINT`]], which copies it back into `R0`.
- **`wold`**: $\Omega$ at the start of the step, rad s$^{-1}$, `(JSON)`; set by [[hpoint.f#HPOINT|`HPOINT`]] and [[starin.f#STARIN|`STARIN`]]; read by [[wtime.f#WTIME|`WTIME`]] (the time step), [[checkj.f#CHECKJ|`CHECKJ`]], [[getw.f#GETW|`GETW`]] and `HPOINT`. *Name:* W ($\Omega$) OLD.

## OP95INTERP_MOD

The interpolation stencil and weights for the OPAL 1995 opacity tables, computed by [[getopal95.f#GETOPAL95|`GETOPAL95`]] for the current $\rho$, $T$, $X$, $Z$ and applied by [[op952d.f#OP952D|`OP952D`]], [[op953d.f#OP953D|`OP953D`]] and [[op954d.f#OP954D|`OP954D`]].

- **`bd`**: the four-point weights in $R = \rho/T_6^3$ for each of the four temperatures, `(4,4)`; set by [[getopal95.f#GETOPAL95|`GETOPAL95`]] (through [[interp.f#INTERP|`INTERP`]]).
- **`bdd`**: `INTERP`'s weights for the derivative in $R$, `(4,4)`; set by [[getopal95.f#GETOPAL95|`GETOPAL95`]].
- **`bt`**: the four-point weights in $T$, `(4)`; set by [[getopal95.f#GETOPAL95|`GETOPAL95`]] (through `INTERP`).
- **`btt`**: `INTERP`'s weights for the derivative in $T$, `(4)`; set by [[getopal95.f#GETOPAL95|`GETOPAL95`]].
- **`bx`**: the four-point weights in $X$ for each of the four $Z$, `(4,4)`; set by [[getopal95.f#GETOPAL95|`GETOPAL95`]] (through [[intrp2.f#INTRP2|`INTRP2`]]).
- **`bz`**: the four-point weights in $Z$, `(4)`; set by [[getopal95.f#GETOPAL95|`GETOPAL95`]] (through `INTRP2`).
- **`jd`**: the first table index of the stencil in $R$ for each of the four temperatures, `(4)`, initially 1; set by [[getopal95.f#GETOPAL95|`GETOPAL95`]].
- **`jt`**: the first table index of the stencil in $T$, initially 1; set by [[getopal95.f#GETOPAL95|`GETOPAL95`]].
- **`jx`**: the first table index of the stencil in $X$ for each of the four $Z$, `(4,4)`, initially 1; set by [[getopal95.f#GETOPAL95|`GETOPAL95`]].
- **`jz`**: the first table index of the stencil in $Z$, initially 1; set by [[getopal95.f#GETOPAL95|`GETOPAL95`]].
- **`lexh`**: whether to extrapolate above the table in $R$ (the empty high-density corner), for each of the four temperatures, `(4)`; set by [[getopal95.f#GETOPAL95|`GETOPAL95`]]. *Name:* L (logical), EXtrapolate High.
- **`lexth`**: whether to extrapolate above the table in $R$ at all; set by [[getopal95.f#GETOPAL95|`GETOPAL95`]]. *Name:* L (logical), EXTrapolate High.
- **`lextl`**: whether to extrapolate below the table in $R$; set by [[getopal95.f#GETOPAL95|`GETOPAL95`]]. *Name:* L (logical), EXTrapolate Low.
- **`rho_t63l`**: $\log R = \log\rho - 3(\log T - 6)$, the table's density variable; set by [[getopal95.f#GETOPAL95|`GETOPAL95`]]. *Name:* RHO over $T_6^3$, Log (renamed from `RL` of `COMMON/OP95EXT/`).
- **`rho_t63ll`**: the table's lowest $\log R$, used in place of `RHO_T63L` below the table; set by [[getopal95.f#GETOPAL95|`GETOPAL95`]]. *Name:* `RHO_T63L`, Lowest (renamed from `RLL`).
- **`rlh`**: the table's upper edge in $\log R$ at each of the four temperatures, from which the extrapolation is linear, `(4)`; set by [[getopal95.f#GETOPAL95|`GETOPAL95`]].

## OVRTRN_MOD

The convective overturn time and the photospheric pressure at the start and end of a step, and the fraction of the step reached, for the wind laws and the rotational mixing.

- **`fracstep`**: the fraction $f$ of the step at which the wind is evaluated, $\tau = \tau_0 + f(\tau_1-\tau_0)$; set to 0.5 by [[starin.f#STARIN|`STARIN`]] and by [[getw.f#GETW|`GETW`]] (which also sets it to the fraction reached in its substeps). *Name:* FRACtion of the STEP.
- **`pphot`**: $\log P$ at the photosphere (cgs), at the end of the step; set by [[envint.f#ENVINT|`ENVINT`]] (0 first by [[gettau.f#GETTAU|`GETTAU`]]); read by [[amcalc.f#AMCALC|`AMCALC`]] and [[wrtout.f#WRTOUT|`WRTOUT`]]. *Name:* P (pressure), PHOTosphere.
- **`pphot0`**: `PPHOT` at the start of the step ($\log P$); copied by [[starin.f#STARIN|`STARIN`]] and [[wrtout.f#WRTOUT|`WRTOUT`]].
- **`taucz`**: the convective overturn time $\tau_\mathrm{cz}$ of the surface convection zone, in s (not a logarithm), at the end of the step; computed by [[taucal.f#TAUCAL|`TAUCAL`]], [[tauint.f#TAUINT|`TAUINT`]] or [[tauintnew.f#TAUINTNEW|`TAUINTNEW`]], 0 without a convective envelope. *Name:* $\tau$, Convection Zone.
- **`taucz0`**: `TAUCZ` at the start of the step, s; copied by [[starin.f#STARIN|`STARIN`]] and [[wrtout.f#WRTOUT|`WRTOUT`]].

## PREVCZ_MOD

The state of the surface convection zone and of light-element burning, carried from one step to the next for [[liburn.f#LIBURN|`LIBURN`]] and [[liburn2.f#LIBURN2|`LIBURN2`]].

- **`bbe9old`**: the natural logarithm of the mass-averaged ⁹Be burning rate in the convection zone (s$^{-1}$) at the end of the previous step; stored by [[liburn.f#LIBURN|`LIBURN`]], and reused as the next step's starting rate while `LBLIOLD` is set. *Name:* B (burning rate), BE9, OLD.
- **`bli6old`**: as `BBE9OLD`, for ⁶Li.
- **`bli7old`**: as `BBE9OLD`, for ⁷Li.
- **`lbliold`**: true when `BLI6OLD`, `BLI7OLD` and `BBE9OLD` hold `LIBURN`'s end-of-step rates (`LOGICAL*4`, initially `.FALSE.`); set by [[liburn.f#LIBURN|`LIBURN`]], cleared by `LIBURN` when it skips the zone, by [[liburn2.f#LIBURN2|`LIBURN2`]] and by the [[main.f#(file level)|main program]] at each kind card (since `7be4133`, in place of the test `BLI6OLD` ≤ 0, which the logarithms of small rates always passed). *Name:* L (logical), BLI OLD.
- **`jenvos`**: the shell of the envelope's base at the end of the step, used as the next step's starting `JENV0`; stored by [[liburn.f#LIBURN|`LIBURN`]], [[liburn2.f#LIBURN2|`LIBURN2`]]. *Name:* `JENV` + OS (old step).
- **`rbase0`**: the radius of the base of the convection zone (with overshoot) at the start of the step, cm (not a logarithm); computed by [[liburn.f#LIBURN|`LIBURN`]], [[liburn2.f#LIBURN2|`LIBURN2`]] when 0, which store the step's ending base in it; reset to 0 by the [[main.f#(file level)|main program]] when `LEXCOM` is set.

## PUALPHA_MOD

Three mixing-length quantities at the current point, for the pulsation output ("DBG 7/95").

- **`alfmlt`**: a mixing-length quantity for the envelope's pulsation output; set to 0 on every entry to [[tpgrad.f#TPGRAD|`TPGRAD`]] and computed nowhere; written by [[envint.f#ENVINT|`ENVINT`]] (`IPVER` = 3). *What was it meant to hold: the $\alpha$ of the mixing-length theory at the point?*
- **`cmxmlt`**: as `ALFMLT`, always 0. *What was it meant to hold?*
- **`phmlt`**: as `ALFMLT`, always 0. *What was it meant to hold?*

## PULSE1_MOD

The thermodynamic and opacity derivatives at every shell of the interior, stored for the pulsation output, and the switch that makes the envelope routines keep theirs.

- **`lpumod`**: whether the envelope routines save their point's values in [[pulse2_mod.f#PULSE2_MOD|`PULSE2_MOD`]]; set by [[envint.f#ENVINT|`ENVINT`]] to `LPULPT .AND. LPRT`; read by [[qenv.f#QENV|`QENV`]] and [[qatm.f#QATM|`QATM`]].
- **`pemu`**: `EMU` $= \mu_e^{-1}$ at each shell, `(JSON)`; stored by [[coefft.f#COEFFT|`COEFFT`]] when `LPULSE` is set; written by [[wrtmod.f#WRTMOD|`WRTMOD`]].
- **`pqcp`**: $c_P$ (`QCP`) at each shell, erg g$^{-1}$ K$^{-1}$, `(JSON)`; stored by [[coefft.f#COEFFT|`COEFFT`]] when `LPULSE` is set.
- **`pqdp`**: $\partial\ln\rho/\partial\ln P$ (`QDP`) at each shell, `(JSON)`; stored by [[coefft.f#COEFFT|`COEFFT`]] always (for `GAM1` and the stored model, "JVS 01/11").
- **`pqdt`**: $\partial\ln\rho/\partial\ln T$ (`QDT`) at each shell, `(JSON)`; stored by [[coefft.f#COEFFT|`COEFFT`]] always; also written to the stored model by [[stitch.f#STITCH|`STITCH`]].
- **`pqed`**: the energy generation's $\partial\ln\epsilon/\partial\ln\rho$ (`QED`) at each shell, `(JSON)`; stored by [[coefft.f#COEFFT|`COEFFT`]] when `LPULSE` is set.
- **`pqet`**: the energy generation's $\partial\ln\epsilon/\partial\ln T$ (`QET`) at each shell, `(JSON)`; stored by [[coefft.f#COEFFT|`COEFFT`]] when `LPULSE` is set.
- **`pqod`**: the opacity's $\partial\ln\kappa/\partial\ln\rho$ (`QOD`) at each shell, `(JSON)`; stored by [[coefft.f#COEFFT|`COEFFT`]] when `LPULSE` is set.
- **`pqot`**: the opacity's $\partial\ln\kappa/\partial\ln T$ (`QOT`) at each shell, `(JSON)`; stored by [[coefft.f#COEFFT|`COEFFT`]] when `LPULSE` is set.
- **`prmu`**: `RMU` $=\mathcal{R}/\mu$ at each shell, erg g$^{-1}$ K$^{-1}$, `(JSON)`; stored by [[coefft.f#COEFFT|`COEFFT`]] when `LPULSE` is set.

## PULSE2_MOD

The physics at the current point of the envelope or atmosphere integration, saved by [[qenv.f#QENV|`QENV`]] and [[qatm.f#QATM|`QATM`]] for [[envint.f#ENVINT|`ENVINT`]] to write in the envelope's pulsation output. All are scalars, set when `LSAVE` or `LPUMOD` is on.

- **`qd`**: $\rho$ at the point, g cm$^{-3}$ (not a logarithm).
- **`qdel`**: $\nabla$ at the point.
- **`qdela`**: $\nabla_\mathrm{ad}$ at the point.
- **`qdl`**: $\log\rho$ at the point.
- **`qemu`**: `EMU` $=\mu_e^{-1}$ at the point.
- **`qfs`**: the mass fraction $m/M$ at the point (`QENV`: $10^{\,\log m - \log M}$); set to 1 by `ENVINT` at the first point.
- **`qo`**: the opacity $\kappa$ at the point, cm$^2$ g$^{-1}$ (not a logarithm).
- **`qol`**: $\log\kappa$ at the point; read nowhere.
- **`qp`**: $P$ at the point, dyn cm$^{-2}$ (not a logarithm); also overwritten by [[coefft.f#COEFFT|`COEFFT`]], whose Henyey coefficient of the same name is this variable.
- **`qpl`**: $\log P$ at the point.
- **`qqcp`**: $c_P$ at the point, erg g$^{-1}$ K$^{-1}$; `QENV` sets it always.
- **`qqdp`**: $\partial\ln\rho/\partial\ln P$ at the point; `QENV` sets it always.
- **`qqdt`**: $\partial\ln\rho/\partial\ln T$ at the point; `QENV` sets it always.
- **`qqed`**: the energy generation's $\partial\ln\epsilon/\partial\ln\rho$; always set to 0 (by `QENV`, `QATM`, `ENVINT`).
- **`qqet`**: the energy generation's $\partial\ln\epsilon/\partial\ln T$; set to 0 (by `QENV`, `QATM`, `ENVINT`).
- **`qqod`**: the opacity's $\partial\ln\kappa/\partial\ln\rho$ at the point.
- **`qqot`**: the opacity's $\partial\ln\kappa/\partial\ln T$ at the point.
- **`qrmu`**: `RMU` $=\mathcal{R}/\mu$ at the point.
- **`qt`**: $T$ at the point, K (not a logarithm); also overwritten by [[coefft.f#COEFFT|`COEFFT`]] (a Henyey coefficient of the same name).
- **`qtl`**: $\log T$ at the point; also overwritten by [[coefft.f#COEFFT|`COEFFT`]] (a Henyey coefficient of the same name).

## QENVMIX_MOD

Relays the mixing-length parameter from [[envint.f#ENVINT|`ENVINT`]] to [[qenv.f#QENV|`QENV`]], whose argument list cannot change.

- **`cmixlq`**: the mixing-length parameter $\alpha$; set to `ENVINT`'s argument `CMIXL` on every entry; read by [[qenv.f#QENV|`QENV`]], which passes it to [[tpgrad.f#TPGRAD|`TPGRAD`]]. *Name:* `CMIXL` + Q for `QENV`.

## QUADD_MOD

Terms of the potential of a rotating star at each shell, and the quadrupole correction factor of the meridional circulation.

- **`phidis`**: the distortion term of the potential, $\tfrac{4\pi}{3}\,\mathtt{AINT}/r_\phi^3$, `(JSON)`; computed by [[fpft.f#FPFT|`FPFT`]]; read by no routine. *Name:* $\Phi$, DIStortion.
- **`phirot`**: the rotational term of the potential, $\Omega^2 r_\phi^2$, erg g$^{-1}$, `(JSON)`; computed by [[fpft.f#FPFT|`FPFT`]]; read by no routine. *Name:* $\Phi$, ROTation.
- **`phisp`**: the spherical potential $Gm/r_\phi$, erg g$^{-1}$, `(JSON)`; computed by [[fpft.f#FPFT|`FPFT`]]; read by no routine. *Name:* $\Phi$, SPherical.
- **`rat`**: the ratio of the corrected to the classical Eddington–Sweet circulation velocity (the quadrupole term, "as per Zahn (1992)"), `(JSON)`; set by [[vcirc.f#VCIRC|`VCIRC`]] from `QUAD` and `GG`; read by `VCIRC` and written by [[checkj.f#CHECKJ|`CHECKJ`]]. *Name:* RATio.

## QUADRU_MOD

The quadrupole moment of a rotating star's potential at each shell and the gravity it goes with.

- **`gg`**: the local gravity `HG` that [[getqua.f#GETQUA|`GETQUA`]] used, cm s$^{-2}$, `(JSON)`; set by `GETQUA`; read by [[vcirc.f#VCIRC|`VCIRC`]].
- **`quad`**: the quadrupole moment, the solution `U` of [[getqua.f#GETQUA|`GETQUA`]]'s tridiagonal system (0 at the centre, varying as $r^{-4}$ beyond the surface), `(JSON)`; read by [[vcirc.f#VCIRC|`VCIRC`]] and, at the surface, printed by [[getw.f#GETW|`GETW`]]. *Units not stated: in cgs as a potential term (erg g$^{-1}$)?*

## ROTDER_MOD

Three quantities at each shell, passed from the structure equations ([[coefft.f#COEFFT|`COEFFT`]]) to the setup of rotational mixing ([[setupv.f#SETUPV|`SETUPV`]]).

- **`fracnuc`**: the nuclear share of the energy generation, $(\epsilon_\mathrm{tot}-\epsilon_\nu)/\epsilon_\mathrm{tot}$ (0 when $\epsilon_\mathrm{tot}\le0$), `(JSON)`; stored by [[coefft.f#COEFFT|`COEFFT`]] when `LROT` is set. *Name:* FRACtion NUClear.
- **`sqet`**: the energy generation's $\partial\ln\epsilon/\partial\ln T$ (`QET`), `(JSON)`; stored by [[coefft.f#COEFFT|`COEFFT`]] when `LROT` is set. *Name:* S (stored) + `QET`.
- **`sqot`**: the opacity's $\partial\ln\kappa/\partial\ln T$ (`QOT`), `(JSON)`; stored by [[coefft.f#COEFFT|`COEFFT`]] when `LROT` is set. *Name:* S (stored) + `QOT`.

## ROTEN_MOD

The change of rotational kinetic energy at each shell over the step, a term of the energy equation.

- **`derot`**: $\Delta t\,(E_\mathrm{rot}-E_\mathrm{rot,old})/\Delta m$ at each shell ("7/92"), from `HKEROT`, `HKEROTO` and `HS2`, `(JSON)`; set by [[coefft.f#COEFFT|`COEFFT`]] when `LROT` is set and subtracted from the luminosity equation; written by [[putstore.f#PUTSTORE|`PUTSTORE`]] and [[stitch.f#STITCH|`STITCH`]]. *Name:* Delta E ROTational.

## RUNLOOP_MOD

The state of the run loop that is not in the namelist: for each of up to 50 runs (kind cards), its kind, its rescaling targets and its stop switches, indexed by the run `NK`.

- **`iresca`**: the run's kind, 1 evolve, 2 rescale, 3 rescale and evolve, `(50)`; copied by [[parmin.f#PARMIN|`PARMIN`]] from the namelist's `KINDRN`, reset to 1 by [[setcal.f#SETCAL|`SETCAL`]] and [[setscal.f#SETSCAL|`SETSCAL`]].
- **`lendag`**: whether the run evolves until a stop condition (the age `ENDAGE`, or a central D, X or Y), `(50)`; set by [[parmin.f#PARMIN|`PARMIN`]] and by the calibrations. *Name:* L (logical), END AGe.
- **`lsetdt`**: whether the run takes a fixed time step (`SETDT` > 0), `(50)`; set by [[parmin.f#PARMIN|`PARMIN`]], `SETCAL`, `SETSCAL`. *Name:* L (logical), SET DT.
- **`rescal`**: the rescaling targets, in order the mass ($M_\odot$), $X$, $Z$ and the core mass ($M_\odot$), `(4,50)`; copied by [[parmin.f#PARMIN|`PARMIN`]] from `RSCLM`, `RSCLX`, `RSCLZ`, `RSCLCM` (a target is applied when positive), changed by the calibrations; applied by [[rscale.f#RSCALE|`RSCALE`]].

## SCRTCH_MOD

The local physics of the interior at each shell, as computed in the last pass of the structure equations, stored by [[coefft.f#COEFFT|`COEFFT`]] (and in part again by [[physic.f#PHYSIC|`PHYSIC`]]) for mixing, burning, regridding and output.

- **`locons`**: whether conduction dominates the opacity (`LOCOND`), `(JSON)`; set by [[coefft.f#COEFFT|`COEFFT`]]; read by no routine.
- **`sbeta`**: $\beta = P_\mathrm{gas}/P$, `(JSON)`; stored by [[coefft.f#COEFFT|`COEFFT`]] for the stored model.
- **`scp`**: $c_P$, erg g$^{-1}$ K$^{-1}$, `(JSON)`; stored by [[coefft.f#COEFFT|`COEFFT`]] for the stored model.
- **`sdel`**: $\nabla_\mathrm{rad}$, $\nabla$, $\nabla_\mathrm{ad}$, `(3,JSON)`; stored by [[coefft.f#COEFFT|`COEFFT`]] and [[physic.f#PHYSIC|`PHYSIC`]]; [[rotmix.f#ROTMIX|`ROTMIX`]] replaces `SDEL(2,·)` for a while.
- **`seg`**: the five nuclear terms `EG(1)`…`EG(5)` as fractions of `SESUM`, then the neutrino term $\epsilon_\nu$ and the gravitational term $\epsilon_\mathrm{grav}$ (erg g$^{-1}$ s$^{-1}$), `(7,JSON)`; stored by [[coefft.f#COEFFT|`COEFFT`]].
- **`sesum`**: the nuclear energy generation $\epsilon_\mathrm{nuc}$, the sum of `EG(1)`…`EG(5)` (0 below `TCUT(1)`), erg g$^{-1}$ s$^{-1}$, `(JSON)`; stored by [[coefft.f#COEFFT|`COEFFT`]].
- **`seta`**: the degeneracy parameter $\eta$, `(JSON)`; stored by [[coefft.f#COEFFT|`COEFFT`]] for the stored model.
- **`sfxion`**: the ionization fractions of H$^+$, He$^+$ and He$^{++}$ (`FXION`), `(3,JSON)`; stored by [[coefft.f#COEFFT|`COEFFT`]] for the stored model.
- **`so`**: the opacity $\kappa$ (not a logarithm), cm$^2$ g$^{-1}$, `(JSON)`; stored by [[coefft.f#COEFFT|`COEFFT`]] and [[physic.f#PHYSIC|`PHYSIC`]].
- **`svel`**: the convective velocity, cm s$^{-1}$, `(JSON)`; stored by [[coefft.f#COEFFT|`COEFFT`]] and [[physic.f#PHYSIC|`PHYSIC`]].

## SCVEOS_MOD

The tables of the SCV equation of state ("MHP 5/97"): pure hydrogen, pure helium and the metals as read, the table built from them for the envelope's mixture, and the search indices of the last interpolation.

- **`idp`**: the first index in pressure of the four-point stencil, kept between calls as the start of the next search; set and read by [[eqscve.f#EQSCVE|`EQSCVE`]], [[eqscvg.f#EQSCVG|`EQSCVG`]] and [[setscv.f#SETSCV|`SETSCV`]].
- **`idtscv`**: the first index in temperature of the four-point stencil, kept between calls; set and read by `EQSCVE`, `EQSCVG`, `SETSCV`. *Name:* `IDT` (index in T) + SCV, renamed from `IDT` (10/9/26).
- **`nps`**: the number of pressures per temperature, 76; a `PRIVATE` parameter (the importing files declare their own). *Name:* Number of Pressures, SCV.
- **`nptsx`**: the number of pressure points at each temperature, `(NTS)`; read by [[setups.f#SETUPS|`SETUPS`]] from the hydrogen table. *Name:* Number of PoinTS, X (hydrogen).
- **`nts`**: the number of temperatures, 63; a `PRIVATE` parameter. *Name:* Number of Temperatures, SCV.
- **`smix`**: the entropy of mixing of hydrogen and helium, `(NTS,NPS)`; computed by [[setscv.f#SETSCV|`SETSCV`]]; read by `SETSCV` and [[eqscvg.f#EQSCVG|`EQSCVG`]]. *Units not stated: erg g$^{-1}$ K$^{-1}$, or per unit of $k/m_\mathrm{H}$?*
- **`tablenv`**: the table for the envelope's mixture ($\log P$, $\log\rho$, the derivatives, $c_P$, $\mathrm{d}U/\mathrm{d}T$, …), `(NTS,NPS,12)`; built by [[setscv.f#SETSCV|`SETSCV`]]; read by `SETSCV`, [[eqscve.f#EQSCVE|`EQSCVE`]], [[eqscvg.f#EQSCVG|`EQSCVG`]]. *Name:* TABLE, ENVelope.
- **`tablex`**: the hydrogen table, 11 columns as read (the first $\log P$) and column 12 $\mathrm{d}U/\mathrm{d}T$ added by [[setscv.f#SETSCV|`SETSCV`]], `(NTS,NPS,12)`; read by [[setups.f#SETUPS|`SETUPS`]]. *Name:* TABLE, X (hydrogen).
- **`tabley`**: the helium table, laid out as `TABLEX`, `(NTS,NPS,12)`; read by [[setups.f#SETUPS|`SETUPS`]]. *Name:* TABLE, Y (helium).
- **`tablez`**: the metals' table, `(NTS,NPS,13)`; read by [[setups.f#SETUPS|`SETUPS`]]. *Name:* TABLE, Z (metals). *What do its 13 columns hold?*
- **`tlogx`**: the tables' $\log T$ values, `(NTS)`; read by [[setups.f#SETUPS|`SETUPS`]] from the hydrogen table. *Name:* T, LOG, X (hydrogen table).

## SOUND_MOD

The adiabatic exponent $\Gamma_1$ at each shell and the switch for the sound-speed output ("MHP 7/96 … for solar model").

- **`gam1`**: $\Gamma_1 = \chi_\rho\,c_P/c_V$, with $\chi_\rho = 1/(\partial\ln\rho/\partial\ln P)$, `(JSON)`; computed by [[coefft.f#COEFFT|`COEFFT`]] at every shell; read by [[wrtmod.f#WRTMOD|`WRTMOD`]], written by [[putstore.f#PUTSTORE|`PUTSTORE`]] and [[stitch.f#STITCH|`STITCH`]]. *Name:* $\Gamma_1$.
- **`lsound`**: whether to write the sound-speed output; set by the [[main.f#(file level)|main program]], true at a run's last model; read by [[wrtmod.f#WRTMOD|`WRTMOD`]].

## SPLIN_MOD

Work arrays of the interpolations by [[osplin.f#OSPLIN|`OSPLIN`]] between the model's grid and the even grid in $\chi$ of rotational mixing; scratch space, passing no value between routines.

- **`xtab`**: the abscissas of the table to interpolate, `(JSON)`; filled by each user ([[eq2mod.f#EQ2MOD|`EQ2MOD`]], [[mixcom.f#MIXCOM|`MIXCOM`]], [[mixgrid.f#MIXGRID|`MIXGRID`]], [[rotgrid.f#ROTGRID|`ROTGRID`]]). *Name:* X, TABle.
- **`xval`**: the abscissas at which to evaluate, `(JSON)`; filled by each user. *Name:* X, VALues.
- **`ytab`**: the ordinates of the table, `(JSON)`; filled by each user. *Name:* Y, TABle.
- **`yval`**: the interpolated values returned by `OSPLIN`, `(JSON)`; read by each user. *Name:* Y, VALues.

## TAUKH_MOD

Factors at each interface of the rotating model, set by [[setupv.f#SETUPV|`SETUPV`]] once per step for [[vcirc.f#VCIRC|`VCIRC`]]'s circulation velocities (the name, from "Kelvin–Helmholtz," is older than its content). Below, at the interface: $m$ the mass, $\rho$, $g$, $L/m$, $\eta = \tfrac23 r^3/(Gm)$ (`SETUPV`'s local `ETA`), $\Delta\nabla = \nabla_\mathrm{ad}-\nabla$ (floored) and $F = P/(g\,\Delta\nabla\,c_P\,\rho\,T)$.

- **`fact6`**: the term of the Eddington–Sweet velocity in the derivative of $\Omega^2 r^2$, $-(\nabla_\mathrm{ad}/g)(L/m)/(4\pi G\rho r)$, `(JSON)`; read by `VCIRC`.
- **`fes1`**: the Zahn-type term $2\eta F\,(L/m - \epsilon)$, `(JSON)`; read by `SETUPV` and `VCIRC`. *Name:* F (factor), ES (Eddington–Sweet), 1.
- **`fes2`**: the Zahn-type term $-\eta F\,(L/m)/(\pi G\rho)$, `(JSON)`; read by `SETUPV` and `VCIRC`. *Name:* F, ES, 2.
- **`fes3`**: the Zahn-type term $\tfrac13 F\,(L/m)\,r/(\pi G\rho)$, `(JSON)`; read by `VCIRC`. *Name:* F, ES, 3.
- **`fgsfj`**: the factor $|2\eta F\,(L/m)\,H_T|\,r$ of an earlier form of the Goldreich–Schubert–Fricke velocity, `(JSON)`; used only in `VCIRC`'s commented-out lines. *Name:* F, GSF, J.
- **`fgsfk`**: the factor $8H_P\,\eta/\Delta\nabla$ of the Goldreich–Schubert–Fricke velocity, `(JSON)`; read by `VCIRC`. *Name:* F, GSF, K.

## TEMP2_MOD

The velocities of rotational mixing at each interface, computed by [[vcirc.f#VCIRC|`VCIRC`]] and turned into diffusion coefficients by [[codiff.f#CODIFF|`CODIFF`]].

- **`hle`**: a length scale ("characteristic velocity length scales," CODIFF's comment), `(JSON)`; set to 0 at every interface by [[codiff.f#CODIFF|`CODIFF`]] (its assignments are commented out); written by [[checkj.f#CHECKJ|`CHECKJ`]] as "LENGTH."
- **`ves`**: the Eddington–Sweet circulation velocity, cm s$^{-1}$, `(JSON)`; set by [[vcirc.f#VCIRC|`VCIRC`]]; read by `CODIFF`, `CHECKJ`, [[putstore.f#PUTSTORE|`PUTSTORE`]], [[stitch.f#STITCH|`STITCH`]]. *Name:* V, Eddington–Sweet.
- **`ves0`**: the previous iteration's `VES`, `(JSON)`; saved by `VCIRC` from the second iteration on, which averages old and new.
- **`vgsf`**: the Goldreich–Schubert–Fricke velocity, cm s$^{-1}$, `(JSON)`; set by [[vcirc.f#VCIRC|`VCIRC`]]. *Name:* V, GSF.
- **`vgsf0`**: the previous iteration's `VGSF`, `(JSON)`; saved by `VCIRC`.
- **`vmu`**: the $\mu$-current velocity, `(JSON)`; set by [[vcirc.f#VCIRC|`VCIRC`]]; read by `CODIFF`, `CHECKJ`. *Name:* V, $\mu$.
- **`vss`**: the secular-shear velocity, cm s$^{-1}$, `(JSON)`; set by [[vcirc.f#VCIRC|`VCIRC`]]. *Name:* V, Secular Shear.
- **`vss0`**: the previous iteration's `VSS`, `(JSON)`; saved by `VCIRC`.

## TEMP_MOD

Physics at each shell for rotational mixing: specific heat, mean molecular weight, a density derivative, the radiative diffusivity and the viscosity; [[hpoint.f#HPOINT|`HPOINT`]] saves them as the start-of-step values and [[midmod.f#MIDMOD|`MIDMOD`]] interpolates.

- **`cp`**: $c_P$ (`QCP`), erg g$^{-1}$ K$^{-1}$, `(JSON)`; set by [[physic.f#PHYSIC|`PHYSIC`]]; read by [[viscos.f#VISCOS|`VISCOS`]].
- **`hamu`**: the mean molecular weight $\mu$ of a fully ionized gas, $\mu_\mathrm{ion}\mu_e/(\mu_\mathrm{ion}+\mu_e)$, `(JSON)`; set by [[physic.f#PHYSIC|`PHYSIC`]]; read by [[getw.f#GETW|`GETW`]].
- **`sqdt`**: $\partial\ln\rho/\partial\ln T$ (`QDT`), `(JSON)`; set by [[physic.f#PHYSIC|`PHYSIC`]]. *Name:* S (stored) + `QDT`.
- **`thdif`**: the radiative diffusivity $16\sigma T^3/(3\kappa\rho^2 c_P)$, cm$^2$ s$^{-1}$, `(JSON)`; set by [[viscos.f#VISCOS|`VISCOS`]]. *Name:* THermal DIFfusivity.
- **`visc`**: the kinematic viscosity, radiative plus molecular, cm$^2$ s$^{-1}$, `(JSON)`; set by [[viscos.f#VISCOS|`VISCOS`]]. *Name:* VISCosity.

## TRIDI_MOD

A tridiagonal system $a_i u_{i-1} + b_i u_i + c_i u_{i+1} = d_i$ and its solution, shared between the routines that set up the implicit steps of rotational mixing and those that solve them.

- **`a`**: the sub-diagonal $a_i$, `(JSON)`; set by [[dcoeft.f#DCOEFT|`DCOEFT`]], [[ccoeft.f#CCOEFT|`CCOEFT`]] and [[getqua.f#GETQUA|`GETQUA`]].
- **`b`**: the diagonal $b_i$, `(JSON)`; set like `A`.
- **`c`**: the super-diagonal $c_i$, `(JSON)`; set like `A`.
- **`d`**: the right-hand side $d_i$, `(JSON)`; set like `A`.
- **`gama`**: the Thomas algorithm's work array, `(JSON)`; set and read by the solvers ([[tridia.f#TRIDIA|`TRIDIA`]], [[ctridi.f#CTRIDI|`CTRIDI`]], `GETQUA`); `DCOEFT` also uses it as work space. *Name:* $\gamma$.
- **`u`**: the solution $u_i$, `(JSON)`; set by [[tridia.f#TRIDIA|`TRIDIA`]], [[ctridi.f#CTRIDI|`CTRIDI`]] and [[getqua.f#GETQUA|`GETQUA`]]; read by `TRIDIA`, [[mixcom.f#MIXCOM|`MIXCOM`]] and `GETQUA`.

## VFACT_MOD

Factors at each interface from which the circulation velocities and the stability criteria of rotational mixing are computed, set by [[setupv.f#SETUPV|`SETUPV`]] once per step and used by [[vcirc.f#VCIRC|`VCIRC`]] (symbols as in `TAUKH_MOD` above).

- **`fact1`**: $1/[(\partial\ln\rho/\partial\ln T)\,\max(\nabla_\mathrm{ad}-\nabla, 10^{-3})]$, of the Eddington–Sweet velocity `VES` = `FACT1`·`FACT2`·$\Omega^2$ ("Endal and Sofia paper II"), `(JSON)`; read by `VCIRC`, also for the $\mu$ currents.
- **`fact2`**: $(\nabla_\mathrm{ad}/g)\,\eta\,(\epsilon - L/m)$, the other factor of `VES`, `(JSON)`; read by `VCIRC`.
- **`fact3`**: $|H_T r|$, for the Goldreich–Schubert–Fricke velocity, `(JSON)`; read only in `VCIRC`'s commented-out lines.
- **`fact4`**: $\frac{r^2}{Gm\rho}(P - aT^4/3)/\sqrt g$, of the "fictitious $\mu$ currents" (Kippenhahn, IAU 66), `(JSON)`; read by `VCIRC`.
- **`fact5`**: the Richardson criterion of the secular shear with $\mu$ gradients, $\frac{\rho g^2}{P\,\Delta\ln P}\cdot\frac{p_r-1}{1+3p_r}$ with $p_r = aT^4/(3P)$, `(JSON)`; read by `VCIRC`.
- **`fact7`**: the terms of order $d\Omega/dr$ (Zahn and Maeder 1998), computed only with `LDIFAD`, `(JSON)`; read by `VCIRC`.
- **`fact8`**: a second term of order $d\Omega/dr$, always 0 (its formulas are commented out), `(JSON)`; read by `VCIRC`.

## ZLAOL_MOD

The LAOL89 opacity table for pure metals ("pure Z," "DBG 12/95"), as read by [[rdzlaol.f#RDZLAOL|`RDZLAOL`]], used at high $Z$ and $T$ when `LPUREZ` is set.

- **`numrhoz`**: the number of densities in the table (at most 104); read by [[rdzlaol.f#RDZLAOL|`RDZLAOL`]]. *Name:* NUMber of RHO, Z table.
- **`numtz`**: the number of temperatures in the table (at most 52); read by [[rdzlaol.f#RDZLAOL|`RDZLAOL`]]. *Name:* NUMber of T, Z table.
- **`zolaol`**: the opacity $\kappa$ at each density and temperature (not a logarithm; 0 where the table has no entry), `(104,52)`; read by [[rdzlaol.f#RDZLAOL|`RDZLAOL`]]. *Name:* Z, O (opacity), LAOL.
- **`zorho`**: the density grid $\rho$ (not a logarithm), `(104)`; read by [[rdzlaol.f#RDZLAOL|`RDZLAOL`]]. *Name:* Z, O, RHO.
- **`zot`**: the temperature grid, read as $T$ by [[rdzlaol.f#RDZLAOL|`RDZLAOL`]] and replaced by $\log T$ in place by [[zsulaol.f#ZSULAOL|`ZSULAOL`]], `(52)`. *Name:* Z, O, T.

## ZSLAOL_MOD

The density splines of the pure-metal LAOL89 opacity table, one natural cubic spline of $\log\kappa$ against $\log\rho$ per temperature, set by [[zsulaol.f#ZSULAOL|`ZSULAOL`]] and read by [[gtpurz.f#GTPURZ|`GTPURZ`]].

- **`numrsz`**: the number of nonzero entries at each temperature, or 0 when there are fewer than four (no spline), `(52)`. *Name:* NUMber of Rho, Spline, Z.
- **`zsdorl`**: the spline's second derivatives, from [[cspline.f#CSPLINE|`CSPLINE`]], `(104,52)`.
- **`zslaoll`**: $\log\kappa$ at the table's nonzero entries, `(104,52)`. *Name:* Z, Spline, LAOL, Log.
- **`zsrhol`**: $\log\rho$ at those entries, `(104,52)`. *Name:* Z, Spline, RHO, Log.
