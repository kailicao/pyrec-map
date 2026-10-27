## Explanation

**Purpose.** `GETTAU` computes the convective overturn timescale $\tau_\mathrm{cz}$ one pressure scale height above the base of the surface convection zone ("G Somers, 3/17"; its comment calls it "a new, systematic method"). Depending on where that point lies, it uses the interior model, the envelope integration, or the two stitched together.

**How it fits.**
- **Who calls it:** [[getw.f#GETW|GETW]], [[starin.f#STARIN|STARIN]] and [[wrtout.f#WRTOUT|WRTOUT]].
- **Inputs:** the model arrays (`HCOMP`, `HR`, `HP`, `HD`, `HS1`, `HT`, `LC`, `M`), the form factors `FP`, `FT`, the surface `TEFFL`, `BL`, `HSTOT`; the mixing-length parameter `CMIXL` (an argument since `rp_1`, passed on to `ENVINT`); and from `SCRTCH_MOD`, the interior's convective velocities `SVEL` and gradients `SDEL`, left there by an earlier physics pass.
- **What it calls:** [[envint.f#ENVINT|ENVINT]] (the envelope, which also sets the photospheric pressure `PPHOT` and, in the old scheme, `TAUCZ`), then [[tauintnew.f#TAUINTNEW|TAUINTNEW]] or [[tauint.f#TAUINT|TAUINT]].
- **Outputs:** `TAUCZ` and `PPHOT` in `OVRTRN_MOD`, read by about twenty routines (wind and magnetic braking among them: [[mwind.f#MWIND|MWIND]], `COWIND`, `DADCOEFT`, …); `RBCZ` (argument), the radius of the convection zone's base in solar radii, set by `TAUINTNEW` (0 if it finds none); the old method (`TAUINT`) leaves it unchanged.
- **Modules** (COMMON blocks until `rp_1`): `OVRTRN_MOD` (`LNEWTCZ` selects the new method, `LCALCENV` tells `ENVINT` whether to store the envelope's structure); `ENVSTRUCT_MOD` (the envelope solution); `SCRTCH_MOD` (interior velocities and gradients); `NMLPAR_MOD` (the starspot parameters `SPOTF`, `SPOTX`, formerly `/SPOTS/`); `DIMENSIONS_MOD` and `CONSTANTS_MOD`.

**The method.**
1. Find the base of the surface convection zone, `IMAX`, scanning inward from the surface.
2. If $\log P_\mathrm{base} - \log P_\mathrm{surf} < 1$ (or the old method is chosen), the point one scale height up may be in the envelope, so `LCALCENV` is set and the envelope's structure kept.
3. Integrate the envelope with `ENVINT` from the surface conditions (radius and gravity from $L$ and $T_\mathrm{eff}$, as in [[getnewenv.f#GETNEWENV|GETNEWENV]], with the starspot correction to $T_\mathrm{eff}$). In the old method, `ENVINT` sets `TAUCZ` itself and the routine ends there.
4. Copy the interior into work arrays, with $g = Gm/r^2$, the velocities and gradients from `SCRTCH_MOD`: `DELF1` = $\nabla_\mathrm{rad}$ (`SDEL(1,·)`) and `DELF2` = $\nabla_\mathrm{ad}$ (`SDEL(3,·)`, as PHYSIC stores them). With the new method and `LCALCENV`, append the envelope points 2 to `NUMENV` (the first is the last interior point), taking the same two gradients from `EDELS(1,·)` and `EDELS(2,·)`, which QENV stores in the order $\nabla_\mathrm{rad}$, $\nabla_\mathrm{ad}$, $\nabla$.
5. `TAUINTNEW` (new method) or `TAUINT` (old) integrates the overturn time over these arrays.
6. `LCALCENV` is reset to true.

**KC's changes.** The unused arguments `HG` (here), `HCOMPF`, `HS2` and `HSTOT` (in the calls to `TAUINTNEW` and `TAUINT`) were removed (2025-05-31); the elements of `/ENVSTRUCT/` (now `ENVSTRUCT_MOD`) were reordered (2025-05-30).

**Changed since `rp_1`.** A new last argument `CMIXL`, passed on to `ENVINT` (which no longer takes the mixing length from a COMMON block); COMMON blocks to modules, `IMPLICIT NONE`, and the unused `/LUOUT/`, `/INTENV/`, `/INTATM/` and `/ENVGEN/` removed. No question settled.

## Questions for the experts

1. **Composition from beyond the model.** The envelope points copy their composition from `HCOMP(J,M+1)`, one point past the model's last point. Should it be `HCOMP(J,M)`? (The composition is not passed on to `TAUINT*` since KC's change, so this may have no effect now.)
2. **"At least 3 pressure scale heights".** The comment says a difference of 1 in $\log P$ means "at least 3 PSCAS", but one dex in $P$ is $\ln 10 \approx 2.3$ scale heights. Is the threshold of 1 meant to be safe for one scale height, or should the comment change?
3. **Stale interior velocities.** `SVEL` and `SDEL` come from `SCRTCH_MOD`, written by whichever routine ran the physics last. Are they guaranteed to belong to the current model when `GETTAU` is called from `STARIN` and `WRTOUT`?
4. **Unused variable.** `LALLCZ` (fully convective star) is set but never used.

### GETTAU

Convective overturn time one pressure scale height above the base of the surface convection zone, from the interior, the envelope, or both stitched together (method above).
