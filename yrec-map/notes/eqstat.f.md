## Explanation

**Purpose.** `EQSTAT` is the equation of state that the rest of YREC calls. Its header says it was added ("LLP 10-22-06") as a "new front end" so that the derivatives of the equation of state can be computed numerically, by calling the older routine, now [[eqstat2.f#EQSTAT2|EQSTAT2]], at neighbouring points. All the physics is in `EQSTAT2`.

**How it fits.**
- **Who calls it:** ten routines across the code: [[coefft.f#COEFFT|COEFFT]], [[envint.f#ENVINT|ENVINT]], [[hsubp.f#HSUBP|HSUBP]], [[massloss.f#MASSLOSS|MASSLOSS]], [[physic.f#PHYSIC|PHYSIC]], [[qatm.f#QATM|QATM]], [[qenv.f#QENV|QENV]], [[sconvec.f#SCONVEC|SCONVEC]], [[starin.f#STARIN|STARIN]] and [[wrtout.f#WRTOUT|WRTOUT]].
- **Inputs:** `TL`, `PL` ($\log_{10}$ of $T$ in K and $P$ in dyn cm$^{-2}$), `X`, `Z`, and the flags `LDERIV` (second derivatives wanted) and `LATMO` (atmosphere). `DL` serves as a starting guess.
- **What it calls:** only `EQSTAT2`.
- **Outputs:** those of `EQSTAT2`: `T`, `P`, `D`, `DL`, `BETA`, `FXION`, `RMU`, `AMU`, `EMU`, `ETA`, `QDT` $=\partial\ln\rho/\partial\ln T|_P$, `QDP` $=\partial\ln\rho/\partial\ln P|_T$, `QCP` ($c_P$), `DELA` ($\nabla_\mathrm{ad}$), and the derivatives `QDTT`, `QDTP`, `QAT`, `QAP`, `QCPT`, `QCPP`.
- **Modules:** it reads only `CLN` ($\ln 10$, from [[constants_mod.f#CONSTANTS_MOD|`CONSTANTS_MOD`]]) and `LNumDeriv` (from [[nmlpar_mod.f#NMLPAR_MOD|`NMLPAR_MOD`]], set in the `PHYSICS` namelist read by [[parmin.f#PARMIN|PARMIN]]).

**The method.** If `LDERIV` and `LNumDeriv` are both set, `EQSTAT2` is called four times without derivatives, at $\log T \pm h_T$ and $\log P \pm h_P$, with $h_T = 3\times10^{-4}$ and $h_P = 1.5\times10^{-3}$ (the "approximate table intervals," 0.03 and 0.15, scaled down by 100: "empirically, scaling the intervals down by 100 seemed to work best"). Central differences give the second derivatives, for example
$$\frac{\partial Q_{\rho T}}{\partial\ln T} = \frac{Q_{\rho T}^{+} - Q_{\rho T}^{-}}{2h_T\ln 10},\qquad \frac{\partial\log c_P}{\partial\log T} = \frac{\log c_P^{+} - \log c_P^{-}}{2h_T},\qquad \frac{\partial\log\nabla_\mathrm{ad}}{\partial\log T} = \frac{\log\nabla_\mathrm{ad}^{+} - \log\nabla_\mathrm{ad}^{-}}{2h_T},$$
and the same in $\log P$. A last call at the point itself, without derivatives, gives the values; its derivative outputs go to dummy variables so they cannot overwrite the numerical ones. Otherwise `EQSTAT2` is called once, with analytic derivatives if `LDERIV` is set. The second derivatives are needed because the Henyey method linearizes the structure equations in $\ln P$ and $\ln T$: [[tpgrad.f#TPGRAD|TPGRAD]] differentiates the temperature gradient (`QAT`, `QAP` $=\partial\ln\nabla_\mathrm{ad}/\partial\ln T, \partial\ln P$, and `QCPT`, `QDTT`, `QDTP` for the convective gradient), and [[coefft.f#COEFFT|COEFFT]] differentiates $\epsilon_\mathrm{grav}$, which contains $Q_{\rho T}$ and $\nabla_\mathrm{ad}$ (`QDTT`, `QDTP`, `QAT`, `QAP`). The symbols are in the overview's Notation: $Q_{\rho T}$ = `QDT` $= -\delta$ and $Q_{\rho P}$ = `QDP` $= \alpha$ in the notation of Kippenhahn, Weigert & Weiss.

> **Question** ([[#L96-L100]]; [[eqstat2.f#L192-L202]]). **The step size.** The steps are 1/100 of an assumed table spacing of 0.15 in $\log P$ and 0.03 in $\log T$. `EQSTAT2`'s own comment gives the SCV tables' spacing as 0.20 and 0.08. Was the step tested for each table `EQSTAT2` can use?

**From YREC's documentation.** [Microphysics in YREC](https://yrec.readthedocs.io/en/latest/microphysics.html): `LNUMDERIV` (default false) replaces YREC's semi-analytic EOS derivatives by numerical ones from the OPAL tables, at about three times the cost and with little effect on the solution.

**Changed since `rp_1`.** Declarations only: COMMON blocks to modules, `IMPLICIT NONE`; the unused COMMON blocks copied from `EQSTAT2` are gone, which settles the former question 3.

## Bugs, by priority

1. **(harmless in the runs)** **A misspelled counter.** ([[#L31]]; [[#L85]]; [[#L111-L113]]) The line `KSSAHAx = KSAHA` assigns a misspelled variable (declared as `KSSAHAX`, so `IMPLICIT NONE` does not flag it), and `KSSAHAX` is never read; the four derivative calls then pass `KSAHAx`, a saved local with no `DATA`, which is never set. `KSAHA` is only an iteration counter of [[eqsaha.f#EQSAHA|`EQSAHA`]] ([[eqsaha.f#L95]]), and `KSAHAx` is never copied back, so no result changes today: The caller's counter misses the derivative calls' iterations either way, and `KSAHAx` grows from an undefined start. Only with `LNumDeriv` (off by default, [[nmlpar_mod.f#L123]]).

    **A possible fix:**

    ```diff
    --- a/src/eqstat.f
    +++ b/src/eqstat.f
    @@ -28,7 +28,10 @@
          *       QAT1,QATX,QCP,QCP1,QCP2,QCPP,QCPP1,QCPPX,QCPT,QCPT1,QCPTX,
          *       QDP,QDP1,QDP2,QDT,QDT1,QDT2,QDTP,QDTP1,QDTPX,QDTT,QDTT1,
          *       QDTTX,RMU,T,TL,TLO,TTL,X,Z
    -      INTEGER KSAHA,KSAHAX,KSSAHAX
    +C 11/09/26 KC via Claude
    +C code changed to start the derivative calls' counter from KSAHA, as
    +C the misspelled KSSAHAX was meant to.
    +      INTEGER KSAHA,KSAHAX
           LOGICAL*4 LATMO,LATMOX,LDERIV,LDERIV2
     c
     c  Input Arguments: TL, PL, X, Z, LDERIV, LATMO
    @@ -82,7 +85,7 @@
           PLO = PL
           TLO = TL
           LATMOx = LATMO
    -      KSSAHAx = KSAHA
    +      KSAHAx = KSAHA
     
           IF(LDERIV .AND. LNumDeriv) THEN
     c Get Numerical Derivatives of Current EOS    LLP  8/5/07
    ```

    **Checked by running YREC** (Nov 9, 2026; a line added at each suspected path counted how often it was taken, the outputs otherwise unchanged). No YREC case sets `LNumDeriv`, so it was run in `testsuite/Test_m1p0feh+0p0GS98_base_TAMS` with `LNumDeriv` on, as `docs/source/microphysics.md` (line 33) offers. The path was taken 2,310,528 times, and in all but the first the derivative calls' counter `KSAHAx` differed from the caller's `KSAHA`: It grew to about $1.68\times10^{7}$, while `KSAHA` stayed between 0 and 18,758. With the page's fix, the `.track` and `.store` files are identical (728 models, ending at 9.86674 Gyr), as expected, since `KSAHAx` is never copied back. Intent: none found. The counter is wrong, but the results are not.

### EQSTAT

Front end to `EQSTAT2`: second derivatives by central differences when `LNumDeriv` is set, otherwise analytic; always returns `EQSTAT2`'s values at the point.
