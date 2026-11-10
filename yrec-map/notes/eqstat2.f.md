## Explanation

**Purpose.** `EQSTAT2` is the core of YREC's equation of state: it chooses among, and blends, the Yale Saha solver, the relativistic degenerate gas, the SCV tables and the OPAL 2006 table, depending on temperature, density and the run's settings. Its header calls it "the old EOS routine"; since 2006 the code calls it through [[eqstat.f#EQSTAT|EQSTAT]].

**How it fits.**
- **Who calls it:** `EQSTAT` (once or five times per call, see there) and [[calcad.f#CALCAD|CALCAD]] directly.
- **Inputs:** `TL`, `PL`, `X`, `Z`, `LDERIV`, `LATMO`; `DL` as a starting guess.
- **What it calls:** [[eqsaha.f#EQSAHA|EQSAHA]] (Saha ionization), [[eqscve.f#EQSCVE|EQSCVE]] (SCV tables), [[eqrelv.f#EQRELV|EQRELV]] (fully ionized, degenerate gas), and for OPAL [[oeqos06.f#OEQOS06|OEQOS06]] with [[eqbound06.f#EQBOUND06|EQBOUND06]] (the OPAL 1995 and 2001 tables, with `OEQOS`, `EQBOUND`, `OEQOS01` and `EQBOUND01`, removed since `rp_1`).
- **Outputs:** as listed in `EQSTAT`: $T$, $P$, $\rho$, $\beta$, the ionization fractions, $\mu$ terms, $\eta$, $Q_{\rho T}$, $Q_{\rho P}$, $c_P$, $\nabla_\mathrm{ad}$ and their derivatives.
- **Modules:** `NMLPAR_MOD` (the namelist settings: the flag `LOPALE06`, `LSCV`, `TSCUT`, the temperature below which Saha is solved, and `LDIFZ`, metal diffusion); `COMP_MOD` (the envelope composition `XENV`, `ZENV`, `AMUENV`, `FXENV`, set in [[starin.f#STARIN|STARIN]]); `CONSTANTS_MOD` (constants: $\ln 10$, $R$ as `CGAS`, $a/3$ as `CA3`); `IOUNITS_MOD` (`ISHORT`).

**The method.**
1. **Composition.** `AMU` $=\sum_i X_i/A_i$ (ions per unit mass, in units of $1/m_\mathrm{H}$) and the number fractions `FX` of 12 species (Na, Al, Mg, Fe, Si, C, H, O, N, Ar, Ne, He; atomic weights in `ATOMW2`) are rescaled from the envelope values. Without metal diffusion, any change in $Z$ is taken as carbon ("ASSUME EXCESS Z(METALS) IS IN THE FORM OF CARBON(12)"); with it, all metals scale together by $Z/Z_\mathrm{env}$.
2. **Radiation.** $1-\beta = aT^4/(3P)$; then `BETA14` is redefined as $4(1-\beta)/\beta$ (with $1-\beta$ capped at 1). This is the radiation term of the gas's response to temperature: for an ideal gas with radiation, $Q_{\rho T} = -(4-3\beta)/\beta = -1 - 4(1-\beta)/\beta$, and [[eqsaha.f#EQSAHA|EQSAHA]] builds its $Q_{\rho T}$ (`QDT = -1 - BETA14 - …`, the last term from ionization), $c_P$ and their derivatives on it. After an OPAL result `BETA14` is set to $1-\beta$ instead ([[#L334]], [[#L348]]), which would be wrong in these formulas, but no caller reads the `BETA14` it gets back: `EQSAHA` receives it within this call, before the OPAL step, and the callers of `EQSTAT` and `EQSTAT2` only declare it and pass it on (settled from the code, Nov 9, 2026: [[#L165]], [[#L182-L184]], [[#L311-L358]]).

    > **Question** ([[#L159-L164]]). **Negative $\beta$.** When radiation pressure exceeds $P$, the routine writes a message and continues with $\beta < 0$ (so `BETAI` and `BETA14` are negative too). Should it stop, or tell the caller?

3. **Fully ionized gas** ($\log T \ge$ `TSCUT`): [[eqrelv.f#EQRELV|EQRELV]] alone, with $\mu_e^{-1} = 0.9921X + 0.4995(1-X)$ and $R/\mu = R(\mu_\mathrm{ion}^{-1} + \mu_e^{-1})$.
4. **Partial ionization** ($\log T <$ `TSCUT`): `EQSAHA`, and if `LSCV` is set, `EQSCVE`, which overwrites $\rho$ and the first derivatives where its table covers the point. A block after it would compute the SCV second derivatives numerically, but `LSCVD` is set to false just before it, so it never runs: unused? ([[#L189-L241]]; see bug 1).

    Where SCV supplies $\rho$, `RMU`, `EMU` and the second derivatives still come from `EQSAHA` ([[#L181-L187]]; [[eqsaha.f#L194-L195]]), so below the transition band $\mathcal{R}/\mu$ is not $\beta P/(\rho T)$ there: [[eqscve.f#q1|EQSCVE's question 1]].

5. **Transition band** (`TSCUT` − 0.5 < $\log T$ < `TSCUT`): `EQRELV` is also called, and the two are blended with a smooth step. With $w = 2(\mathrm{TSCUT} - \log T)$, between 0 and 1,
$$W(w) = w^3(6w^2 - 15w + 10),\qquad q = q_\mathrm{rel} + W\,(q_\mathrm{Saha} - q_\mathrm{rel})$$
for $\log\rho$, the ionization fractions and the derivatives; then $R/\mu = \beta P/(\rho T)$ and $\mu_e^{-1}$ follows. Two gaps in the blend of the second derivatives are known to the developers (`KNOWN_ISSUES.md`, section 40, "EOS second derivatives"): The differences are not formed for `QDTT` and `QDTP`, so they come out as $q_\mathrm{rel} + W\,q_\mathrm{Saha}$ ([[#L255-L256]], [[#L277-L285]], [[#L298-L299]]), and the term from $dW/d\log T$ is left out (`WT1`, commented out, [[#L276]]). The same section records that the converged models are unaffected; what suffers is the rate and robustness of the Newton iteration.
6. **OPAL.** If `LOPALE06` is set and the point is in the table's rough range ($1870 \le T \le 2\times10^8$ K, $\log\rho \le 7$), OPAL's values replace the above, or are blended with them by the weight $f$ from `EQBOUND06`:
$$q = q_\mathrm{Yale} + f\,(q_\mathrm{OPAL} - q_\mathrm{Yale})$$
for $\log\rho$, $\beta$, the $\mu$ terms, $Q_{\rho T}$, $Q_{\rho P}$, $c_P$ and $\nabla_\mathrm{ad}$. OPAL gives no second derivatives, so those stay from the Yale/SCV result. If OPAL fails (alternate return) or the point is out of its table, the routine exits with the Yale/SCV result. At the end the routine restores `Z` from its copy `Z0` ([[#L91]], [[#L362]]), but nothing changes `Z`: no statement here, and neither `OEQOS06` nor `EQSCVE` (or `EQSCVG`) assigns it (settled from the code, Nov 9, 2026: [[oeqos06.f#L91]], [[oeqos06.f#L122]]): unused?

    > **Question** ([[#L311-L312]]). **Hard-coded OPAL range.** The rough range ($1870 \le T \le 2\times10^8$ K, $\log\rho \le 7$) is hard-coded; the real edges are checked in `EQBOUND06`. Is this range still needed, and is it right for the 2006 table?

    > **Question** ([[#L117-L152]]; [[#L344-L355]]). **The OPAL table's heavy-element mixture.** The Yale EOS takes its 12 species from the envelope's `FXENV`, with any excess $Z$ as carbon; the OPAL 2006 table (`FOPALE06`, `EOSOPAL06Z0.016492` in the documentation's example) is computed for one fixed mixture. In the ramp the two are averaged. Which mixture is the OPAL table for, and do the `FX` fractions match it? If not, the ramp blends two compositions; the effect on $P$ is small (the documentation notes that $P$ hardly depends on the metals), but it would show in $\nabla_\mathrm{ad}$ and $c_P$ across the ramp.


**From YREC's documentation.** [Microphysics in YREC](https://yrec.readthedocs.io/en/latest/microphysics.html) describes the layers: OPAL (`LOPALE06`, the 2006 tables, Rogers & Nayfonov 2002, valid for $3.3 < \log T < 8.3$ with a density edge; "strongly recommended," although off by default), then SCV (`LSCV`, from three tables for pure H, He and metals, combined in a thermodynamically consistent way; the metal table was made with YREC's own EOS), then YREC's own EOS, with a ramp near the edge of the OPAL tables. With both on, SCV is used only outside OPAL; a full SCV calculation needs OPAL off and SCV on. OPAL assumes a fixed heavy-element mixture, so settling does not change $Z$ in it (a minor effect, since $P$ hardly depends on the metals). YREC's own EOS assumes full ionization above $\log T$ = `TSCUT` (default 6.0); the documentation warns not to change it, since the Saha equation for H and He fails at high density. YREC's semi-analytic derivatives are used for the structure equations even where a table gives the pressure.

> **Question** ([[nmlpar_mod.f#L122]]). **The documentation's removed options.** The microphysics page (`docs/source/microphysics.md`, lines 29–51) still describes `LOPALE`, `LOPALE01` and `FOPALE` (the 1996 and 2002 OPAL EOS) and the MHD EOS (`FMHD1`–`FMHD7`), all removed from the code since `rp_1`; it calls `LOPALE06` "strongly recommended" and says "We should alter the defaults to make LOPALE06 = TRUE," while its default is still false. Should the page be updated, and the default changed?

**What the code uses.** The documentation's last sentence holds for the second derivatives only: where OPAL applies, its own first derivatives ($Q_{\rho T}$, $Q_{\rho P}$, $c_P$, $\nabla_\mathrm{ad}$) replace or are blended with the Yale ones (step 6), and SCV's replace them where its tables cover the point (step 4). Beyond OPAL's range ($T > 2\times10^8$ K or $\log\rho > 7$) only `EQRELV` applies: full ionization, relativistic degenerate electrons, and, as its one Coulomb term, the Debye–Hückel correction when `LDH` is set (as in every test-suite run; see [[eqrelv.f#EQRELV|EQRELV]] for its defaults). Of the 51 test-suite runs, 45 set `LOPALE06` and 47 `LSCV`.

> **Question** ([[#L167-L177]]; [[eqrelv.f#L179-L185]]). **The EOS beyond OPAL's range.** Above $2\times10^8$ K or $\log\rho > 7$ only `EQRELV` applies, whose only non-ideal term is Debye–Hückel, a weak-coupling correction. Is that adequate for the advanced stages the test suite runs (the runs to the end of core helium burning, `…_TAHB`), where a reader would expect a strong-coupling (ion-sphere or one-component-plasma) term?

**Changed since `rp_1`.** The OPAL 1995 and 2001 equations of state are removed (with their flags and calls), leaving OPAL 2006 alone; COMMON blocks to modules (`TSCUT`, `LDIFZ`, `LSCV` and `LOPALE06` now from `NMLPAR_MOD`; the unused `/CTLIM/`, `/DEBHU/` and `/SCVEOS/` declarations dropped), `IMPLICIT NONE`, and the local `FMU` renamed `FMUENV`.

## Bugs, by priority

1. **(cannot be reached)** **A dead block with unset variables.** ([[#L189-L241]]) `LSCVD` is set to false just before the block that would compute the SCV second derivatives numerically, so it never runs. If it were switched on, it would be wrong: Both temperature calls write `QDT1`, `QCP1`, `DELA1` ([[#L208]], [[#L213]]), so `QDT2`, `QCP2`, `DELA2` are never set before they are used ([[#L215-L217]]), and `DL1`, `D1` are never initialized.

    **A possible fix:** a choice for the developers: delete the block, or, to keep it, write the second temperature call into `QDT2`, `QDP2`, `QCP2`, `DELA2` and start `DL1`, `D1` from `DL`, `D`.

    **Checked by running YREC** (Nov 9, 2026; a line added at each suspected path counted how often it was taken, the outputs otherwise unchanged). The block's counting line never fired in the 34 cases run, and cannot at 7be4133: `LSCVD` is set false at [[#L189]], just before the test at [[#L190]]. No fix was run, since deleting or repairing a block that never runs changes nothing. Intent: The comment at [[#L189]], "Do not do SCV derivatives," shows that the block was switched off on purpose; the errors inside it are not explained.

### EQSTAT2

Chooses and blends the equations of state by regime (method above): composition, radiation, Saha or SCV below `TSCUT`, the relativistic gas above it with a smooth-step blend between, and OPAL 2006 on top where its table covers the point.
