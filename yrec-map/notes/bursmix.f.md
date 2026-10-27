## Explanation

**Purpose.** This file evolves the abundances over one time step when rotational mixing and nuclear burning act together. In its own words, it alternates "between nuclear burning plus gravitational settling and mixing in a series of progressively smaller timesteps, extrapolating to the answer for zero timestep". The diffusion coefficients, structure and reaction rates are held fixed during the step.

**How it fits.**
- **Inputs:** the arguments, the model (`HD`, `HL`, `HP`, `HR`, `HS`, `HS1`, `HS2`, `HT`, `HV`), the mixing coefficients `COD2`, the time step `DELTS`, the zones (`MRZONE`, `MXZONE`, `NRZONE`, `NZONE`, `LCZ`); `LEXCOM` from [[nmlpar_mod.f#NMLPAR_MOD|`NMLPAR_MOD`]] (whether the extended set of 15 species, with the light elements, is followed); `HCOMPP` in [[oldmod_mod.f#OLDMOD_MOD|`OLDMOD_MOD`]], the composition at the start of the step.
- **Who calls it:** [[getw.f#GETW|GETW]], the rotation step, only when `LINSTB` is true, `LALLCZ` false and `LBURS` true.
- **What it calls:** [[rotmix.f#ROTMIX|ROTMIX]] (burning, by its header with [[kemcom.f#KEMCOM|KEMCOM]] in radiative regions), [[ndifcom.f#NDIFCOM|NDIFCOM]] (mixing by angular-momentum transport), [[liburn2.f#LIBURN2|LIBURN2]] (light-element burning, if `LEXCOM`), and [[bsrotmix.f#BSROTMIX|BSROTMIX]] (the extrapolation).
- **Outputs:** `HCOMP`, the abundances at the end of the step. If `LEXCOM`, it copies the new lithium and beryllium rates ([[newrat_mod.f#NEWRAT_MOD|`NEWRAT_MOD`]]) into the old ones ([[oldrat_mod.f#OLDRAT_MOD|`OLDRAT_MOD`]]), and sets `JENV0 = JENV1`, `PSCAL0 = PSCAL1` ([[liov_mod.f#LIOV_MOD|`LIOV_MOD`]]).
- **Modules:** `OLDMOD_MOD` (18 units, among them [[crrect.f#CRRECT|CRRECT]], [[kemcom.f#KEMCOM|KEMCOM]], [[liburn.f#LIBURN|LIBURN]]); `NEWRAT_MOD`, `OLDRAT_MOD`, `LIOV_MOD` (GETW, LIBURN, LIBURN2, LIRATE88); `NMLPAR_MOD`.

**The method.**
1. Save the composition at the start of the step (`HCOMPP`), and $X$, $Y$, $Z$ of the input `HCOMP`, which the caller's full step has already produced.
2. Pass the composition of the full step, already computed by the caller, to BSROTMIX as sequence 1.
3. For sequences $k = 2, \dots, 11$, with $n_k$ = 2, 4, 6, …, 20 substeps of $\Delta t/n_k$: reset the composition, then for each substep burn and, if `LDIFY`, settle (ROTMIX, which calls MICRODIFF or GRSETT), mix (NDIFCOM) and, if `LEXCOM`, burn the light elements (LIBURN2); the end of each substep becomes the start of the next (`HCOMPP`, which KEMCOM reads as the start-of-step state). Then call BSROTMIX; stop when it reports convergence.
4. If no sequence converges, print a warning and keep the composition of the last (finest) sequence.
5. Restore $X$ and $Z$ to their input values (those of the caller's full step, not those at the start of the time step), and set $Y = 1 - X - Z - X_3$.

Only species 4 onward (from $^3$He) are extrapolated (`JBEG = 4`).

**KC's changes.** 2025-05-31: unused arguments dropped from the calls to ROTMIX (`ITLVL`, passed as 5), NDIFCOM (`NTOT`) and LIBURN2 (`HD`); the old calls kept as comments.

**Changed since `rp_1`.** Declarations only: COMMON blocks to modules, `IMPLICIT NONE`.

## Questions for the experts

1. **$X$ and $Z$ restored.** After the extrapolation, $X$ and $Z$ are reset to their values on entry (`HKEEP`), that is, to the caller's full step, so the burning and mixing of hydrogen computed in the substeps are discarded, and $Y$ absorbs the difference. Is this reset meant?
2. **Uninitialized arrays.** `ECOD2`, `EM`, `IBEG` and `IEND` are local (listed under "INPUT VARIABLES" but not arguments) and never set here. NDIFCOM sets them (through MIXGRID) when `LOK` is true, and reads them as they are when `LOK` is false; `LOK` is passed from GETW, which gets it from SECULR. When `LOK` is false, are these arrays undefined?
3. **`HCOMPP` left at the end of the step.** The substeps overwrite `HCOMPP`, the start-of-step composition in `OLDMOD_MOD` that CRRECT, KEMCOM and others read, and leave it at the end-of-step composition for all species, although the comment says it is overwritten "temporarily". GETW also overwrites `HCOMPP` for species 12–15 elsewhere. Is the end state intended?
4. **Two `NSEQ` sequences.** `NSEQ` here starts 1, 2, 4, 6, … (step by 2), while [[bsstep.f#BSSTEP|BSSTEP]] uses 2, 4, 6, 8, 12, … Is the choice deliberate?

### BURSMIX

Burn–mix substepping over one time step for increasing numbers of substeps, extrapolated to zero substep by [[bsrotmix.f#BSROTMIX|BSROTMIX]]; resets $X$, $Z$ and updates $Y$.
