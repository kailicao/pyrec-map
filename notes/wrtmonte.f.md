## Explanation

**Purpose.** `WRTMONTE` writes the output of one model in a Monte Carlo series of solar models: the converged model itself, and a block of summary lines for the parameters drawn for that model (`NN`).

**How it fits.**
- **Inputs:** the model (arguments) and, through COMMON blocks: the drawn parameters of model `NN` (`MONTE2`: the nuclear factors `S11`, `S33`, `S34`, `S17`, `ZX`, `FHE`, `FZDIF`, `FLUM`, `FAGE`, read in the main program from `IDYN`), the solar calibration's derivatives $\partial L/\partial X$, $\partial R/\partial X$, $\partial L/\partial\alpha$, $\partial R/\partial\alpha$ (`CALSUN`, from [[setcal.f#SETCAL|SETCAL]] and [[chkcal.f#CHKCAL|CHKCAL]]), the neutrino fluxes (`FLUXES`, from [[engeb.f#ENGEB|ENGEB]]), the central values and convection-zone base (`CENT`, from [[wrtout.f#WRTOUT|WRTOUT]]), the runs' compositions and mixing lengths (`CKIND`, `NEWXYM`), and the units (`IOMONTE`, opened by [[parmin.f#PARMIN|PARMIN]]).
- **Who calls it:** the main program, [[main.f#(file level)|main.f]], after a calibrated model.
- **What it calls:** [[wrtlst.f#WRTLST|WRTLST]], to store the model on `IMONTE2` (with `NN` as its model number).
- **Outputs:** on `IMONTE1` (unit 70), seven lines: the drawn parameters; the number of calibration iterations `ICONV` and the four derivatives; Cl and Ga capture rates and eight neutrino fluxes; $T_c/10^6$, $\rho_c$, $P_c/10^{17}$, $X_c$, $Z_c$; the number of shells, $\alpha$, the initial $Y$ and $Z$, $\log L$ and the radius `RLL`; the base of the convection zone (radius and mass), surface $Y$, $Z$, $Z/X$; and the luminosity fractions of pp I, II, III, CNO and gravity.

**KC's changes.** Removed the unused arguments `MODEL`, `GL`, `LSHELL`, `JXBEG`, `JXMID`, `JXEND` (2025-05-31).

## Questions for the experts

1. **The run index `NK-2`.** The initial $Y$ and $Z$ come from `RESCAL(·, NK-2)`, the mixing length from `CMIXLA(NK)`. Why two runs back? For `NK` < 3 the index is out of bounds.
2. **Fixed-width formats.** $P_c/10^{17}$ in `F6.3` and $\rho_c$ in `F7.2` overflow for stars far from the Sun; the routine is meant for solar models only?

### WRTMONTE

Stores a Monte Carlo solar model (through `WRTLST`) and writes its drawn parameters and summary to `IMONTE1`.
