## Explanation

**Purpose.** Sets up the equally spaced grid for mixing one unstable region (in the coordinate $\chi$ of [[getgrid.f#GETGRID|GETGRID]]) and puts the mass of each grid zone and the diffusion coefficient on it, for [[mixcom.f#MIXCOM|MIXCOM]].

**How it fits.**
- **Inputs:** the mixing coefficients `COD2` at the model interfaces (from [[codiff.f#CODIFF|CODIFF]]); the model (`HD`, `HL`, `HP`, `HR`, `HS`, `HS1`, `HS2`, `HSTOT`); the region `IBEG..IEND`; `LCZ`; the energy generation `EPSM` at the intermediate time (`MDPHY_MOD`, from [[midmod.f#MIDMOD|MIDMOD]]); and the weights `HPTTOL` of the rezoning, a namelist variable in `NMLPAR_MOD`.
- **Who calls it:** only [[ndifcom.f#NDIFCOM|NDIFCOM]].
- **What it calls:** [[getgrid.f#GETGRID|GETGRID]] (the grid, in `EGRID_MOD`) and [[osplin.f#OSPLIN|OSPLIN]].
- **Outputs:** the zone masses `EM`, the coefficients `ECOD2`, and `LDUM2` (true if the region spans only one unstable interface, in which case nothing else is done).
- **Modules:** `EGRID_MOD`, `SPLIN_MOD`, `MDPHY_MOD`, `NMLPAR_MOD` (`HPTTOL`), `CONSTANTS_MOD` (`CLSUN`, `CLN`, `C4PI`, `CGL`) and `DIMENSIONS_MOD`. [[rotgrid.f#ROTGRID|ROTGRID]] does the same for angular momentum.

**The method.**
1. **The coordinate.** GETGRID defines, at each model point, $\chi = \log m/\Delta_m + L/\Delta_L - \log P/\Delta_P$, with $\Delta_m$, $\Delta_L$, $\Delta_P$ from `HPTTOL`, and an equal grid in $\chi$ (`ECHI`, step `DCHI`).
2. **Zone masses.** Interior zones: $\Delta M_i = \tfrac12 (m_{i+1} - m_{i-1})$ (`ES1` are the grid points' masses). The first and last zones reach to the midpoint with the neighbouring model point (or to the centre, or the surface), and add any adjoining convection zone's mass. The loops that do so also set `I0 = I + 1` and `I1 = I - 1` ([[#L89]], [[#L110]]), with `I` left over from the loop of the interior zones rather than the loop variable `II`; `I0` and `I1` are read nowhere (unused?).
3. **The coefficient.** `COD2` is interpolated to the zone edges (taken as constant beyond the end interfaces). It is multiplied by $\rho r^2\, d\chi/dr$, where, as the comment derives with $\mathrm{FAC} = 4\pi\rho r^2$,
$$\frac{d\chi}{dr} = \frac{4\pi\rho r^2}{\ln 10\,\Delta_m\, m} + \frac{4\pi\rho r^2\,\epsilon}{\Delta_L} + \frac{G m \rho}{\ln 10\,\Delta_P\, P\, r^2},$$
interpolated in $\log$ to the grid with `OSPLIN`. Here $\Delta_m$ = `HPTTOL(2)`, $\Delta_L$ = `HPTTOL(9)`$\times L_\ast$ (`HL(M)*CLSUN`, in erg s⁻¹; GETGRID uses the same scale, `HPTTOL(9)*HL(M)`, in the solar units of `HL`), $\Delta_P$ = `HPTTOL(11)`, and $\epsilon$ = `EPSM`. The coefficient `ECOD2(I)` lies at the edge between grid points `I-1` and `I` (`XVAL(I) = ECHI(I) - DCHI/2`), where [[ccoeft.f#CCOEFT|CCOEFT]] uses it.

    **The comment's last term omits $P$.** The comment writes it as `RHO*GM/(LN10*DP*R**2)` ([[#L153]]); the code divides by $P$ as well, with `-HP(II)` in the exponent ([[#L156-L157]]), which is the correct $-d\log P/dr$, so the comment should read `RHO*GM/(LN10*DP*P*R**2)`.

**Changed since `rp_1`.** Declarations only: COMMON blocks to modules, `IMPLICIT NONE`.
