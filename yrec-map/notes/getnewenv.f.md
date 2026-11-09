## Explanation

**Purpose.** `GETNEWENV` moves the outer fitting point of the interior model outward, by turning part of the envelope into new interior points, so that the envelope again holds the fraction of the mass it held before the step's mass change ($\log(m_\mathrm{fit}/M)$ = `SENVOLD`). Its header (MHP 07/02): "move the outer fitting point when the total mass is being decreased; add new points by dropping a sinkline from the surface down and including new points up to the desired envelope mass". It integrates the envelope once from the surface, then copies the points between the old and the new fitting point into the model.

**When it runs.** The main program calls it when [[massloss.f#MASSLOSS|MASSLOSS]] has set `LNEWFIT`, which it does whenever its rate `DMDT` is positive (massloss.f line 131), whichever rate applies: the constant `DMDT0` or the Reimers rate `CREIM`$\,L/(gR)$. [[mdot.f#MDOT|MDOT]] adds `DELM` = `DMDT`$\cdot\Delta t$ to the total mass, so a positive `DMDT` raises $M$ while the interior points keep their masses, and the envelope above the last point grows; main.f's comment reads "restore prior fitting point if mass accretion is being included". The defaults of both rates are negative (`DMDT0` = $-10^{-14}$, `CREIM` = $-4\times10^{-13}$, parmin.f), so with them the routine is not called; the header's "mass is being decreased" disagrees with this trigger.

> **Question** ([[#L2-L5]]; [[massloss.f#L131]]). **Header and trigger.** The header says the routine is for a decreasing total mass, but it runs only when `DMDT` > 0, which MDOT applies as a mass gain (`SMASS = SMASS + DELM/CMSUN`, [[mdot.f#L262]]); main.f's comment says accretion. With mass loss (`DMDT` < 0) MDOT instead compresses the convective-envelope shells and no points are added. Is the header out of date, or was the routine meant for mass loss too?

**How it fits.**
- **Who calls it:** only the main program ([[main.f#(file level)|main.f]]), when `LNEWFIT` is set (above); it then calls [[fpft.f#FPFT|FPFT]] with its own `OMEGA`.
- **Inputs:** `SENVOLD` (the desired fitting point, below); the model arrays (`HCOMP`, `HD`, `HL`, `HP`, `HR`, `HS`, `HT`, `LC`, `M`), the surface `BL` ($\log L/L_\odot$) and `TEFFL`, the rotation arrays, and `CMIXL`, the mixing-length parameter, passed on to `ENVINT`.
- **What it calls:** [[envint.f#ENVINT|ENVINT]] (the envelope integration) and, for rotating models, [[getrot.f#GETROT|GETROT]].
- **Outputs:** the model with `M` increased and the new points filled; `HS1`, `HS2` (unlogged masses and shell masses) for the new points; for rotating models, `HJM`, `HI`, `ETA2`, `QIW`, `R0`, `HKEROT` (not `OMEGA`, which is local: suspected bug 1) and the totals `SJTOT`, `SKEROT`; `LNEW` = true; `SENV` in `COMP_MOD`. It prints the new points to standard output.

    > **Question** ([[#L315-L324]]). **Output to standard output.** The routine writes the new points and the old and new `SENV` to `*` rather than to the run's output units (`ISHORT`). Intended?

- **Modules:** `ENVSTRUCT_MOD` (the envelope solution `ENVP`, `ENVT`, `ENVS`, `ENVD`, `ENVR`, `ENVX`, `ENVZ`, `LCENV`, `NUMENV`, written by `ENVINT`); `NMLPAR_MOD` (the envelope step sizes `ENVMAX`, `ENVMIN`, `ENVBEG`, temporarily set to `HPTTOL(8)` and restored; the starspot parameters `SPOTF`, `SPOTX`; `LROT`, `WALPCZ`; `LEXCOM`); `COMP_MOD` (`STOTAL` = $\log M$, `SENV`); `DEBHU_MOD` (the Debye–Hückel composition, set here from the surface shell); `CONSTANTS_MOD`; `DIMENSIONS_MOD` (`JSON`).

**The method.**
1. **Surface quantities.** From $L = 4\pi R^2\sigma T_\mathrm{eff}^4$ and $g = GM/R^2$:
$$\log R = \tfrac12\left(\log\frac{L}{L_\odot} + \log L_\odot - 4\log T_\mathrm{eff} - \log 4\pi - \log\sigma\right), \qquad \log g = \log G + \log M - 2\log R.$$
With spots (fraction $f$ = `SPOTF`, temperature ratio $x$ = `SPOTX`) and a convective surface, the ambient temperature is $\log T_\mathrm{amb} = \log T_\mathrm{eff} - \tfrac14\log(f x^4 + 1 - f)$.
2. **Envelope integration** from the surface down to the current fitting point with `ENVINT`, at the spacing `HPTTOL(8)`, without rotational distortion ($f_P = f_T = 1$).
3. **Matching.** The envelope's first point is at the mass of the last interior point; the differences there in $\log P$, $\log\rho$, $\log T$, $\log r$ are added to all envelope points, which shift down by one (the convective flag `LCENV` with them), and points closer than $10^{-10}$ in $\log m$ are dropped.
4. **New points.** Each envelope point below the new fitting point becomes an interior point, with $L$ held at its value at the old fitting point and the abundances other than $X$ and $Z$ copied from it ([[#L184-L201]]). The copy matches the envelope: ENVINT integrates it with the surface $X$ and $Z$ of shell `M` at every point (`ENVX`, `ENVZ`: [[#L112-L113]], [[envint.f#L633-L634]], [[envint.f#L760-L761]]), so the whole envelope has the old fitting point's composition (settled from the code, Nov 9, 2026). The last point is interpolated linearly in $\log m$ to the new fitting point.

    > **Question** ([[#L186-L187]]). **Constant luminosity.** The new points take $L$ of the old fitting point. Fine for a thin envelope; is it still right when much mass is shed or gained at once?

5. **Shell masses.** $m = 10^{\log m}$, $\Delta m_j = \tfrac12(m_{j+1} - m_{j-1})$, and the last shell takes the rest of the star.
6. **Rotation.** The new points get, as a first guess, constant $j$ if $\alpha$ = `WALPCZ` $\le -2$, solid body if $\alpha \ge 0$, and otherwise $\Omega \propto r^{\alpha}$, the law [[wczimp.f#WCZIMP|`WCZIMP`]] imposes (PARMIN limits $\alpha$ to $[-2, 0]$); with $I = \tfrac23 r^2$ and $j = \Omega I$. `GETROT` then finds the rotation law, and the totals $J = \sum j\,\Delta m$ and $E_\mathrm{rot} = \sum\tfrac12\Omega j\,\Delta m$ are recomputed.

`SENV` is the fitting point's $\log(m/M)$, as can be read from `HS = ENVS + STOTAL`; it is limited to at most $-10^{-12}$.

**Changed since `rp_1`.** `CMIXL` is a new argument, passed on to `ENVINT` (it was in `/CONST3/`); COMMON blocks to modules (the namelist parameters from `/INTENV/`, `/CTOL/`, `/SPOTS/`, `/ROT/` and `/FLAG/` now come from `NMLPAR_MOD`; the unused `/ENVPRT/` dropped), `IMPLICIT NONE`. No question is settled.

**Changed since `a8a5950`.** The shift of the envelope points moves `LCENV` with the other arrays, so the new points' convective flags are no longer read one point off; the general rotation case follows $\Omega = C\,r^{\alpha}$, as WCZ does, rather than $\Omega\,r^{\alpha}$ constant (settles former question 7).

## Bugs, by priority

1. **(a)** **`OMEGA` is a local array.** ([[#L74-L75]]; [[#L281-L299]]; [[#L300]]) `OMEGA` is not an argument: It is declared in `DIMENSION` and is local. In step 6, the solid-body and general cases read `OMEGA(MM)`, which is never set in this routine before (it keeps whatever an earlier call left, or its initial value at the first call), so the new points' $j$ (`HJM(J) = OMEGA(MM)*HI(J)`, or through `W0`) comes from that stale value. Then `GETROT` overwrites the local `OMEGA` and the result is used only for $E_\mathrm{rot}$, while the main program goes on to call FPFT with its own `OMEGA`, which has no values for the new points ([[main.f#L1040-L1045]]). What follows: wrong specific angular momentum for the accreted shells and wrong $f_P$, $f_T$ there until the next GETROT. Only with rotation (`LROT`) and a positive mass-change rate (both off by default); with them, the default `WALPCZ` = 0 takes the solid-body case. Read from the code, not run. **A possible fix:**

    ```fortran
          SUBROUTINE GETNEWENV(SENVOLD,HCOMP,HD,HL,HP,HR,HS,HS1,HS2,
         *                     HSTOT,HT,LC,ETA2,HI,HJM,QIW,R0,
         *                     HKEROT,BL,SJTOT,SKEROT,TEFFL,M,LNEW,CMIXL,
         *                     OMEGA)
    C 11/09/26 KC via Claude
    C code changed to take OMEGA from the main program as an argument; the
    C local array was read at OMEGA(MM) before it was set, and the values
    C GETROT gives it did not reach the main program's FPFT.
    ...
    ```

    with `OMEGA` added at the end of the call in main.f (line 1043).

2. **(d)** **A sign error in the interpolation of $X$ and $Z$.** ([[#L217-L218]]) When the new fitting point lies between the last interior point and the first envelope point, `HCOMP(1,J) = HCOMP(1,M)+FX*(HCOMP(1,M)-ENVX(JM))`, and the same for $Z$. Every other interpolation is $a + f(b - a)$; this one is $a + f(a - b)$. Harmless today: `ENVX` and `ENVZ` hold the surface `X`, `Z`, which are `HCOMP(1,M)`, `HCOMP(3,M)` (step 4), so the difference is zero. It would matter once the envelope's composition varied. Read from the code, not run. **A possible fix:**

    ```fortran
    C 11/09/26 KC via Claude
    C code changed to interpolate X and Z from the last interior point
    C toward the envelope point, as for the other quantities.
                   HCOMP(1,J) = HCOMP(1,M)+FX*(ENVX(JM)-HCOMP(1,M))
                   HCOMP(3,J) = HCOMP(3,M)+FX*(ENVZ(JM)-HCOMP(3,M))
    ```

### GETNEWENV

Moves the fitting point outward after mass loss: integrates the envelope from the surface, matches it to the last interior point, adds the envelope points as new shells, and resets rotation for them (method above).
