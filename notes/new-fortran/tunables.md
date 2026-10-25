# Tunable numbers

*In Python: [[new/pyrec/__init__.py|`pyrec`]].*

The notes found these values written into the code. Each becomes an UPPERCASE named constant in the module or type that uses it, with its unit and source in a comment, or a configuration entry where users already change it or should be able to. "Config" means a namelist entry with today's value as its default, so that results do not change.

| Value today | Where | Becomes |
| --- | --- | --- |
| `JSON = 5000` shells, in 123 of the 254 files | many | removed: arrays are allocated to $m$ |
| `IOWR = 9`; `IMILNE = 21` | [[main.f]], [[wrtmil.f]] | units from `newunit=`, held by each writer |
| $L_\odot$ = 3.844 × 10³³ erg s⁻¹ (`SUNL`), the base of the Monte Carlo draws, while `PARMIN`'s default `CLSUN` is 3.8515 × 10³³ | [[main.f]] | `MonteCarlo`: `L_SUN_BASE`, or the configured `CLSUN`; which is meant is a question ([Section 8](overview.md)) |
| `ENDAGE(2)` = 10⁸ yr, `ENDAGE(3)` = 4.57 × 10⁹ yr; up to 1000 parameter sets | Monte Carlo set-up | `MonteCarlo`: `AGE_RELAX`, `AGE_SUN`, `MAX_SETS` |
| $\log T_c$ < 6.6 for relaxing pre-main-sequence models | [[main.f]] | `Step`: `LOGTC_PMS = 6.6` |
| 15 cycles (the message says 10, the test 11) | [[chkcal.f]], [[main.f]] | `SolarCalibr`: `MAX_CYCLES = 15`, used by both (MAIN question 5) |
| 48 = 16 × 3 and 50 = 25 × 2 kind cards | [[setcal.f]], [[setscal.f]] | derived from `MAX_CYCLES`, not typed |
| `1.0D-3*DAGE*CSECYR`, the final step's floor | [[main.f]] | `TimeStepper`: `FINAL_STEP_FRAC = 1.0e-3_dp` (MAIN question 7 on its units) |
| 10⁻³⁴ $L_\odot$ "no burning"; 10²⁰ s "no limit" | [[htimer.f]] | `TimeStepper`: `L_NOBURN`, `DT_NOLIMIT` |
| $\log\rho_c \ge 5$ for the flash; 10¹⁵; floor 10⁻²² | [[ytime.f]] | `HeliumCriterion`: `LOGRHOC_FLASH`, `C_YTIME`, `Y_FLOOR` |
| Steps 3 × 10⁻⁴ and 1.5 × 10⁻³ of the numerical derivatives | [[eqstat.f]] | `EosBlend`: `DLOGT_NUM`, `DLOGP_NUM` ([Section 3.3](microphysics.md)) |
| Rough OPAL ranges, different by table | [[eqstat2.f]] | components of `OpalEosTable`, read with the table |
| `KRA` lists of 191 indices; 57 rows, 18 to 14 densities, filler 9 | [[readco.f]], [[readcoeos01.f]], [[rhoofp.f]], [[ll95tbl.f]] | read from the table files, or parameters of the subclass in one place |
| Rates below 10⁻³⁰ (before) and 10⁻⁵ (after); `SUM1` ≤ 10⁻¹² | [[engeb.f]] | `ReactionRates`: `RATE_FLOOR_IN`, `RATE_FLOOR_OUT`, `SUM_FLOOR` |
| ⁷Be screening constants of `RATES` (`ZPRDBE7P`, ...) | [[rates.f]] | `ReactionRates`, an option until the experts decide (RATES question 5) |
| 10⁻⁸ to zero matrix entries; 5 × 10⁻⁷ to reset $Z$ | [[kemcom.f]] | `NuclearNetwork`: `MATRIX_FLOOR`, `Z_RESET_TOL` |
| $\log T$ = 7 for destruction; $\lambda h \ge 30$; floor 10⁻²⁴; tolerances 10⁻⁶ | [[liburn.f]] | `LightElements`: `LOGT_DESTROY`, `LAMBDAH_MAX`, `ABUND_FLOOR`, `TOL` |
| `TLIM` = 6 in $\log T$ | [[lirate88.f]] | `LightElements`: `LOGT_RATES_MIN` |
| Relative tolerance 10⁻³ | [[bsrotmix.f]] | `Config%num`, beside `BSSTEP`'s own (from `/INTPAR/`) |
| 0.2 in `ECOD3`/`ECOD4`, 5 in `VESN`, the 10% limit on corrections | [[dadcoeft.f]] | `RotationTransport`: `ECOD_FAC`, `VESN_FAC`, `MAX_CORR` (DADCOEFT question 5 on their source) |
| `FAC = 0.2D0*C4PI*FW` (probably the 1/5 of Zahn 1992) | [[rotgrid.f]] | `RotationTransport`: `ZAHN_FIFTH = 0.2_dp`, with its source once confirmed |
| $\Delta\log T = 0.25\,\Delta\log P$; $\log\rho = \log P - \log T - 8$ for an added outer point | [[hpoint.f]] | `Rezoner`: `DLOGT_DLOGP_NEW`, `LOGRHO_OFFSET_NEW` |
| $\log T_\mathrm{eff}$ bounds 3.5, −0.5, 4.5, 4.55 | [[surfp.f]], [[kcsurfp.f]] | components of `KuruczAtmosphere`, `CastelliAtmosphere`, set from the table read |
| Gray switch at $\log T_\mathrm{eff}$ = 3.95 for Kurucz tables | [[surfbc.f]] | `KuruczAtmosphere%teffl_max`, from the table, as for Allard (SURFBC question 4) |
| Atomic mass unit, $\sigma$, isotope masses written in the code | [[viscos.f]] | `constants`, one value each (VISCOS question on the masses) |
| He-flash threshold $\log T$ = 7.98; period cap 9999 d (version 0) | [[wrtout.f]] | `TrackWriter`: `LOGT_HEFLASH`, `PERIOD_CAP_V0` |
| `LNUTAB = .FALSE.`, a block switched off in the code | [[main.f]] | removed or repaired, as the experts decide (MAIN question 4) |

The many controls that users already set (`ATIME`, `HTOLER`, `HPTTOL`, `NITER1`–`NITER4`, `DTWIND`, the wind and settling factors) stay configuration entries; [Section 3.2](kernels.md) names where each group goes.
