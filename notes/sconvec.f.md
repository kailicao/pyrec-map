## Explanation

**Purpose.** Tests the edge of every convection zone for semiconvection and, where the region next to it is unstable, extends the zone, following Castellani et al. (1971, Ap&SS 10, 340), as the header comment says. It then merges zones that have come to overlap.

**How it fits.**
- **Who calls it:** [[mix.f#MIX|`MIX`]], before the composition is mixed in the convection zones.
- **Inputs:** the step `DELTS` (s), the model's $\log\rho$ (`HD`), $L$ (`HL`, in solar units, by the factor `CLSUN`), $\log P$, $\log r$, $\log m$, $\log T$ (`HP`, `HR`, `HS`, `HT`), the composition `HCOMP`, `TEFFL`, and the zones `MXZONE(12,2)` (bottom and top shell of each), `NZONE`.
- **What it calls:** for each test point, [[eqstat.f#EQSTAT|`EQSTAT`]] (equation of state: $\nabla_\mathrm{ad}$, the mean molecular weights), [[getopac.f#GETOPAC|`GETOPAC`]] (opacity) and [[tpgrad.f#TPGRAD|`TPGRAD`]] (the radiative gradient $\nabla_\mathrm{rad}$).
- **Outputs:** `MXZONE` and `NZONE`, changed; a line in the short output (`ISHORT`) for each edge it moves and each merger. Also, `HD` at the shells it tests is overwritten with the density returned by `EQSTAT`.
- **COMMON:** `/DEBHU/` (it loads `XXDH`, `YYDH`, `ZZDH`, `ZDH(1..3)` with each test point's composition for the Debye–Hückel correction in `EQSTAT`), `/CONST/`, `/CONST1/`, `/FLAG/`, `/LUOUT/`; `/NWLAOL/` is declared but not used.

**The method.** For each zone and each edge that is not the center or the surface (`LFLAGD`, `LFLAGU`); a fully convective star is skipped:
1. At the first radiative shell outside the edge (`JMR`), compute $\nabla_\mathrm{rad}$ with the zone's composition. If $\nabla_\mathrm{rad} < \nabla_\mathrm{ad}$, the edge is stable. Otherwise keep $\nabla_\mathrm{rad,1}$, the mean molecular weight $\mu_\mathrm{CZ}$ (`XINTMU = AMU + EMU`), and $1 - \nabla_\mathrm{ad}/\nabla_\mathrm{rad}$.
2. Recompute at the same shell with its own composition: $\nabla_\mathrm{rad,0}$, and the ratio $f = \nabla_\mathrm{rad,1}/\nabla_\mathrm{rad,0}$ (`FDEL`).
3. The farthest the instability can reach in one step is the propagation speed (eq. 5′, p. 347 of the paper) times the step:
   $$R_\mathrm{max} = \Bigl(1 - \frac{\nabla_\mathrm{ad}}{\nabla_\mathrm{rad,1}}\Bigr)\,\frac{L}{10\cdot4\pi P\,r^2}\,\Delta t,$$
   with $L$, $P$, $r$ at the zone's edge shell.
4. Walk outward from the edge (down for the bottom edge, up for the top), shell by shell, accumulating
   $$R_\Sigma = \sum \Bigl(1 - \frac{\mu_\mathrm{CZ}}{\mu}\Bigr)\,\Delta r .$$
   Stop when $R_\Sigma > R_\mathrm{max}$ (the limit, `LMAX` true) or when the shell is stable against the rescaled gradient, $f\,\nabla_\mathrm{rad} < \nabla_\mathrm{ad}$. The edge moves to the last unstable shell.
5. **Mergers.** If the top of zone $j$ is now above the bottom of zone $j+1$, they become one zone, and the list is shifted down.

## Questions for the experts

1. **The radius is not updated in the walk.** In the loop over shells `II`, every quantity passed to `TPGRAD` is reset for the shell, except `RL`, which stays at `HR(JMR)`. `TPGRAD`'s $\nabla_\mathrm{rad}$ does not use the radius, so the stability test is not affected; only the gravity $G m/r^2$ that `TPGRAD` computes for the convective case is, and its results are not used here. Still, should `RL = HR(II)` be added for safety?
2. **Overwriting the model's density.** `EQSTAT` lists `DL` among its outputs (the density for the given $P$, $T$ and composition), and `HD(JMR) = DL` and `HD(II) = DL` write it back into the model. At `JMR`, the value kept is the one from the second call, with the shell's own composition; but in the walk it is computed for the shell as it is, before any mixing. Is this write-back needed, and is it safe for the next steps of `MIX`?
3. **The factor 10.** $R_\mathrm{max}$ has $L/(10\cdot4\pi P r^2)$. Is the 10 from the paper's equation 5′, or a tuning factor?
4. **"Overshoot" in the comments.** Comments speak of "OVERSHOOT" for what is semiconvective mixing here. A wording leftover?
5. **Touching zones.** Zones are merged only when they overlap (`MXZONE(J,2) .GT. MXZONE(J+1,1)`), not when they become adjacent (top of one = bottom of the next − 1), which leaves no radiative shell between them. Should adjacency also merge?
6. **A merger keeps the upper zone's top.** When zones $j$ and $j+1$ overlap, the merged zone takes the bottom of zone $j$ and the top of zone $j+1$ (`MXZONE(J+1,1) = MXZONE(J,1)`, then the list is shifted). If the semiconvective extension carried the top of zone $j$ past the top of zone $j+1$, the merged zone would be smaller than zone $j$ alone. Should the top be `MAX(MXZONE(J,2), MXZONE(J+1,2))`?
