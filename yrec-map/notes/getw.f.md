## Explanation

**Purpose.** `GETW` evolves the internal rotation over one model time step. In its header's words (MHP 11/91, replacing the old `FINDW`): it "enforces local conservation of angular momentum in radiative regions, and enforces the user-specified rotation law in convective regions"; it solves for the transport of angular momentum and the associated mixing if desired (`LINSTB`), accounts for angular momentum loss by a magnetic wind (`LJDOT0`), and, with instabilities, burns lithium and beryllium (`LEXCOM`). The method is that of Pinsonneault, Kawaler, Sofia and Demarque (1989, ApJ 338, 424), as the header cites. It is the central routine of YREC's rotation.

**How it fits.**
- **Who calls it:** only the main program ([[main.f#(file level)|main.f]]), once per model step.
- **Inputs:** the model at the end of the step (`HCOMP`, `HD`, `HL`, `HP`, `HR`, `HS`, `HS1`, `HS2`, `HT`, `LC`, `M`, `HSTOT`, `BL`, `TEFFL`, `SMASS`), the form factors `FP`, `FT`, the step `DELTS`, the limit `DWMAX`, `HJM` ($j$ per shell), the mixing-length parameter `CMIXL` (passed to `PHYSIC` and `GETTAU`) and the print flag `LPRT0` (set by the main program); both are arguments since `rp_1`. The model at the start of the step comes from the modules `OLDMOD_MOD`, `OLDPHY_MOD`, `OLDROT_MOD`, `OLDROT2_MOD`.
- **What it calls** (in order of use): [[ovrot.f#OVROT|OVROT]] (convective and overshoot zones for angular momentum: the flags `LCZ`), [[getrot.f#GETROT|GETROT]] ($\Omega$ from $j$), [[mwind.f#MWIND|MWIND]] (wind loss) and [[wczimp.f#WCZIMP|WCZIMP]] (rotation law in the surface convection zone after the loss), [[physic.f#PHYSIC|PHYSIC]] (gradients, viscosities, diffusivities), [[gettau.f#GETTAU|GETTAU]] (convective overturn time for the wind; its argument `RBCZ`, the radius of the convection zone's base, goes to `ENVR`, a local scalar never read afterwards, [[#L243-L244]]: unused?), [[midmod.f#MIDMOD|MIDMOD]] (the structure interpolated in time within the step), [[mixcz.f#MIXCZ|MIXCZ]] (homogenize convection zones), [[seculr.f#SECULR|SECULR]] (the secular instabilities, solved as diffusion equations), [[convec.f#CONVEC|CONVEC]], [[lirate88.f#LIRATE88|LIRATE88]], [[liburn.f#LIBURN|LIBURN]] or [[liburn2.f#LIBURN2|LIBURN2]] (light-element burning), and [[bursmix.f#BURSMIX|BURSMIX]] (Bulirsch–Stoer mixing plus burning).
- **Outputs:** `HJM`, `OMEGA`, `HI`, `ETA2`, `QIW`, `R0` (new rotation), `HCOMP` (mixed and burned composition), `LJDOT`, `JENV0`; and through modules: `HCOMPP` in `OLDMOD_MOD` (beginning-of-step composition for the next step), the lithium rates in `OLDRAT_MOD`, `PSCAL0`/`PSCAL1` in `LIOV_MOD`, `FRACSTEP` and `TAUCZ` in `OVRTRN_MOD`. `HCOMPS`, the composition at the start of the step (the former `/OLDAB/`), is now GETW's own array, filled by `MIDMOD` and passed to `SECULR`.
- **Modules** (COMMON blocks until `rp_1`, about thirty then, several of them unused): `NMLPAR_MOD` for the run's settings (`LINSTB`, `LSOLID`, `IMPJMOD`, `LJDOT0`, `LDISK`, `TDISK`, `DTDIF`, `DTWIND`, `LEXCOM`, and the overshoot's `LOVSTE`, `ALPHAE`), `DISK_MOD` (`SAGE`), `OLDMOD_MOD`, `OLDROT_MOD`, `OLDROT2_MOD` (previous model), `MDPHY_MOD`, `TEMP_MOD`, `OLDPHY_MOD` (physics at mid-step and at the start), `NEWRAT_MOD`, `OLDRAT_MOD` (lithium rates), `QUADRU_MOD` (quadrupole moment, from [[getqua.f#GETQUA|GETQUA]]), `LIOV_MOD` (overshoot), `OVRTRN_MOD`, `DIMENSIONS_MOD`, `CONSTANTS_MOD`.

**The method.**
1. `OVROT` marks the shells that rotate as convective (convection zones plus overshoot). Disk locking holds the surface rotation while the age is below `TDISK`.
2. **Without instabilities** (`LINSTB` false): $\Omega$ from $j$ (`GETROT`; with `LSOLID` or `IMPJMOD` = 1 the whole star is treated as convective, so it rotates as a solid body). If the wind is on and the surface is convective, `MWIND` removes angular momentum over the whole step from the surface convection zone (or the whole star), with `FRACSTEP` = 0.5 ("timestep average loss rate": the point in the step at which [[mwind.f#MWIND|MWIND]] interpolates $\tau_\mathrm{cz}$, so 0.5 uses its mid-step value), and `WCZIMP` resets its rotation. Done.

    > **Question** ([[#L204-L210]]; [[#L304-L311]]). **Wind without instabilities.** Here the wind acts once over the whole step, with `FRACSTEP` = 0.5, whereas with instabilities it acts per substep (in `SECULR`, or at [[#L304-L311]] for a fully convective star), with `FRACSTEP` the substep's fraction. Are the two treatments meant to agree for the same model?

3. **With instabilities**, the step is divided into $N$ diffusion substeps, $\Delta t = \Delta t_\mathrm{model}/N$, $N = \min(\lceil \mathrm{DWMAX}/\mathrm{DTDIF}\rceil, \lceil \mathrm{DTWIND}/\mathrm{DTDIF}\rceil)$. All three are fractional changes of $\Omega$, not times: `DWMAX` is the largest $2|\Omega-\Omega_\mathrm{old}|/(\Omega+\Omega_\mathrm{old})$ of the last step ([[wtime.f#WTIME|WTIME]]), `DTWIND` the largest $\Delta\Omega/\Omega$ allowed per model step (WTIME's comment), `DTDIF` the largest per substep ([[remap.f#REMAP|REMAP]] sets them from `TIME_DW_GLOBAL` and `TIME_DW_MIX`); `DWMAX` = 0 is replaced by `DTWIND`. `PHYSIC` and `GETTAU` are called once. Then, for each substep:
   - `MIDMOD` interpolates the structure linearly in time to the substep's fraction $f$ = `SUMDT/DELTS`, and the time derivative of $\theta$ (Maeder & Zahn 1998, per the comment) is updated from $\Omega$: $\theta \propto \bar\Omega\,\Delta\Omega/\Delta r$. GETW stores, at each interface, `THP` $= (r^2/g)\,\bar\Omega\,d\Omega/dr$, with `THM` $= r^2/g$ from [[setupv.f#SETUPV|SETUPV]], and with `LDIFAD` [[vcirc.f#VCIRC|VCIRC]] turns its change over the substep into the $d\Theta/dt$ term (`THN`) of the meridional circulation. At the first substep `THP` is the previous model's value `THO` ([[#L271-L278]]); at later ones it is recomputed from `OMEGA`, which is not updated until the end of the step (bug 1);

    > **Question** ([[#L286]]; [[setupv.f#L306-L308]]). **A factor of 2/3 in $\Theta$?** Zahn (1992) and Maeder & Zahn (1998) write $\Theta = \frac{r^2}{3g}\frac{d\Omega^2}{dr} = \frac23\frac{r^2}{g}\Omega\frac{d\Omega}{dr}$; GETW's `THP(I) = THM(I)*WMID*QW`, with `THM` $= r^2/g$ (SETUPV), has no $\tfrac23$, and VCIRC's `THN = FESTIME*(THM*QW-THP)/DT` ([[vcirc.f#L256]]), with `FESTIME` $= P/(g\,\Delta\nabla\,\rho)$ (SETUPV), adds none, so if the code's $\theta$ (named only as the "d theta/dt term from Zahn & Maeder 1998," [[#L269-L290]]) is Zahn's $\Theta$, `THP` is $\tfrac32\Theta$. Is the factor absorbed elsewhere (in `FACT7`/`FACT8`, or in the factor $\tfrac15$ of `VESA`), or missing?

   - for a fully convective star (`LALLCZ`), `MWIND` and `WCZIMP` remove angular momentum over the substep here; otherwise the wind's quantities (`HICZ`, `HSBOT`, `HSTOP`, `OMEGAS`, `LCZSUR`) go to `SECULR`, which calls `MWIND` itself;
   - unless the star is fully convective, `MIXCZ` homogenizes convection zones and `SECULR` solves the diffusion equations for $j$ and composition. If it asks for a shorter step (`LREDO`), [[checkj.f#CHECKJ|CHECKJ]] or [[checkc.f#CHECKC|CHECKC]] has already halved `DT`; $j$, the composition and $\mu$ are restored, `SUMDT` goes back by $2\,$`DT` (the old substep), and the substep is redone;
   - the composition at the start of the next substep is stored (`HCOMPP`);
   - with the extended composition (`LEXCOM`): the depth of the convection zone (`CONVEC`), the overshoot depth $\ell = \alpha_e H_p$ with $H_p = Pr^2/(\rho Gm)$, the light-element rates (`LIRATE88`: its end-of-step rates `RLI6`, `RLI7`, `RBE9`, on the model `HDM`, `HTM` from `MIDMOD`) and burning (`LIBURN`, or `LIBURN2` with the Bulirsch–Stoer option), mixing, and abundances below $10^{-24}$ set to zero. The Bulirsch–Stoer option is unused?: `LBURS` is set false at [[#L140]] and never changed, so the `LIBURN2` branch ([[#L414-L418]]) and the call to `BURSMIX` ([[#L455-L461]]) are never reached. So [[bursmix.f#BURSMIX|BURSMIX]] and [[bsrotmix.f#BSROTMIX|BSROTMIX]] are not reached at 7be4133; their suspected bugs ([[bursmix.f#b1]], [[bsrotmix.f#b1]]) are marked so.
4. At the end, $\Omega$ is recomputed from the final $j$ with `GETROT`.
5. If `LPRT0` is set, it prints the surface quadrupole term: with $R$ from $L$ and $T_\mathrm{eff}$, $Q_\mathrm{surf} = (r_M/R)^3\,\phi_M$, $\Phi = GM/R$, and $-\tfrac32 Q_\mathrm{surf}/\Phi$. The argument `BL` is first overwritten with $\log_{10}$ `HL(M)` ([[#L472]]), the value and units (solar) that [[crrect.f#CRRECT|CRRECT]] gives it ([[crrect.f#L112]]); the units match, as line 473 adds `CLSUNL` to it (settled from the code, Nov 9, 2026).

**Changed since `rp_1`.** Two new arguments, `CMIXL` (passed on to `PHYSIC` and `GETTAU`) and `LPRT0` (formerly `/ROTPRT/`); `HCOMPS` (formerly `/OLDAB/`) is a local array passed to `MIDMOD` and `SECULR`; the local `LFIRST` renamed `LFIRSTIT`; COMMON blocks to modules, `IMPLICIT NONE`, and the unused blocks removed. `ENVR` is now declared (see What it calls).

**Changed since `a8a5950`.** `LIRATE88` is called with `J` = 1, which evaluates the model passed in and fills the end-of-step rates; with `J` = 2 it ignored `HDM` and `HTM` and recomputed the start-of-step rates, so that `LIBURN` interpolated between two copies of the start-of-step rates.

## Bugs, by priority

1. **(changes results, small)** **Checked by KC** (Nov 10, 2026). **`THP` and `WMST` recomputed from a stale `OMEGA` after the first substep.** ([[#L280-L290]]; [[#L465-L467]]) From the second substep on, GETW recomputes `THP` (the previous $\theta$, for VCIRC's $d\Theta/dt$ term `THN = FESTIME*(THM*QW-THP)/DT`, [[vcirc.f#L256]]) and `WMST` (the starting rotation; SECULR passes `WMST(M)` to MCOWIND as the wind's starting rate `WBEG`, [[seculr.f#L201]]) from the argument `OMEGA`. But `OMEGA` is set by GETROT before the substeps ([[#L223]]) and copied from `OMEGAM` only after the last one ([[#L465-L467]]); the rotation evolved by SECULR is `OMEGAM`. So at every substep after the first, `THP` is the same profile, while `THM`, `HRM` and the current `QW` in VCIRC belong to the latest substep, and `THN` divides by one substep's `DT` a change accumulated over several. At the first substep the values are the previous model's (`THO`, `WOLD`, [[#L271-L278]]), the start of that substep, which is what the later ones would need too. What follows: `THN` wrong at substeps 2 and later, only with `LINSTB` and `LDIFAD` (both off by default) and more than one substep; the wind's starting rate likewise with `LINSTB` and the wind. `QWRMST`, also set here, is read nowhere (unused?).

    **A possible fix:** store the values at the end of each completed substep, from `OMEGAM`, so that a redo keeps those of the previous substep:

    ```diff
    --- a/src/getw.f
    +++ b/src/getw.f
    @@ -268,6 +268,10 @@
           ENDIF
     C COPY OVER PRIOR THETA(TIME) TERM TO TEMPORARY SLOT
     C FOR USE IN THE ADVECTION/DIFFUSION TREATMENT OF MAEDER&ZAHN 1998
    +C 11/09/26 KC via Claude
    +C code changed to store theta and the rotation at the end of each
    +C completed substep, from OMEGAM, for the next substep; the ELSE
    +C branch that recomputed them from OMEGA is removed.
           IF(LFIRSTIT)THEN
              THP(1) = THO(1)
              WMST(1) = WOLD(1)
    @@ -276,17 +280,6 @@
                 THP(I) = THO(I)
                 WMST(I) = WOLD(I)
              END DO
    -C RECOMPUTE THETA
    -      ELSE
    -         WMST(1) = OMEGA(1)
    -         DO I = 2,M
    -            WMID = 0.5D0*(OMEGA(I)+OMEGA(I-1))
    -            DR = 10.0D0**HRM(I)-10.0D0**HRM(I-1)
    -            QW = (OMEGA(I)-OMEGA(I-1))/DR
    -            THP(I) = THM(I)*WMID*QW
    -            QWRMST(I) = QW
    -            WMST(I) = OMEGA(I)
    -         END DO
           ENDIF
           FX = SUMDT/DELTS
           FRACSTEP = FX
    @@ -363,6 +356,15 @@
        80       CONTINUE
                 GOTO 40
              ENDIF
    +         WMST(1) = OMEGAM(1)
    +         DO I = 2,M
    +            WMID = 0.5D0*(OMEGAM(I)+OMEGAM(I-1))
    +            DR = 10.0D0**HRM(I)-10.0D0**HRM(I-1)
    +            QW = (OMEGAM(I)-OMEGAM(I-1))/DR
    +            THP(I) = THM(I)*WMID*QW
    +            QWRMST(I) = QW
    +            WMST(I) = OMEGAM(I)
    +         END DO
           ENDIF
     C MHP 05/02 TAKEN OUT OF LOOP SO THAT NUCLEAR BURNING
     C IS ACCOUNTED FOR IN MODELS THAT ARE FULLY CONVECTIVE
    ```

    **How the code itself shows it.** The first substep's values are the rotation at the start of the step: HPOINT, under "STORE THE OLD MODEL STRUCTURE FOR USE IN DIFFUSION," sets `WOLD(I) = OMEGA(I)` ([[hpoint.f#L812-L814]]) and forms `THO(I)` from that `OMEGA` with `WMID = 0.5D0*(OMEGA(I)+OMEGA(I-1))` and `DW = OMEGA(I) - OMEGA(I-1)` ([[hpoint.f#L859-L866]]), the same form as [[#L283-L286]]. Within the step, the rotation that changes is `OMEGAM`: MIDMOD sets it from the current `HJM` at each substep ([[midmod.f#L494]]; [[midmod.f#L500]]), GETW passes it to SECULR as SECULR's `OMEGA` ([[#L344-L345]]; [[seculr.f#L6-L7]]), and GETW's `OMEGA` takes its value only after the last substep, under "UPDATE OMEGA ARRAY TO REFLECT NEW ANGULAR MOMENTUM DISTRIBUTION" ([[#L464-L467]]). In SECULR, the line that `WBEG = WMST(M)` replaced, `WBEG = OMEGA(M)`, is commented out under "STORE INITIAL SURFACE ANGULAR VELOCITY" ([[seculr.f#L198-L201]]); it read `OMEGAM(M)` as the substep began, the value the fix stores in `WMST`, up to MIDMOD's recomputation of `OMEGAM` at the next substep's start ([[midmod.f#L494]]; [[midmod.f#L500]]).

    **Checked by running YREC** (Nov 9, 2026; a line added at each suspected path counted how often it was taken, the outputs otherwise unchanged): The recomputation from `OMEGA` ran at every substep after the first in the four rotating test cases with `LINSTB` and more than one substep: 4,407 times in the solar case (`testsuite/Test_solarGS98_difrotmixper18p4d1p0`), 2,696 in the 0.8 $M_\odot$ case (`testsuite/Test_m0p8feh+0p0GS98_rotp8p0d0p1mag1e4std_TAMS`), and 48 and 50 in the two 2 $M_\odot$ cases. The surface `OMEGA` differed from the latest `OMEGAM` (by up to $8\times10^{-6}$ rad s$^{-1}$) in 1,019, 1,954, 48, and 50 of them. With the fix, the solar case stays within the noise ($\log L$ moves by up to 0.00013 dex, against 0.00019 for a null change, nearly every opacity (all with $3 \le \log T \le 9$ and $-6 \le \log\rho \le 9.75$) times $1 + 10^{-10}$ on the same case); the 0.8 $M_\odot$ case moves a little beyond it near its end, central $\log T$ by up to 0.0015 dex at 21.69 Gyr against 0.0002, and $\log L$ by 0.0004 against 0.00014, with 762 models instead of 763. So the wind's starting rate is stale, with a small effect. The `THN` part cannot be reached at 7be4133: It needs `LDIFAD`, and PARMIN stops any run that sets `LDIFAD` with rotation ([[parmin.f#L999-L1006]]). Intent: none found.

### GETW

Evolves $j$ and $\Omega$ over a model step: rotation laws in convective regions, wind loss, diffusion of angular momentum and composition by secular instabilities in substeps, and light-element burning (method above).
