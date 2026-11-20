## Explanation

**Purpose.** `VCIRC` estimates the velocities of the rotational mixing processes at each interface between shells of a radiative region: meridional (Eddington–Sweet) circulation, the Goldreich–Schubert–Fricke (GSF) instability, and the secular and dynamical shear instabilities. Its header comment: "skipping convective regions, check for instability against each secular mechanism; if unstable, compute a circulation velocity." The sum of the velocities, `HV`, sets the diffusion coefficient for angular momentum and mixing: each "velocity" becomes a diffusion coefficient over a length, $`D = 4\pi f_w\,v\,r`$ ([CODIFF](codiff.f.md#codiff)), so that, for example, $`v_\mathrm{SS} \propto K/r`$ gives $`D_\mathrm{SS} \propto K`$.

**How it fits.**
- **Inputs:** arguments from [SECULR](https://github.com/yreclab/yrec/blob/7be4133/src/seculr.f#L6-L532): $`\log r`$ and $`r`$ (`HR`, `HRU`), the range `IMIN`–`IMAX`, the iteration `IT`, `LCZ`, `OMEGA`, the shear `QWLNR` (in `SECULR`, $`\tfrac14(\Omega_i - \Omega_{i-1})`$ times a radial factor), its limit for dynamical shear `QWRMAX` (from [SETUPV](https://github.com/yreclab/yrec/blob/7be4133/src/setupv.f#L3-L467)), the total luminosity `CLTOT`, the time step `DT`, $`\log P`$, and the interpolation weights `FACI` (filled by `SETUPV`; formerly COMMON `INTFAC`, now owned by `SECULR`). Through modules, mostly filled by `SETUPV`: the velocity factors `FES1`–`FES3`, `FGSFK`, `FACT6` (`TAUKH_MOD`), `FACT1`–`FACT8` (`VFACT_MOD`), the shell-midpoint quantities (`INTVAR_MOD`: `RM`, `HGM`, `ALM`, …), the physics at each shell (`MDPHY_MOD`: $`\mu`$ `AMUM`, the viscosity `VISCM`, the thermal diffusivity `THDIFM`, …), the quadrupole moment and gravity (`QUADRU_MOD`: `QUAD`, `GG`), the $`\theta`$ terms (`OLDROT2_MOD`), and the namelist parameters in `NMLPAR_MOD` (formerly `VMULT`, `VMULT2`, `NOTRAN`, `VARFC`): the scale factors `FES`, `FGSF`, `FSS`, `FMU`, `FC`, `FESC`, `FGSFC`, `RCRIT` and the switches `IES`, `IGSF`, `IMU`, `LNOJ`, `LDIFAD`.
- **Who calls it:** only [SECULR](https://github.com/yreclab/yrec/blob/7be4133/src/seculr.f#L6-L532), before and inside its iterations; `SECULR` may then call [GETFC](getfc.f.md#getfc) with `HV`.
- **Outputs:** `HV` (total velocity per interface) and `LDO` (true if any is positive); in `TEMP2_MOD`, `VES`, `VGSF`, `VSS`, `VMU` and their previous values, read by [CHECKJ](checkj.f.md#checkj), [CODIFF](codiff.f.md#codiff), [PUTSTORE](https://github.com/yreclab/yrec/blob/7be4133/src/putstore.f#L13-L360) and [STITCH](stitch.f.md#stitch); with `LDIFAD`, the advective and diffusive parts `VESA`, `VESD` (`DIFAD2_MOD`, shared with [CHECKJ](checkj.f.md#checkj) and [ROTGRID](https://github.com/yreclab/yrec/blob/7be4133/src/rotgrid.f#L2-L285)) and `VESD2`, `VESD3`, `DSS`, `DGSF`, `FV0` (`DIFAD3_MOD`, shared with [DADCOEFT](dadcoeft.f.md#dadcoeft) and [SETUPV](https://github.com/yreclab/yrec/blob/7be4133/src/setupv.f#L3-L467)); `RAT` (`QUADD_MOD`), read by [CHECKJ](checkj.f.md#checkj) and [FPFT](fpft.f.md#fpft); and `FESTIME`, `FV0` rescaled in place. The midpoint values `VISCMI`, `THDIFMI`, `AMUMI`, `WM` and the previous `VMU`, `VMUP`, are now local arrays kept between calls (formerly COMMON `INTVR2` and `PREVMU`).

**The method.** At the interface between shells $`i-1`$ and $`i`$, with $`q = d\Omega/d\ln r`$ there (`QWLNR`, from SECULR); $`q_\mathrm{max}`$ (`QWRMAX`, from [SETUPV](https://github.com/yreclab/yrec/blob/7be4133/src/setupv.f#L3-L467)) the largest shear stable against the dynamical shear instability, from the Richardson criterion $`\mathrm{Ri} = N^2/q^2 \ge \tfrac14`$; $`F_1`$, $`F_2`$, $`F_3`$ = `FES1`–`FES3` and $`F_K`$ = `FGSFK`, from SETUPV:
1. **Midpoint values.** The viscosity $`\nu`$ and thermal diffusivity $`K`$ by 4-point interpolation in their logarithms (weights `FACI`); $`\mu`$ and $`\bar\Omega`$ (`WM`) as the means of the two shells.
2. **Meridional circulation** (Zahn [1991](https://ui.adsabs.harvard.edu/abs/1991A%26A...252..179Z), by the comments): $`v_\mathrm{ES} = \bar\Omega^2 (F_1 + \bar\Omega^2 F_2)`$, multiplied by the quadrupole correction of Zahn ([1992](https://ui.adsabs.harvard.edu/abs/1992A%26A...265..115Z)),
   
   $$\displaystyle R = \frac{\Phi\_s + \Phi\_2}{\Phi\_\mathrm{std}},\quad \Phi\_\mathrm{std} = \frac{4}{3}\\,\frac{\bar\Omega^2 r}{\bar g},\quad \Phi\_s = \frac13\\,\bar\Omega^2\\,\frac{d}{dr}\\!\left(\frac{r^2}{g}\right),\quad \Phi\_2 = -\frac{d}{dr}\\!\left(\frac{Q}{g}\right),$$
   
   with a warning printed if $`R \lt{} 0`$. Without `LDIFAD`, $`v_\mathrm{ES} = |R\,v_\mathrm{ES} - F_3\,\bar\Omega\,d\Omega/dr|`$. With `LDIFAD` (MHP 05/02, 06/02), it is split into an advective part, $`v_A = \tfrac15(R\,v_\mathrm{ES} + \dot\theta)`$ with $`\dot\theta`$ = `THN`, and diffusive parts of first to third order.

   **`IES = 2`** (Kippenhahn & Möllenhoff [1974](https://ui.adsabs.harvard.edu/abs/1974Ap%26SS..31..117K), restored MHP 4/26) replaces this: $`v_\mathrm{ES} = |F_1'(F_2' R\,\bar\Omega^2 + F_6\,\Delta(\Omega r)^2/\Delta r)|`$, with $`F_1'`$, $`F_2'`$, $`F_6`$ = `FACT1`, `FACT2`, `FACT6` and $`R`$ = `PHIS2/PHISTD` (the quadrupole term is computed, then dropped); `QW`, `THN` and the `LDIFAD` parts are not set (bug 4).

    > **Question** ([lines 222–223](https://github.com/yreclab/yrec/blob/7be4133/src/vcirc.f#L222-L223)). **`RAT` with `IES = 2`.** `RAT(I) = (PHIS2+PHI2)/PHISTD` is overwritten at once by `RAT(I) = PHIS2/PHISTD`, so the quadrupole term is dropped, unlike the default branch ([line 241](https://github.com/yreclab/yrec/blob/7be4133/src/vcirc.f#L241)). Intended?

3. **Inhibition by $`\mu`$ gradients** (Zahn & Maeder [1998](https://ui.adsabs.harvard.edu/abs/1998A%26A...334.1000M)): every velocity is multiplied by
   
   $$\displaystyle f\_\mu = \frac{\max(\Delta\nabla, 10^{-3})}{\max(\Delta\nabla + \nabla\_\mu, 10^{-3})},\qquad \nabla\_\mu = \frac{\Delta\ln\mu}{\Delta\ln P},$$
   
   with $`\Delta\nabla`$ = `DDELM` (in `SETUPV`, $`\nabla_\mathrm{ad} - \nabla + \nabla_\mu`$, at least a minimum). The loop also multiplies `FESTIME` and `FV0` by $`f_\mu`$ in place (bug 1; `FV0` is read by no other routine: unused?), and computes `V2` ([line 314](https://github.com/yreclab/yrec/blob/7be4133/src/vcirc.f#L314)), which is never used: unused?.

    > **Question** ([lines 297–320](https://github.com/yreclab/yrec/blob/7be4133/src/vcirc.f#L297-L320)). **The $`\mu`$ loop does not skip convective interfaces.** The meridional, GSF, and shear loops skip interfaces inside convection zones ([line 230](https://github.com/yreclab/yrec/blob/7be4133/src/vcirc.f#L230), [line 352](https://github.com/yreclab/yrec/blob/7be4133/src/vcirc.f#L352)); this loop does not, and rescales there the `LDIFAD` parts `VESA`, `VESD`, `VESD2`, `VESD3`, which loop 31 did not set at those interfaces in this call, and `FESTIME`. Harmless, or should it skip them?


   **`IMU = 3`** (Kippenhahn & Möllenhoff 1974, restored MHP 4/26) replaces this with "fictitious $`\mu`$ currents" at each radiative interface, $`v_\mu = |f_\mu\,F_1' F_4\,\bar\mu\,(d\mu/dr)/\sqrt{\nu c/K}|`$ (`VMU`, with $`f_\mu`$ = `FMU`, $`F_4`$ = `FACT4`, $`c`$ = `CC`) and $`v_{\mu2} = f_\mu\,\bar g\,|d\mu/dr|/(\bar\mu\,\bar\Omega^2)`$ (`VMU2`), which are subtracted in step 6. `CC`, the speed of light by the comment, is never set (bug 2). At a convective interface `VMU2` keeps the value of an earlier call, but it only divides velocities that are zero there ([lines 152–153](https://github.com/yreclab/yrec/blob/7be4133/src/vcirc.f#L152-L153), [line 230](https://github.com/yreclab/yrec/blob/7be4133/src/vcirc.f#L230), [line 352](https://github.com/yreclab/yrec/blob/7be4133/src/vcirc.f#L352)), and its $`\bar\Omega^2`$ needs $`\Omega \gt{} 0`$, which the logarithms of step 4 already need (settled from the code, Nov 9, 2026).
4. **GSF** (Kippenhahn [1980](https://ui.adsabs.harvard.edu/abs/1974IAUS...66...20K); the year is the code's, whose comments elsewhere cite the same estimate as Kippenhahn, IAU Symp. 66, p. 20, 1974, “Circulation and Mixing”): if specific angular momentum decreases outward ($`\Omega_i r_i^2 \lt{} \Omega_{i-1} r_{i-1}^2`$),
   
   $$\displaystyle v\_\mathrm{GSF} = F\_K\\,K\\,\frac{\bar\Omega^2}{r}\\,\max\\!\left(2\left\|\frac{d\ln j}{dr}\right\|, \tfrac14\left\|\frac{d\ln\Omega}{dr}\right\|\right),$$
   
   otherwise $`v_\mathrm{GSF} = \tfrac14 F_K K\,\bar\Omega^2\,|d\ln\Omega/dr|/r`$ ([lines 396–405](https://github.com/yreclab/yrec/blob/7be4133/src/vcirc.f#L396-L405)). With `IGSF` = 0 or 2 it is damped by viscosity: zero if $`|q| \lt{} q_\nu = 2\sqrt{\nu/K}\,q_\mathrm{max}`$, else multiplied by $`\sqrt{(|q| - q_\nu)/q_\nu}`$; with `IGSF` = 0 also by the $`\mu`$ gradient, likewise.

    > **Question** ([lines 396–402](https://github.com/yreclab/yrec/blob/7be4133/src/vcirc.f#L396-L402)). **$`j`$ decreasing outward.** This step treats $`\Omega_i r_i^2 \lt{} \Omega_{i-1}r_{i-1}^2`$ as a stronger GSF case, still at a thermal-diffusion rate ($`\propto K`$). A specific angular momentum that decreases outward is dynamically unstable (the Rayleigh, or Solberg–Høiland, criterion). Should this case be handled as dynamical (immediate redistribution), as for the dynamical shear, rather than at the GSF's thermal rate?

5. **Shear** (Endal & Sofia, paper II; Zahn 1991). If $`|q| \gt{} q_\mathrm{max}`$ (dynamical shear), $`v_\mathrm{SS} = \tfrac{8}{45} K (|q|/q_\mathrm{max})^2/r`$, and $`v_\mathrm{GSF}`$ is rescaled to the gradient at the limit (a message is written to unit 6, the screen, for every such interface at every call, [lines 494–496](https://github.com/yreclab/yrec/blob/7be4133/src/vcirc.f#L494-L496)): With $`\Omega_\mathrm{min} = \Omega_i + (\Omega_{i-1} - \Omega_i)\,q_\mathrm{max}/|q|`$ (`WMIN`), the value of $`\Omega_{i-1}`$ at which $`|q|`$ would equal $`q_\mathrm{max}`$, the gradients of $`\ln\Omega`$ and $`\ln j`$ from $`\Omega_i`$ to $`\Omega_\mathrm{min}`$ replace those from $`\Omega_i`$ to $`\Omega_{i-1}`$ in the formulae of step 4, the branch being chosen from the actual $`\Omega_i r_i^2`$ and $`\Omega_{i-1} r_{i-1}^2`$ ([lines 445–497](https://github.com/yreclab/yrec/blob/7be4133/src/vcirc.f#L445-L497)). The rescaling divides by no zero: The branch runs only when $`|q| \gt{} q_\mathrm{max}`$, and $`q`$ is proportional to $`\Omega_i - \Omega_{i-1}`$ ([seculr.f, line 177](https://github.com/yreclab/yrec/blob/7be4133/src/seculr.f#L177)), so the two differ and `DLNWDR0` and `FX2` are positive (settled from the code, Nov 9, 2026); the logarithms need $`\Omega \gt{} 0`$. `WMID`, computed at [lines 451–455](https://github.com/yreclab/yrec/blob/7be4133/src/vcirc.f#L451-L455), is never used: unused?. Otherwise the secular shear is unstable if
   
   $$\displaystyle \|q\| \gt{} q\_\mathrm{crit} = \sqrt{\frac{\nu}{K}\\,\frac{R\_\mathrm{crit}}{8}}\\;q\_\mathrm{max},$$
   
   and then $`v_\mathrm{SS} = \tfrac{8}{45} K\,\left[(|q| - q_\mathrm{crit})/q_\mathrm{max}\right]^2/r`$, with $`q_\mathrm{crit}`$ raised by a $`\mu`$ gradient if that gives the larger limit.

    > **Question** ([lines 445–447](https://github.com/yreclab/yrec/blob/7be4133/src/vcirc.f#L445-L447)). **Dynamical shear at a thermal rate.** For $`|q| \gt{} q_\mathrm{max}`$, $`v_\mathrm{SS} = \tfrac{8}{45}K(|q|/q_\mathrm{max})^2/r`$ is scaled by the thermal diffusivity $`K`$, although the dynamical shear instability acts on a dynamical timescale and would mix far faster. Why is its rate tied to $`K`$; is the intent only to make it large enough to remove the excess shear within a step?

6. **Scale and average.** The velocities are multiplied by the user's factors `FES`, `FGSF`, `FSS`. With `IMU = 3`, after `VMU` is averaged with its previous value (`IT > 1`), the $`\mu`$ currents are subtracted instead: $`v_\mathrm{ES} \to \max(0, F v_\mathrm{ES} - \sqrt{F v_\mathrm{ES}\,r}\,\sqrt{f_c f_{c,\mathrm{ES}}}\,v_\mu)`$ with $`F`$ = `FES`, $`f_c`$ = `FC`, $`f_{c,\mathrm{ES}}`$ = `FESC`, or $`|F v_\mathrm{ES}|/(1 + v_{\mu2})`$ where that is not positive; likewise $`v_\mathrm{GSF}`$ with `FGSF` and `FGSFC` (but with `FES` where the result is not positive: bug 3); $v_\mathrm{SS} \to \max(0, $ `FSS` $`v_\mathrm{SS})`$. with `LDIFAD`, the GSF and shear velocities times $`r`$ join the diffusive part. After the first iteration (`IT > 1`) each is averaged with the previous one. `HV` = $`v_\mathrm{ES} + v_\mathrm{GSF} + v_\mathrm{SS}`$ (zero below $`10^{-20}`$). Without `IMU = 3`, `VMU` is only zeroed ([line 155](https://github.com/yreclab/yrec/blob/7be4133/src/vcirc.f#L155)) and copied to `VMUP` ([line 138](https://github.com/yreclab/yrec/blob/7be4133/src/vcirc.f#L138)): unused? there.

    > **Question** ([line 595](https://github.com/yreclab/yrec/blob/7be4133/src/vcirc.f#L595); [lines 269–271](https://github.com/yreclab/yrec/blob/7be4133/src/vcirc.f#L269-L271); [line 605](https://github.com/yreclab/yrec/blob/7be4133/src/vcirc.f#L605)). **Sign of the meridional velocity.** With `LDIFAD`, the circulation is signed, but `VES` is made positive by `ABS(FES*VES)` for every interface before `HV` is formed, so `HV` never sees a negative `VES`; only `VESA` (the advective part) keeps its sign. So `HV` takes $`|v_\mathrm{ES}|`$ of a signed circulation: intended?

7. **No transport in the core** (`LNOJ`, 9/93): from `IMIN` outward, the velocities are zeroed while $`L(r)/L_\mathrm{tot} \lt{} 0.99`$, "to avoid numerical problems in the H-burning shell."

    > **Question** ([lines 671–687](https://github.com/yreclab/yrec/blob/7be4133/src/vcirc.f#L671-L687)). **`LNOJ`'s threshold.** The core is defined as $`L(r)/L_\mathrm{tot} \lt{} 0.99`$, hard-coded. Should it be a parameter?

**Design.** Many older prescriptions are kept as comments (James & Kahn [1971](https://ui.adsabs.harvard.edu/abs/1971A%26A....12..332J) GSF, older $`\mu`$ treatments); `IES = 2` and `IMU = 3` select the restored Kippenhahn & Möllenhoff (1974) treatments, and any other value (the defaults are 1) the Zahn (1991) circulation and the Zahn & Maeder (1998) $`\mu`$ factor.

**From YREC's documentation.** [Physics Options](https://yrec.readthedocs.io/en/latest/namelist_physics.html): `IGSF` chooses the stability condition for the GSF and ABCD instabilities; 1 is recommended. In the code, 1 applies none, 2 the condition on the angular-velocity gradient against viscosity and thermal diffusion, and 0 adds a mean-molecular-weight condition. `LDIFAD`, experimental, treats meridional circulation as diffusion plus advection; `FC` scales the mixing coefficients relative to angular momentum.

**Changed since `rp_1`.** The options `IES = 2` (Kippenhahn & Möllenhoff circulation) and `IMU = 3` (their $`\mu`$ currents, `VMU` and the restored `VMU2`, with the scale factors applied in the same step) are restored (MHP 4/26); `FACI` is now an argument; the midpoint arrays and `VMUP` are local; declarations: COMMON blocks to modules, `IMPLICIT NONE`. `VMU` is computed again with `IMU = 3`.

**Changed since `a8a5950`.** In the dynamical-shear branch, `WMIN` is taken from the centred gradient `QWLNR` that triggers the branch, so that it lies between $`\Omega_i`$ and $`\Omega_{i-1}`$ and is positive; the plain difference quotient used before could put it beyond $`\Omega_{i-1}`$, or at or below zero (a NaN in its logarithm). The GSF branch is chosen from the actual profile, as its normalization `FX2` is, not from the limited one.

## Bugs, by priority

1. **(cannot be reached)** **The $`\mu`$ factor compounds on `FESTIME`.** ([line 256](https://github.com/yreclab/yrec/blob/7be4133/src/vcirc.f#L256); [lines 304–317](https://github.com/yreclab/yrec/blob/7be4133/src/vcirc.f#L304-L317)) The $`\mu`$ loop multiplies `FESTIME` (and `FV0`) by $`f_\mu`$ in place at every call. [SETUPV](https://github.com/yreclab/yrec/blob/7be4133/src/setupv.f#L3-L467) sets them once per call of [SECULR](https://github.com/yreclab/yrec/blob/7be4133/src/seculr.f#L6-L532) ([setupv.f, line 337](https://github.com/yreclab/yrec/blob/7be4133/src/setupv.f#L337)), before its iterations, and SECULR calls VCIRC once per iteration ([seculr.f, lines 190–191](https://github.com/yreclab/yrec/blob/7be4133/src/seculr.f#L190-L191), [seculr.f, lines 230–231](https://github.com/yreclab/yrec/blob/7be4133/src/seculr.f#L230-L231)), so at iteration $`n`$, `THN = FESTIME*(THM*QW-THP)/DT` carries the $`n-1`$ earlier factors ($`f_\mu^{\,n-1}`$ when $`\mu`$ does not change); and `THN` enters `VESA` and `VES` ([line 257](https://github.com/yreclab/yrec/blob/7be4133/src/vcirc.f#L257), [line 269](https://github.com/yreclab/yrec/blob/7be4133/src/vcirc.f#L269)), which the same loop then multiplies by $`f_\mu`$ once more. `FESTIME` is read nowhere else, and `FV0` nowhere at all. What follows: `THN` wrong from the second iteration on, only with `LDIFAD` (off by default) and `ITDIF2` > 1 (the default is 1).

    **A possible fix:**

    ```diff
    --- a/src/vcirc.f
    +++ b/src/vcirc.f
    @@ -313,8 +313,12 @@
                 DR = HRU(I) - HRU(I-1)
                 V2 = 0.2D0*(Q0+Q1)*(OMEGA(I)-OMEGA(I-1))/DR/WM(I)
     C ADD MU GRADIENTS TO VELOCITY ESTIMATES
    -            FESTIME(I) = FESTIME(I)*QQQ
    -            FV0(I) = FV0(I)*QQQ
    +C 11/09/26 KC via Claude
    +C code changed to stop rescaling FESTIME and FV0 in place: THN takes
    +C the mu factor through VES and VESA, and the rescaling compounded
    +C over SECULR's iterations.
    +C           FESTIME(I) = FESTIME(I)*QQQ
    +C           FV0(I) = FV0(I)*QQQ
     C         WRITE(*,911)I,WM(I),VESA(I),V2,Q0,Q1,THN(I),VES(I),QQQ
     C 911           FORMAT(I5,1P8E12.3)
              END DO
    ```

    **Checked by running YREC** (Nov 9, 2026; a line added at each suspected path counted how often it was taken, the outputs otherwise unchanged): The rescaling ran in the four rotating test cases with `IMU` $`\ne 3`$ (from about 0.65 to 2.2 million times, at SECULR's iterations 1 to 10, with $`f_\mu`$ from 0.13 to 1.28), so `FESTIME` does compound. But it is read only for `THN` in the `LDIFAD` branch ([line 256](https://github.com/yreclab/yrec/blob/7be4133/src/vcirc.f#L256)), and PARMIN stops any run that sets `LDIFAD` with rotation ([parmin.f, lines 999–1006](https://github.com/yreclab/yrec/blob/7be4133/src/parmin.f#L999-L1006)), so the wrong `THN` cannot be reached at 7be4133; the condition line never fired. What remains is a factor that compounds unread. Intent: none found.

2. **(changes results, small)** **Checked by KC** (Nov 10, 2026). **`CC` is never set.** ([lines 121–122](https://github.com/yreclab/yrec/blob/7be4133/src/vcirc.f#L121-L122); [lines 286–288](https://github.com/yreclab/yrec/blob/7be4133/src/vcirc.f#L286-L288)) With `IMU = 3`, `TKHS = SQRT(VISCMI(I)*CC/THDIFMI(I))` uses the local `CC`, whose `DATA` statement (the speed of light) is commented out, so `CC` is undefined: zero if the compiler zeroes saved storage, which makes `TKHS` zero and `VMU` infinite (or NaN where $`\mu`$ is uniform). Then the reduction of step 6 ([lines 550–556](https://github.com/yreclab/yrec/blob/7be4133/src/vcirc.f#L550-L556)) never leaves a positive `VEST`, and `VES` always falls back to `ABS(FES*VES(I)/FM)`. Only with `IMU = 3` (the default is 1).

    **A possible fix:**

    ```diff
    --- a/src/vcirc.f
    +++ b/src/vcirc.f
    @@ -119,7 +119,9 @@
          *          QWLNR(JSON),QWRMAX(JSON),HV(JSON),VMU2(JSON),
          *          HP(JSON)
     C SPEED OF LIGHT.
    -C       DATA CC/2.99792458D10/
    +C 11/09/26 KC via Claude
    +C code changed to restore the speed of light, CC, used by TKHS.
    +      DATA CC/2.99792458D10/
           SAVE
     
     C   SKIPPING CONVECTIVE REGIONS, CHECK FOR INSTABILITY AGAINST EACH
    ```

    **How the code itself shows it.** `CC` gets a value nowhere: Its only `DATA` line is commented out ([line 122](https://github.com/yreclab/yrec/blob/7be4133/src/vcirc.f#L122), `C       DATA CC/2.99792458D10/`), and no other line assigns it, so the speed of light that this line comments out is the only value the code ever gave it, the value it had before the cleanup, which is what the fix above restores. The units, however, do not fit the comment above the formula, which calls `TKHS` the square root of Kippenhahn's timescale $`t_\mathrm{KH}^*`$ ([lines 284–285](https://github.com/yreclab/yrec/blob/7be4133/src/vcirc.f#L284-L285)): VISCOS computes the kinematic viscosity ([viscos.f, line 47](https://github.com/yreclab/yrec/blob/7be4133/src/viscos.f#L47)) and the radiative diffusivity `THDIF` $`= 16\sigma T^3/(3\kappa\rho^2 c_P)`$ ([viscos.f, lines 104–107](https://github.com/yreclab/yrec/blob/7be4133/src/viscos.f#L104-L107)), both in $`\mathrm{cm^2\,s^{-1}}`$, so `VISCMI*CC/THDIFMI` with `CC` $`= c`$ has units of $`\mathrm{cm\,s^{-1}}`$, and its square root is not a time. Was `CC` meant to be the speed of light here, or another constant (a length, or $`c`$ with a factor that the comment's equation (12) supplies)? The run below measures what restoring $`c`$ does; the right value is for the developers.

    **Checked by running YREC** (Nov 9, 2026; a line added at each suspected path counted how often it was taken, the outputs otherwise unchanged): The case run with `IMU = 3` (`testsuite/Test_m2p0_feh+0p0_vzams150_IES2_TAMS`) took the path 472,022 times, at shells 2 to 748, and `CC` was 0 every time, so `TKHS` was zero; the run, in the release build, went on without a message. With the speed of light restored, the track changes far beyond the noise: $`\log L`$ moves by up to $`0.0056\,\mathrm{dex}`$, $`\log T_\mathrm{eff}`$ by 0.0020, and central $`\log T`$ by 0.0055 (at its end, $`1.2\,\mathrm{Gyr}`$), against about $`2\times10^{-8}`$ for a null change (nearly every opacity, all with $`3 \le \log T \le 9`$ and $`-6 \le \log\rho \le 9.75`$, times $`1 + 10^{-10}`$, on the same case), and central $`X`$ by 0.00016 (at $`0.076\,\mathrm{Gyr}`$), with the same 546 models. The other two cases with `IMU = 3` (`testsuite/Test_m2p0_feh+0p0_vzams150_NoJMixIES2_TAMS` and `testsuite/Test_m2p0_feh+0p0_vzams150_DRIES2_TAMS`) were not run. Intent: The speed of light was commented out as an unused variable (commit c6a51f3, "commented out unused variables detected by ifx"), when the `IMU = 3` branch was itself commented out; when that branch was switched back on (commit 49dfbec), the `DATA` line ([lines 121–122](https://github.com/yreclab/yrec/blob/7be4133/src/vcirc.f#L121-L122)) was not restored: a slip in restoring the branch, though whether $`c`$ is the right constant there is asked below.

3. **(never occurred)** **`FES` for the GSF velocity.** ([lines 564–568](https://github.com/yreclab/yrec/blob/7be4133/src/vcirc.f#L564-L568)) With `IMU = 3`, when the reduced GSF velocity is not positive, `VGSF(I) = ABS(FES*VGSF(I)/FM)` uses `FES`, the circulation's factor, where the rest of the GSF branch uses `FGSF` ([line 559](https://github.com/yreclab/yrec/blob/7be4133/src/vcirc.f#L559)). Only with `IMU = 3` and `FES` different from `FGSF` (both default to 1).

    **A possible fix:**

    ```diff
    --- a/src/vcirc.f
    +++ b/src/vcirc.f
    @@ -562,7 +562,9 @@
                    VGSFT = 0.0D0
                 ENDIF
                 IF(VGSFT.LE.0.0D0)THEN
    -               VGSF(I) = ABS(FES*VGSF(I)/FM)
    +C 11/09/26 KC via Claude
    +C code changed to scale the GSF velocity by FGSF, not FES.
    +               VGSF(I) = ABS(FGSF*VGSF(I)/FM)
                 ELSE
                    VGSF(I) = VGSFT
                 ENDIF
    ```

    **Checked by running YREC** (Nov 9, 2026; a line added at each suspected path counted how often it was taken, the outputs otherwise unchanged): In `testsuite/Test_m2p0_feh+0p0_vzams150_IES2_TAMS` the fallback ran 473,160 times, but with `VGSF` = 0 every time, so the factor multiplied zero; and `FES` = `FGSF` = 1 in every namelist, so the condition line never fired. A run with `IMU = 3`, `FES` $`\ne`$ `FGSF`, and a positive GSF velocity would reach it; none was run. Intent: none found.

4. **(cannot be reached)** **`IES = 2` with `LDIFAD` reuses the previous call's parts.** ([lines 202–226](https://github.com/yreclab/yrec/blob/7be4133/src/vcirc.f#L202-L226); [lines 602–607](https://github.com/yreclab/yrec/blob/7be4133/src/vcirc.f#L602-L607); [lines 629–632](https://github.com/yreclab/yrec/blob/7be4133/src/vcirc.f#L629-L632)) The `IES = 2` loop sets only `VES` and `RAT`; `THN`, `VESA`, `VESD`, `VESD2`, `VESD3` and `EQQCOD` keep the values of the previous call (they are not cleared at [lines 150–156](https://github.com/yreclab/yrec/blob/7be4133/src/vcirc.f#L150-L156)). With `LDIFAD`, they are then multiplied by $`f_\mu`$ and by `FES` again, and `VESD` gains `RM*(VGSF+VSS)` again, at every call, so it grows from call to call. Only with `IES = 2` and `LDIFAD` (both off by default).

    **A possible fix:** a choice for the developers: stop with a message when `IES = 2` and `LDIFAD` are both set, or compute the `LDIFAD` parts in the `IES = 2` loop as the default loop does.

    **Checked by running YREC** (Nov 9, 2026; a line added at each suspected path counted how often it was taken, the outputs otherwise unchanged): `testsuite/Test_m2p0_feh+0p0_vzams150_IES2_TAMS` took the `IES = 2` path 1,142 times, but never with `LDIFAD`: PARMIN stops any run that sets `LDIFAD` with rotation ([parmin.f, lines 999–1006](https://github.com/yreclab/yrec/blob/7be4133/src/parmin.f#L999-L1006)), so the bug cannot be reached at 7be4133. What remains is code that no run takes.

### VCIRC

Velocities of meridional circulation (Zahn 1991, with Zahn 1992's quadrupole term, or Kippenhahn & Möllenhoff 1974), the GSF instability (Kippenhahn 1980) and secular and dynamical shear at each radiative interface, with $`\mu`$-gradient inhibition (Zahn & Maeder 1998, or Kippenhahn & Möllenhoff's $`\mu`$ currents), the user's scale factors and averaging between iterations.
