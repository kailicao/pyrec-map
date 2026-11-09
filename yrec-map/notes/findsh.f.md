## Explanation

**Purpose.** `FINDSH` locates, in a model, the outer edge of a central convection zone, the inner edge of a surface convection zone, and, once the core's hydrogen falls below a threshold, the beginning, middle and end of the hydrogen-burning shell. Its comment lists a planned addition ("TO BE ADDED"): finding the exact edges of the convection zones and adding points there.

**How it fits.**
- **Who calls it:** the main program ([[main.f#(file level)|main.f]]) and [[rscale.f#RSCALE|RSCALE]].
- **Inputs:** `HCOMP` (abundances; row 1 is $X$), `HL` (luminosity in solar units), `LC` (convective flags), `M` (number of points).
- **Outputs:** `JCORE` (outermost point of the convective core; 1 if none), `JENV` (innermost point of the surface convection zone; `M` if none), `LSHELL` (a hydrogen shell exists), and `JXBEG`, `JXMID`, `JXEND` (the shell's start, middle and end).
- **Modules:** [[nmlpar_mod.f#NMLPAR_MOD|`NMLPAR_MOD`]], for `ATIME(1)` (formerly in `/CTLIM/`), the central $X$ below which the star has a shell rather than a core (set in [[parmin.f#PARMIN|PARMIN]]).

**The method.**
1. **Shell** (if $X_\mathrm{c} \le$ `ATIME(1)`): going outward, `JXBEG` counts the points with $X \le$ `ATIME(1)`, `JXMID` also those with $X \le X_\mathrm{surf}/2$; the shell ends (`JXEND`) at the first point where $L_i - L_{i-1} < 10^{-5}L_\mathrm{surf}$ or $X_\mathrm{surf} - X_i < 10^{-5}$. The difference `HL(I) - HL(I-1)` would read `HL(0)` at the centre, which the compiler flags, but at `I = 1` the first test always holds, since $X_\mathrm{c} \le$ `ATIME(1)` there, so `HL(0)` is never read (settled from the code, Nov 9, 2026: [[#L80]]; [[#L85-L92]]).

    > **Question** ([[#L85-L91]]). **The shell's middle and end.** `JXMID` counts points rather than recording an index; it equals the first point with $X > X_\mathrm{surf}/2$ only if the composition increases monotonically outward (and likewise `JXBEG`, the first point with $X >$ `ATIME(1)`, as the header says). Is that guaranteed?

    > **Question** ([[#L57-L59]]; [[#L72-L73]]; [[#L83]]). **A comment's variable.** The comments speak of `ENDSHL`; the code uses `DLMIN` and `XLEND` = `DLMIN*HL(M)`. Should the comments name `XLEND`?
2. **Core:** `JCORE` is the last point of the run of convective points from the centre.
3. **Envelope:** `JENV` is the first point of the run of convective points from the surface.
4. For a fully convective star (`JENV` = 1), `JCORE` is set to 1, "because JCORE is used in computing the nuclear timestep, and putting it at the surface does strange things".

**Changed since `rp_1`.** Declarations only: COMMON blocks to modules, `IMPLICIT NONE`.

### FINDSH

Finds the convective core's edge, the surface convection zone's base, and the hydrogen shell's start, middle and end (method above).
