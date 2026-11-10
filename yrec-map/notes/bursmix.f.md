## Explanation

**Purpose.** This file evolves the abundances over one time step when rotational mixing and nuclear burning act together. In its own words, it alternates "between nuclear burning plus gravitational settling and mixing in a series of progressively smaller timesteps, extrapolating to the answer for zero timestep." The diffusion coefficients, structure and reaction rates are held fixed during the step.

**How it fits.**
- **Inputs:** the arguments, the model (`HD`, `HL`, `HP`, `HR`, `HS`, `HS1`, `HS2`, `HT`, `HV`), the mixing coefficients `COD2`, the time step `DELTS`, the zones (`MRZONE`, `MXZONE`, `NRZONE`, `NZONE`, `LCZ`); `LEXCOM` from [[nmlpar_mod.f#NMLPAR_MOD|`NMLPAR_MOD`]] (whether the extended set of 15 species, with the light elements, is followed); `HCOMPP` in [[oldmod_mod.f#OLDMOD_MOD|`OLDMOD_MOD`]], the composition at the start of the step.
- **Who calls it:** [[getw.f#GETW|GETW]], the rotation step, only when `LINSTB` is true, `LALLCZ` false and `LBURS` true ([[getw.f#L455-L460]]). GETW sets its local `LBURS` to false on every call and never changes it ([[getw.f#L140]]), so at 7be4133 BURSMIX is never called, nor [[bsrotmix.f#BSROTMIX|BSROTMIX]] through it: unused?
- **What it calls:** [[rotmix.f#ROTMIX|ROTMIX]] (burning, by its header with [[kemcom.f#KEMCOM|KEMCOM]] in radiative regions), [[ndifcom.f#NDIFCOM|NDIFCOM]] (mixing by angular-momentum transport), [[liburn2.f#LIBURN2|LIBURN2]] (light-element burning, if `LEXCOM`), and [[bsrotmix.f#BSROTMIX|BSROTMIX]] (the extrapolation).
- **Outputs:** `HCOMP`, the abundances at the end of the step. If `LEXCOM`, it copies the new lithium and beryllium rates ([[newrat_mod.f#NEWRAT_MOD|`NEWRAT_MOD`]]) into the old ones ([[oldrat_mod.f#OLDRAT_MOD|`OLDRAT_MOD`]]), and sets `JENV0 = JENV1`, `PSCAL0 = PSCAL1` ([[liov_mod.f#LIOV_MOD|`LIOV_MOD`]]).
- **Modules:** `OLDMOD_MOD` (18 units, among them [[crrect.f#CRRECT|CRRECT]], [[kemcom.f#KEMCOM|KEMCOM]], [[liburn.f#LIBURN|LIBURN]]); `NEWRAT_MOD`, `OLDRAT_MOD`, `LIOV_MOD` (GETW, LIBURN, LIBURN2, LIRATE88); `NMLPAR_MOD`.

**The method.**
1. Save the composition at the start of the step (`HCOMPP`), and $X$, $Y$, $Z$ of the input `HCOMP`, which the caller's full step has already produced ([[#L75-L82]]).
2. Pass the composition of the full step, already computed by the caller, to BSROTMIX as sequence 1.
3. For sequences $k = 2, \dots, 11$, with $n_k$ = 2, 4, 6, …, 20 substeps of $\Delta t/n_k$: reset the composition, then for each substep burn and, if `LDIFY`, settle (ROTMIX, which calls MICRODIFF or GRSETT), mix (NDIFCOM) and, if `LEXCOM`, burn the light elements (LIBURN2); the end of each substep becomes the start of the next (`HCOMPP`, which KEMCOM reads as the start-of-step state). Then call BSROTMIX; stop when it reports convergence ([[#L87-L126]]). On convergence `HCOMPP` is set to the end-of-step composition ([[#L118-L123]]), and otherwise it is left there by the last substep, though the comment says it is overwritten "temporarily" ([[#L72-L74]]); GETW does the same on its other path, copying the end-of-step composition into `HCOMPP` when `LBURS` is false ([[getw.f#L372-L377]]), so it is the start of the next step (settled from the code, Nov 9, 2026).

    > **Question** ([[#L52]]; [[#L95-L96]]). **Two `NSEQ` sequences.** `NSEQ` here starts 1, 2, 4, 6, … (step by 2), while [[bsstep.f#BSSTEP|BSSTEP]] uses 2, 4, 6, 8, 12, … Is the choice deliberate?

4. If no sequence converges, print a warning and keep the composition of the last (finest) sequence.
5. Restore $X$ and $Z$ to their input values (those of the caller's full step, not those at the start of the time step), and set $Y = 1 - X - Z - X_3$ ([[#L131-L136]]).

    > **Question** ([[#L132-L136]]). **$X$ and $Z$ restored.** After the extrapolation, $X$ and $Z$ are reset to their values on entry (`HKEEP`), that is, to the caller's full step, so the burning and mixing of hydrogen computed in the substeps are discarded, and $Y$ absorbs the difference. Is this reset meant?

Only species 4 onward (from $^3$He) are extrapolated (`JBEG = 4`).

**Changed since `rp_1`.** Declarations only: COMMON blocks to modules, `IMPLICIT NONE`.

## Bugs, by priority

1. **(cannot be reached)** **NDIFCOM gets a region never set when `LOK` is false.** ([[#L28-L31]]; [[#L46-L49]]; [[#L103-L106]]) `IBEG`, `IEND`, `ECOD2` and `EM` are locals of BURSMIX, listed as input variables but set nowhere in it; only NDIFCOM sets them, through MIXGRID, and only when `LOK` is true. With `LOK` false, NDIFCOM passes them straight to MIXCOM ([[ndifcom.f#L64-L66]]). GETW passes the `LOK` that SECULR returns, which is false when SECULR finds no instability and leaves early ([[seculr.f#L202]], [[seculr.f#L289]]). What follows: On the first such call `IBEG` = `IEND` = 0 if the compiler zeroes saved locals, and MIXCOM reads `HCOMP(J,0)`, out of bounds ([[mixcom.f#L61]]), before finding nothing to do; after an earlier call with `LOK` true, MIXCOM mixes again the last region of that call, with its old coefficients, in a model SECULR found stable.

    **A possible fix:**

    ```diff
    --- a/src/bursmix.f
    +++ b/src/bursmix.f
    @@ -100,10 +100,15 @@
                 CALL ROTMIX(DT,HCOMP,HS2,HT,M,MRZONE,MXZONE,
          *               NRZONE,NZONE,HSTOT,HD,HS,HR,HP,LCZ,HS1)
     C PERFORM MIXING
    -            CALL NDIFCOM(DT,COD2,ECOD2,EM,HD,HL,HP,HR,HS,HS1,HS2,
    +C 11/09/26 KC via Claude
    +C code changed to mix only when SECULR found unstable regions (LOK);
    +C IBEG, IEND, ECOD2 and EM are set only by such a call.
    +            IF(LOK)THEN
    +               CALL NDIFCOM(DT,COD2,ECOD2,EM,HD,HL,HP,HR,HS,HS1,HS2,
     C      *                   HSTOT,HV,IBEG,IEND,IMAX,IMIN,LCZ,LOK,M,NTOT,  ! KC 2025-05-31
    -     *                   HSTOT,HV,IBEG,IEND,IMAX,IMIN,LCZ,LOK,M,
    -     *                   HCOMP,JBEG,JEND)
    +     *                      HSTOT,HV,IBEG,IEND,IMAX,IMIN,LCZ,LOK,M,
    +     *                      HCOMP,JBEG,JEND)
    +            ENDIF
                 IF(LEXCOM)THEN
     C                CALL LIBURN2(DT,HCOMP,HD,HR,HS1,HS2,HT,JENV1,JENV0,M)  ! KC 2025-05-31
                    CALL LIBURN2(DT,HCOMP,HR,HS1,HS2,HT,JENV1,JENV0,M)
    ```

    **Checked by running YREC** (Nov 9, 2026; a line added at each suspected path counted how often it was taken, the outputs otherwise unchanged): Cannot be reached at 7be4133. GETW sets `LBURS = .FALSE.` on every call ([[getw.f#L140]]) and calls BURSMIX only when it is true ([[getw.f#L455-L461]]); no namelist can change that. No counting line fired in any case run, the five rotating test cases run (`testsuite/Test_3Msolar_GS_rot_gray_OPALSCV_SF2_GS98_OP_CF10_RGp2diffrotI3cz2`, `testsuite/Test_solarGS98_difrotmixper18p4d1p0`, `testsuite/Test_m0p8feh+0p0GS98_rotp8p0d0p1mag1e4std_TAMS`, `testsuite/Test_m2p0_feh+0p0_vzams150_IES1_TAMS`, and `testsuite/Test_m2p0_feh+0p0_vzams150_IES2_TAMS`) among them. A run would reach it only if the extrapolation were switched on in GETW. Intent: none found.

### BURSMIX

Burn–mix substepping over one time step for increasing numbers of substeps, extrapolated to zero substep by [[bsrotmix.f#BSROTMIX|BSROTMIX]]; resets $X$, $Z$ and updates $Y$.
