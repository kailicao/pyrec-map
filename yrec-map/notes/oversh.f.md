## Explanation

**Purpose.** Extends each convection zone by convective overshoot. Its comment: it "computes the local pressure scale height at both edges of a given convective region and locates the boundaries of overshoot regions based on the user-specified extent."

**How it fits.**
- **Inputs:** the model (`HCOMP`, `HD`, `HP`, `HR`, `HS`, `HT`, `M`), the convection zones `MXZONE` and `MXZON0` (without overshoot) and `NZONE`; from `NMLPAR_MOD` the switches `LOVSTC`, `LOVSTE`, `LOVSTM` (core, envelope, intermediate zones), the extents `ALPHAC`, `ALPHAE`, `ALPHAM` (in pressure scale heights), `LOVMAX` with `BETAC`, and the flags `LROT` and `LINSTB`.
- **Who calls it:** only [[convec.f#CONVEC|CONVEC]].
- **What it calls:** [[hsubp.f#HSUBP|HSUBP]], the pressure scale height at a zone's edge.
- **Outputs:** `MXZONE` with the new edges (CONVEC then merges zones that overshoot made overlap); `IOV1`, `IOV2` in `DPMIX_MOD` ("store position of overshoot for adiabatic extension", DBG 8/94): the new and the formal lower edge of a zone overshooting downward. With `LADOV`, [[tpgrad.f#TPGRAD|TPGRAD]] gives every radiative point with index `IOVIM` between them the adiabatic gradient, $\nabla = \nabla_\mathrm{ad}$ (`IOVIM` is the point being computed, set by [[coefft.f#COEFFT|COEFFT]] and [[physic.f#PHYSIC|PHYSIC]]). The zones with and without overshoot are printed to `ISHORT`.

**The method.** For each zone, by type:
- **Core** (starts at the centre): overshoot upward by $d = \alpha_c H_P$; with `LOVMAX`, $d = \min(\alpha_c H_P,\ \beta_c\, r_\mathrm{edge})$, which limits overshoot above small convective cores "as per Woo & Demarque 2001". A fully convective star gets no overshoot.
- **Envelope** (reaches the surface): downward by $\alpha_e H_P$.
- **Intermediate:** both ways by $\alpha_m H_P$, each with the scale height at that edge.

Here $H_P = P r^2/(\rho\, G m)$ is the pressure scale height at the zone's formal (Schwarzschild) edge, from HSUBP, in cm, like $d$ and $r$. The new edge is the last model point within $d$ in radius of the formal edge: downward, the innermost point with $r \ge r_\mathrm{edge} - d$; upward, the outermost point with $r \le r_\mathrm{edge} + d$; or the centre or surface if $d$ reaches beyond. For rotating models with `LINSTB`, the zone is widened by one more point if overshoot moved no edge (MHP 11/91), so that each overshoot region has at least one radiative point.

**Changed since `rp_1`.** Declarations only: COMMON blocks to modules (the settings of `/DPMIX/` and `/ROT/` to `NMLPAR_MOD`, `IOV1`, `IOV2` to `DPMIX_MOD`, `/CONST1/` to `CONSTANTS_MOD`, `/LUOUT/` to `IOUNITS_MOD`), `JSON` from `DIMENSIONS_MOD`, `IMPLICIT NONE`.

## Questions for the experts

1. **`IOV1`, `IOV2` for one zone only.** They are reset to −1 and then overwritten by every zone with downward overshoot, so they keep only the last such zone (usually the envelope). With an intermediate zone and an envelope, the intermediate zone's downward overshoot does not get the adiabatic gradient of `LADOV`; nor does any upward overshoot (above a core or an intermediate zone), since only the downward branch sets them. Intended (`LADOV` meant for the envelope's base only)?
2. **The output format.** The print formats hold four zones per line; more zones continue on new lines without their label. Cosmetic.
3. **The fully convective exit.** It prints only the first zone and returns before the "with overshoot" line, which tools that parse `ISHORT` may expect.

### OVERSH

Moves each convection zone's edges by $\alpha H_P$ (core, envelope or intermediate parameters), optionally limited by $\beta_c r$ for convective cores.
