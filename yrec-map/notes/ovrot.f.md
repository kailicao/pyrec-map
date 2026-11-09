## Explanation

**Purpose.** Sets the convection flags `LCZ` used for rotation and mixing so that they include convective overshoot: it calls [[convec.f#CONVEC|CONVEC]], which finds the mixed zones with overshoot, and marks every shell in a mixed zone convective and every shell in a radiative zone not.

**How it fits.**
- **Inputs:** the model (`HCOMP`, `HD`, `HP`, `HR`, `HS`, `HT`), the Schwarzschild flags `LC` and `M`.
- **Who calls it:** [[getw.f#GETW|GETW]], [[hpoint.f#HPOINT|HPOINT]], [[midmod.f#MIDMOD|MIDMOD]] and [[starin.f#STARIN|STARIN]].
- **What it calls:** [[convec.f#CONVEC|CONVEC]] (which in turn calls [[oversh.f#OVERSH|OVERSH]]).
- **Outputs:** `LCZ`, and the zone lists `MRZONE`, `MXZONE`, `NRZONE`, `NZONE`. The edges `JCORE`, `JENV` and the zones without overshoot `MXZON0` are local and dropped.

**The method.** The radiative zones are marked first, then the mixed zones ([[#L24-L34]]); a check `I .GT. 0` guards `LCZ(I) = .FALSE.` (comment: "to avoid runtime error"). The check cannot fail: CONVEC gives every radiative region it counts a lower edge of at least 1 ([[convec.f#L183-L205]]), and the loop counts up from it (settled from the code, Nov 9, 2026: [[#L25-L27]]). The out-of-range index is more likely CONVEC's bug 1 ([[convec.f#b1]]), which leaves the top radiative region's upper edge stale, possibly beyond `M` (from an earlier call with more shells), which the check does not catch; the loop over `MXZONE` has no check either. That bug also makes the first loop mark shells 1 to `M` radiative, which is harmless here, since the second loop then marks the mixed zones.

**Changed since `rp_1`.** Declarations only: `JSON` from `DIMENSIONS_MOD`, `IMPLICIT NONE`.
