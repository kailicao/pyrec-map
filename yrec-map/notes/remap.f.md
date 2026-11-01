## Explanation

**Purpose.** Translates newer, "more intuitively named" namelist parameters (MHP 6/2014) into the arrays the rest of the code uses: the nuclear cross sections and their energy derivatives, and the tolerances for the mesh and the time step.

**How it fits.**
- **Who calls it:** [[parmin.f#PARMIN|`PARMIN`]], after reading the namelists.
- **Inputs, through modules:** [[nmlbypass_mod.f#NMLBYPASS_MOD|`NMLBYPASS_MOD`]] (formerly `/NEWPARAM/`, `/NEWCROSS/` and `/XSECT/`: the new cross-section parameters, such as `S0_1_1` for p+p and `S0P_1_12` for the first derivative of p+C12, the switch `LNEWNUC`, the new tolerance names, such as `TOL_DM_MAX` and `TIME_DX_SHELL`, and the switches `LNEWVARS`, `LSTRUCT_TIME`); shared only with `PARMIN`, which reads them, and [[starin.f#STARIN|`STARIN`]], which uses none of them yet.
- **Outputs, through modules:**
  - [[cross_mod.f#CROSS_MOD|`CROSS_MOD`]]: `QS0E(8)`, `QQS0EE(8)`, `FC12`, `FO16`, and [[nmlpar_mod.f#NMLPAR_MOD|`NMLPAR_MOD`]]: `SSTANDARD(17)`, all read by [[rates.f#RATES|`RATES`]] and [[engeb.f#ENGEB|`ENGEB`]];
  - `NMLPAR_MOD`: `HPTTOL(12)`, the mesh tolerances, used by [[hpoint.f#HPOINT|`HPOINT`]] and others;
  - `NMLPAR_MOD`: `ATIME(14)`, the time-step limits, used by [[htimer.f#HTIMER|`HTIMER`]] and others;
  - `NMLPAR_MOD`: `DTWIND`, `DTDIF`, `LPTIME`.

**The method.**
1. **Defaults.** `QS0E`, `QQS0EE`, `FC12`, `FO16` are set to 1.
2. **Cross sections, when `LNEWNUC` is true.** `SSTANDARD` becomes the ratio of each new zero-energy S-factor to the reference value hard-coded here (`…_REF`, the values that `RATES` and `ENGEB` assume):
   $$\texttt{SSTANDARD}(j) = \frac{S_{0,j}}{S_{0,j}^{\mathrm{ref}}},\qquad f_{C12} = \frac{S_{0}^{\,15(p,\alpha)}}{6.75\times10^4},\qquad f_{O16} = \frac{S_0^{\,15(p,\gamma)}}{64}.$$
   The resonant helium-burning reactions (8, 10, 11, 12) and the unused ones (9, 13) are left at 1. The derivative factors are ratios of $S'/S$ (and $S''/S$) to those of Solar Fusion I (Adelberger et al. 1998), whose values are hard-coded (`QS0E_…_A98`, `QQS0EE_…_A98`, in b):
   $$\texttt{QS0E}(j) = \frac{S'_j/S_{0,j}}{\bigl(S'/S_0\bigr)_j^{\mathrm{A98}}},\qquad \texttt{QQS0EE}(j) = \frac{S''_j/S_{0,j}}{\bigl(S''/S_0\bigr)_j^{\mathrm{A98}}},$$
   set to 0 when $S_{0,j} \le 0$. `RATES` multiplies its $Q_2, Q_3$ terms by `QS0E` and its $Q_4, Q_5$ terms by `QQS0EE`.
3. **Tolerances, when `LNEWVARS` is true.** A one-to-one copy, with a comment on each: for example `HPTTOL(1)` = `TOL_DM_MIN` (minimum log mass spacing), `HPTTOL(11)` = `TOL_DP_CORE_MAX`, `ATIME(7)` = `TIME_DX_SHELL` (maximum fraction of X burned in a shell in a step), `ATIME(13)` = `TIME_MAX_DT_FRAC`.

**KC's changes.** The unused `DATA` values of the Adelberger reference S-factors were commented out, keeping only `S0_1_1_A98` and `S0_1_BE7P_A98` (KC 2025-05-31; those of reactions 2–7 are restored since `09c3b9b`, below); the members of `/NEWPARAM/` were reordered, `LSTRUCT_TIME` moved to just before `LNEWVARS` (KC 2025-05-30).

**From YREC's documentation.** [Physics Options](https://yrec.readthedocs.io/en/latest/namelist_physics.html) lists the parameters that `REMAP` copies, with these meanings (defaults from [[nmlbypass_mod.f#NMLBYPASS_MOD|`NMLBYPASS_MOD`]]); `REMAP` copies them only when `LNEWVARS` is true, and `LNEWNUC` likewise gates the S-factors.

| variable | default | goes to | meaning (documentation) |
| --- | --- | --- | --- |
| `TOL_DM_MIN` | 1.0D-8 | `HPTTOL(1)` | minimum mass spacing (matters most for thin outer fitting points) |
| `TOL_DM_MAX` | 0.08 | `HPTTOL(2)` | maximum log mass spacing (matters most in cores) |
| `FLAG_DX`, `FLAG_DZ` | 0.05, 0.05 | `HPTTOL(3)`, `(4)` | smallest jump in $X$, $Z$ kept as a discontinuity |
| `TOL_DX_MAX`, `TOL_DZ_MAX` | 1.0, 1.0 | `HPTTOL(5)`, `(6)` | legacy mesh spacing in $X$, $Z$ |
| `TOL_CZBASE_FINE_WIDTH` | 0.0 | `HPTTOL(7)` | width of the finely zoned region at the base of the convection zone (0.4 for red giants) |
| `TOL_DP_ENV_MAX` | 0.05 | `HPTTOL(8)` | maximum $\Delta\log P$ in the outer convection zone |
| `TOL_DL_MAX` | 0.02 | `HPTTOL(9)` | maximum spacing in $L/L_\mathrm{surf}$ (energy-generating regions) |
| `TOL_DP_CZBASE_MAX` | 0.05 | `HPTTOL(10)` | maximum $\Delta\log P$ at the base of the surface convection zone |
| `TOL_DP_CORE_MAX` | 0.05 | `HPTTOL(11)` | maximum $\Delta\log P$ below it (between the burning regions and that base) |
| `FLAG_DW` | 0.10 | `HPTTOL(12)` | smallest jump in $\Omega$ kept as a discontinuity |
| `TIME_CORE_MIN` | 1.0D-3 | `ATIME(1)` | central $X$ (or $Y$) below which shell-burning rather than core-burning limits apply |
| `TIME_DX_CORE_TOT`, `TIME_DX_CORE_FRAC` | 0.02, 0.5 | `ATIME(2)`, `(3)` | largest absolute and fractional $\Delta X$ per step in core hydrogen burning |
| `TIME_DY_CORE_TOT`, `TIME_DY_CORE_FRAC` | 0.02, 0.5 | `ATIME(4)`, `(5)` | the same for $Y$ in core helium burning (red clump, horizontal branch) |
| `TIME_DX_TOTAL`, `TIME_DX_SHELL` | 1.5D-3, 0.1 | `ATIME(6)`, `(7)` | hydrogen burned per step after the main sequence: total, and fractional in the shell |
| `TIME_DT`, `TIME_DP`, `TIME_DR`, `TIME_DL` | 0.02, 0.04, 0.02, 0.02 | `ATIME(8)`–`(11)` | largest local change of $T$, $P$, $R$, $L$ per step (pre-main sequence) |
| `TIME_DY_SHELL`, `TIME_DY_TOTAL` | 0.1, 1.5D-3 | `ATIME(12)`, `(14)` | the same for helium shells (AGB) |
| `TIME_MAX_DT_FRAC` | 1.5 | `ATIME(13)` | largest growth of the step from one model to the next |
| `LSTRUCT_TIME` | false | `LPTIME` | limit the step by structural changes; switched off once $L_\mathrm{grav} < 0$ (near the ZAMS) |
| `TIME_DW_GLOBAL`, `TIME_DW_MIX` | 0.08, 0.08 | `DTWIND`, `DTDIF` | largest $\Delta\Omega$ per model, and per mixing substep |

**Changed since `rp_1`.** The reference value `S0_1_16_REF` is now the double-precision `9.4D0` (it was `9.4E0`, a single-precision constant, about $4\times10^{-8}$ smaller), which changes `SSTANDARD(7)` in the same proportion; otherwise COMMON blocks to modules (`/NEWPARAM/` and `/NEWCROSS/` merged into `NMLBYPASS_MOD`; the tolerances, time-step limits and `SSTANDARD` into `NMLPAR_MOD`), `IMPLICIT NONE`.

**Changed since `09c3b9b`.** The derivative factors `QS0E(2)`–`QS0E(7)` and `QQS0EE(4)`, `QQS0EE(5)`, `QQS0EE(7)` are now normalized by each reaction's own A98 S-factor (`S0_3_3_A98`, `S0_3_4_A98`, `S0_1_12_A98`, `S0_1_13_A98`, `S0_1_14_A98`, `S0_1_16_A98`, whose `DATA` values, 5.4D3, 5.3D-1, 1.34D0, 7.6D0, 3.5D0 and 9.4D0 keV b, are restored) instead of p+p's `S0_1_1_A98`. Before, these factors came out of order $10^{-22}$, so with `LNEWNUC` the S′ and S″ terms of reactions 2–7 were dropped and the `S0P_…`, `S0PP_…` inputs had no effect; now they are of order 1, as intended. This settles former question 1; former questions 2–4 are now 1–3.

## Questions for the experts

1. **Units of the derivatives.** The comments give the reference S-factors in keV b and the first derivatives in b; is the user expected to give `S0P_…` in b as well, and `S0PP_…` in b keV$^{-1}$? The namelist documentation should say.
2. **"NRATES".** A comment says the derivatives are used "in ENGEB AND NRATES"; the routine is `RATES`.
3. **Both switches change other inputs silently.** With `LNEWNUC`, any `SSTANDARD` given in the namelist is overwritten; with `LNEWVARS`, `HPTTOL` and `ATIME` are. Is a message printed anywhere to warn a user who sets both?
4. **`LNEWVARS` listed as legacy.** The documentation presents the `TOL_…`, `FLAG_…` and `TIME_…` names as the mesh and time-step controls, but lists `LNEWVARS` ("use updated variable names for tolerances") and `LNEWNUC` under "Legacy options". Their default is false, so without `LNEWVARS = .TRUE.` in the namelist every one of these parameters is ignored and the old `HPTTOL`, `ATIME` values are used. Should the default become true (or the old vectors go), or should the documentation say that `LNEWVARS` must be set?

