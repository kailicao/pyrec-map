## Explanation

**Purpose.** `EOS06MISC_MOD` holds the results and workspace of the OPAL 2006 equation-of-state interpolation: the interpolated quantities, the grid indices of the current point, the composition of the tables, the order of the quantities, and the extent of each table row, shared by 9 routines. It replaces four COMMON blocks of `rp_1`, `/EEOS06/` (`ESACT`, `EOS`), `/AAEOS06/` (`Q`, `H`, `XXH`), `/BBEOS06/` (`L1`–`L4`, `K1`–`K4`, `IP`, `IQ`), and `/BEOS06/` (`ZZ`, `IRI`, `INDEX`, `NTA`, `NRA`), first merged into `COMMON/EOS06MISC/` and then made a module (MHP via Claude, 10/20/26). The table dimensions `MX` = 5, `MV` = 10, `NR` = 169, `NT` = 197 are `PRIVATE`.

**What its variables hold, who sets them, who reads them.**
- `EOS(MV)`: the interpolated quantities (in the order of ESAC06's notes: $`P`$, $`E`$, $`S`$, … , $`\Gamma_2/(\Gamma_2-1)`$; the tenth place, $`\Gamma_3 - 1`$, is never computed, [ESAC06](esac06.f.md#esac06)), set by [`ESAC06`](esac06.f.md#esac06) (from `ESACT`, then scaled by $`P_0`$, $`T_6`$, and the mean molecular weight) and corrected for radiation by [`RADSUB06`](https://github.com/yreclab/yrec/blob/7be4133/src/radsub06.f#L7-L117); read by the callers, [`OEQOS06`](https://github.com/yreclab/yrec/blob/7be4133/src/oeqos06.f#L30-L132), [`RHOOFP06`](https://github.com/yreclab/yrec/blob/7be4133/src/rhoofp06.f#L8-L147), and [`CALCAD`](calcad.f.md#calcad).
- `ESACT`: one quantity interpolated in $`T_6`$ and $`\rho`$ by [`T6RINTEOS06`](t6rinteos06.f.md#t6rinteos06), from the quadratics `H(4)` (in $`\rho`$ at fixed $`T`$) and `Q(4)` (in $`T`$), its workspace.
- `L1`–`L4`, `K1`–`K4`, `IP`, `IQ` (`INTEGER*4`): the four density and four temperature indices around the point and the number of points used in each direction, set by `ESAC06`; read by `T6RINTEOS06` and [`EQBOUND06`](eqbound06.f.md#eqbound06).
- `ZZ(MX)`: the $`Z`$ of each table, read from the table headers by [`READCOEOS06`](https://github.com/yreclab/yrec/blob/7be4133/src/readcoeos06.f#L7-L163); read by `ESAC06`.
- `INDEX(10)`: the order in which the quantities are stored (1 to 10, initialized); `IRI(10)`: its inverse, set by [`SETEOS06`](esac06.f.md#seteos06); read by `ESAC06` and `RADSUB06`.
- `NTA(NR)`, `NRA(NT)`: for each density the number of temperatures in the tables, and for each temperature the number of densities (the tables are not rectangular); initialized, read by `READCOEOS06`, `EQBOUND06`, and `RHOOFP06`.
- `XXH` ([line 43](https://github.com/yreclab/yrec/blob/7be4133/src/eos06misc_mod.f#L43)): set and read nowhere (unused?).

**Design.** A blanket `USE EOS06MISC_MOD`. `L1`–`L4` are `INTEGER*4` despite their initial letter, as CALCAD typed them. The initial values of `INDEX`, `NTA`, `NRA` moved from ESAC06's `DATA` statements (whole-array `DATA` in the module, the same values).

**Changed since `rp_1`.** New file: `/EEOS06/`, `/AAEOS06/`, `/BBEOS06/`, and `/BEOS06/` as one module, with the initial values moved from ESAC06.
