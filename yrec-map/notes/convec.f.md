## Explanation

**Purpose.** This file finds the convective and radiative regions of a model: the boundaries of each convection zone, without and with overshoot, the edge of the convective core (`JCORE`) and the base of the convective envelope (`JENV`), and the radiative regions between them. Its header stresses that overshoot here means "overmixing": overshoot shells are mixed with the convection zone but keep the radiative temperature gradient.

**How it fits.**
- **Inputs:** the arguments `LC` (convective or not, per shell, from [[coefft.f#COEFFT|COEFFT]] via the structure solution; set by the Schwarzschild test $\nabla_\mathrm{rad} > \nabla_\mathrm{ad}$ in [[tpgrad.f#TPGRAD|TPGRAD]], so composition gradients play no part in the zone edges unless semiconvection, `LSEMIC` in [[sconvec.f#SCONVEC|SCONVEC]], is on), `M`, and the model (`HCOMP`, `HD`, `HP`, `HR`, `HS`, `HT`), which only [[oversh.f#OVERSH|OVERSH]] uses; the overshoot switches `LOVSTC`, `LOVSTE`, `LOVSTM` (core, envelope, intermediate zones) in [[nmlpar_mod.f#NMLPAR_MOD|`NMLPAR_MOD`]]; the unit `ISHORT` from [[iounits_mod.f#IOUNITS_MOD|`IOUNITS_MOD`]].
- **Who calls it:** the main program ([[main.f#(file level)|main.f]]), [[mix.f#MIX|MIX]], [[getw.f#GETW|GETW]] and [[ovrot.f#OVROT|OVROT]].
- **What it calls:** [[oversh.f#OVERSH|OVERSH]], which moves the zone edges outward by the overshoot distance.
- **Outputs:** `MXZON0`, `NZONE0` (the zones without overshoot), `MXZONE`, `NZONE` (with overshoot, after merging zones that overlap), `MRZONE`, `NRZONE` (the radiative regions), `JCORE`, `JENV` (both before overshoot). [[mix.f#MIX|MIX]] uses the zones to treat burning in radiative and convective regions differently; [[ovrot.f#OVROT|OVROT]] (which sets the flags `LCZ` from them), [[rotmix.f#ROTMIX|ROTMIX]] and [[midmod.f#MIDMOD|MIDMOD]] also loop over the radiative regions; `JENV` is used throughout the code. The callers take the zones with overshoot, `MXZONE`, for burning and mixing; `MXZON0` (the formal zones) serves only inside, in OVERSH (its printout, and the `LINSTB` test of whether overshoot moved an edge), and `JCORE`, `JENV` are the formal edges.

**The method.**
1. Scan the shells for runs of convective shells; a run of a single shell is ignored (the test `I1.NE.I-1`). At most 11 zones: as soon as the 11th is stored, the routine prints "TOO MANY MIX ZONES" (whether or not more follow) and stops the scan.

    > **Question** ([[#L96-L103]]). **One-shell zones.** A single convective shell is treated as radiative (the test `I1.NE.I-1`). Is this a deliberate filter against noise in `LC`?
2. No zone: `JCORE = 1`, `JENV = M`, one radiative region. One zone covering the whole star: fully convective, `JCORE = JENV = 1`, `NRZONE = 0` (`MRZONE` is left as it was; every reader loops from 1 to `NRZONE`, so none reads it), and overshoot and merging are skipped.
3. `JCORE` is the top of a zone starting at shell 1; `JENV` the bottom of a zone ending at shell `M`.

    **The header names the zones in the reverse order.** It says `JCORE` and `JENV` are "THE EDGES OF THE SURFACE AND CENTRAL CONVECTION ZONES RESPECTIVELY" ([[#L67-L69]]), but the code makes `JCORE` the core's outer edge, from `MXZONE(1,2)`, and `JENV` the envelope's base, from `MXZONE(NZONE,1)` ([[#L129-L150]]), so the header should say "central and surface."
4. If any overshoot switch is on, call OVERSH, then merge zones whose (overshot) edges now meet, with a message to `ISHORT`.
5. The radiative regions: below the first zone, between zones, above the last (but see bug 1).

**Changed since `rp_1`.** Declarations only: COMMON blocks to modules, `IMPLICIT NONE`.

## Bugs, by priority

1. **(harmless in the runs)** **The upper edge of the last radiative region is written to the first.** ([[#L200-L205]]) For a radiative region above the last convection zone, the code sets `MRZONE(1,2) = M` instead of `MRZONE(NRZONE,2) = M`. When that region is the only one (a convective core under a radiative envelope), the two are the same element and nothing goes wrong. When it is the second or a later one (a radiative surface and at least two radiative regions, for example a radiative core, a thin convection zone, and a radiative surface, or a convective core, an intermediate convection zone, and a radiative surface), the top region's upper edge keeps an old value and the first region's upper edge becomes `M`. What follows: [[mix.f#MIX|MIX]] then burns the shells of the convection zones above the first region one by one, as radiative (up to the `TCUT(1)` cutoff, [[mix.f#L249-L261]]), before it treats each zone as a unit, which recomputes those shells from the start of the step (see below); [[rotmix.f#ROTMIX|ROTMIX]] and [[midmod.f#MIDMOD|MIDMOD]] treat those shells as radiative too ([[ovrot.f#OVROT|OVROT]] sets the convective flags after the radiative ones, so its `LCZ` comes out right). On the default path whenever a model has a radiative surface and two or more radiative regions.

    **A possible fix:**

    ```diff
    --- a/src/convec.f
    +++ b/src/convec.f
    @@ -198,10 +198,13 @@
       110    CONTINUE
           ENDIF
     C CHECK FOR A RADIATIVE REGION ABOVE THE LAST CONVECTION ZONE.
    +C 11/09/26 KC via Claude
    +C code changed to set the upper edge of the last radiative region,
    +C MRZONE(NRZONE,2), instead of that of the first.
           IF(MXZONE(NZONE,2).LT.M)THEN
              NRZONE = NRZONE + 1
              MRZONE(NRZONE,1) = MXZONE(NZONE,2) + 1
    -         MRZONE(1,2) = M
    +         MRZONE(NRZONE,2) = M
           ENDIF
      9999 CONTINUE
     
    ```

    **Checked by running YREC** (Nov 9, 2026, the counts of `testsuite/Test_m1p0feh+0p0GS98_base_HeIgnite` repeated on Nov 10 with a private start model; a line added at each suspected path counted how often it was taken, the outputs otherwise unchanged): Of 34 runs (26 of YREC's cases, from a 0.04 $M_\odot$ brown dwarf and the solar models to 9 $M_\odot$, rotation, and helium burning, and 8 made-up ones), 7 took this branch, and in 3 the region above the last zone was the second or a later one, so the wrong element was written: 3,344 times in `testsuite/Test_m9p0feh+0p0GS98_base_TAHB`, 2,752 in `testsuite/Test_m1p0feh+0p0GS98_base_HeIgnite`, and 264 in `sample_cases/UpperMS/Sample_m9p0feh+0p0GS98_none_TAHB`, with up to 4 radiative regions. With the fix, the 9 $M_\odot$ helium-burning case's track and `.store` file are identical to the unfixed run's (4,582 models, the same end age), where a null change (nearly every opacity, all with $3 \le \log T \le 9$ and $-6 \le \log\rho \le 9.75$, times $1 + 10^{-10}$) moves $\log L$ by up to 0.0988 dex. The reason is in MIX: The sweep of the first region stops for all regions once $T$ falls below `TCUT(1)` ([[mix.f#L249-L260]]), and [[kemcom.f#KEMCOM|KEMCOM]] starts every shell and zone from the start-of-step abundances `HCOMPP` ([[kemcom.f#L109]]; [[kemcom.f#L117]]), so each zone's own call ([[mix.f#L266-L273]]) overwrites what the sweep wrote into its shells; ROTMIX has the same lines ([[rotmix.f#L118-L142]]). It is a wrong element, with no effect on the results today.

2. **(changes results, small)** **Checked by KC** (Nov 10, 2026). **A merger keeps the upper zone's top.** ([[#L161-L173]]) When a zone's top reaches the next zone's bottom after overshoot, the merged zone takes the bottom of zone $j$ and the top of zone $j+1$ (`MXZONE(J+1,1) = MXZONE(J,1)`, then the list is shifted). Core overshoot extends only zone 1's top ([[oversh.f#OVERSH|OVERSH]]), which can pass the top of a thin zone above it when that zone has no overshoot of its own (`LOVSTM` off); the merged zone then ends at the thin zone's top, below the overshoot edge just found, and the shells between are left out of the core's mixed region. The merger after semiconvection, [[sconvec.f#b1]], has the same flaw. With `LOVSTC` (on in many of YREC's cases, such as `testsuite/Test_m9p0feh+0p0GS98_base_TAHB` and `testsuite/Test_m2p0_feh+0p0_vzams150_IES1_TAMS`) and a thin convection zone just above the overshot core.

    **A possible fix:**

    ```diff
    --- a/src/convec.f
    +++ b/src/convec.f
    @@ -164,7 +164,10 @@
          *              MXZONE(J+1,2)
        93    FORMAT(2X,'CONVECTION ZONES MERGED DUE TO OVERSHOOT'/2X,
          *          'OLD',2('[',I3,'-',I3,']'),' NEW','[',I3,'-',I3,']')
    +C 11/10/26 KC via Claude
    +C code changed to keep the higher of the two tops when two zones merge.
              MXZONE(J+1,1) = MXZONE(J,1)
    +         MXZONE(J+1,2) = MAX(MXZONE(J,2),MXZONE(J+1,2))
              DO 90 K = J,NZONE-1
                 DO 95 J2 = 1,2
                    MXZONE(K,J2) = MXZONE(K+1,J2)
    ```

    **How the code itself shows it.** The merger's own message names the new zone `MXZONE(J,1)`, `MXZONE(J+1,2)` ([[#L163-L166]]), and in the run it printed `OLD[  1-170][167-168] NEW[  1-168]`: Zone 1's top, shell 170, lies above the whole of zone 2, yet the merged zone ends at 168. The test for a merger, `IF(MXZONE(J,2).GE.MXZONE(J+1,1))` ([[#L161]]), compares zone $j$'s top with zone $j+1$'s bottom only, and the shift `MXZONE(K,J2) = MXZONE(K+1,J2)` ([[#L168-L172]]) then drops zone $j$'s top, whatever it was. That a zone's top can pass the next zone's top comes from OVERSH: For a convective core it overshoots upward only (`LFLAGU = .TRUE.`, `LFLAGD = .FALSE.`, [[oversh.f#L78-L81]]), moving the top to the last shell within the overshoot distance, `MXZONE(I,2) = J - 1` ([[oversh.f#L148-L164]]), however many shells that passes, while an intermediate zone overshoots only with `LOVSTM` (`IF(.NOT.LOVSTM)GOTO 100`, [[oversh.f#L105-L108]]).

    **Checked by running YREC** (Nov 10, 2026; a line added at each suspected path counted how often it was taken, the outputs otherwise unchanged): In `testsuite/Test_m9p0feh+0p0GS98_base_TAHB` (core helium burning), 22 of the 130 mergers cut the core's overshot top, at shells 169 to 181, back by one or two shells, to 168 to 180 (for example `OLD[  1-170][167-168] NEW[  1-168]` in the `.short` file, whose 22 such lines agree with the count), from just after model 1448 (0.03021 Gyr) on. With the fix, the first difference comes at the first such merger, as it should; to 0.0303 Gyr (about 110 models), $\log L$ moves by up to $1.45\times10^{-3}$ dex, against $7.0\times10^{-6}$ for a null change (nearly every opacity, all with $3 \le \log T \le 9$ and $-6 \le \log\rho \le 9.75$, times $1 + 10^{-10}$), about 200 times as much. Later in the run the null change itself grows, to $3.4\times10^{-3}$ dex by 0.0305 Gyr and 0.099 dex over the whole run (4,795 models instead of 4,582; with the fix, 4,585), so the effect over the whole track cannot be separated from noise; the test suite's 2% test fails on the `.track`, `.short`, and `.store` files for both. In `testsuite/Test_solarGS98_allard` no zones merged. Intent: none found.

### CONVEC

Finds the convection zones (without and with overshoot, merging overlaps), the radiative regions between them, and `JCORE`, `JENV`.
