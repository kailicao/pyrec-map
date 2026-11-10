## Explanation

**Purpose.** This file computes acoustic depths: the sound travel time from the surface to the center, $t_\mathrm{norm}$, and from the surface to the base of the convection zone, $t_\mathrm{CZ}$. It joins the interior model and a fresh envelope integration into one profile, computes the sound speed at each point from the equation of state, and integrates $dr/c_s$.

**How it fits.**
- **Inputs:** the arguments, the interior model `HR`, `HD`, `HP`, `HT` ($\log r$, $\log\rho$, $\log P$, $\log T$), `HCOMP` (composition), `M` (last interior point), `JENV` (the base of the convection zone), `RCZL` ($\log r_\mathrm{CZ}/R_\odot$), `BL`, `TEFFL`, `FP`, `FT`, `HSTOT`, `DAGE` (the age), `CMIXL` (the mixing length, passed on to ENVINT).
- **Who calls it:** [[wrtout.f#WRTOUT|WRTOUT]], when the options `LACOUT` and `LADON` are on and the model has a convective envelope (`JENV > 1`) ([[wrtout.f#L696-L700]]). `LACOUT` is in no namelist and set nowhere, so it keeps its initial value, false ([[acdpth_mod.f#L55]]), and CALCAD never runs today (settled from the code, Nov 9, 2026; see [[acdpth_mod.f#ACDPTH_MOD|`ACDPTH_MOD`]]).
- **What it calls:** [[envint.f#ENVINT|ENVINT]] (the envelope, which fills `/ENVSTRUCT/`); for the sound speed, [[esac06.f#ESAC06|ESAC06]] (OPAL 2006 EOS) or [[eqstat2.f#EQSTAT2|EQSTAT2]]; [[splinj.f#SPLINJ|SPLINJ]] and [[splint.f#SPLINT|SPLINT]] to interpolate at $r_\mathrm{CZ}$; [[boole.f#BOOLE|BOOLE]] to integrate.
- **Outputs:** in `/ACDPTH/`, `TNORM`, `TCZ`, `TAUCZN` $= t_\mathrm{CZ}/t_\mathrm{norm}$, `TATMOS` (always 0, see below) and `DELADJ` ($\nabla_\mathrm{ad}$ at each point). WRTOUT prints them in its output columns (its comment: columns 68–70). A line to `ISHORT` at every call; with `LCLCD`, the full profile to unit `ICLCD`.
- **Modules:** [[acdpth_mod.f#ACDPTH_MOD|`ACDPTH_MOD`]] (with ENVINT, [[getopal95.f#GETOPAL95|GETOPAL95]], the main program, PARMIN, WRTOUT; it also holds the output switches `LCLCD`, `LADON`, `LACOUT`); [[envstruct_mod.f#ENVSTRUCT_MOD|`ENVSTRUCT_MOD`]] (the envelope profile, filled by ENVINT); [[nmlpar_mod.f#NMLPAR_MOD|`NMLPAR_MOD`]] (the integration step sizes `ATMBEG` … `ENVMAX` and `ATMSTP`, `ENVSTP`, the spot parameters `SPOTF`, `SPOTX`, and the switch `LOPALE06`); [[eos06misc_mod.f#EOS06MISC_MOD|`EOS06MISC_MOD`]] (ESAC06's output `EOS`); `COMP_MOD`, `CONSTANTS_MOD`, `IOUNITS_MOD` (the units `ISHORT`, `ICLCD`) and `DIMENSIONS_MOD`.

**The method.**
1. **The envelope.** Set the atmosphere and envelope step sizes to the fixed values `ATMSTP`, `ENVSTP`, then integrate the envelope with [[envint.f#ENVINT|ENVINT]] (with the model's mixing length `CMIXL`), from the surface to the interior's outer point, with
$$\log R = \tfrac12(\log L - \log 4\pi - \log\sigma - 4\log T_\mathrm{eff}), \qquad \log g = \log G + \log M - 2\log R.$$
For a spotted star (`SPOTF` $\ne 0$, `SPOTX` $\ne 1$) and only when `JENV = M`, the envelope uses the ambient temperature
$$\log T_\mathrm{amb} = \log T_\mathrm{eff} - \tfrac14\log_{10}\!\left(f_s x_s^4 + 1 - f_s\right),$$
with $f_s$ = `SPOTF` (the spot filling factor) and $x_s$ = `SPOTX` (probably the spot-to-ambient temperature ratio).

    `JENV = M` holds when no surface convection zone is found ([[findsh.f#L113-L120]]), so the spot correction here applies only to stars without one, the opposite of the routines that test `LC(M)` ([[stitch.f#b6]]).

2. **One profile.** The interior points $1..M$, then envelope points $2..N_\mathrm{env}$, in linear units, $T$ in $10^6$ K.
3. **Sound speed.** With the OPAL 2006 EOS, $\Gamma_1$ = `EOS(8)` and $\nabla_\mathrm{ad} = 1/$`EOS(9)` (`EOS(9)` is $\Gamma_2/(\Gamma_2-1)$). Otherwise, from EQSTAT2's derivatives (`QDPJ`, `QDTJ`, probably $(\partial\ln\rho/\partial\ln P)_T$ and $(\partial\ln\rho/\partial\ln T)_P$) and $c_P$, by Cox and Giuli's chapter 9:
$$\chi_\rho = \frac{1}{\mathtt{QDP}}, \quad \chi_T = -\chi_\rho\,\mathtt{QDT}, \quad c_V = c_P - \frac{P}{\rho T}\frac{\chi_T^2}{\chi_\rho}, \quad \Gamma_1 = \frac{\chi_\rho\,c_P}{c_V}.$$
The code stores the inverse sound speed $1/c_s$, with $c_s = \sqrt{\Gamma_1 P/\rho}$.
4. **Integrate** with Boole's rule:
$$t_\mathrm{norm} = \int_0^{R} \frac{dr}{c_s}, \qquad t_\mathrm{CZ} = \int_{r_\mathrm{CZ}}^{R} \frac{dr}{c_s},$$
in seconds. For $t_\mathrm{CZ}$, the point just below $r_\mathrm{CZ}$ is replaced by $r_\mathrm{CZ}$ itself, with $1/c_s$ from a cubic spline through 7 neighboring points.

    The surface point of the profile is left out of both integrals ([[#b8]]).

5. $\tau_\mathrm{CZ,n} = t_\mathrm{CZ}/t_\mathrm{norm}$.

The atmosphere's acoustic depth (`TATMOS`) was computed by a section now commented out ([[#L387-L437]]), so it is always 0.

> **Question** ([[#L186]]; [[#L444-L446]]). **The atmosphere's acoustic depth.** `TATMOS` is always 0, yet it is written to `ISHORT` at every call. Should the atmosphere part be restored or removed?

**Design.** The header lists `IACAT`, `IJLAST` and other output switches, some marked "obsolete?" (`IACAT` and the other unused unit numbers are no longer in the module). Many local variables and arrays remain from the commented-out sections.

**Changed since `rp_1`.** The new argument `CMIXL`, passed on to ENVINT; otherwise declarations only: COMMON blocks to modules, `IMPLICIT NONE`, unused blocks removed (among them a wrong `/LLOT95/` declaration that aliased `ZTAB` to an opacity value, harmless since nothing here reads it).

## Bugs, by priority

1. **(cannot be reached)** **Step sizes not restored.** ([[#L196-L207]]; [[#L233-L235]]; [[wrtmod.f#L237-L242]]) The routine saves `ATMBEG`, `ATMMIN`, `ATMMAX`, `ENVBEG`, `ENVMIN`, `ENVMAX` in `ABEG0` … `EMAX0`, sets them to `ATMSTP`/`ENVSTP` for its own envelope integration, and never restores them. Later envelope integrations in the same run (the surface boundary condition at every step) then use the fixed steps. [[wrtmod.f#WRTMOD|WRTMOD]], whose code the comment says CALCAD copied ([[#L194-L195]]), does restore them. Not reachable today (`LACOUT` is set nowhere, above).

    **A possible fix:**

    ```diff
    --- a/src/calcad.f
    +++ b/src/calcad.f
    @@ -230,9 +230,18 @@
           ELSE
                 ATEFFL = TEFFL
           ENDIF
    +C 11/09/26 KC via Claude
    +C code changed to restore the integration step sizes after the
    +C envelope integration, as WRTMOD does.
           CALL ENVINT(BJ,FPLJ,FTLJ,GLJ,HSTOT,IXXJ,LPRTJ,LSBC0J,
          *         PLIMJ,RLJ,ATEFFL,XJ,ZJ,DUM1,IDUMJ,KATMJ,KENVJ,KSAHAJ,
          *         DUM2,DUM3,DUM4,LPULPTJ,CMIXL)
    +      ATMBEG = ABEG0
    +      ATMMIN = AMIN0
    +      ATMMAX = AMAX0
    +      ENVBEG = EBEG0
    +      ENVMIN = EMIN0
    +      ENVMAX = EMAX0
     C      G Somers END
     
     
    ```

    **Checked by running YREC** (Nov 9, 2026; a line added at each suspected path counted how often it was taken, the outputs otherwise unchanged): Not reached in any of 34 runs: 26 of YREC's cases, from a 0.04 $M_\odot$ brown dwarf and the solar models to 9 $M_\odot$, rotation, and helium burning, and 8 made-up ones; it cannot be reached at 7be4133, since CALCAD runs only when `LACOUT` is true, and `LACOUT` is false in the source and in no namelist ([[acdpth_mod.f#b1]]). The fix was not run. Since nothing goes wrong until that switch is opened, it is fragile code, to be fixed before `LACOUT` is made settable. Intent: none found; [[wrtmod.f#WRTMOD|WRTMOD]], which the comment says this code copies, restores the step sizes. Related: [[stitch.f#STITCH|STITCH]] sets the same six step sizes and does not restore them either ([[stitch.f#b1]]); it runs at each store with `LSTORE`, `LSTCH`, and `LSTENV` on, and its check in the same round found a real but small effect ($\log L$ by up to 5.8e-5 dex, against 9.4e-9 dex for the null change).

2. **(cannot be reached)** **The interior's $Z$.** ([[#L246-L247]]; [[#L283]]) `STARZ(I) = HCOMP(3,M)` for every interior point: the envelope's $Z$, not the local one, while `STARX(I)` takes the local $X$. It is used only on the non-OPAL path (EQSTAT2, when `LOPALE06` is off, its default). With diffusion or burning that changes $Z$, the interior $Z$ differs. Not reachable today (`LACOUT` is set nowhere, above).

    **A possible fix:**

    ```diff
    --- a/src/calcad.f
    +++ b/src/calcad.f
    @@ -244,7 +244,9 @@
                 STARD(I)=DEXP(CLN*HD(I))
                 STARP(I)=DEXP(CLN*HP(I))
                 STARX(I)=HCOMP(1,I)
    -            STARZ(I)=HCOMP(3,M)
    +C 11/09/26 KC via Claude
    +C code changed to take the local Z at each interior point, as for X.
    +            STARZ(I)=HCOMP(3,I)
     34      CONTINUE
           DO 35, I=1,NUMENV-1
                 STARR(M+I)=DEXP(CLN*ENVR(I+1))
    ```

    **Checked by running YREC** (Nov 9, 2026; a line added at each suspected path counted how often it was taken, the outputs otherwise unchanged): Not reached in the same 34 runs; it cannot be reached at 7be4133, since CALCAD runs only when `LACOUT` is true, and `LACOUT` is false in the source and in no namelist ([[acdpth_mod.f#b1]]). Once it runs, this needs `LOPALE06` off (as in `testsuite/Test_solarGS98_yaleeos`) and a $Z$ that varies inside, as with diffusion. The fix was not run. Since nothing goes wrong until that switch is opened, it is fragile code, to be fixed before `LACOUT` is made settable. Intent: none found; the envelope loop takes the outer point's $X$ and $Z$ throughout ([[#L249-L256]]), while this loop takes the local $X$.

3. **(cannot be reached)** **`ICZ` may be stale.** ([[#L333-L351]]; [[#L370-L373]]) `ICZ`, the point just below $r_\mathrm{CZ}$, is set only when a pair of points brackets $r_\mathrm{CZ}$, and is kept between calls (`SAVE`). Inside the loop, the replacement at `I.EQ.ICZ` is tested before the bracket is found, so a value from an earlier call that is below this call's bracket matches first: The spline replaces a point below $r_\mathrm{CZ}$, `FLG` is set, and the real point just below $r_\mathrm{CZ}$ is not replaced, so $t_\mathrm{CZ}$ starts from that point instead of $r_\mathrm{CZ}$. If no pair brackets $r_\mathrm{CZ}$, the old `ICZ` is used (undefined at the first call; 0 makes loop 27 read `STARR(0)`). The 7-point stencil `ICZ-3 … ICZ+3` is also not checked against the end of the profile. Not reachable today (`LACOUT` is set nowhere, above).

    **A possible fix:**

    ```diff
    --- a/src/calcad.f
    +++ b/src/calcad.f
    @@ -330,10 +330,15 @@
     
     
     C      get the location of the convection zone, and count nonzero entries:
    +C 11/09/26 KC via Claude
    +C code changed to reset ICZ at each call and to find the bracket
    +C before the replacement is tested.
                       IENDJ=0
                       FLG=0
    +                  ICZ=0
                       DO 22, I=1,K
    -                        IF (STARR(I).LE.RCZ(1) .AND. STARR(I+1).GE.RCZ(1)) THEN
    +                        IF (ICZ.EQ.0 .AND. STARR(I).LE.RCZ(1) .AND.
    +     *                      STARR(I+1).GE.RCZ(1)) THEN
                                   ICZ = I
                             ENDIF
     
    ```

    (A call with no bracket would still need a decision, such as `TCZ` = 0.)

    **Checked by running YREC** (Nov 9, 2026; a line added at each suspected path counted how often it was taken, the outputs otherwise unchanged): Not reached in the same 34 runs; it cannot be reached at 7be4133, since CALCAD runs only when `LACOUT` is true, and `LACOUT` is false in the source and in no namelist ([[acdpth_mod.f#b1]]). Once it runs, a stale `ICZ` needs a second call with a surface convection zone. The fix was not run. Since nothing goes wrong until that switch is opened, it is fragile code, to be fixed before `LACOUT` is made settable. Intent: none found.

4. **(cannot be reached)** **`FXIONJ` is a scalar.** ([[#L82]]; [[#L292]]; [[eqstat2.f#L54]]; [[eqstat2.f#L171-L173]]) CALCAD passes the scalar `FXIONJ` where EQSTAT2 declares `FXION(3)` and writes three elements, so EQSTAT2 writes past it, into whatever CALCAD stores next. On the non-OPAL path (`LOPALE06` off, its default). Not reachable today (`LACOUT` is set nowhere, above).

    **A possible fix:**

    ```diff
    --- a/src/calcad.f
    +++ b/src/calcad.f
    @@ -79,9 +79,13 @@
     C explicit declarations.
           IMPLICIT NONE
           REAL*8 AMUJ,ATEFFL,BET14J,BETAIJ,BETAJ,BL,CHRH,CHT,CMIXL,CVJ,DAGE,
    -     *       DELAJ,EMUJ,ETAJ,FP,FPLJ,FT,FTLJ,FXIONJ,HCOMP,HD,HP,HR,
    +     *       DELAJ,EMUJ,ETAJ,FP,FPLJ,FT,FTLJ,HCOMP,HD,HP,HR,
          *       HSTOT,HT,QAPJ,QATJ,QCPJ,QCPPJ,QCPTJ,QDPJ,QDTJ,QDTPJ,QDTTJ,
          *       RCZ,RCZL,RMUJ,STD,STDL,STP,STPL,STT,STTL,STX,STZ,TEFFL
    +C 11/09/26 KC via Claude
    +C code changed to declare FXIONJ with the three elements EQSTAT2
    +C fills.
    +      REAL*8 FXIONJ(3)
           INTEGER IORDER,IRAD,JENV,KHI,KLO,M,MV,MX,NR,NT
           LOGICAL*4 LATMOJ,LCALCJ,LDERIJ
     C 10/9/26 MHP via Claude
    ```

    (with `FXIONJ` dropped from the `REAL*8` list at [[#L82]]).

    **Checked by running YREC** (Nov 9, 2026; a line added at each suspected path counted how often it was taken, the outputs otherwise unchanged): Not reached in the same 34 runs; it cannot be reached at 7be4133, since CALCAD runs only when `LACOUT` is true, and `LACOUT` is false in the source and in no namelist ([[acdpth_mod.f#b1]]). Once it runs, this needs `LOPALE06` off. The write past `FXIONJ` cannot be counted without reading the memory it overwrites, so only the call was to be counted. The fix was not run. Since nothing goes wrong until that switch is opened, it is fragile code, to be fixed before `LACOUT` is made settable. Intent: none found.

5. **(cannot be reached)** **EOS errors ignored.** ([[#L269-L273]]) ESAC06's alternate return `*999` jumps to the next statement, so a failed EOS call uses the `EOS` values of the previous point; ESAC06 writes a message to `ISHORT`, but CALCAD goes on. Only with `LOPALE06`, for points outside the OPAL table. Not reachable today (`LACOUT` is set nowhere, above).

    **A possible fix:** a choice for the developers: fall back to EQSTAT2 for that point, as the EOS does elsewhere outside the table, or stop.

    **Checked by running YREC** (Nov 9, 2026; a line added at each suspected path counted how often it was taken, the outputs otherwise unchanged): Not reached in the same 34 runs; it cannot be reached at 7be4133, since CALCAD runs only when `LACOUT` is true, and `LACOUT` is false in the source and in no namelist ([[acdpth_mod.f#b1]]). Once it runs, this needs `LOPALE06` on and points outside the OPAL table ([[esac06.f#L488-L494]]). The fix (measurement only: recomputing such a point with EQSTAT2) was not run. Since nothing goes wrong until that switch is opened, it is fragile code, to be fixed before `LACOUT` is made settable. Intent: none found.

6. **(cannot be reached)** **Output format.** ([[#L445-L446]]) Format 67 has no space before "Acoustic depth of atmopshere" (also misspelled), so the line runs the two together. Not reachable today (`LACOUT` is set nowhere, above).

    **A possible fix:**

    ```diff
    --- a/src/calcad.f
    +++ b/src/calcad.f
    @@ -442,8 +442,11 @@
     
     C Output acoustic depth info to ISHORT
           WRITE(ISHORT,67)TCZ,TNORM,TAUCZN,TATMOS
    +C 11/09/26 KC via Claude
    +C code changed to separate and correct the last label of format 67.
     67       FORMAT(1X,'Acoustic depth to CZ:',F14.8,2X,'Acoustic depth to center',
    -     *F13.7,2X,'Normalized taucz:',F11.9, 'Acoustic depth of atmopshere:',F16.8,2X)
    +     *F13.7,2X,'Normalized taucz:',F11.9,2X,'Acoustic depth of atmosphere:',
    +     *F16.8,2X)
     
     C 555            CONTINUE
     C--------------------------------------------------------------
    ```

    **Checked by running YREC** (Nov 9, 2026; a line added at each suspected path counted how often it was taken, the outputs otherwise unchanged): Not reached in the same 34 runs; it cannot be reached at 7be4133, since CALCAD runs only when `LACOUT` is true, and `LACOUT` is false in the source and in no namelist ([[acdpth_mod.f#b1]]). The fix was not run. Since nothing goes wrong until that switch is opened, it is a defect only in output that is never written, to be fixed before `LACOUT` is made settable. Intent: none found.

7. **(cannot be reached)** **A short profile.** ([[#L317-L322]]; [[#L441]]; [[boole.f#L56-L63]]) If `K ≤ 3`, `NN = 2` and BOOLE returns 0, so `TAUCZN` divides by zero. A profile that short does not occur in a real model. Not reachable today (`LACOUT` is set nowhere, above).

    **A possible fix:**

    ```diff
    --- a/src/calcad.f
    +++ b/src/calcad.f
    @@ -437,8 +437,10 @@
     c      CALL BOOLE(ATMOSR,ATMOSC,V,NN,TATMOS)
     
     C Output normalized acoustic depth
    +C 11/09/26 KC via Claude
    +C code changed to leave TAUCZN at zero when TNORM is zero.
           TAUCZN=0.0D0
    -      TAUCZN=TCZ/TNORM
    +      IF (TNORM.GT.0.0D0) TAUCZN=TCZ/TNORM
     
     C Output acoustic depth info to ISHORT
           WRITE(ISHORT,67)TCZ,TNORM,TAUCZN,TATMOS
    ```

    **Checked by running YREC** (Nov 9, 2026; a line added at each suspected path counted how often it was taken, the outputs otherwise unchanged): Not reached in the same 34 runs; it cannot be reached at 7be4133, since CALCAD runs only when `LACOUT` is true, and `LACOUT` is false in the source and in no namelist ([[acdpth_mod.f#b1]]), and `K` ≤ 3 needs a profile of 5 points or fewer. The fix was not run. Intent: none found.

8. **(cannot be reached)** **The surface point is left out of the integrals.** ([[#L310-L322]]; [[#L241-L256]]; [[boole.f#L41-L52]]) Loops 34 and 35 build a profile of $M + N_\mathrm{env} - 1$ points, and the sound speed is computed at all of them ([[#L264]]; [[#L278]]), but `K = NUMENV-1+M-1` ([[#L310]]), one point fewer, is passed to BOOLE as the number of points, and BOOLE integrates over its first `N` points only ([[boole.f#L41-L52]]). The profile for $t_\mathrm{CZ}$ ends at point `K` too ([[#L370-L373]]). What follows: Both $t_\mathrm{norm}$ and $t_\mathrm{CZ}$ leave out the outermost interval, between the envelope's last two points, although the sound speed at the surface point is computed as at the others. Not reachable today (`LACOUT` is set nowhere, above).

    **A possible fix:**

    ```diff
    --- a/src/calcad.f
    +++ b/src/calcad.f
    @@ -307,8 +307,11 @@


     C Integrate for the full acoustic depth for normalization
    -      K=NUMENV-1+M-1
    -      U=MOD((NUMENV-1+M-1),4)
    +C 11/10/26 KC via Claude
    +C code changed to integrate over all M+NUMENV-1 points of the profile,
    +C the surface point included.
    +      K=NUMENV-1+M
    +      U=MOD(K,4)
           IF (U.NE.0) THEN
                 NN=K+4-U+1
           ELSE
    @@ -332,7 +335,10 @@
     C      get the location of the convection zone, and count nonzero entries:
                       IENDJ=0
                       FLG=0
    -                  DO 22, I=1,K
    +C 11/10/26 KC via Claude
    +C code changed to stop the search one point short of K, so that
    +C STARR(I+1) stays inside the profile.
    +                  DO 22, I=1,K-1
                             IF (STARR(I).LE.RCZ(1) .AND. STARR(I+1).GE.RCZ(1)) THEN
                                   ICZ = I
                             ENDIF
    ```

    **Checked by running YREC** (Nov 10, 2026; a line added at each suspected path counted how often it was taken, the outputs otherwise unchanged): Not reached in five of YREC's cases, `testsuite/Test_m1p0feh+0p0GS98_base_TAMS`, `testsuite/Test_m0p3feh+0p0GS98_base_ZAMS`, `testsuite/Test_m1p4feh+0p0GS98_dif_TAMS` (with diffusion), `testsuite/Test_m0p8feh+0p0GS98_rotp8p0d0p1mag1e4std_TAMS` (with rotation), and `examples/run_standard_solar_model/Test_solarcal_noGS_norot` (the solar calibration): A line at [[#L310]] never counted a call. It cannot be reached at 7be4133, since CALCAD runs only when `LACOUT` is true, and `LACOUT` is false in the source and in no namelist ([[acdpth_mod.f#b1]]). The fix was not run; since nothing goes wrong until that switch is opened, it is fragile code, to be fixed before `LACOUT` is made settable. Intent: none found.

### CALCAD

Integrates the envelope, joins it to the interior, computes $1/c_s$ from the EOS and integrates it with [[boole.f#BOOLE|BOOLE]] to get the acoustic depth of the star and of its convection zone (`TNORM`, `TCZ`, `TAUCZN` in `/ACDPTH/`).
