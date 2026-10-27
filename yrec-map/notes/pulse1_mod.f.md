## Explanation

**Purpose.** `PULSE1_MOD` holds the thermodynamic and opacity derivatives at every shell of the interior, stored for the pulsation output, and the switch that makes the envelope routines keep their derivatives. Shared by 6 routines. It replaces `COMMON/PULSE1/` (MHP via Claude, 10/14/26); `JSON` comes from `DIMENSIONS_MOD`.

**What its variables hold, who sets them, who reads them.**
- `PQDP`, `PQDT`, `PQED`, `PQET`, `PQOD`, `PQOT`, `PQCP`, `PRMU`, `PEMU` (`JSON` each): at each shell, the equation of state's $\partial\ln\rho/\partial\ln P$ and $\partial\ln\rho/\partial\ln T$ (`QDP`, `QDT`), the energy generation's and the opacity's logarithmic derivatives in $\rho$ and $T$ (`QED`, `QET`, `QOD`, `QOT`), $c_P$ (`QCP`), and `RMU`, `EMU`. Stored by [[coefft.f#COEFFT|`COEFFT`]] when `LPULSE` is set; `PQDP` and `PQDT` always, since `GAM1` (`SOUND_MOD`) and the storage file need them ("JVS 01/11"). [[wrtmod.f#WRTMOD|`WRTMOD`]] writes them in the pulsation model; [[stitch.f#STITCH|`STITCH`]] writes `PQDT` to the stored model.
- `LPUMOD`: set by [[envint.f#ENVINT|`ENVINT`]] to `LPULPT .AND. LPRT` (pulsation output of the envelope); [[qenv.f#QENV|`QENV`]] and [[qatm.f#QATM|`QATM`]] then save their point's values in `PULSE2_MOD`.

**Design.** A blanket `USE PULSE1_MOD` in each routine.

**Changed since `rp_1`.** New file: `COMMON/PULSE1/` as a module.
