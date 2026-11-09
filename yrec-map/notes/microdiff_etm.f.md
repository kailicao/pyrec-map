## Explanation

**Purpose.** "Equal to model": the last step of [[microdiff.f#MICRODIFF|MICRODIFF]]. It interpolates the changes in abundance from the equally spaced grid back to the model points, applies them to `HCOMP`, recomputes helium, and converts the variables changed by [[microdiff_setup.f#MICRODIFF_SETUP|MICRODIFF_SETUP]] back to cgs units.

**How it fits.**
- **Inputs:** the equal grid radii `ER`, the changes `EDELX`, `EDELZ`, `EDELLI` from [[microdiff_run.f#MICRODIFF_RUN|MICRODIFF_RUN]], `IBEGIN`, `IEND`, `NPT`, and the conversion factors in `CONFAC_MOD` (written by `MICRODIFF_SETUP`).
- **Who calls it:** only `MICRODIFF`.
- **What it calls:** [[intrp2.f#INTRP2|INTRP2]], for four-point Lagrange weights.
- **Outputs:** `HCOMP` updated in place; `HRU`, `HTU`, `HS1`, `HQPR`, `DT` and `STOT` converted back ([[#L165-L172]]), though [[microdiff.f#MICRODIFF|MICRODIFF]] passes its local `HRU` and `HTU` and copies of the other four, and returns right after the call ([[microdiff.f#L112-L117]]; [[microdiff.f#L242-L244]]): unused?
- **Modules:** `CONFAC_MOD`, `NMLPAR_MOD` (`LDIFZ`, `LDIFLI`), `DIMENSIONS_MOD` (`JSON`).

**The method.**
1. **Central region** (points `1..IBEGIN`, the convective core or the hydrogen-exhausted centre): the change at the first grid point is added to each point: $X \to \max(X + \Delta X_1, 0)$, the light elements likewise floored at zero, and $Z \to \min(Z + \Delta Z_1,\ 1 - X - X_3)$.
2. **Radiative interior** (points `IBEGIN+1..IEND-1`): the change is interpolated with four-point Lagrange weights $w_k$ over the grid points around the model radius, $\Delta X(r) = \sum_k w_k\,\Delta X_{k_0+k-1}$, and $X \to \min(X + \Delta X, 1 - Z - X_3)$.
3. **Envelope** (points `IEND..M`): the change at the last grid point is added, with $X$ capped as above and $Z$ floored at zero.

    > **Question** ([[#L47-L48]]; [[#L104-L111]]; [[#L135-L142]]). **The guard comment.** The comment says the failsafes guard "against negative X and Z>1 respectively", and so they do in the centre ($X \ge 0$, $Z \le 1 - X - X_3$); but in the interior $X$ and $Z$ are both capped from above, and in the envelope $X$ is capped from above and $Z$ floored at zero. Which guards are intended where?

4. **Metals** are scaled as a whole: with $Z' = Z + \Delta Z$ (capped at $1 - X - X_3$ in the centre and the interior), the individual metal rows 5–11 of `HCOMP` (¹²C, ¹³C, ¹⁴N, ¹⁵N, ¹⁶O, ¹⁷O, ¹⁸O, as STARIN names them) are multiplied by $Z'/Z$.
5. **Helium** follows from closure: $Y = 1 - X - Z - X_3$, where $X_3$ is ³He, `HCOMP(4,·)` ([[starin.f#STARIN|STARIN]] fills it from `XHE3_INI`).

**Changed since `rp_1`.** Declarations only: COMMON blocks to modules, `IMPLICIT NONE`.

**Changed since `a8a5950`.** The file is unchanged, but [[microdiff_mte.f#MICRODIFF_MTE|`MICRODIFF_MTE`]] now gives the grid at least 4 points, so `K0` stays within the grid; this settles former question 5.

## Bugs, by priority

1. **(a)** **Light elements in the interior and the envelope are not floored at zero.** ([[#L66-L74]]; [[#L122-L131]]; [[#L156-L163]]) The light elements (`HCOMP(13..15,·)`) are floored at zero only in the centre (`MAX(…,XMINIM)`); in the interior (`HCOMP(II,I) + DXMOD`, with `DXMOD` from four-point Lagrange interpolation, which can overshoot) and in the envelope the change is added with no floor. What follows: where an element is nearly depleted, its abundance can become negative and stays in the model. Only with `LNEWDIF` and `LDIFLI` (both off by default; the test suite's settling decks set them); whether a run produces a negative value was not traced. Read from the code, not run. **A possible fix:**

    ```fortran
    C 11/09/26 KC via Claude
    C code changed to floor the light elements at zero in the interior
    C and the envelope too, as in the centre.
                   HCOMP(II,I) = MAX(HCOMP(II,I) + DXMOD,0.0D0)
    ...
                   HCOMP(II,I)=MAX(HCOMP(II,I) + EDELLI(KK,NPT),0.0D0)
    ```

2. **(b)** **Division by zero where $Z = 0$.** ([[#L53]]; [[#L112]]; [[#L143]]) `ZZ2 = ZZ/HCOMP(3,I)` divides by zero at a point with $Z = 0$; with IEEE arithmetic it gives an infinity or NaN rather than a stop, and the metal rows 5–11 (zero there) become NaN. Only with `LNEWDIF` and `LDIFZ` and a model with $Z = 0$ somewhere (a metal-free model). Read from the code, not run. **A possible fix** (the same at the three places; where $Z = 0$ the rows 5–11 stay zero):

    ```fortran
    C 11/09/26 KC via Claude
    C code changed to avoid a division by zero where Z = 0.
                IF(HCOMP(3,I).GT.0.0D0)THEN
                   ZZ2 = ZZ/HCOMP(3,I)
                ELSE
                   ZZ2 = 1.0D0
                ENDIF
    ```
