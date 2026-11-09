## Explanation

**Purpose.** Prepares the gravitational settling (microscopic diffusion) of helium, and optionally of metals, for the older settling solver: it finds the range of shells where settling is computed, converts the model to the units of Bahcall and Loeb, and computes the diffusion coefficients and their derivatives with respect to $X$.

**How it fits.**
- **Who calls it:** [[grsett.f#GRSETT|`GRSETT`]], the Bahcall–Loeb settling solver (used when `LNEWDIF` is false; see [[rotmix.f#ROTMIX|`ROTMIX`]] and [[mix.f#MIX|`MIX`]]). The newer path is [[microdiff_setup.f#MICRODIFF_SETUP|`MICRODIFF_SETUP`]].
- **Inputs:** the step `DT` (s), $d\ln P/dr$ (`HQPR`), $\log r$, $\log\rho$, $\log T$ (`HR`, `HD`, `HT`), the enclosed masses `HS1` (g), the total mass `STOT`, the convection flags `LC` and `HCOMP`; from modules, `SDEL(2,·)` (`SCRTCH_MOD`, which `ROTMIX` loads with the gradient `DELM`) and the namelist parameters in `NMLPAR_MOD`: `ILAMBDA`, `XMIN`, `YMIN`, `LTHOULFIT`, `FGRY`, `FGRZ`, `LTHOUL`, `LDIFZ`, `CSTMIXING` and `CSTDIFFMIX`.
- **What it calls:** [[thdiff.f#THDIFF|`THDIFF`]], the full diffusion coefficients of Thoul et al., when `LTHOUL` is true and `LTHOULFIT` false.
- **Outputs:** `IBEGIN`, `IEND` (the range), `LALLCZ` (true when settling is skipped), `HRU`, `HTU` (radius and temperature in Bahcall–Loeb units), `HQPR`, `HS1`, `DT`, `STOT` converted in place, and the coefficients `COD1`, `COD2`, `QCOD1X`, `QCOD2X`; for metals, `COD1Z`, `COD2Z`, `QCOD1Z`, `QCOD2Z`, arguments whose storage `GRSETT` owns and passes on to [[model_to_equal.f#MODEL_TO_EQUAL|`MODEL_TO_EQUAL`]]. The conversion factors go to `CONFAC_MOD` (`CON_RAD`, `CON_MASS`, `CON_TEMP`, `CON_TIME`), shared with [[equal_to_model.f#EQUAL_TO_MODEL|`EQUAL_TO_MODEL`]] and the `MICRODIFF` routines.

**The method.**
1. **Range.** `IBEGIN` is the first shell above a convective core with $X >$ `XMIN`; `IEND` is the last shell below a convective envelope. The helium check then moves `IEND` down to the first shell at or below it with $Y >$ `YMIN` (settled from the code, Nov 9, 2026: `IEND = I` after label 47, [[#L149-L160]]). A fully convective model, or one with no shell above either limit, is skipped (`LALLCZ`), with a message; the comment before the helium check's exit says "HYDROGEN-FREE MODEL", but the test and the printed message are on helium ([[#L154-L156]]). The coefficients below are computed for every shell, 1 to `M`, not only within the range.
2. **Units** (Bahcall and Loeb): $r$ in $R_\odot$ (6.9598×10$^{10}$ cm), $T$ in $10^7$ K, masses multiplied by `CON_MASS` $=10^{-2}/R_\odot^3$ ($R_\odot$ in cm), time in $2.7\times10^{13}$ yr ("includes factor of 2.2 from ln lambda").

    > **Question** ([[#L168-L169]]; [[#L206]]). **$\ln\Lambda$ counted twice?** `CON_TIME` "includes factor of 2.2 from ln lambda", and `FAC` also divides by $\ln\Lambda$, which is 2.2 by default. Does the time unit already absorb the 2.2, so that dividing again gives a factor $1/2.2$ too many? Or is the comment about the unit's history only?
3. **Coulomb logarithm** $\ln\Lambda$, by `ILAMBDA`: 2.2 (default); Noerdlinger (1977), $\ln\Lambda = -19.7 - \tfrac12\ln\frac{4}{3X+1} - \tfrac12\ln\rho + \tfrac32\ln T$; Loeb (1989), $\ln\Lambda = -19.105747 - \tfrac12\ln\rho + \tfrac32\ln T$; or (4) a separate value for each pair of species from the Debye length or interionic distance, $\ln\Lambda_{ij} = 0.81245\,\ln\bigl(1 + 0.18769\,x_{ij}^{1.2}\bigr)$. Option 4 reaches only `THDIFF` (helium with `LTHOUL` true and `LTHOULFIT` false); `FAC` below, and the metals' factor, then use the default 2.2.

    > **Question** ([[#L193-L204]]; [[#L228-L267]]; [[parmin.f#L1245-L1252]]). **`ILAMBDA`.** In the code, 2 is Noerdlinger's formula, 3 Loeb's, 4 (in the Thoul solution) a value from the local density and temperature, and any other value the constant 2.2; the default is 1, the constant. The documentation recommends 4 and calls it "a constant, 2.2". Which value is recommended, and should the default follow? (`LDIFLI` sets `ILAMBDA = 4` in [[parmin.f#PARMIN|PARMIN]]; `LTHOUL`, "rarely used" in the documentation, is also forced on by `LDIFZ` and `LDIFLI` there.)
4. **Helium coefficients.** The equation, in the comment's words, is
   $$\frac{\partial X}{\partial t} = \frac{1}{\rho r^2}\frac{\partial}{\partial r}\Bigl(D_1 + D_2\frac{\partial X}{\partial r}\Bigr),$$
   with $F = f_Y\,r^2 T^{5/2}/\ln\Lambda$ (`FAC`, $f_Y$ = `FGRY`). Without `LTHOUL` (Bahcall and Loeb):
   $$D_1 = F\,\frac{d\ln P}{dr}\,X(1-X-Z)\left[\frac54 + \nabla\,\frac{6(X+0.32)}{5.4+6.3X-4.5X^2}\right],\qquad D_2 = F\,\frac{X+3}{(X+1)(5X+3)},$$
   with $\nabla$ = `SDEL(2,I)` and $Z$ = `HCOMP(3)` + `HCOMP(4)`. With `LTHOUL` (Thoul et al.): $D_1 = c\,F\,\frac{d\ln P}{dr}\,X\,(A_P + A_T)$ and $D_2 = c\,F\,A_C$, where $A_P$, $A_T$ come from `THDIFF` or from the quadratic fits in $X$ (`LTHOULFIT`), $A_C = 1.15 - 1.42X + 0.647X^2$, and $c$ = `CSTMIXING` ("FD 10/09, mimic mixing to reduce settling"). `QCOD1X`, `QCOD2X` are the derivatives with respect to $X$; with `ILAMBDA = 2`, `QCOD1X` gets an extra term from the $X$-dependence of $\ln\Lambda$. The variable `X3` ([[#L213]]) is set and never read (unused?).

    > **Question** ([[#L186-L187]]; [[#L214-L220]]). **$+0.32$ or $-0.32$?** The comment writes the thermal term as `DEL*6*(X-0.32)/(5.4+6.3X-4.5X**2)`; the code uses `(X+0.32D0)`, and its derivative `QCOD1X` (the factor `3.384D0+2.88D0*X+4.5D0*X2`) is that of the $+0.32$ form. Which is Bahcall and Loeb's?

    > **Question** ([[#L275-L285]]). **Derivatives from the fits, coefficients from `THDIFF`.** With `LTHOUL` and not `LTHOULFIT`, $A_P$ and $A_T$ come from `THDIFF`, but their $X$-derivatives (`QAPX`, `QATX`) and $A_C$ always come from the quadratic fits. Is this intended as an approximation, and how far do the fits' derivatives stray from those of `THDIFF`'s coefficients over the range of $X$ in a solar model?
5. **Metals** (with `LDIFZ` and `LTHOUL`): the same form with Thoul's coefficients for fully ionized iron, $f_Z$ = `FGRZ`, and the factor `CSTDIFFMIX` on $D_1$. `LDIFZ` always comes with `LTHOUL`, since [[parmin.f#PARMIN|PARMIN]] sets `LTHOUL` (and `LDIFY`) whenever `LDIFZ` is on, so the metals' coefficients are always set when they are used (settled from the code, Nov 9, 2026: [[parmin.f#L1239-L1242]]; [[#L295-L319]]).

**From YREC's documentation.** [Physics Options](https://yrec.readthedocs.io/en/latest/namelist_physics.html) (Gravitational settling & microscopic diffusion): `LDIFY`, `LDIFZ`, `LDIFLI` turn on the settling of helium, metals and the light species; `FGRY`, `FGRZ` (default 1) scale the diffusion coefficients of helium and metals (for example 0.75 without rotational mixing); `XMIN` and `YMIN` (1.0D-3) turn diffusion off at low central $X$ (and, the documentation says, low surface $Y$). `ILAMBDA` chooses the Coulomb logarithm of the collision integrals: the documentation's line reads "4 (recommended) is a constant, 2.2". Among the rarely used options: `LTHOUL`, the formalism of Thoul et al., and `LTHOULFIT`, its published fit instead of the full solution (not recommended).

**Changed since `rp_1`.** The metals' coefficients `COD1Z`, `COD2Z`, `QCOD1Z`, `QCOD2Z` are arguments (formerly `/GRAVSZ/`); the unused `/GSCOF/` is dropped; otherwise declarations only: COMMON blocks to modules, `IMPLICIT NONE`.

## Bugs, by priority

1. **(a)** **The derivatives miss the mixing factors.** ([[#L288-L291]]; [[#L311]]; [[#L316]]) With `LTHOUL`, `COD1` and `COD2` are multiplied by `CSTMIXING`, but their $X$-derivatives `QCOD1X`, `QCOD2X` are not; `COD1Z` is multiplied by `CSTDIFFMIX*CSTMIXING`, but its derivative `QCOD1Z` by `CSTMIXING` only. [[grsett.f#GRSETT|`GRSETT`]] uses the derivatives to correct the coefficients for the change in $X$ (and $Z$) within the step ([[grsett.f#L173-L185]]; [[get_imp_diffco.f#L19-L21]]), so with a factor other than 1 the correction is that of the unscaled coefficient. What follows: The second-order correction of the settling coefficients is off by the factor; the size of the effect was not estimated. Only with `LTHOUL` (off by default; forced on by `LDIFZ` and `LDIFLI`) and `CSTMIXING` or `CSTDIFFMIX` set to a value other than 1 (both default 1). Read from the code, not run. **A possible fix:**

    ```fortran
    C 11/09/26 KC via Claude
    C code changed to scale the X-derivatives by the same mixing factors
    C as the coefficients.
                COD1(I) = CSTMIXING*FAC*HQPR(I)*X*(AP+AT)
                COD2(I) = CSTMIXING*FAC*AC
                QCOD1X(I) = CSTMIXING*FAC*HQPR(I)*(AP+AT+X*(QAPX+QATX))
                QCOD2X(I) = CSTMIXING*FAC*QACX
    ...
                   QCOD1Z(I) = CSTDIFFMIX*CSTMIXING*FAC*HQPR(I)*(AP+AT)
    ```
