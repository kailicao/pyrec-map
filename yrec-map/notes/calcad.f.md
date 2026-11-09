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

    > **Question** ([[#L228-L232]]; [[#L328]]). **Spots only at `JENV = M`.** The ambient temperature is used only when `JENV = M`, which is also exactly the case in which no convection zone is found (`TCZ` needs `JENV < M`), so the spot correction applies only to stars for which `TCZ = 0`. [[wrtmod.f#WRTMOD|WRTMOD]] has the same condition ([[wrtmod.f#L228]]). Why that condition?

2. **One profile.** The interior points $1..M$, then envelope points $2..N_\mathrm{env}$, in linear units, $T$ in $10^6$ K.
3. **Sound speed.** With the OPAL 2006 EOS, $\Gamma_1$ = `EOS(8)` and $\nabla_\mathrm{ad} = 1/$`EOS(9)` (`EOS(9)` is $\Gamma_2/(\Gamma_2-1)$). Otherwise, from EQSTAT2's derivatives (`QDPJ`, `QDTJ`, probably $(\partial\ln\rho/\partial\ln P)_T$ and $(\partial\ln\rho/\partial\ln T)_P$) and $c_P$, by Cox and Giuli's chapter 9:
$$\chi_\rho = \frac{1}{\mathtt{QDP}}, \quad \chi_T = -\chi_\rho\,\mathtt{QDT}, \quad c_V = c_P - \frac{P}{\rho T}\frac{\chi_T^2}{\chi_\rho}, \quad \Gamma_1 = \frac{\chi_\rho\,c_P}{c_V}.$$
The code stores the inverse sound speed $1/c_s$, with $c_s = \sqrt{\Gamma_1 P/\rho}$.
4. **Integrate** with Boole's rule:
$$t_\mathrm{norm} = \int_0^{R} \frac{dr}{c_s}, \qquad t_\mathrm{CZ} = \int_{r_\mathrm{CZ}}^{R} \frac{dr}{c_s},$$
in seconds. For $t_\mathrm{CZ}$, the point just below $r_\mathrm{CZ}$ is replaced by $r_\mathrm{CZ}$ itself, with $1/c_s$ from a cubic spline through 7 neighboring points.

    > **Question** ([[#L310]]; [[#L322]]; [[#L249-L256]]). **The last point.** `K = M + NUMENV - 2` is passed to BOOLE as the number of points, but the profile has $M + N_\mathrm{env} - 1$ points, so the outermost point is left out of both integrals. Is this intended (the surface point having $c_s$ ill-defined)?

5. $\tau_\mathrm{CZ,n} = t_\mathrm{CZ}/t_\mathrm{norm}$.

The atmosphere's acoustic depth (`TATMOS`) was computed by a section now commented out ([[#L387-L437]]), so it is always 0.

> **Question** ([[#L186]]; [[#L444-L446]]). **The atmosphere's acoustic depth.** `TATMOS` is always 0, yet it is written to `ISHORT` at every call. Should the atmosphere part be restored or removed?

**Design.** The header lists `IACAT`, `IJLAST` and other output switches, some marked "obsolete?" (`IACAT` and the other unused unit numbers are no longer in the module). Many local variables and arrays remain from the commented-out sections.

**Changed since `rp_1`.** The new argument `CMIXL`, passed on to ENVINT; otherwise declarations only: COMMON blocks to modules, `IMPLICIT NONE`, unused blocks removed (among them a wrong `/LLOT95/` declaration that aliased `ZTAB` to an opacity value, harmless since nothing here reads it).

## Bugs, by priority

1. **(a)** **Step sizes not restored.** ([[#L196-L207]]; [[#L233-L235]]; [[wrtmod.f#L237-L242]]) The routine saves `ATMBEG`, `ATMMIN`, `ATMMAX`, `ENVBEG`, `ENVMIN`, `ENVMAX` in `ABEG0` … `EMAX0`, sets them to `ATMSTP`/`ENVSTP` for its own envelope integration, and never restores them. Later envelope integrations in the same run (the surface boundary condition at every step) then use the fixed steps. [[wrtmod.f#WRTMOD|WRTMOD]], whose code the comment says CALCAD copied ([[#L194-L195]]), does restore them. Not reachable today (`LACOUT` is set nowhere, above). Read from the code, not run. **A possible fix:**

    ```fortran
    C 11/09/26 KC via Claude
    C code changed to restore the integration step sizes after the
    C envelope integration, as WRTMOD does.
          CALL ENVINT(BJ,FPLJ,FTLJ,GLJ,HSTOT,IXXJ,LPRTJ,LSBC0J,
         *         PLIMJ,RLJ,ATEFFL,XJ,ZJ,DUM1,IDUMJ,KATMJ,KENVJ,KSAHAJ,
         *         DUM2,DUM3,DUM4,LPULPTJ,CMIXL)
          ATMBEG = ABEG0
          ATMMIN = AMIN0
          ATMMAX = AMAX0
          ENVBEG = EBEG0
          ENVMIN = EMIN0
          ENVMAX = EMAX0
    ```

2. **(a)** **The interior's $Z$.** ([[#L246-L247]]; [[#L283]]) `STARZ(I) = HCOMP(3,M)` for every interior point: the envelope's $Z$, not the local one, while `STARX(I)` takes the local $X$. It is used only on the non-OPAL path (EQSTAT2, when `LOPALE06` is off, its default). With diffusion or burning that changes $Z$, the interior $Z$ differs. Not reachable today (`LACOUT` is set nowhere, above). Read from the code, not run. **A possible fix:**

    ```fortran
    C 11/09/26 KC via Claude
    C code changed to take the local Z at each interior point, as for X.
                STARZ(I)=HCOMP(3,I)
    ```

3. **(a)** **`ICZ` may be stale.** ([[#L333-L351]]; [[#L370-L373]]) `ICZ`, the point just below $r_\mathrm{CZ}$, is set only when a pair of points brackets $r_\mathrm{CZ}$, and is kept between calls (`SAVE`). Inside the loop, the replacement at `I.EQ.ICZ` is tested before the bracket is found, so a value from an earlier call that is below this call's bracket matches first: The spline replaces a point below $r_\mathrm{CZ}$, `FLG` is set, and the real point just below $r_\mathrm{CZ}$ is not replaced, so $t_\mathrm{CZ}$ starts from that point instead of $r_\mathrm{CZ}$. If no pair brackets $r_\mathrm{CZ}$, the old `ICZ` is used (undefined at the first call; 0 makes loop 27 read `STARR(0)`). The 7-point stencil `ICZ-3 … ICZ+3` is also not checked against the end of the profile. Not reachable today (`LACOUT` is set nowhere, above). Read from the code, not run. **A possible fix:**

    ```fortran
    C 11/09/26 KC via Claude
    C code changed to reset ICZ at each call and to find the bracket
    C before the replacement is tested.
                      IENDJ=0
                      FLG=0
                      ICZ=0
                      DO 22, I=1,K
                            IF (ICZ.EQ.0 .AND. STARR(I).LE.RCZ(1) .AND.
         *                      STARR(I+1).GE.RCZ(1)) THEN
                                  ICZ = I
                            ENDIF
    ...
    ```

    (A call with no bracket would still need a decision, such as `TCZ` = 0.)

4. **(b)** **`FXIONJ` is a scalar.** ([[#L82]]; [[#L292]]; [[eqstat2.f#L54]]; [[eqstat2.f#L171-L173]]) CALCAD passes the scalar `FXIONJ` where EQSTAT2 declares `FXION(3)` and writes three elements, so EQSTAT2 writes past it, into whatever CALCAD stores next. On the non-OPAL path (`LOPALE06` off, its default). Not reachable today (`LACOUT` is set nowhere, above). Read from the code, not run. **A possible fix:**

    ```fortran
    C 11/09/26 KC via Claude
    C code changed to declare FXIONJ with the three elements EQSTAT2
    C fills.
          REAL*8 FXIONJ(3)
    ```

    (with `FXIONJ` dropped from the `REAL*8` list at [[#L82]]).

5. **(c)** **EOS errors ignored.** ([[#L269-L273]]) ESAC06's alternate return `*999` jumps to the next statement, so a failed EOS call uses the `EOS` values of the previous point; ESAC06 writes a message to `ISHORT`, but CALCAD goes on. Only with `LOPALE06`, for points outside the OPAL table. Not reachable today (`LACOUT` is set nowhere, above). Read from the code, not run. **A possible fix:** a choice for the developers: fall back to EQSTAT2 for that point, as the EOS does elsewhere outside the table, or stop.

6. **(c)** **Output format.** ([[#L445-L446]]) Format 67 has no space before "Acoustic depth of atmopshere" (also misspelled), so the line runs the two together. Not reachable today (`LACOUT` is set nowhere, above). Read from the code, not run. **A possible fix:**

    ```fortran
    C 11/09/26 KC via Claude
    C code changed to separate and correct the last label of format 67.
    67       FORMAT(1X,'Acoustic depth to CZ:',F14.8,2X,'Acoustic depth to center',
         *F13.7,2X,'Normalized taucz:',F11.9,2X,'Acoustic depth of atmosphere:',
         *F16.8,2X)
    ```

7. **(d)** **A short profile.** ([[#L317-L322]]; [[#L441]]; [[boole.f#L56-L63]]) If `K ≤ 3`, `NN = 2` and BOOLE returns 0, so `TAUCZN` divides by zero. A profile that short does not occur in a real model. Not reachable today (`LACOUT` is set nowhere, above). Read from the code, not run. **A possible fix:**

    ```fortran
    C 11/09/26 KC via Claude
    C code changed to leave TAUCZN at zero when TNORM is zero.
          TAUCZN=0.0D0
          IF (TNORM.GT.0.0D0) TAUCZN=TCZ/TNORM
    ```

### CALCAD

Integrates the envelope, joins it to the interior, computes $1/c_s$ from the EOS and integrates it with [[boole.f#BOOLE|BOOLE]] to get the acoustic depth of the star and of its convection zone (`TNORM`, `TCZ`, `TAUCZN` in `/ACDPTH/`).
