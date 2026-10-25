## Explanation

**Purpose.** "Equal to model": the last step of [[microdiff.f#MICRODIFF|MICRODIFF]]. It interpolates the changes in abundance from the equally spaced grid back to the model points, applies them to `HCOMP`, recomputes helium, and converts the variables changed by [[microdiff_setup.f#MICRODIFF_SETUP|MICRODIFF_SETUP]] back to cgs units.

**How it fits.**
- **Inputs:** the equal grid radii `ER`, the changes `EDELX`, `EDELZ`, `EDELLI` from [[microdiff_run.f#MICRODIFF_RUN|MICRODIFF_RUN]], `IBEGIN`, `IEND`, `NPT`, and the conversion factors in `/CONFAC/` (written by `MICRODIFF_SETUP`).
- **Who calls it:** only `MICRODIFF`.
- **What it calls:** [[intrp2.f#INTRP2|INTRP2]], for four-point Lagrange weights.
- **Outputs:** `HCOMP` updated in place; `HRU`, `HTU`, `HS1`, `HQPR`, `DT` and `STOT` converted back.
- **COMMON blocks:** `/CONFAC/`, `/GRAVS3/` (`LDIFZ`), `/GRAVS4/` (`LDIFLI`).

**The method.**
1. **Central region** (points `1..IBEGIN`, the convective core or the hydrogen-exhausted centre): the change at the first grid point is added to each point: $X \to \max(X + \Delta X_1, 0)$, the light elements likewise floored at zero, and $Z \to \min(Z + \Delta Z_1,\ 1 - X - X_4)$.
2. **Radiative interior** (points `IBEGIN+1..IEND-1`): the change is interpolated with four-point Lagrange weights $w_k$ over the grid points around the model radius, $\Delta X(r) = \sum_k w_k\,\Delta X_{k_0+k-1}$, and $X \to \min(X + \Delta X, 1 - Z - X_4)$.
3. **Envelope** (points `IEND..M`): the change at the last grid point is added, with $X$ capped as above and $Z$ floored at zero.
4. **Metals** are scaled as a whole: with $Z' = Z + \Delta Z$ (capped at $1 - X - X_4$ in the centre and the interior), the individual metal rows 5–11 of `HCOMP` (¹²C, ¹³C, ¹⁴N, ¹⁵N, ¹⁶O, ¹⁷O, ¹⁸O, as STARIN names them) are multiplied by $Z'/Z$.
5. **Helium** follows from closure: $Y = 1 - X - Z - X_4$, where $X_4$ is `HCOMP(4,·)`, ³He ([[starin.f#STARIN|STARIN]] fills it from `XHE3_INI`).

**KC's changes.** 2025-05-30: `CSLIGHT` declared `INTEGER` (fixing `-Wconversion`).

## Questions for the experts

1. **Light elements in the interior are not floored.** Light-element abundances are floored at zero only in the centre; in the interior (`HCOMP(II,I) + DXMOD`) and the envelope the change is added with no floor. Can a light element become negative where it is nearly depleted?
2. **Division by zero.** `ZZ2 = ZZ/HCOMP(3,I)` fails if $Z = 0$ at a point (a metal-free model with `LDIFZ` on).
3. **The guard comment.** The comment says the failsafes guard "against negative X and Z>1 respectively", but in the interior and envelope $X$ is capped from above and $Z$ floored at zero (envelope) or capped (interior). Which guards are intended where?
4. **`HRU` and `HTU`.** They are converted back, but `MICRODIFF` does not use them afterwards (they are its local arrays). Harmless; is it needed?
5. **Very small grids.** In the interior loop, `K0 = MIN(MAX(J-2,1), NPT-3)`. For `NPT = 2`, which [[microdiff_mte.f#MICRODIFF_MTE|MICRODIFF_MTE]] allows, `K0 = -1`; the "JVS fix for NPT = 3?" (`IF (K0 .EQ. 0) K0=1`) does not catch it, and the interpolation reads `EDELX(-1)`. For `NPT = 3`, `K0 = 1` and it reads `EDELX(4)`, beyond the grid. Both cases arise only when the radiative region holds very few model points; should they be trapped?
