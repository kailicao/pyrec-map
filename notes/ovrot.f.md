## Explanation

**Purpose.** Sets the convection flags `LCZ` used for rotation and mixing so that they include convective overshoot: it calls [[convec.f#CONVEC|CONVEC]], which finds the mixed zones with overshoot, and marks every shell in a mixed zone convective and every shell in a radiative zone not.

**How it fits.**
- **Inputs:** the model (`HCOMP`, `HD`, `HP`, `HR`, `HS`, `HT`), the Schwarzschild flags `LC` and `M`.
- **Who calls it:** [[getw.f#GETW|GETW]], [[hpoint.f#HPOINT|HPOINT]], [[midmod.f#MIDMOD|MIDMOD]] and [[starin.f#STARIN|STARIN]].
- **What it calls:** [[convec.f#CONVEC|CONVEC]] (which in turn calls [[oversh.f#OVERSH|OVERSH]]).
- **Outputs:** `LCZ`, and the zone lists `MRZONE`, `MXZONE`, `NRZONE`, `NZONE`. The edges `JCORE`, `JENV` and the zones without overshoot `MXZON0` are local and dropped.

**KC's changes.** 2025-05-30: a check `I .GT. 0` added before `LCZ(I) = .FALSE.`, "to avoid runtime error".

## Questions for the experts

1. **Where the bad index comes from.** KC's check guards against an index $I \le 0$, but `CONVEC` sets every zone it counts in `NRZONE` with a lower edge $\ge 1$, so the source is unclear (a stale `NRZONE` or zone list from an earlier call?). A related problem: CONVEC's index error ([[convec.f#CONVEC|CONVEC]], question 1) sets `MRZONE(1,2) = M` instead of `MRZONE(NRZONE,2) = M` for a radiative region above the last convection zone. Here that makes the first loop mark shells 1 to `M` radiative (harmless, since the second loop then marks the mixed zones) and lets the top region run to a stale upper bound, possibly beyond `M`, which the check does not catch. The loop over `MXZONE` has no check either.
