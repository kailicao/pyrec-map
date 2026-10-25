## Explanation

**Purpose.** `FINDSH` locates, in a model, the outer edge of a central convection zone, the inner edge of a surface convection zone, and, once the core's hydrogen falls below a threshold, the beginning, middle and end of the hydrogen-burning shell. Its comment lists a planned addition ("TO BE ADDED"): finding the exact edges of the convection zones and adding points there.

**How it fits.**
- **Who calls it:** the main program ([[main.f#(file level)|main.f]]) and [[rscale.f#RSCALE|RSCALE]].
- **Inputs:** `HCOMP` (abundances; row 1 is $X$), `HL` (luminosity in solar units), `LC` (convective flags), `M` (number of points).
- **Outputs:** `JCORE` (outermost point of the convective core; 1 if none), `JENV` (innermost point of the surface convection zone; `M` if none), `LSHELL` (a hydrogen shell exists), and `JXBEG`, `JXMID`, `JXEND` (the shell's start, middle and end).
- **COMMON blocks:** `/CTLIM/`, for `ATIME(1)`, the central $X$ below which the star has a shell rather than a core (set in [[parmin.f#PARMIN|PARMIN]]; shared with 27 routines).

**The method.**
1. **Shell** (if $X_\mathrm{c} \le$ `ATIME(1)`): going outward, `JXBEG` counts the points with $X \le$ `ATIME(1)`, `JXMID` also those with $X \le X_\mathrm{surf}/2$; the shell ends (`JXEND`) at the first point where $L_i - L_{i-1} < 10^{-5}L_\mathrm{surf}$ or $X_\mathrm{surf} - X_i < 10^{-5}$.
2. **Core:** `JCORE` is the last point of the run of convective points from the centre.
3. **Envelope:** `JENV` is the first point of the run of convective points from the surface.
4. For a fully convective star (`JENV` = 1), `JCORE` is set to 1, "because JCORE is used in computing the nuclear timestep, and putting it at the surface does strange things".

## Questions for the experts

1. **The shell's middle and end.** `JXMID` counts points rather than recording an index; it equals the first point with $X > X_\mathrm{surf}/2$ only if the composition increases monotonically outward. Is that guaranteed?
2. **`HL(I-1)` at the centre.** If `HCOMP(1,1)` exceeds both `ATIME(1)` and `XMID`, which cannot happen when `LSHELL` is set, the loop would read `HL(0)`. Safe as written, but fragile.
3. **A comment's variable.** The comments speak of `ENDSHL`; the code uses `DLMIN` and `XLEND`.

### FINDSH

Finds the convective core's edge, the surface convection zone's base, and the hydrogen shell's start, middle and end (method above).
