## Explanation

**Purpose.** `CONSTANTS_MOD` holds the physical and mathematical constants (solar units, $\ln 10$, $\pi$, $G$, $\sigma$, the gas constant, and logarithms of them) shared by 89 routines. It replaces `COMMON/CONST/`, `/CONST1/`, `/CONST2/` and `/CONST3/` of `rp_1`, first merged into `COMMON/CONSTANTS/` and then made a module (MHP via Claude, 10/14/26), without `CMIXL` (now passed as an argument) and with `C_2` from `COMMON/CWIND/`. All members are `REAL*8`.

**What its variables hold, who sets them, who reads them.**
- `CLSUN`, `CRSUN`: the solar luminosity and radius (cgs), with initial values 3.8515D33 and 6.9598D10 moved from PARMIN's `DATA` statement; both are in the `PHYSICS` namelist read by [[parmin.f#PARMIN|`PARMIN`]], so a run can change them.
- Set once in [[setups.f#SETUPS|`SETUPS`]] (its comments name them): `CLNDP` and `CLN` ($\ln 10$), `CLNI` ($1/\ln 10$), `CLSUNL`, `CMSUNL`, `CRSUNL` (log of the solar luminosity, mass, radius), `CLNSUN` ($\ln 10/L_\odot$), `CMSUN` (1.9891D33 g), `CMBOL` (the Sun's bolometric magnitude, 4.79), `CSECYR` (seconds per year, 3.1558D7), `CC13`, `CC23` (1/3, 2/3), `CPI`, `C4PI`, `C4PIL` ($\log 4\pi$), `C4PI3L` ($\log 4\pi/3$), `CSIG` and `CSIGL` (Stefan–Boltzmann), `CA3` $=4\sigma/3c$ ($a/3$) and `CA3L`, `CGAS` (the gas constant), `CGL` ($\log G$), `CMKH` ($\log[(2\pi m_e)^{3/2}k^{5/2}/h^3]$, for the Saha equation), `CDELRL` $= -\log(4\pi/3) - \log\sigma - \log 16$ (the radiative gradient), `CMIXL2` (1/3) and `CMIXL3` $=16\sqrt2\,\sigma$ (mixing length).
- `CLN`, `CC13`, `CC23` are also set in `PARMIN` (to the same values, before `SETUPS` runs) and written in its `DERIVED` namelist to the `.short` file. `C_2` (0.0506, the centrifugal term of the Matt et al. wind law) is set in `PARMIN` and read by [[mwind.f#MWIND|`MWIND`]] and [[mcowind.f#MCOWIND|`MCOWIND`]].
- Readers: nearly every physics routine; `CLN` alone by 68 files, `CGL` by 34.
- `CMKHN` is set and read nowhere; `CA3L` and `CMSUNL` are set but never read.

**Design.** A blanket `USE CONSTANTS_MOD` in each routine. The constants are module variables set at run time rather than `PARAMETER`s, so a routine run before `SETUPS` would see them undefined.

**Changed since `rp_1`.** New file: `COMMON/CONST/`–`/CONST3/` as one module, without `CMIXL`, with `C_2` from `/CWIND/`, and the defaults of `CLSUN`, `CRSUN` moved from PARMIN.

## Questions for the experts

1. **Unused members.** `CMKHN` is used nowhere, and `CA3L`, `CMSUNL` are set but never read. Can they go?
