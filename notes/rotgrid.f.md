## Explanation

**Purpose.** For the transport of angular momentum and the mixing it drives, maps one radiative region (shells `IBEG` to `IEND`) onto an auxiliary grid of points equally spaced in a mesh coordinate $\chi$, and computes there what the diffusion solver needs: each zone's mass, moment of inertia, angular momentum and angular velocity at the zone centers, and the diffusion coefficients, multiplied by the Jacobian of the change of variables, at the zone edges.

**How it fits.**
- **Who calls it:** [[seculr.f#SECULR|`SECULR`]] (the secular transport of angular momentum and composition), for each region it treats.
- **What it calls:** [[getgrid.f#GETGRID|`GETGRID`]], which defines the coordinate $\chi$ (`CHI` at the model's shells, `ECHI` at the new points, spacing `DCHI`, `NTOT` points, and their masses `ES1`; all in `/EGRID/`), and [[osplin.f#OSPLIN|`OSPLIN`]] for every interpolation, through the work arrays of `/SPLIN/`.
- **Inputs (arguments):** the model's log density `HD`, log radius `HR` and radius `HRU`, log pressure `HP`, luminosity `HL`, log mass `HS`, masses `HS1` (enclosed) and `HS2` (of each shell), moments of inertia `HI`, specific angular momenta `HJMSAV`, angular velocities `WSAV`, the convection flags `LCZ`, and the diffusion coefficients `COD` (angular momentum) and `COD2` (composition). Also, from COMMON: the mesh tolerances `HPTTOL` (`/CTOL/`), the energy generation `EPSM` (`/MDPHY/`), and, with `LDIFAD` (`/VARFC/`), the advective and diffusive velocities `VESA`, `VESD` (`/DIFAD2/`) and the factor `FW` (`/VMULT/`).
- **Outputs:** on the new grid, `EM` (zone masses), `EI` (moments of inertia), `EJ` (angular momenta), `EW` (angular velocities), `ECOD`, `ECOD2` (the two diffusion coefficients with their factors), and with `LDIFAD` `ECOD3`, `ECOD4` in `/DIFAD/`; `DR` is set to `DCHI`. `SECULR` solves the diffusion on this grid and maps the result back. `LDUM2` returns true, and nothing else is done, when the region has only one interface (`IEND - IBEG <= 1`).

**The method.**
1. **Zone centers.** $\log r$, $I/(m r^2)$ (`EI0`), $j = J/m$ and $\Omega$ are interpolated from the shells onto the new points. Then, for the interior zones,
   $$\Delta m_k = \tfrac12\,(m_{k+1} - m_{k-1}),\qquad I_k = \frac{I}{m r^2}\Big|_k\,\Delta m_k\,r_k^2,\qquad J_k = j_k\,\Delta m_k .$$
2. **The two end zones** run from the half-way point to the next equally spaced point out to the half-way point to the next original shell (or the center, or the surface, where the mass is $10^{\texttt{HSTOT}}$). If the region borders a convection zone, all of that zone's shells are added to the end zone, so a convection zone moves as one block.
3. **Zone edges.** The diffusion coefficients are interpolated at $\chi_k - \tfrac12\Delta\chi$, assumed constant beyond the region's ends. With `LDIFAD`, the advective and diffusive terms $0.2\cdot4\pi f_W\,v$ are interpolated too, and the composition coefficient is added to the diffusive one (following Zahn 1992, as the comment says).
4. **The Jacobian.** The mesh coordinate is defined by the comment as
   $$\chi = \frac{\log m}{\delta_m} + \frac{L}{\delta_L} - \frac{\log P}{\delta_P},$$
   with $\delta_m$ = `HPTTOL(2)`, $\delta_L$ = `HPTTOL(9)` times the surface luminosity, $\delta_P$ = `HPTTOL(11)`, so that
   $$\frac{d\chi}{dr} = \frac{4\pi\rho r^2}{\ln 10\;\delta_m\,m} + \frac{4\pi\rho r^2\,\varepsilon}{\delta_L} + \frac{G m \rho}{\ln 10\;\delta_P\,P\,r^2}.$$
   The composition coefficient is multiplied by $\rho r^2\,d\chi/dr$, and the angular-momentum coefficients by $\rho r^2\,(I/m)\,d\chi/dr$ (for a thin spherical shell, $I/m = \tfrac23 r^2$, the comment notes), each interpolated in $\log_{10}$.

## Questions for the experts

1. **Stale loop variable at the region's ends.** In the loops that add a neighboring convection zone, `I0 = I + 1` and `I1 = I - 1` use `I`, which is left over from an earlier loop (the zone-center loop), not the loop variable `II`. `I0` and `I1` are not used afterwards, so there is no effect today, but they look like a remnant of an index meant to be `II`. Remove them?
2. **The comment's $d\chi/dr$ omits $P$.** The comment writes the third term as `RHO*GM/(LN10*DP*R**2)`; the code computes $G m\rho/(P r^2)$ (with `-HP(II)` in the exponent), which is the correct $d\log P/dr$ term. The comment should include $1/P$.
3. **Hard-coded 0.2.** In the advection–diffusion option, `FAC = 0.2D0*C4PI*FW`. Where does the 1/5 come from (probably the $\frac15$ of Zahn's 1992 transport equation)? A comment would help.
4. **End zones use `HRU` but interior zones use interpolated $\log r$.** `EI(1)` and `EI(NTOT)` take $r^2$ at the original shells `IBEG` and `IEND`, while the interior zones use $r$ interpolated at their centers. Intended?
