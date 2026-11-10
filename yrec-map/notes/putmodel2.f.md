## Explanation

**Purpose.** Writes a stellar model to a text file in the "MODEL2" format (LLP 4/16/03), which YREC can read back as a starting model.

**How it fits.**
- **Inputs:** the model and its global quantities, as arguments: the header values (model number, number of shells `M`, mass, $\log T_\mathrm{eff}$, $\log L$, $\log M$, age, step, inner and outer $\log m$), the physics flags and labels (EOS, atmosphere, opacity, mixture strings), the luminosities by source `TLUMX`, the envelope data (`TRIT`, `TRIL`, `PS`, `TS`, `RS`, `CFENV`), and the shell arrays.
- **Who calls it:** [[wrtlst.f#WRTLST|WRTLST]], for the last model.
- **Who reads its output:** [[starin.f#STARIN|STARIN]], which recognizes the leading `MOD2 ` and calls [[getmodel2.f#GETMODEL2|GETMODEL2]].
- **Output:** the file on unit `IWRITE`; warnings to `ISHORT`.

**The format.** A header line (`MOD2 `, the number format chosen by the age's size); a line of physics flags; a `TLUMX` line of seven luminosities in erg s⁻¹ (pp chains I, II, III, CNO, helium burning, neutrinos, gravitational contraction, by GETYREC7's comment); three `ENV` lines (negative indices if `FTRI < 0`); column titles; then one line per shell: shell, $\log m$, $\log r$, $L$, $\log P$, $\log T$, $\log\rho$, $\Omega$ (unlogged, a change from YREC7 files), the convection flag, and the 15 abundances.

> **Question** ([[#L90-L98]]). **`TLUMX(8)` not written.** The eighth entry is the luminosity of $\alpha$ captures ([[coefft.f#COEFFT|COEFFT]] adds `ECA = EALPCA` to it; [[crrect.f#CRRECT|CRRECT]] counts it with helium burning, `TLUMX(5) + TLUMX(8)`), but only seven are checked, converted, and written, so a model read back has no $\alpha$-capture luminosity. Should the format carry it?


**Design.** If the largest of the luminosities is at most $10^{20}$, they are taken to be in solar units and multiplied by $L_\odot$, in place: the caller's `TLUMX` changes too (bug 1). $L_\odot$ (`CLSUN`) comes from `CONSTANTS_MOD`. The warning for the atmosphere label `' ? '` ([[#L54-L58]]) is never written, since WRTLST, the only caller, never passes that label (settled from the code, Nov 9, 2026: [[wrtlst.f#L93-L106]]).

**Changed since `rp_1`.** Declarations only: `/CONST/` to `CONSTANTS_MOD`, `JSON` from `DIMENSIONS_MOD`, `IMPLICIT NONE`.

## Bugs, by priority

1. **(wrong output)** **Checked by KC** (Nov 10, 2026). **The caller's luminosities are left in erg s⁻¹.** ([[#L90-L97]]) The conversion to erg s⁻¹ is made in place, so after each model, when WRTOUT has called WRTLST ([[wrtout.f#L666-L669]]), the main program's `TLUMX(1..7)` are in erg s⁻¹ while `TLUMX(8)` stays in solar units, until COEFFT recomputes them at the next model. Two readers in between expect solar units. At the start of a kind card that continues the model in memory (`LFIRST(NK)` false: STARIN skips reading a model, [[starin.f#L255-L262]]), HTIMER sums `TLUMX(1..4)` as the hydrogen-burning luminosity "in solar units" ([[main.f#L584-L586]]; [[htimer.f#L133-L134]]), and once the core's hydrogen is below `ATIME(1)`, XTIME divides by it ([[xtime.f#L65]]; [[xtime.f#L74]]), so the first time step of that kind card comes out about $L_\odot \approx 3.85\times10^{33}$ times too short ([[htimer.f#L171-L176]]). And the main program's last `ISNU` output, with `LCALS`, `LSNU`, and `LSOL`, writes `TLUMX(1..4)` and `TLUMX(7)` as "energy generation fractions" ([[main.f#L1228-L1229]]) in erg s⁻¹. Only on these paths (the default is `LFIRST` true for every kind card); how the near-zero step changes the following models was not traced. [[putstore.f#PUTSTORE|PUTSTORE]] converts in place in the same way ([[putstore.f#L243-L249]]).

    **A possible fix** (and the same in PUTSTORE):

    ```diff
    --- a/src/putmodel2.f
    +++ b/src/putmodel2.f
    @@ -23,6 +23,10 @@
           REAL*8 BL,CCCMAX,CFENV,CMIXL,DAGE,DDAGE,FTRI,HCOMP,HD,HL,HP,HR,HS,
          *       HSTOT,HT,OMEGA,PDISK,PS,RS,SMASS,TDISK,TEFFL,TLUMX,TRIL,
          *       TRIT,TS,WMAX
    +C 11/09/26 KC via Claude
    +C code changed to convert a copy of TLUMX, so that the caller's
    +C luminosities stay in solar units.
    +      REAL*8 TLUMXO(7)
           INTEGER I,I0,ISHORT,IWRITE,J,JCORE,JENV,M,MODEL
           LOGICAL*4 LC,LDIFY,LDIFZ,LDISK,LEXCOM,LINSTB,LJDOT0,LOVSTC,LOVSTE,
          *       LOVSTM,LPUREZ,LROT,LSEMIC
    @@ -89,12 +93,15 @@
     
           CCCMAX = DMAX1(TLUMX(1),TLUMX(2),TLUMX(3),TLUMX(4),TLUMX(5),
          *     DABS(TLUMX(6)),TLUMX(7))
    +      DO J = 1,7
    +         TLUMXO(J) = TLUMX(J)
    +      ENDDO
           IF(CCCMAX.LE.1.0D20) THEN
            DO J = 1,7
    -          TLUMX(J) = TLUMX(J) * CLSUN
    +          TLUMXO(J) = TLUMX(J) * CLSUN
              ENDDO
           ENDIF
    -      WRITE(IWRITE,40) (TLUMX(J),J=1,7)
    +      WRITE(IWRITE,40) (TLUMXO(J),J=1,7)
        40 FORMAT('TLUMX',5X,1P7E17.9)
     
     C write ENVELOPE DATA
    ```

    **How the outputs show it.** In `examples/run_standard_solar_model/Test_solarcal_noGS_norot`, the `.snu` file's last line, the "energy generation fractions" of the final model 449 ([[main.f#L1229]]), reads 3.440E+33, 3.686E+32, 2.371E+29, 1.958E+31, and -7.673E+29, the numbers of the `.last` file's `TLUMX` line ([[#L97]]), which is meant to be in erg s⁻¹. The `.track` line of model 449 ([[wrtout.f#L558]]) gives the same five terms (ppI_lsun, ppII_lsun, ppIII_lsun, CNO_lsun, and Egrav_lsun) in solar units: 8.98735537E-001, 9.62952015E-002, 6.19428809E-005, 5.11441212E-003, and -2.00444567E-004. The `.snu` values are these times 3.828×10³³, the case's `CLSUN`.

    **Checked by running YREC** (Nov 9, 2026, the counts of `testsuite/Test_m1p0feh+0p0GS98_base_HeIgnite` repeated on Nov 10 with a private start model; a line added at each suspected path counted how often it was taken, the outputs otherwise unchanged): Of 34 runs (26 of YREC's cases, from a 0.04 $M_\odot$ brown dwarf and the solar models to 9 $M_\odot$, rotation, and helium burning, and 8 made-up ones), 33 took the in-place conversion, after every model: from 10 times in `examples/run_from_seed_to_start/m10000gs98z001000_prems` to 8,571 in `testsuite/Test_m1p0feh+0p0GS98_base_HeIgnite`. Two lines, counted together, tested the two readers that expect solar units: HTIMER's hydrogen-burning luminosity, and the `ISNU` energy fractions. Values above $10^{20}$, so in erg s⁻¹, reached them in 27 runs, once in most, twice in `testsuite/Test_m0p95feh+0p0_GN93_TAHB`, in `examples/run_from_zahb_to_tahb/ZAHB_m0p8feh+0p0_TAHB`, and in YREC's 1 $M_\odot$ helium-burning case run with the AAG21 table, and 7 times in `examples/run_standard_solar_model/Test_solarcal_noGS_norot`, from $5.2\times10^{26}$ to $3.7\times10^{37}$. With the fix, `testsuite/Test_m0p3feh+0p0GS98_scv_ZAMS` gives an identical track, and `Test_solarcal_noGS_norot` differs exactly as for the null change ($\log L$ by up to 0.000322 dex for both): within the noise. In `testsuite/Test_m0p95feh+0p0_GN93_TAHB`, which runs past the core's hydrogen exhaustion to the end of helium burning and where the condition held twice, the track with the fix is identical, models and end age included (the null change moves $\log L$ by up to 1.67e-7 dex); only the `.short` file differs beyond 2%. So the erg luminosity did not change the evolution there. Why (rechecked on Nov 10, 2026, with lines counting HTIMER's reading and the step it gives): Both hits of this case came at the start of a kind card (the second and third), with central $X$ = 0, and each gave a step of about $1.1\times10^{-28}$ yr, through XTIME's shell criterion ([[xtime.f#L74]]). Neither step was used: The second kind card is a rescaling, which does not age the model ([[main.f#L712]]), and the third starts from the model numbered −3 that the rescalings left, so its first three models are relaxed without aging too (`MODEL.GE.0`, [[main.f#L712]]; the step is then made negative, [[main.f#L825]]), and HTIMER's next call ([[main.f#L1055]]), after the luminosities are recomputed in solar units, sets the step the evolution takes. With the fix, HTIMER no longer reads an erg luminosity, and the track is identical again. In `examples/class_exercises/exercise_4/Grid_m4p0feh+0p0GS98_std25_TAMS`, also rerun, the one hit came at the second kind card, whose starting model still burns hydrogen in its core, with central $X$ = 0.72, above `ATIME(1)` ($10^{-3}$); XTIME's core criterion then takes the step from the core's mass and luminosity ([[xtime.f#L65-L69]]), and the hydrogen-burning luminosity only decides whether XTIME is called, which it is in either unit; the other cases were not rerun. The erg step would be used only at a kind card that continues the model in memory, ages its first model, and starts with central $X$ below `ATIME(1)`; none of the runs did. What the runs show is wrong output (the `.short` file; the `ISNU` energy fractions, a file not compared). Intent: The comment "If TLUMX are in solar units, convert to ergs" ([[#L87-L88]]) expects either unit on entry; nothing says the caller's array is meant to change.
