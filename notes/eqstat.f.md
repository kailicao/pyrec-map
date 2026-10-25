## Explanation

**Purpose.** `EQSTAT` is the equation of state that the rest of YREC calls. Its header says it was added ("LLP 10-22-06") as a "new front end" so that the derivatives of the equation of state can be computed numerically, by calling the older routine, now [[eqstat2.f#EQSTAT2|EQSTAT2]], at neighbouring points. All the physics is in `EQSTAT2`.

**How it fits.**
- **Who calls it:** ten routines across the code: [[coefft.f#COEFFT|COEFFT]], [[envint.f#ENVINT|ENVINT]], [[hsubp.f#HSUBP|HSUBP]], [[massloss.f#MASSLOSS|MASSLOSS]], [[physic.f#PHYSIC|PHYSIC]], [[qatm.f#QATM|QATM]], [[qenv.f#QENV|QENV]], [[sconvec.f#SCONVEC|SCONVEC]], [[starin.f#STARIN|STARIN]] and [[wrtout.f#WRTOUT|WRTOUT]].
- **Inputs:** `TL`, `PL` ($\log_{10}$ of $T$ in K and $P$ in dyn cm$^{-2}$), `X`, `Z`, and the flags `LDERIV` (second derivatives wanted) and `LATMO` (atmosphere). `DL` serves as a starting guess.
- **What it calls:** only `EQSTAT2`.
- **Outputs:** those of `EQSTAT2`: `T`, `P`, `D`, `DL`, `BETA`, `FXION`, `RMU`, `AMU`, `EMU`, `ETA`, `QDT` $=\partial\ln\rho/\partial\ln T|_P$, `QDP` $=\partial\ln\rho/\partial\ln P|_T$, `QCP` ($c_P$), `DELA` ($\nabla_\mathrm{ad}$), and the derivatives `QDTT`, `QDTP`, `QAT`, `QAP`, `QCPT`, `QCPP`.
- **COMMON blocks:** it reads only `CLN` ($\ln 10$, from `/CONST1/`) and `LNumDeriv` (from `/OPALEOS/`, set in the `PHYSICS` namelist read by [[parmin.f#PARMIN|PARMIN]]). It declares the same blocks as `EQSTAT2` (`/COMP/`, `/CTLIM/`, `/DEBHU/`, `/SCVEOS/`, `/GRAVS3/`, …) without using them.

**The method.** If `LDERIV` and `LNumDeriv` are both set, `EQSTAT2` is called four times without derivatives, at $\log T \pm h_T$ and $\log P \pm h_P$, with $h_T = 3\times10^{-4}$ and $h_P = 1.5\times10^{-3}$ (the "approximate table intervals", 0.03 and 0.15, scaled down by 100: "empirically, scaling the intervals down by 100 seemed to work best"). Central differences give the second derivatives, for example
$$\frac{\partial Q_{\rho T}}{\partial\ln T} = \frac{Q_{\rho T}^{+} - Q_{\rho T}^{-}}{2h_T\ln 10},\qquad \frac{\partial\log c_P}{\partial\log T} = \frac{\log c_P^{+} - \log c_P^{-}}{2h_T},\qquad \frac{\partial\log\nabla_\mathrm{ad}}{\partial\log T} = \frac{\log\nabla_\mathrm{ad}^{+} - \log\nabla_\mathrm{ad}^{-}}{2h_T},$$
and the same in $\log P$. A last call at the point itself, without derivatives, gives the values; its derivative outputs go to dummy variables so they cannot overwrite the numerical ones. Otherwise `EQSTAT2` is called once, with analytic derivatives if `LDERIV` is set.

**KC's changes.** Unused arrays and DATA statements were commented out (2025-05-31), and the elements of `/OPALEOS/` were reordered (2025-05-30).

## Questions for the experts

1. **A typo that leaves a variable undefined.** The line `KSSAHAx = KSAHA` assigns a misspelled variable; the calls then pass `KSAHAx`, which is never set. `KSAHAx` is a saved local that only the four derivative calls increment and nothing reads, so no result changes; the caller's counter `KSAHA` just misses those iterations. Should it read `KSAHAx = KSAHA`?
2. **The step size.** The steps are 1/100 of an assumed table spacing of 0.15 in $\log P$ and 0.03 in $\log T$. EQSTAT2's own comment gives the SCV tables' spacing as 0.20 and 0.08. Was the step tested for each table `EQSTAT2` can use?
3. **Unused declarations.** Most COMMON blocks here are copies from `EQSTAT2` and are not used. Can they be removed?

### EQSTAT

Front end to `EQSTAT2`: second derivatives by central differences when `LNumDeriv` is set, otherwise analytic; always returns `EQSTAT2`'s values at the point.
