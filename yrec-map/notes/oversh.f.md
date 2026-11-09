## Explanation

**Purpose.** Extends each convection zone by convective overshoot. Its comment: it "computes the local pressure scale height at both edges of a given convective region and locates the boundaries of overshoot regions based on the user-specified extent."

**How it fits.**
- **Inputs:** the model (`HCOMP`, `HD`, `HP`, `HR`, `HS`, `HT`, `M`), the convection zones `MXZONE` and `MXZON0` (without overshoot) and `NZONE`; from `NMLPAR_MOD` the switches `LOVSTC`, `LOVSTE`, `LOVSTM` (core, envelope, intermediate zones), the extents `ALPHAC`, `ALPHAE`, `ALPHAM` (in pressure scale heights), `LOVMAX` with `BETAC`, and the flags `LROT` and `LINSTB`.
- **Who calls it:** only [[convec.f#CONVEC|CONVEC]].
- **What it calls:** [[hsubp.f#HSUBP|HSUBP]], the pressure scale height at a zone's edge.
- **Outputs:** `MXZONE` with the new edges (CONVEC then merges zones that overshoot made overlap); `IOV1`, `IOV2` in `DPMIX_MOD` ("store position of overshoot for adiabatic extension", DBG 8/94): the new and the formal lower edge of a zone overshooting downward. With `LADOV`, [[tpgrad.f#TPGRAD|TPGRAD]] gives every radiative point with index `IOVIM` between them the adiabatic gradient, $\nabla = \nabla_\mathrm{ad}$ (`IOVIM` is the point being computed, set by [[coefft.f#COEFFT|COEFFT]] and [[physic.f#PHYSIC|PHYSIC]]). The zones with and without overshoot are printed to `ISHORT`, four to a line; more zones continue on new lines without the label, by Fortran's reuse of the format ([[#L170-L176]]).

> **Question** ([[#L61-L62]]; [[#L143-L145]]). **`IOV1`, `IOV2` for one zone only.** They are reset to −1 and then overwritten by every zone with downward overshoot, so they keep only the last such zone (usually the envelope). With an intermediate zone and an envelope, the intermediate zone's downward overshoot does not get the adiabatic gradient of `LADOV`; nor does any upward overshoot (above a core or an intermediate zone), since only the downward branch sets them. Is this intended (`LADOV` meant for the envelope's base only)?

**The method.** For each zone, by type:
- **Core** (starts at the centre): overshoot upward by $d = \alpha_c H_p$; with `LOVMAX`, $d = \min(\alpha_c H_p,\ \beta_c\, r_\mathrm{edge})$, which limits overshoot above small convective cores "as per Woo & Demarque 2001". A fully convective star gets no overshoot: OVERSH has an exit for it that prints the first zone and returns ([[#L70-L76]]), but it is never reached, since [[convec.f#CONVEC|CONVEC]], its only caller, returns before calling OVERSH when one zone covers the whole star ([[convec.f#L131-L138]]) (unused?).
- **Envelope** (reaches the surface): downward by $\alpha_e H_p$.
- **Intermediate:** both ways by $\alpha_m H_p$, each with the scale height at that edge.

Here $H_p = P r^2/(\rho\, G m)$ is the pressure scale height at the zone's formal (Schwarzschild) edge, from HSUBP, in cm, like $d$ and $r$. `LOVMAX` (off by default), which the documentation calls a test "to avoid pathologies in overshoot of small cores", caps the distance at $\beta_c r_\mathrm{edge}$ (`BETAC`, "maximum overshoot in fraction of physical size of core"). The new edge is the last model point within $d$ in radius of the formal edge: downward, the innermost point with $r \ge r_\mathrm{edge} - d$; upward, the outermost point with $r \le r_\mathrm{edge} + d$; or the centre or surface if $d$ reaches beyond. For rotating models with `LINSTB`, the zone is widened by one more point if overshoot moved no edge (MHP 11/91), so that each overshoot region has at least one radiative point.

> **Question** ([[#L82-L92]]). **Step overshoot, and its default near small cores.** Overshoot here is a step (full mixing over $\alpha H_p$, $H_p$ at the formal edge), with no exponential or diffusive option, as the YREC paper (§2.3.3) says ("a step overshoot model"). Near the centre $H_p$ should grow without bound as $m \to 0$ (with $m \propto r^3$, $H_p \propto 1/r$), so that $\alpha_c H_p$ above a small core could exceed the core's radius unless `LOVMAX` is set: Are these the "pathologies" the documentation means? `LOVMAX` is off by default. Is the uncapped step meant to be the default for stars with small convective cores?

**From YREC's documentation.** [Physics Options](https://yrec.readthedocs.io/en/latest/namelist_physics.html) (Convective mixing & overshoot): `LOVSTC` with `ALPHAC` overshoots convective cores, by `ALPHAC` pressure scale heights; unless `LADOV` is on, this is overmixing only and does not change the thermal structure. `LOVMAX` (checked only with `LOVSTC`) is an alternative test that avoids pathologies above small cores, limiting overshoot to the fraction `BETAC` (default 0.15) of the core's size. `LOVSTE` with `ALPHAE` overshoots the envelope; `LOVSTM` with `ALPHAM` overshoots intermediate convection zones above and below, which the documentation recommends leaving off ("needs to be checked"). All extents default to 0. `LADOV` is listed among the experimental options.

**Changed since `rp_1`.** Declarations only: COMMON blocks to modules (the settings of `/DPMIX/` and `/ROT/` to `NMLPAR_MOD`, `IOV1`, `IOV2` to `DPMIX_MOD`, `/CONST1/` to `CONSTANTS_MOD`, `/LUOUT/` to `IOUNITS_MOD`), `JSON` from `DIMENSIONS_MOD`, `IMPLICIT NONE`.

### OVERSH

Moves each convection zone's edges by $\alpha H_p$ (core, envelope or intermediate parameters), optionally limited by $\beta_c r$ for convective cores.
