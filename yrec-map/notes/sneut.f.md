## Explanation

**Purpose.** The thermal neutrino energy-loss rate of stellar matter, from the analytic fits of Itoh et al. (1996, ApJS 102, 411), with its derivatives with respect to temperature, density, mean atomic weight and mean charge. Five processes are summed: pair annihilation, plasmon decay, the photoneutrino process, bremsstrahlung and recombination. The routine is written in a different style from the rest of YREC (lower case, `implicit none`, `c..` comments); it is probably an import of a widely used public routine, our inference.

**How it fits.**
- **Who calls it:** [[nulosses.f#NULOSSES|`NULOSSES`]], which first computes $\bar A$ and $\bar Z$ from the mass fractions (`AZBAR`); `NULOSSES` is called by [[neutrino.f#NEUTRINO|`NEUTRINO`]], which [[engeb.f#ENGEB|ENGEB]] calls only when `LNULOS1` is set ([[engeb.f#L1240-L1244]]). `LNULOS1` is off by default ([[nmlpar_mod.f#L246]]; a legacy option in the documentation, "Use Itoh et al. (1996) neutrino loss rates"), but 710 of the 965 namelists in the repository that set it turn it on, with the comment "recommended to be set to TRUE" (settled from the code, Nov 9, 2026).
- **What it calls:** [[ifermi12.f#IFERMI12|`IFERMI12`]] (the inverse Fermi–Dirac integral of order 1/2, to get the electron chemical potential) and [[zfermim12.f#ZFERMIM12|`ZFERMIM12`]] (the integral of order −1/2, for its derivative), in the recombination part.
- **Inputs:** `temp` ($T$, K), `den` ($\rho$, g cm$^{-3}$), `abar` ($\bar A$), `zbar` ($\bar Z$).
- **Outputs:** `snu`, the total loss in erg g$^{-1}$ s$^{-1}$, and its derivatives `dsnudt`, `dsnudd`, `dsnuda`, `dsnudz`. No COMMON blocks.

**The method.** Below $T = 10^7$ K everything is zero. Otherwise, with $Y_e = \bar Z/\bar A$, $T_9 = T/10^9$ K, $\lambda = T_9/5.9302$ (that is, $kT/m_ec^2$, `xl`) and $\xi = (\rho Y_e/10^9)^{1/3}/\lambda$ (`zeta`), each process follows the equations of Itoh et al. that the comments cite:
- **Pair** (eqs. 2.5–2.8): $Q_\mathrm{pair} = \tfrac12\bigl[C_+ + C_-\,q_\mathrm{pair}\bigr]\,g(\lambda)\,e^{-2/\lambda}\,f_\mathrm{pair}$, where, with $n$ = `xnufam` neutrino flavors,
  $$C_\pm = C_V^2 \pm C_A^2 + (n-1)\bigl(C_V'^2 \pm C_A'^2\bigr),\qquad C_V = \tfrac12 + 2\sin^2\theta_W,\ C_A = \tfrac12,\ C_V' = 1 - C_V,\ C_A' = 1 - C_A,$$
  ($C_+$ is `tfac1`, $C_-$ is `tfac2`, `tfac3` $= C_-/C_+$, `tfac4` $= C_+/2$, `tfac5` $= C_-/2$), $g(\lambda)$ a polynomial in $\lambda^2$ and $f_\mathrm{pair}$ a rational function of $\xi$ and $\lambda$.

    > **Question** ([[#L109]]; [[#L117]]). **Number of flavors.** The comment gives "xnufam … = 3.02 plus/minus 0.005 (1998)", the code uses 3.0. Which value is meant, and should the comment say so?

- **Plasma** (eqs. 4.1–4.11): transverse and longitudinal plasmon terms with a correction factor $f_{xy}$.
- **Photoneutrino** (eqs. 3.2–3.8): a Fourier-type fit in $\tau = \log_{10}(T/10^7)$, with coefficient sets for $10^7$–$10^8$, $10^8$–$10^9$ and above $10^9$ K; negative results are set to zero.
- **Bremsstrahlung** (eqs. 5.1–5.26): the weakly degenerate form when $T > 0.01\,T_F$, with $T_F = 5.9302\times10^9\bigl(\sqrt{1 + 1.018(\rho Y_e/10^6)^{2/3}} - 1\bigr)$ K; otherwise the liquid-metal form "with C12 parameters (not too different for other elements)".
- **Recombination** (eqs. 6.5–6.14): with the chemical potential $\nu$ from $\mathcal F_{1/2}^{-1}$, only for $-20 \le \nu \le 10$.

    > **Question** ([[#L1212-L1232]]; [[#L1237]]). **Recombination limited to $-20 \le \nu \le 10$.** Outside this range the recombination loss is zero. Is that a property of Itoh's fit, or a cut that could matter in degenerate cores?

The sum is converted from erg cm$^{-3}$ s$^{-1}$ to erg g$^{-1}$ s$^{-1}$ by dividing by $\rho$ ("comment these out to duplicate the Itoh et al. plots"), and every derivative is carried along by the chain rule.

**Changed since `rp_1`.** Three single-precision constants in the recombination part became double precision: the table-12 coefficients `c` (`9.06e-1` and `8.97e-1` to `9.06D-1` and `8.97D-1`) and the exponent and factor 4.55 in `dd01 = dum**(-4.55D0)` and `c01`; this changes the recombination rate by a few parts in $10^8$. The `tfac2` typo (bug 1) is unchanged.

## Bugs, by priority

1. **(a)** **A typo in `tfac2`.** ([[#L124-L125]]) The parameter is `tfac2 = cv*cv - ca*ca + (xnufam-1.0d0) * (cvp*cvp - cap-cap)`. By the pattern of `tfac1` and the definition of $C_-$, the last term should be `cvp*cvp - cap*cap`. As written it is $C_V'^2 - 2C_A' = C_V'^2 - 1$, so $C_-$ = −1.318 instead of 0.182, and `tfac3` $= C_-/C_+$ = −0.784 instead of 0.108. `tfac3` enters the pair rate as $1 + $ `tfac3`$\,q_\mathrm{pair}$ ([[#L356-L357]]) and the photoneutrino rate as $1 - $ `tfac3`$\,q_\mathrm{phot}$ ([[#L834-L835]]), and `tfac5` enters both bremsstrahlung forms ([[#L1015]], [[#L1171]]). Taken whenever `LNULOS1` is on (off by default, on in most of the repository's namelists) and $\log T$ is above `TCUT(5)`. Read from the code, not run; the effect on the total loss was not computed. **A possible fix:**

    ```fortran
    c 11/09/26 KC via Claude
    c code changed to square cap in tfac2, as in tfac1 and C- of Itoh et al.
         8                  tfac2  = cv*cv - ca*ca +
         9                           (xnufam-1.0d0) * (cvp*cvp - cap*cap),
    ```

