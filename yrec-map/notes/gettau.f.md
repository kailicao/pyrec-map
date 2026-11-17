## Explanation

**Purpose.** `GETTAU` computes the convective overturn timescale $`\tau_\mathrm{cz}`$ one pressure scale height above the base of the surface convection zone ("G Somers, 3/17"; its comment calls it "a new, systematic method"). Depending on where that point lies, it uses the interior model, the envelope integration, or the two stitched together. In the new method ([TAUINTNEW](tauintnew.f.md#tauintnew)) the timescale is local, $`\tau_\mathrm{cz} = H_p/v_\mathrm{conv}`$ (`PSCA/CVEL`), evaluated one $`H_p`$ above the base; for a zone thinner than $`H_p`$ it is the crossing time $`\Delta r/v_\mathrm{conv}`$ (`DELR/CVEL`, with $`\Delta r`$ the zone's width and $`v_\mathrm{conv}`$ at its middle), and with no surface convection zone it is 0.

> **Question** ([lines 64–77](https://github.com/yreclab/yrec/blob/7be4133/src/gettau.f#L64-L77)). **Why one $`H_p`$ above the base.** The timescale is evaluated one $`H_p`$ above the base of the convection zone. Why this point rather than, say, half a mixing length above the base, or a global, integrated $`\tau = \int dr/v`$? Is it the convention of the calibration the wind law uses (`PMMSOLTAU`), so that the two must be computed the same way?

**How it fits.**
- **Who calls it:** [GETW](getw.f.md#getw), [STARIN](starin.f.md#starin) and [WRTOUT](wrtout.f.md#wrtout).
- **Inputs:** the model arrays (`HCOMP`, `HR`, `HP`, `HD`, `HS1`, `HT`, `LC`, `M`), the form factors `FP`, `FT`, the surface `TEFFL`, `BL`, `HSTOT`; the mixing-length parameter `CMIXL` (an argument since `rp_1`, passed on to `ENVINT`); and from `SCRTCH_MOD`, the interior's convective velocities `SVEL` and gradients `SDEL`, left there by an earlier physics pass.
- **What it calls:** [ENVINT](envint.f.md#envint) (the envelope, which also sets the photospheric pressure `PPHOT` and, in the old scheme, `TAUCZ`), then [TAUINTNEW](tauintnew.f.md#tauintnew) or [TAUINT](tauint.f.md#tauint).
- **Outputs:** `TAUCZ` and `PPHOT` in `OVRTRN_MOD`, read by about twenty routines (wind and magnetic braking among them: [MWIND](mwind.f.md#mwind), `COWIND`, `DADCOEFT`, …); `RBCZ` (argument), the radius of the convection zone's base in solar radii, set by `TAUINTNEW` (0 if it finds none); the old method (`TAUINT`) leaves it unchanged.
- **Modules** (COMMON blocks until `rp_1`): `OVRTRN_MOD` (`TAUCZ`, `PPHOT`); `ENVSTRUCT_MOD` (the envelope solution); `SCRTCH_MOD` (interior velocities and gradients); `NMLPAR_MOD` (`LNEWTCZ`, which selects the new method, and `LCALCENV`, which tells `ENVINT` whether to store the envelope's structure, both formerly in `/OVRTRN/`; the starspot parameters `SPOTF`, `SPOTX`, formerly `/SPOTS/`); `DIMENSIONS_MOD` and `CONSTANTS_MOD`.

**The method.**
1. Find the base of the surface convection zone, `IMAX`, scanning inward from the surface. A fully convective star sets `LALLCZ`, which nothing reads (unused?, [line 91](https://github.com/yreclab/yrec/blob/7be4133/src/gettau.f#L91)).
2. If $`\log P_\mathrm{base} - \log P_\mathrm{surf} \lt{} 1`$ (or the old method is chosen), the point one scale height up may be in the envelope, so `LCALCENV` is set and the envelope's structure kept.

    > **Question** ([lines 95–103](https://github.com/yreclab/yrec/blob/7be4133/src/gettau.f#L95-L103)). **"At least 3 pressure scale heights."** The comment says a difference of 1 in $`\log P`$ means "AT LEAST 3 PSCAS," but one $`\mathrm{dex}`$ in $`P`$ is $`\ln 10 \approx 2.3`$ scale heights. Is the threshold of 1 meant to be safe for one scale height, or should the comment change?

3. Integrate the envelope with `ENVINT` from the surface conditions (radius and gravity from $`L`$ and $`T_\mathrm{eff}`$, as in [GETNEWENV](getnewenv.f.md#getnewenv), with the starspot correction to $`T_\mathrm{eff}`$). In the old method, `ENVINT` sets `TAUCZ` itself and the routine ends there.
4. Copy the interior into work arrays, with $`g = Gm/r^2`$, the velocities and gradients from `SCRTCH_MOD`: `DELF1` = $`\nabla_\mathrm{rad}`$ (`SDEL(1,·)`) and `DELF2` = $`\nabla_\mathrm{ad}`$ (`SDEL(3,·)`, as PHYSIC stores them). With the new method and `LCALCENV`, append the envelope points 2 to `NUMENV` (the first is the last interior point), taking the same two gradients from `EDELS(1,·)` and `EDELS(2,·)`, which QENV stores in the order $`\nabla_\mathrm{rad}`$, $`\nabla_\mathrm{ad}`$, $`\nabla`$. The composition is copied too, into `HCOMPF`, for the envelope points from `HCOMP(J,M+1)`, one point past the model; but since the calls no longer pass `HCOMPF`, it is read nowhere (unused?, [lines 144–147](https://github.com/yreclab/yrec/blob/7be4133/src/gettau.f#L144-L147), [lines 166–169](https://github.com/yreclab/yrec/blob/7be4133/src/gettau.f#L166-L169)).

    > **Question** ([lines 155–157](https://github.com/yreclab/yrec/blob/7be4133/src/gettau.f#L155-L157)). **Stale interior velocities.** `SVEL` and `SDEL` come from `SCRTCH_MOD`, written by whichever routine ran the physics last. Are they guaranteed to belong to the current model when `GETTAU` is called from `STARIN` and `WRTOUT`?

5. `TAUINTNEW` (new method) evaluates the overturn time from these arrays, as above; `TAUINT` (old) computes it its own way.
6. `LCALCENV` is reset to true.

**Changed since `rp_1`.** A new last argument `CMIXL`, passed on to `ENVINT` (which no longer takes the mixing length from a COMMON block); COMMON blocks to modules, `IMPLICIT NONE`, and the unused `/LUOUT/`, `/INTENV/`, `/INTATM/` and `/ENVGEN/` removed. No question settled.

### GETTAU

Convective overturn time one pressure scale height above the base of the surface convection zone, from the interior, the envelope, or both stitched together (method above).
