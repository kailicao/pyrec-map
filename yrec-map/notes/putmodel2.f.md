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

1. **(a)** **The caller's luminosities are left in erg s⁻¹.** ([[#L90-L97]]) The conversion to erg s⁻¹ is made in place, so after each model, when WRTOUT has called WRTLST ([[wrtout.f#L666-L669]]), the main program's `TLUMX(1..7)` are in erg s⁻¹ while `TLUMX(8)` stays in solar units, until COEFFT recomputes them at the next model. Two readers in between expect solar units. At the start of a kind card that continues the model in memory (`LFIRST(NK)` false: STARIN skips reading a model, [[starin.f#L255-L262]]), HTIMER sums `TLUMX(1..4)` as the hydrogen-burning luminosity "in solar units" ([[main.f#L584-L586]]; [[htimer.f#L133-L134]]), and once the core's hydrogen is below `ATIME(1)`, XTIME divides by it ([[xtime.f#L65]]; [[xtime.f#L74]]), so the first time step of that kind card comes out about $L_\odot \approx 3.85\times10^{33}$ times too short ([[htimer.f#L171-L176]]). And the main program's last `ISNU` output, with `LCALS`, `LSNU`, and `LSOL`, writes `TLUMX(1..4)` and `TLUMX(7)` as "energy generation fractions" ([[main.f#L1228-L1229]]) in erg s⁻¹. Only on these paths (the default is `LFIRST` true for every kind card); how the near-zero step changes the following models was not traced. [[putstore.f#PUTSTORE|PUTSTORE]] converts in place in the same way ([[putstore.f#L243-L249]]). Read from the code, not run. **A possible fix** (and the same in PUTSTORE):

    ```fortran
    C 11/09/26 KC via Claude
    C code changed to convert a copy of TLUMX, so that the caller's
    C luminosities stay in solar units.
          REAL*8 TLUMXO(7)
    ...
          DO J = 1,7
             TLUMXO(J) = TLUMX(J)
          ENDDO
          IF(CCCMAX.LE.1.0D20) THEN
           DO J = 1,7
              TLUMXO(J) = TLUMX(J) * CLSUN
             ENDDO
          ENDIF
          WRITE(IWRITE,40) (TLUMXO(J),J=1,7)
    ```
