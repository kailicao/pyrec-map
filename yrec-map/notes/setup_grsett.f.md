## Explanation

**Purpose.** Prepares the gravitational settling (microscopic diffusion) of helium, and optionally of metals, for the older settling solver: it finds the range of shells where settling is computed, converts the model to the units of Bahcall and Loeb, and computes the diffusion coefficients and their derivatives with respect to $X$.

**How it fits.**
- **Who calls it:** [[grsett.f#GRSETT|`GRSETT`]], the Bahcall–Loeb settling solver (used when `LNEWDIF` is false; see [[rotmix.f#ROTMIX|`ROTMIX`]] and [[mix.f#MIX|`MIX`]]). The newer path is [[microdiff_setup.f#MICRODIFF_SETUP|`MICRODIFF_SETUP`]].
- **Inputs:** the step `DT` (s), $d\ln P/dr$ (`HQPR`), $\log r$, $\log\rho$, $\log T$ (`HR`, `HD`, `HT`), the enclosed masses `HS1` (g), the total mass `STOT`, the convection flags `LC` and `HCOMP`; from modules, `SDEL(2,·)` (`SCRTCH_MOD`, which `ROTMIX` loads with the gradient `DELM`) and the namelist parameters in `NMLPAR_MOD`: `ILAMBDA`, `XMIN`, `YMIN`, `LTHOULFIT`, `FGRY`, `FGRZ`, `LTHOUL`, `LDIFZ`, `CSTMIXING` and `CSTDIFFMIX`.
- **What it calls:** [[thdiff.f#THDIFF|`THDIFF`]], the full diffusion coefficients of Thoul et al., when `LTHOUL` is true and `LTHOULFIT` false.
- **Outputs:** `IBEGIN`, `IEND` (the range), `LALLCZ` (true when settling is skipped), `HRU`, `HTU` (radius and temperature in Bahcall–Loeb units), `HQPR`, `HS1`, `DT`, `STOT` converted in place, and the coefficients `COD1`, `COD2`, `QCOD1X`, `QCOD2X`; for metals, `COD1Z`, `COD2Z`, `QCOD1Z`, `QCOD2Z`, arguments whose storage `GRSETT` owns and passes on to [[model_to_equal.f#MODEL_TO_EQUAL|`MODEL_TO_EQUAL`]]. The conversion factors go to `CONFAC_MOD` (`CON_RAD`, `CON_MASS`, `CON_TEMP`, `CON_TIME`), shared with [[equal_to_model.f#EQUAL_TO_MODEL|`EQUAL_TO_MODEL`]] and the `MICRODIFF` routines.

**The method.**
1. **Range.** `IBEGIN` is the first shell above a convective core with $X >$ `XMIN`; `IEND` is the last shell below a convective envelope. The helium check only tests that some shell at or below `IEND` has $Y >$ `YMIN`; it does not move `IEND` (question 7). A fully convective model, or one with no shell above either limit, is skipped (`LALLCZ`), with a message. The coefficients below are computed for every shell, 1 to `M`, not only within the range.
2. **Units** (Bahcall and Loeb): $r$ in $R_\odot$ (6.9598×10$^{10}$ cm), $T$ in $10^7$ K, masses multiplied by `CON_MASS` $=10^{-2}/R_\odot^3$ ($R_\odot$ in cm), time in $2.7\times10^{13}$ yr ("includes factor of 2.2 from ln lambda").
3. **Coulomb logarithm** $\ln\Lambda$, by `ILAMBDA`: 2.2 (default); Noerdlinger (1977), $\ln\Lambda = -19.7 - \tfrac12\ln\frac{4}{3X+1} - \tfrac12\ln\rho + \tfrac32\ln T$; Loeb (1989), $\ln\Lambda = -19.105747 - \tfrac12\ln\rho + \tfrac32\ln T$; or (4) a separate value for each pair of species from the Debye length or interionic distance, $\ln\Lambda_{ij} = 0.81245\,\ln\bigl(1 + 0.18769\,x_{ij}^{1.2}\bigr)$. Option 4 reaches only `THDIFF` (helium with `LTHOUL` true and `LTHOULFIT` false); `FAC` below, and the metals' factor, then use the default 2.2.
4. **Helium coefficients.** The equation, in the comment's words, is
   $$\frac{\partial X}{\partial t} = \frac{1}{\rho r^2}\frac{\partial}{\partial r}\Bigl(D_1 + D_2\frac{\partial X}{\partial r}\Bigr),$$
   with $F = f_Y\,r^2 T^{5/2}/\ln\Lambda$ (`FAC`, $f_Y$ = `FGRY`). Without `LTHOUL` (Bahcall and Loeb):
   $$D_1 = F\,\frac{d\ln P}{dr}\,X(1-X-Z)\left[\frac54 + \nabla\,\frac{6(X+0.32)}{5.4+6.3X-4.5X^2}\right],\qquad D_2 = F\,\frac{X+3}{(X+1)(5X+3)},$$
   with $\nabla$ = `SDEL(2,I)` and $Z$ = `HCOMP(3)` + `HCOMP(4)`. With `LTHOUL` (Thoul et al.): $D_1 = c\,F\,\frac{d\ln P}{dr}\,X\,(A_P + A_T)$ and $D_2 = c\,F\,A_C$, where $A_P$, $A_T$ come from `THDIFF` or from the quadratic fits in $X$ (`LTHOULFIT`), $A_C = 1.15 - 1.42X + 0.647X^2$, and $c$ = `CSTMIXING` ("FD 10/09, mimic mixing to reduce settling"). `QCOD1X`, `QCOD2X` are the derivatives with respect to $X$; with `ILAMBDA = 2`, `QCOD1X` gets an extra term from the $X$-dependence of $\ln\Lambda$.
5. **Metals** (with `LDIFZ` and `LTHOUL`): the same form with Thoul's coefficients for fully ionized iron, $f_Z$ = `FGRZ`, and the factor `CSTDIFFMIX` on $D_1$.

**Changed since `rp_1`.** The metals' coefficients `COD1Z`, `COD2Z`, `QCOD1Z`, `QCOD2Z` are arguments (formerly `/GRAVSZ/`); the unused `/GSCOF/` is dropped; otherwise declarations only: COMMON blocks to modules, `IMPLICIT NONE`.

## Questions for the experts

1. **$+0.32$ or $-0.32$?** The comment writes the thermal term as `DEL*6*(X-0.32)/(5.4+6.3X-4.5X**2)`; the code uses `(X+0.32D0)`. Which is Bahcall and Loeb's?
2. **$\ln\Lambda$ counted twice?** `CON_TIME` "includes factor of 2.2 from ln lambda", and `FAC` also divides by $\ln\Lambda$, which is 2.2 by default. Does the time unit already absorb the 2.2, so that dividing again gives a factor $1/2.2$ too many? Or is the comment about the unit's history only?
3. **Derivatives without the mixing factors.** `COD1`, `COD2` are multiplied by `CSTMIXING` (and `COD1Z` by `CSTDIFFMIX` too), but `QCOD1X`, `QCOD2X` are not, and `QCOD1Z` lacks `CSTDIFFMIX`. When these factors differ from 1, the derivatives no longer match the coefficients. Should they be scaled the same way?
4. **Derivatives from the fits, coefficients from `THDIFF`.** With `LTHOUL` and not `LTHOULFIT`, $A_P$ and $A_T$ come from `THDIFF`, but their $X$-derivatives (`QAPX`, `QATX`) and $A_C$ always come from the quadratic fits. Intended as an approximation?
5. **Metal coefficients only with `LTHOUL`.** With `LDIFZ` true and `LTHOUL` false, `COD1Z` and the others are not set and keep earlier values. Should this combination be refused?
6. **Comment.** The comment before the helium check's exit says "HYDROGEN-FREE MODEL"; the test is on helium (`YMIN`), and the printed message says so.
7. **`IEND` not reset.** After label 47, the shell found with $Y >$ `YMIN` is not stored: unlike the hydrogen check (`IBEGIN = I`), there is no `IEND = I`. Is that line missing, so that a helium-poor surface is never excluded?
