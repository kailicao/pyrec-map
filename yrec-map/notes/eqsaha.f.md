## Explanation

**Purpose.** `EQSAHA` is the Yale equation of state for partially ionized gas: it solves the Saha equations for hydrogen, helium (two stages) and ten metals, and returns the density, the ionization fractions and the thermodynamic derivatives. The name "Prather EOS" in [[eqstat2.f#EQSTAT2|EQSTAT2]]'s comments refers to it.

**How it fits.**
- **Who calls it:** only `EQSTAT2`, below the temperature `TSCUT`. It is called even when the SCV tables are used, since "this EOS replaces the call to EQSAHA, except for derivative purposes"; [[eqscve.f#EQSCVE|EQSCVE]] then overwrites what it can.
- **Inputs:** `FX`, the number fractions of the twelve species (set by `EQSTAT2` from `FXENV` in `/COMP/`); `TL`, `PL`; `BETA` and its relatives; `AMU`; `LATMO` (skip the derivatives, for atmospheres); `LDERIV` (also compute second derivatives).
- **Outputs:** `D`, `DL`, `EMU`, `RMU` = $R(\mu_\mathrm{ion}^{-1}+\mu_e^{-1}) = \mathcal{R}/\mu$, the gas constant over the mean molecular weight, so that $P_\mathrm{gas} = \rho\,(\mathcal{R}/\mu)\,T$ (`AMU` $=\mu_\mathrm{ion}^{-1}$ and `EMU` $=\mu_e^{-1}$ are its two terms), `FXION` (H$^+$, He$^+$, He$^{++}$ fractions), `QDT`, `QDP`, `QCP`, `DELA` and, with `LDERIV`, their derivatives. `KSAHA` is the caller's iteration counter, to which this call adds its iterations.
- **Modules:** only `CONSTANTS_MOD` (with `CMKH` the constant term of the Saha equation) and `IOUNITS_MOD` (the unit `ISHORT`).

**The method.**
1. **Saha constants.** For each species $i$, with ionization temperature $\chi_i/k$ (`SAHAT`, in K: 59 630 for Na up to 250 200 for Ne; `SAHET0` = 285 270 and `SAHET1` = 631 370 for He and He$^+$) and a constant $u_i$ (`SAHAU`),
$$K_i = \frac{1}{\beta}\exp\!\left[\ln 10\,(u_i + 2.5\log T - \log P + C) - \frac{\chi_i}{kT}\right].$$
The species order is that of `ATOMW2` in `EQSTAT2`: Na, Al, Mg, Fe, Si, C, H, O, N, Ar, Ne, He. The list is in order of increasing ionization temperature. The loop stops at the first species whose exponent is below $-40$: that species and all later ones are treated as neutral (so hydrogen, seventh, counts as ionized only if `NZ0` ≥ 7, and `FXION(1)` is 0 otherwise). A species whose exponent is above $+40$ gets $K_i = 10^{16}$ (fully ionized) and is left out of the derivative sums.

    > **Question** ([[#L47-L49]]). **The constants $u_i$.** `SAHAU` has no comment; they are probably the logarithms of the partition-function ratios. Could their source be cited?
2. **Electron number.** With $E$ the electrons per atom (`E`) and $\epsilon = E/(1+E)$, the ionized fraction of species $i$ (the ten metals and hydrogen) is $x_i = K_i/(K_i + \epsilon)$, and charge balance reads
$$E = \sum_i f_i x_i + f_\mathrm{He}\,(x_1 + 2x_2),$$
with the helium fractions $x_1, x_2$ from their own Saha equations. The routine solves this coupled system by Newton iteration (at most 20 steps, tolerance $10^{-9}$), reducing the 3×3 Jacobian by hand; `E` and the helium fractions keep their values between calls as the next starting guess.

    > **Question** ([[#L94]]; [[#L186-L192]]). **No-convergence path.** After 20 iterations the routine writes "SAHA FAILURE" and continues with the unconverged $E$; the caller is not told. Is that acceptable, or should it be?

    > **Question** ([[#L53]]; [[#L55]]). **State between calls.** `E`, `SAHEX1` and `SAHEX2` persist between calls (`SAVE` and `DATA`). The result can then depend slightly on the order of calls (for example during the numerical derivatives in [[eqstat.f#EQSTAT|EQSTAT]]). Is that a concern at the tolerance used?
3. **Density:** $\mu_e^{-1} = E\,\mu_\mathrm{ion}^{-1}$ and $\rho = \beta P / [R(\mu_\mathrm{ion}^{-1} + \mu_e^{-1})T]$.
4. **Derivatives.** Differentiating the Saha system gives $\partial\ln E/\partial\ln T$ and $\partial\ln E/\partial\ln P$, then $Q_{\rho T}$, $Q_{\rho P}$, the energy derivative $\partial U/\partial T$ (including ionization energy), $c_P = \partial U/\partial T - (P/\rho T)Q_{\rho T}$ and $\nabla_\mathrm{ad} = -(P/\rho T)Q_{\rho T}/c_P$.

**What it leaves out.** The solver has no molecules (H$_2$), no H$^-$, no pressure ionization and no Coulomb terms, and treats the electrons as a classical gas. With the code's defaults (`LOPALE06` and `LSCV` false) it nevertheless gives the equation of state of every layer below `TSCUT`, including the cool, dense envelopes of M dwarfs and brown dwarfs (whether that is adequate there, where molecules and degeneracy would be expected to matter, is the question below). The documentation calls OPAL 2006 "strongly recommended," and 45 of the 51 test-suite runs set `LOPALE06` (47 set `LSCV`), so in practice this solver is used mainly outside those tables and for the second derivatives; whether the default should change is [[eqstat2.f#q4]].

> **Question** ([[nmlpar_mod.f#L122]]; [[nmlpar_mod.f#L258]]). **Low-mass stars with the default equation of state.** With `LOPALE06` and `LSCV` false, the cool, dense envelopes of M dwarfs and brown dwarfs get this solver, which has no molecules, no pressure ionization, and classical electrons. How large are the errors there, and should the default switch on the tables ([[eqstat2.f#q4]])?

**Changed since `rp_1`.** Declarations (COMMON blocks to modules, `IMPLICIT NONE`), and the constants `SAHAU` are now double-precision literals (`-.01D0`, …): before, they were single-precision values (relative errors below $10^{-7}$), so the Saha constants change very slightly.

### EQSAHA

Solves the Saha equations for 12 species and returns $\rho$, the ionization fractions, $c_P$, $\nabla_\mathrm{ad}$ and their derivatives (method above).
