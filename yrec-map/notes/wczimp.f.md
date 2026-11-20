## Explanation

**Purpose.** `WCZIMP` sets the rotation of a convection zone (shells `ISTART`–`IEND`) at fixed total angular momentum, as `wcz.f` (removed since `rp_1`) did, and adds options to impose a rotation profile on the radiative interior below the surface convection zone (JNT, 2015/05/14, copied into this code 2025/09/03–04). `IMPJMOD` ("impose J model," [PARMIN](https://github.com/yreclab/yrec/blob/7be4133/src/parmin.f#L16-L1489)'s comment) chooses: 0, no effect; 1, solid-body rotation; 2, a solid-body core decoupled from the surface convection zone; 3, a solid-body core coupled to it.

**The original date is 2015/05/14.** The header says "copy of 2025/05/14" ([line 40](https://github.com/yreclab/yrec/blob/7be4133/src/wczimp.f#L40)), but the later comments of the same change say "COPY OF 2015/05/14" ([line 52](https://github.com/yreclab/yrec/blob/7be4133/src/wczimp.f#L52)) and "REPLICATING 2015/05/14" ([line 77](https://github.com/yreclab/yrec/blob/7be4133/src/wczimp.f#L77)), and `PARMIN` says "JNT 05/15" ([parmin.f, line 273](https://github.com/yreclab/yrec/blob/7be4133/src/parmin.f#L273)), so the header's 2025 is a typo.

**How it fits.**
- **Who calls it:** [GETROT](getrot.f.md#getrot) and [GETW](getw.f.md#getw) (in place of `WCZ` since 09/25).
- **What it calls:** [SOLID](solid.f.md#solid), for the zone, single shells, or the interior.
- **Inputs and outputs:** the arguments, as in [solid.f](solid.f.md): `HJM`, `OMEGA`, `HI`, `QIW`, `ETA2`, `R0` are updated.
- **Modules:** `NMLPAR_MOD` (the namelist parameters `LSOLID`, `IMPJMOD` and `WALPCZ`, read by `PARMIN`; formerly the COMMON blocks `SBROT` and `ROT`), `CONSTANTS_MOD` (`CLN`; formerly `CONST1`) and `DIMENSIONS_MOD` (`JSON`).

**The method.** With $`m_j`$ = `HS2`, $`j_j`$ = `HJM`, $`I_j`$ = `HI`, $`\alpha`$ = `WALPCZ`, $`r_j = 10^{\texttt{HR}(j)}`$:
- **Solid body** for the zone if $`\alpha \ge 0`$, `LSOLID`, `IMPJMOD = 1`, or the zone is not the surface one (`IEND < M`). Since this test comes first, `IMPJMOD = 2` and `3` take effect only with $`\alpha \lt{} 0`$; with the default `WALPCZ = 0` they act as solid body ([line 48](https://github.com/yreclab/yrec/blob/7be4133/src/wczimp.f#L48)).

    > **Question** ([lines 47–51](https://github.com/yreclab/yrec/blob/7be4133/src/wczimp.f#L47-L51)). **`IMPJMOD` and $`\alpha \ge 0`$.** Since the solid-body test comes first, `IMPJMOD = 2` and `3` have no effect unless `WALPCZ < 0`, and with the default `WALPCZ = 0` the interior is not coupled or decoupled as `PARMIN`'s comment describes. Is that intended, or should `IMPJMOD` be tested first?

- **`IMPJMOD = 2`:** the zone follows $`\Omega_j = \Omega_0 r_j^{\alpha}`$ with $`\Omega_0 = \sum_\mathrm{cz} m_j j_j / \sum_\mathrm{cz} r_j^{\alpha} I_j`$; the interior (shells 1 to `ISTART-1`) is then made a solid body on its own, keeping its own angular momentum.
- **`IMPJMOD = 3`:** the interior and the zone share one angular momentum budget; the interior rotates at the rate of the zone's base:
  
  $$\displaystyle \Omega\_0 = \frac{\sum\_{j \le N} m\_j j\_j}{r\_\mathrm{s}^{\alpha}\sum\_{j \le \mathrm{s}} I\_j + \sum\_{\mathrm{s} \lt{} j \le N} r\_j^{\alpha} I\_j},$$
  
  with $`\mathrm{s}`$ = `ISTART` and $`N`$ = `IEND`; then $`\Omega_j = \Omega_0 r_j^{\alpha}`$ in the zone, $`\Omega_j = \Omega_\mathrm{s}`$ below it ([lines 80–111](https://github.com/yreclab/yrec/blob/7be4133/src/wczimp.f#L80-L111)).

    > **Question** ([lines 56–61](https://github.com/yreclab/yrec/blob/7be4133/src/wczimp.f#L56-L61); [lines 81–92](https://github.com/yreclab/yrec/blob/7be4133/src/wczimp.f#L81-L92)). **The interior's moments of inertia.** In `IMPJMOD = 2` and `3`, the $`I_j`$ of the budget (the zone's, and with `IMPJMOD = 3` the interior's too) are those in `HI` on entry (from the previous rotation), and only the `SOLID` calls that follow the budget update them. Is one pass enough, or should the budget be iterated?

    > **Question** ([lines 104–110](https://github.com/yreclab/yrec/blob/7be4133/src/wczimp.f#L104-L110)). **`IMPJMOD = 3` and `SOLID`.** After the interior is set to $`\Omega_\mathrm{s}`$, `SOLID` is called on shells 1 to `ISTART-1`, which conserves their total angular momentum and may change $`\Omega`$ again. Does the interior stay at the base's rate?

- **Constant specific angular momentum** if $`\alpha \le -2`$ (and `IMPJMOD = 0`), as in `WCZ`.
- **Otherwise the power law** for the zone alone, as in `WCZ`.
After each assignment, `SOLID` is called on single shells to make $`\Omega`$, $`I`$ and $`j`$ consistent.

**From YREC's documentation.** [Physics Options](https://yrec.readthedocs.io/en/latest/namelist_physics.html): `IMPJMOD` sets the global coupling of angular momentum (0 no effect, 1 solid body everywhere, 2 solid-body core with a decoupled convection zone, 3 solid-body core coupled at the zone's base), and `WALPCZ` the profile in the convection zone, $`\Omega \propto r^{\mathrm{WALPCZ}}`$ (0 solid body, −2 uniform specific angular momentum).

**Changed since `rp_1`.** The solid-body test is $`\alpha \ge 0`$ again (`GT` reverted to `GE`, JVS 2026/02/13), as in `WCZ`, which settles the former question 4 ($`\alpha = 0`$); declarations: COMMON blocks to modules, `IMPLICIT NONE`.

### WCZIMP

Rotation of a convection zone at fixed angular momentum (solid body, constant $`j`$, $`\Omega \propto r^{\alpha}`$), with options to impose solid-body rotation on the interior, decoupled from or coupled to the surface zone (`IMPJMOD`).
