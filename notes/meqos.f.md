## Explanation

**Purpose.** `MEQOS` is the interface to the Mihalas–Hummer–Däppen (MHD) equation of state ("implemented by YC March 7, 1990"): given $\log T$, $\log P$ and the composition, it returns the density and the thermodynamic quantities in the same form as the code's other EOS routines ([[eqstat.f#EQSTAT|`EQSTAT`]]).

**How it fits.**
- **Who calls it:** [[coefft.f#COEFFT|`COEFFT`]], [[envint.f#ENVINT|`ENVINT`]], [[physic.f#PHYSIC|`PHYSIC`]], [[qatm.f#QATM|`QATM`]], [[qenv.f#QENV|`QENV`]], [[starin.f#STARIN|`STARIN`]] and [[wrtout.f#WRTOUT|`WRTOUT`]], whenever the run uses the MHD tables (the switch `LMHD`, a namelist parameter of [[parmin.f#PARMIN|`PARMIN`]], default false). The callers do not check that the point lies inside the tables (see [[mhdpx.f|`mhdpx.f`]], question 1).
- **Inputs:** `T10` = $\log T$, `P10` = $\log P$, `XC` = $X$, `Z`.
- **Outputs (arguments):** $T$, $P$, $\log\rho$ and $\rho$, $\beta$ (`BETA`, `BETAI` = $1/\beta$, `BETA14` = $1-\beta$), the ionization fractions `FXION(3)`, `RMU`, `AMU`, `EMU`, the degeneracy `ETA`, the derivatives `QDT`, `QDP`, `QCP`, `DELA` and their second derivatives `QDTT`, `QDPT`, `QAT`, `QAP`, `QCPT`, `QCPP`.
- **Calls:** [[mhdpx.f#MHDPX|`MHDPX`]] (table interpolation, results in COMMON `MHDOUT`) and [[mu.f#MU|`MU`]] (mean molecular weights).
- **COMMON blocks:** `MHDOUT` (`VARMHD(25)`, the interpolated table variables, with `MHDPX`, `MHDPX1`), `LUOUT`, and declared but unused `COMP`, `CTLIM`, `CONST1`, `CONST2`, `CCOUT2`.

**The method.** With $v_k$ = `VARMHD(k)` (the table's variables; the meaning of each index comes from the MHD tables, not from this file), and $c$ = `CNVS` $= \log_{10}e$:

$$\log\rho = v_1,\quad \chi_\rho = v_4,\quad \chi_T = v_5,\quad Q_P = \frac{\partial\ln\rho}{\partial\ln P}\Big|_T = \frac{1}{\chi_\rho},\quad Q_T = \frac{\partial\ln\rho}{\partial\ln T}\Big|_P = -\frac{\chi_T}{\chi_\rho},$$

$$c_P = 10^{v_9},\quad \nabla_\mathrm{ad} = v_8,\quad \beta = 10^{v_{20} - v_2},\quad \eta = v_{18},\quad x_\mathrm{ion} = v_{14..16},\quad \frac{\mathcal{R}}{\mu} = \frac{10^{v_{20}}}{\rho T},$$

and the derivatives of $\log c_P$ and $\ln\nabla_\mathrm{ad}$ by the chain rule from $v_{10}$–$v_{13}$, e.g. $Q_{AP} = Q_P\,v_{10}\,c/\nabla_\mathrm{ad}$. Then it calls `MU` for $\mu$ and stops the run if the two values of $\mathcal{R}/\mu$ differ by more than $5\times10^{-7}$ relatively.

**KC's changes.** 2025-05-31: the unused arguments `LDERIV`, `LATMO`, `KSAHA` and the unused array `ATOMWT` removed (the callers were changed to match).

## Questions for the experts

1. **Which variables.** The meaning of each `VARMHD` index (e.g. whether $v_2$ is $\log P_\mathrm{tot}$ and $v_{20}$ $\log P_\mathrm{gas}$, so that $\beta = P_\mathrm{gas}/P$) is not documented in the code; a table of the 25 variables would help. Is `P10` the total or the gas pressure? `MHDPX`'s header says its argument is the gas pressure.
2. **Unreachable error code.** The lines after `RETURN` ("MHD TABLE FAIL") can never run (their label 999 is commented out). How are table failures reported now? (See `MHDPX1`, which returns silently.)
3. **A strict consistency stop.** The run stops if the table's $\mu$ and `MU`'s differ by $5\times10^{-7}$ relatively; could interpolation alone exceed that near table edges?
4. **Unused.** `IER` and five COMMON blocks.

### MEQOS

MHD EOS interface: table variables to the code's EOS outputs (above).
