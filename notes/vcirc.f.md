## Explanation

**Purpose.** `VCIRC` estimates the velocities of the rotational mixing processes at each interface between shells of a radiative region: meridional (Eddington–Sweet) circulation, the Goldreich–Schubert–Fricke (GSF) instability, and the secular and dynamical shear instabilities. Its header comment: "skipping convective regions, check for instability against each secular mechanism; if unstable, compute a circulation velocity". The sum of the velocities, `HV`, sets the diffusion coefficient for angular momentum and mixing.

**How it fits.**
- **Inputs:** arguments from [[seculr.f#SECULR|SECULR]]: $\log r$ and $r$ (`HR`, `HRU`), the range `IMIN`–`IMAX`, the iteration `IT`, `LCZ`, `OMEGA`, the shear `QWLNR` (in `SECULR`, $\tfrac14(\Omega_i - \Omega_{i-1})$ times a radial factor), its limit for dynamical shear `QWRMAX` (from [[setupv.f#SETUPV|SETUPV]]), the total luminosity `CLTOT`, the time step `DT` and $\log P$. Through COMMON blocks, mostly filled by `SETUPV`: the interpolation weights `FACI` (`INTFAC`), the velocity factors `FES1`–`FES3`, `FGSFK` (`TAUKH`), `FACT1`–`FACT8` (`VFACT`), the shell-midpoint quantities (`INTVAR`: `RM`, `HGM`, `ALM`, …), the physics at each shell (`MDPHY`: $\mu$ `AMUM`, the viscosity `VISCM`, the thermal diffusivity `THDIFM`, …), the quadrupole moment and gravity (`QUADRU`: `QUAD`, `GG`), the $\theta$ terms (`OLDROT2`), the scale factors `FES`, `FGSF`, `FSS`, `RCRIT` (`VMULT`) and the switches `IGSF` (`VMULT2`), `LNOJ` (`NOTRAN`), `LDIFAD` (`VARFC`).
- **Who calls it:** only [[seculr.f#SECULR|SECULR]], before and inside its iterations; `SECULR` may then call [[getfc.f#GETFC|GETFC]] with `HV`.
- **Outputs:** `HV` (total velocity per interface) and `LDO` (true if any is positive); in COMMON `TEMP2`, `VES`, `VGSF`, `VSS` and their previous values, read by [[checkj.f#CHECKJ|CHECKJ]], [[codiff.f#CODIFF|CODIFF]], [[getw.f#GETW|GETW]], [[stitch.f#STITCH|STITCH]], [[wrtout.f#WRTOUT|WRTOUT]] and [[wrtmod.f#WRTMOD|WRTMOD]]; with `LDIFAD`, the advective and diffusive parts `VESA`, `VESD` (`DIFAD2`, shared with [[checkj.f#CHECKJ|CHECKJ]] and [[rotgrid.f#ROTGRID|ROTGRID]]) and `VESD2`, `VESD3`, `DSS`, `DGSF`, `FV0` (`DIFAD3`, shared with [[dadcoeft.f#DADCOEFT|DADCOEFT]] and [[setupv.f#SETUPV|SETUPV]]); `RAT` (`QUADD`), read by [[checkj.f#CHECKJ|CHECKJ]], [[fpft.f#FPFT|FPFT]] and [[wrtmod.f#WRTMOD|WRTMOD]]; and `FESTIME`, `FV0` rescaled in place.

**The method.** At the interface between shells $i-1$ and $i$:
1. **Midpoint values.** The viscosity $\nu$ and thermal diffusivity $K$ by 4-point interpolation in their logarithms (weights `FACI`); $\mu$ and $\bar\Omega$ (`WM`) as the means of the two shells.
2. **Meridional circulation** (Zahn 1991, by the comments): $v_\mathrm{ES} = \bar\Omega^2 (F_1 + \bar\Omega^2 F_2)$, multiplied by the quadrupole correction of Zahn (1992),
   $$R = \frac{\Phi_s + \Phi_2}{\Phi_\mathrm{std}},\quad \Phi_\mathrm{std} = \frac{4}{3}\,\frac{\bar\Omega^2 r}{\bar g},\quad \Phi_s = \frac13\,\bar\Omega^2\,\frac{d}{dr}\!\left(\frac{r^2}{g}\right),\quad \Phi_2 = -\frac{d}{dr}\!\left(\frac{Q}{g}\right),$$
   with a warning printed if $R < 0$. Without `LDIFAD`, $v_\mathrm{ES} = |R\,v_\mathrm{ES} - F_3\,\bar\Omega\,d\Omega/dr|$. With `LDIFAD` (MHP 05/02, 06/02), it is split into an advective part, $v_A = \tfrac15(R\,v_\mathrm{ES} + \dot\theta)$ with $\dot\theta$ = `THN`, and diffusive parts of first to third order.
3. **Inhibition by $\mu$ gradients** (Zahn & Maeder 1998): every velocity is multiplied by
   $$f_\mu = \frac{\max(\Delta\nabla, 10^{-3})}{\max(\Delta\nabla + \nabla_\mu, 10^{-3})},\qquad \nabla_\mu = \frac{\Delta\ln\mu}{\Delta\ln P},$$
   with $\Delta\nabla$ = `DDELM` (in `SETUPV`, $\nabla_\mathrm{ad} - \nabla + \nabla_\mu$, at least a minimum).
4. **GSF** (Kippenhahn 1980): if specific angular momentum decreases outward ($\Omega_i r_i^2 < \Omega_{i-1} r_{i-1}^2$),
   $$v_\mathrm{GSF} = F_K\,K\,\frac{\bar\Omega^2}{r}\,\max\!\left(2\left|\frac{d\ln j}{dr}\right|, \tfrac14\left|\frac{d\ln\Omega}{dr}\right|\right),$$
   otherwise $v_\mathrm{GSF} = \tfrac14 F_K K\,\bar\Omega^2\,|d\ln\Omega/dr|/r$. With `IGSF` = 0 or 2 it is damped by viscosity: zero if $|q| < q_\nu = 2\sqrt{\nu/K}\,q_\mathrm{max}$, else multiplied by $\sqrt{(|q| - q_\nu)/q_\nu}$; with `IGSF` = 0 also by the $\mu$ gradient, likewise.
5. **Shear** (Endal & Sofia, paper II; Zahn 1991). If $|q| > q_\mathrm{max}$ (dynamical shear), $v_\mathrm{SS} = \tfrac{8}{45} K (|q|/q_\mathrm{max})^2/r$, and $v_\mathrm{GSF}$ is rescaled to the gradient at the limit (a message is written to unit 6). Otherwise the secular shear is unstable if
   $$|q| > q_\mathrm{crit} = \sqrt{\frac{\nu}{K}\,\frac{R_\mathrm{crit}}{8}}\;q_\mathrm{max},$$
   and then $v_\mathrm{SS} = \tfrac{8}{45} K\,\left[(|q| - q_\mathrm{crit})/q_\mathrm{max}\right]^2/r$, with $q_\mathrm{crit}$ raised by a $\mu$ gradient if that gives the larger limit.
6. **Scale and average.** The velocities are multiplied by the user's factors `FES`, `FGSF`, `FSS`; with `LDIFAD`, the GSF and shear velocities times $r$ join the diffusive part. After the first iteration (`IT > 1`) each is averaged with the previous one. `HV` = $v_\mathrm{ES} + v_\mathrm{GSF} + v_\mathrm{SS}$ (zero below $10^{-20}$).
7. **No transport in the core** (`LNOJ`, 9/93): from `IMIN` outward, the velocities are zeroed while $L(r)/L_\mathrm{tot} < 0.99$, "to avoid numerical problems in the H-burning shell".

**Design.** Many older prescriptions are kept as comments (Kippenhahn & Möllenhoff 1974 circulation, James & Kahn 1971 GSF, older $\mu$ treatments); the flags `IES` and `IMU` no longer select anything.

**KC's changes.** The unused argument `HJM` was removed (2025-05-31).

## Questions for the experts

1. **The $\mu$ loop does not skip convective interfaces.** The meridional, GSF and shear loops skip interfaces inside convection zones; the Zahn & Maeder loop (step 3) does not, and rescales `FESTIME` and `FV0` there too. Harmless, or should it skip them?
2. **Possible division by zero.** In the dynamical-shear branch, $v_\mathrm{GSF}$ is rescaled by `DLNWDR/DLNWDR0` or `FX/FX2`, where `DLNWDR0` is zero if $\Omega_i = \Omega_{i-1}$; and $\ln\Omega$ requires $\Omega > 0$ everywhere.
3. **Sign of the meridional velocity.** With `LDIFAD`, the circulation is signed, but `VES` is made positive by `ABS(FES*VES)` for every interface before `HV` is formed, so `HV` never sees a negative `VES`; only `VESA` (the advective part) keeps its sign. So `HV` takes $|v_\mathrm{ES}|$ of a signed circulation: intended?
4. **Unused values.** `V2` and `WMID` are computed but never used; `VMU` is zeroed and copied to `VMUP` (COMMON `PREVMU`, used by no other routine) but no longer computed, since the old $\mu$ treatments are commented out. Can they go?
5. **Output to unit 6.** The dynamical-shear message goes to unit 6 (the screen) for every unstable interface, at every iteration.
6. **`LNOJ`'s threshold.** The core is defined as $L(r)/L_\mathrm{tot} < 0.99$, hard-coded. Should it be a parameter?
7. **The $\mu$ factor compounds.** The $\mu$ loop multiplies `FESTIME` and `FV0` (COMMON, set once by `SETUPV` before SECULR's iterations) by $f_\mu$ at every call of `VCIRC`, so the factor compounds over SECULR's iterations ($f_\mu^{\,n}$ after $n$ calls). Should it be applied to a copy?

### VCIRC

Velocities of meridional circulation (Zahn 1991, with Zahn 1992's quadrupole term), the GSF instability (Kippenhahn 1980) and secular and dynamical shear at each radiative interface, with $\mu$-gradient inhibition (Zahn & Maeder 1998), the user's scale factors and averaging between iterations.
