## Explanation

**Purpose.** The entry point of the neutrino-loss routines added by Grant Newsham (9/06). It sets up a four-species composition (hydrogen, helium, ¹²C, ¹⁶O) and returns the neutrino energy-loss rate `SNU` with its derivatives with respect to temperature and density, `DSNUDT` and `DSNUDD`.

**How it fits.**
- **Inputs:** $T$ (K) and $\rho$ (g cm⁻³), unlogged; $X$, $Y$; `ZC` and `ZO`, which [[engeb.f#ENGEB|ENGEB]] sets to ¹²C + ¹³C and ¹⁶O + ¹⁸O.
- **Who calls it:** only [[engeb.f#ENGEB|ENGEB]], when `LNULOS1` is set and $\log T$ is above the cutoff `TCUT(5)`. ENGEB uses $-$`SNU` as the loss and turns the derivatives into logarithmic ones.
- **What it calls:** [[nulosses.f#NULOSSES|NULOSSES]].
- **Outputs:** `SNU`, `DSNUDT`, `DSNUDD`. The units are those of [[sneut.f#SNEUT|SNEUT]] (probably erg g⁻¹ s⁻¹, as in the Timmes codes it comes from; not stated here).
- **Modules:** none.

**The method.** Nuclei with $(A, Z)$ = (1, 1), (4, 2), (12, 6), (16, 8), mass fractions $(X, Y, X_\mathrm{C}, X_\mathrm{O})$; everything else is done in `NULOSSES`.

The rest of $Z$ is left out ([[#b1]]).

**Changed since `rp_1`.** Declarations only: `IMPLICIT NONE`.

## Bugs, by priority

1. **(changes results, small)** **Checked by KC** (Nov 10, 2026). **Metals other than C and O are left out.** ([[#L52-L58]]; [[nulosses.f#L87-L95]]) Nitrogen, neon, iron, and the rest of $Z$ are not passed (`ZC` and `ZO` are ¹²C + ¹³C and ¹⁶O + ¹⁸O, [[engeb.f#L1231-L1232]]), so the four mass fractions sum to less than one, and [[nulosses.f#AZBAR|AZBAR]] does not renormalize them: $\bar A = 1/\sum_i X_i/A_i$ is too large by the factor $1/\sum_i X_i$ against the four fractions renormalized, while $\bar Z = \sum_i Z_i X_i/A_i \big/ \sum_i X_i/A_i$ does not depend on the sum, so $Y_e = \bar Z/\bar A$ is too small by the factor $\sum_i X_i$ against them; against the real mixture, $Y_e$ misses the omitted metals' electrons, about $(1 - \sum_i X_i)/2$. What follows: The neutrino losses, which [[sneut.f#SNEUT|SNEUT]] computes from $\bar A$, $\bar Z$, and $Y_e$, are those of a mixture with too few electrons. Only with `LNULOS1` (off by default; set in many of YREC's cases) and above $\log T$ = `TCUT(5)` (7.5 in YREC's cases).

    **A possible fix,** two ways. (a), the one the run below used, puts the metals other than carbon and oxygen in the oxygen slot, so that the mass fractions sum to one, as AZBAR assumes. It treats every nucleus other than hydrogen as having $Z/A = 1/2$, as YREC's older loss routines do (`EMUE = 0.5*(1.0+X)`, [[engeb.f#L1273]]), and gives the missing metals $A = 16$, which the code does not specify anywhere:

    ```diff
    --- a/src/neutrino.f
    +++ b/src/neutrino.f
    @@ -52,7 +52,10 @@
              xmass(1) = x
              xmass(2) = y
              xmass(3) = zc
    -         xmass(4) = zo
    +C 11/10/26 KC via Claude
    +C code changed to put the metals other than C and O in the oxygen slot,
    +C so that the mass fractions sum to one, as AZBAR assumes.
    +         xmass(4) = 1.0d0 - x - y - zc
     
     
            call nulosses(temp,den,snu,xmass,ymass,aion,zion,dsnudt,dsnudd)
    ```

    Or (b), not run: AZBAR divides by the sum of the mass fractions it is given, so that `abar` and `zbar` are the means over the four species even when they do not sum to one. This is the same as renormalizing the four fractions: It needs no assumption about the missing metals, but gives them the four species' mean $Z/A$, hydrogen's included:

    ```diff
    --- a/src/nulosses.f
    +++ b/src/nulosses.f
    @@ -82,16 +82,21 @@
           integer          i,ionmax
           double precision xmass(ionmax),aion(ionmax),zion(ionmax),
    -     1                 ymass(ionmax),abar,zbar,zbarxx,ytot1
    +     1                 ymass(ionmax),abar,zbar,zbarxx,ytot1,xtot
     
     
           zbarxx  = 0.0d0
           ytot1   = 0.0d0
    +      xtot    = 0.0d0
           do i=1,ionmax
            ymass(i) = xmass(i)/aion(i)
            ytot1    = ytot1 + ymass(i)
            zbarxx   = zbarxx + zion(i) * ymass(i)
    +       xtot     = xtot + xmass(i)
           enddo
    -      abar   = 1.0d0/ytot1
    -      zbar   = zbarxx * abar
    +C 11/10/26 KC via Claude
    +C code changed to divide by the sum of the mass fractions given, so that
    +C abar and zbar are the means over those species even if it is not one.
    +      abar   = xtot/ytot1
    +      zbar   = zbarxx/ytot1
           return
           end
    ```

    **How the code itself shows it.** AZBAR forms `ytot1` as the sum of `xmass(i)/aion(i)` and sets `abar = 1.0d0/ytot1` and `zbar = zbarxx * abar` ([[nulosses.f#L87-L95]]), so `abar` is the mean nucleon number only when the `xmass` sum to one (the mean charge `zbarxx/ytot1` is a ratio and does not depend on it), and SNEUT takes `ye = zbar*abari` ([[sneut.f#L192]]), which therefore does. NEUTRINO passes `x`, `y`, `zc`, and `zo` alone ([[#L52-L55]]), and ENGEB sets `ZC = XC12+XC13` and `ZO = XO16+XO18` ([[engeb.f#L1231-L1232]]), so ¹⁴N and the metals heavier than oxygen are missing.

    **Checked by running YREC** (Nov 10, 2026, the runs repeated the same day with a private start model; a line added at each suspected path counted how often it was taken, the outputs otherwise unchanged): In `testsuite/Test_m1p0feh+0p0GS98_base_HeIgnite` (1 $M_\odot$ from the end of the main sequence, at 9.870 Gyr, up the red giant branch; the run stops near helium ignition, at 12.59 Gyr, when the center's $\log T$ leaves the OPAL 95 table, with `STOP 1`), NEUTRINO was called 33,460,185 times, at $\log T$ = 7.50 to 8.07, and the four fractions summed to 0.984 to 0.991 every time. With fix (a), the neutrino luminosity changes beyond the noise: To 12.5 Gyr it moves by up to 0.000072 $L_\odot$, against 0.0000011 for a null change (nearly every opacity, all with $3 \le \log T \le 9$ and $-6 \le \log\rho \le 9.75$, times $1 + 10^{-10}$, on the same case), and in the last model it is 0.876 $L_\odot$ instead of 0.845, against 0.846 for the null change. The star's luminosity stays within the noise, and its center moves a little beyond it: To 12.5 Gyr $\log L$ moves by up to 0.00016 dex, against 0.00084 for the null change, and central $\log T$ by 0.00020, against 0.000030; the track has 8,611 models instead of 8,571 (8,571 for the null change, too). In `testsuite/Test_solarGS98_difrotmixper18p4d1p0`, which also sets `LNULOS1`, NEUTRINO was never called: The Sun's center stays below $\log T$ = 7.5. Intent: The header says it "currently sets up just hydrogen, helium, carbon and oxygen" ([[#L4-L5]]).
