## Explanation

**Purpose.** `EQSTAT2` is the core of YREC's equation of state: it chooses among, and blends, the Yale Saha solver, the relativistic degenerate gas, the SCV tables and the three OPAL tables, depending on temperature, density and the run's settings. Its header calls it "the old EOS routine"; since 2006 the code calls it through [[eqstat.f#EQSTAT|EQSTAT]].

**How it fits.**
- **Who calls it:** `EQSTAT` (once or five times per call, see there) and [[calcad.f#CALCAD|CALCAD]] directly.
- **Inputs:** `TL`, `PL`, `X`, `Z`, `LDERIV`, `LATMO`; `DL` as a starting guess.
- **What it calls:** [[eqsaha.f#EQSAHA|EQSAHA]] (Saha ionization), [[eqscve.f#EQSCVE|EQSCVE]] (SCV tables), [[eqrelv.f#EQRELV|EQRELV]] (fully ionized, degenerate gas), and for OPAL [[oeqos.f#OEQOS|OEQOS]] with [[eqbound.f#EQBOUND|EQBOUND]], [[oeqos01.f#OEQOS01|OEQOS01]] with [[eqbound01.f#EQBOUND01|EQBOUND01]], [[oeqos06.f#OEQOS06|OEQOS06]] with [[eqbound06.f#EQBOUND06|EQBOUND06]].
- **Outputs:** as listed in `EQSTAT`: $T$, $P$, $\rho$, $\beta$, the ionization fractions, $\mu$ terms, $\eta$, $Q_{\rho T}$, $Q_{\rho P}$, $c_P$, $\nabla_\mathrm{ad}$ and their derivatives.
- **COMMON blocks:** `/OPALEOS/` (the flags `LOPALE`, `LOPALE01`, `LOPALE06`; [[parmin.f#PARMIN|PARMIN]] allows only one at a time); `/SCVEOS/` (`LSCV`; the tables are used by `EQSCVE`); `/COMP/` (the envelope composition `XENV`, `ZENV`, `AMUENV`, `FXENV`, set in [[starin.f#STARIN|STARIN]]); `/CTLIM/` (`TSCUT`, the temperature below which Saha is solved; set in `PARMIN`); `/GRAVS3/` (`LDIFZ`, metal diffusion); `/CONST1/`, `/CONST2/` (constants: $\ln 10$, $R$ as `CGAS`, $a/3$ as `CA3`); `/LUOUT/` (`ISHORT`). `/DEBHU/` (the Debye–Hückel data that `EQRELV` uses) is declared here but not used.

**The method.**
1. **Composition.** `AMU` $=\sum_i X_i/A_i$ (ions per unit mass, in units of $1/m_\mathrm{H}$) and the number fractions `FX` of 12 species (Na, Al, Mg, Fe, Si, C, H, O, N, Ar, Ne, He; atomic weights in `ATOMW2`) are rescaled from the envelope values. Without metal diffusion, any change in $Z$ is taken as carbon ("ASSUME EXCESS Z(METALS) IS IN THE FORM OF CARBON(12)"); with it, all metals scale together by $Z/Z_\mathrm{env}$.
2. **Radiation.** $1-\beta = aT^4/(3P)$; then `BETA14` is redefined as $4(1-\beta)/\beta$ (with $1-\beta$ capped at 1).
3. **Fully ionized gas** ($\log T \ge$ `TSCUT`): [[eqrelv.f#EQRELV|EQRELV]] alone, with $\mu_e^{-1} = 0.9921X + 0.4995(1-X)$ and $R/\mu = R(\mu_\mathrm{ion}^{-1} + \mu_e^{-1})$.
4. **Partial ionization** ($\log T <$ `TSCUT`): `EQSAHA`, and if `LSCV` is set, `EQSCVE`, which overwrites $\rho$ and the first derivatives where its table covers the point.
5. **Transition band** (`TSCUT` − 0.5 < $\log T$ < `TSCUT`): `EQRELV` is also called, and the two are blended with a smooth step. With $w = 2(\mathrm{TSCUT} - \log T)$, between 0 and 1,
$$W(w) = w^3(6w^2 - 15w + 10),\qquad q = q_\mathrm{rel} + W\,(q_\mathrm{Saha} - q_\mathrm{rel})$$
for $\log\rho$, the ionization fractions and the derivatives (but see question 7 for `QDTT` and `QDTP`); then $R/\mu = \beta P/(\rho T)$ and $\mu_e^{-1}$ follows.
6. **OPAL.** If an OPAL table is chosen and the point is in its rough range (1995: $T \ge 5000$ K, $\log T \le 8$, $\log\rho \le 5$; 2001: $2000 \le T \le 10^8$ K, $\log\rho \le 7$; 2006: $1870 \le T \le 2\times10^8$ K, $\log\rho \le 7$), OPAL's values replace the above, or are blended with them by the weight $f$ from `EQBOUND*`:
$$q = q_\mathrm{Yale} + f\,(q_\mathrm{OPAL} - q_\mathrm{Yale})$$
for $\log\rho$, $\beta$, the $\mu$ terms, $Q_{\rho T}$, $Q_{\rho P}$, $c_P$ and $\nabla_\mathrm{ad}$. OPAL gives no second derivatives, so those stay from the Yale/SCV result. If OPAL fails (alternate return) or the point is out of its table, the routine exits with the Yale/SCV result.

**KC's changes.** The first `SAVE`, which came before the declarations, was commented out to silence compiler warnings (a second `SAVE` remains after the DATA statements), and the elements of `/OPALEOS/` were reordered (2025-05-30); the calls were updated for the arguments removed from `EQRELV`, `EQSCVE` and `EQBOUND*` (2025-05-31).

## Questions for the experts

1. **Two meanings of `BETA14`.** In the Yale branch `BETA14` is $4(1-\beta)/\beta$ (step 2), but after an OPAL result it is set to $1-\beta$. Callers receive one or the other depending on the regime. Which do they expect?
2. **Dead SCV derivative block.** `LSCVD` is set to false just before the block that would compute SCV derivatives numerically, so the block never runs. It also has a bug: both temperature calls write `QDT1`, `QCP1`, `DELA1`, so `QDT2`, `QCP2`, `DELA2` are never set, and `DL1`, `D1` are uninitialized. Remove the block, or fix it?
3. **Negative $\beta$.** When radiation pressure exceeds $P$, the routine writes a message and continues with $\beta < 0$. Should it stop?
4. **Mixed outputs with SCV.** `RMU`, `EMU` and the second derivatives come from `EQSAHA` even when SCV supplies $\rho$; see question 2 in [[eqscve.f|eqscve.f]].
5. **Hard-coded OPAL ranges.** The rough ranges in step 6 are hard-coded and differ by table; the real edges are checked in `EQBOUND*`. Are these ranges still needed, and are they right?
6. **`Z` restored.** The routine saves `Z` and restores it at the end (`Z = Z0`), but no statement in it changes `Z`; only the OPAL routines receive it as an argument. Do they change it, or is the restore a leftover?
7. **Second derivatives in the transition band.** The differences Saha − relativistic are formed for `DL0`, `QDT0`, `QDP0`, `QCP0`, `DELA0`, `QCPT0`, `QCPP0`, `QAT0`, `QAP0`, but not for `QDTT0` and `QDTP0`. So `QDTT = QDTT + WT0*QDTT0` adds $W$ times the full Saha value to the relativistic one, instead of $W$ times the difference; the same for `QDTP`. Also, the blended derivatives leave out $dW/d\log T$ (the line for it, `WT1`, is commented out). Are these bugs?

### EQSTAT2

Chooses and blends the equations of state by regime (method above): composition, radiation, Saha or SCV below `TSCUT`, the relativistic gas above it with a smooth-step blend between, and OPAL on top where its table covers the point.
