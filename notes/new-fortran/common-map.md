# The COMMON-block map

*In Python: [[new/pyrec/__init__.py|`pyrec`]].*

## 6.4 What replaces the COMMON blocks

Each block's contents go to the type that owns them, grouped by physics. Settings go into `Config`'s parts, state into the objects of [Section 3](overview.md), and the work arrays of one method become private components of its type. Mutable settings change owner: a switch that a routine turns off in the middle of a run (`LDIFY`, `LPTIME`, `KTTAU`) becomes state of the object that turns it off, so `Config` stays as read. Every one of rp_1's 243 blocks appears once below.

| What it holds | Blocks today | New home |
| --- | --- | --- |
| Physical constants | `/CONST/`, `/CONST1/`, `/CONST2/`, `/CONST3/`, `/CONFAC/` | `constants` (named parameters); `CMIXL` of `/CONST3/` goes to `Config%conv` |
| I/O units and output switches | `/LUNUM/`, `/LUOUT/`, `/CCOUT/`, `/CCOUT1/`, `/CCOUT2/`, `/CHRONE/`, `/TRACK/`, `/DESC/`, `/PO/`, `/PULSE/`, `/ROTPRT/`, `/IOMONTE/` | `Config%io`; units from `newunit=` held by the writers |
| Numerical controls | `/CTOL/`, `/CTLIM/`, `/INTPAR/`, `/INTATM/`, `/INTENV/`, `/BURTOL/`, `/CT2/`, `/CT3/`, `/NEWENG/`, `/GOVS/`, `/ERRMOM/`, `/DIFUS/`, `/DWMAX/`, `/NEWPARAM/` | `Config%num`; `LPTIME` of `/CT3/` as `TimeStepper%use_structure` (`NEWPARAM`'s newer names are read by `read_namelists` and mapped, as `REMAP` does) |
| Composition settings | `/NEWCMP/`, `/NEWMX/`, `/VNEWCB/`, `/I2O/`, `/FLAG/`, `/COMP2/` | `Config%comp`; the surface $Y$, ³He of `/COMP2/` go to `Star%surf` |
| Run cards and per-run values | `/CKIND/`, `/SETT/`, `/NEWXYM/`, `/CORE/`, `/HEFLSH/`, `/LABEL/`, `/ZRAMP/`, `/CENV/` | `KindCard` (`Config%cards`), and `Track` for the current card (`NK`); the triangle sizes of `/CENV/` go to `SurfaceBC`, the opacity units of `/ZRAMP/` to `Config%opac` |
| Convection settings | `/DPMIX/` | `Config%conv`; `IOVIM` becomes an argument |
| EOS settings | `/OPALEOS/`, `/SCV2/`, `/MHD/`, `/DEBHU/`, `/CCR/`, `/LREADCO/` | `Config%eos`; the Debye–Hückel and relativistic values to `YaleEos`; `LREADCO`'s flag to `OpalEos` |
| Opacity settings | `/NEWOPAC/`, `/MISCOPAC/`, `/LOPAL95/`, `/ALEXO/`, `/ALEX06/`, `/ALEXMIX/`, `/OPTAB/` | `Config%opac`; `OPTOL` and the table indices to `OpacityBlend` |
| Nuclear settings | `/CROSS/`, `/NEWCROSS/`, `/WEAK/`, `/NULOSS/`, `/BURNSCS/`, `/XSECT/` | `Config%nuc`, copied once into `ReactionRates`, `LightElements`, `NeutrinoLosses` |
| Settling settings and state | `/GRAVST/`, `/GRAVS2/`, `/GRAVS3/`, `/GRAVS4/`, `/CMIXING/` | `Config%sett`; `LDIFY` as `SettlingBase%active` |
| Settling work arrays | `/GRAVEZ/`, `/GRAVSZ/`, `/GSCOF/` | `GrsettSettling` (private) |
| Rotation settings | `/ROT/`, `/SBROT/`, `/CWIND/`, `/PMMWIND/`, `/NOTRAN/`, `/MAG/`, `/VMULT/`, `/VMULT2/`, `/VARFC/`, `/DIFAD/`, `/ADVEC/` | `Config%rot`; the factors of `/DIFAD/` become constants of `RotationTransport` ([Section 5](tunables.md)) |
| Disk locking | `/DISK/` | `Config%rot` (`TDISK`, `PDISK`, `LDISK`); `SAGE` to `Star` |
| Surface and atmosphere settings | `/ATMOS/`, `/ALATM03/`, `/ALATM04/`, `/SPOTS/`, `/ENVGEN/` | `Config%surf`; `KTTAU`'s change on failure becomes `AtmosphereSwitch` state; `/ALATM04/` holds only dummies and is dropped |
| Mass-loss settings and state | `/MASSCHG/`, `/MASSCHG2/`, `/MASSCHG3/` | `Config%mloss`; `/MASSCHG2/` (entropies, `SMASS0`) becomes arguments of `MassLoss%apply` and a component read by `StructureSolver` |
| Calibration | `/CALSUN/`, `/CALS2/`, `/CALSTAR/`, `/MONTE/`, `/MONTE2/`, `/CENT/` | `SolarCalibr`, `StarCalibr`, `MonteCarlo`; the central values of `/CENT/` are `Star` properties |
| The model | `/COMP/`, `/THEAGE/`, `/ROTEN/`, `/QUADD/`, `/QUADRU/`, `/OVRTRN/` | `Star` and `Star%surf`; the quadrupole to `Distortion`; `TAUCZ` to `OverturnAnal`, `FRACSTEP` to `RotationStep` |
| Start of the step | `/OLDMOD/`, `/OLDPHY/`, `/OLDROT/`, `/OLDROT2/`, `/OLDAB/`, `/OLDRAT/`, `/ORIGSTART/`, `/ENTROP/`, `/PREVCZ/`, `/PREVMID/`, `/PREVMU/`, `/LIOV/` | `StepStart`, held by `Step`; `PSCAL0`, `PSCAL1` of `/LIOV/` to `LightElements` |
| Per-shell physics | `/TEMP/`, `/TEMP2/`, `/MDPHY/`, `/SCRTCH/`, `/ROTDER/`, `/NEWEPS/`, `/GRAB/`, `/FLUXES/`, `/BE7/`, `/PUALPHA/`, `/SOUND/` | `ShellPhysics`; the mid-step copies (`/MDPHY/`) and velocities (`/TEMP2/`) to `RotationTransport`; `PUALPHA` to `PointState` |
| Burning results | `/BURN/`, `/BSBURN/`, `/NEWRAT/`, `/DEUTER/` | returned by `ReactionRates%eval`, `Deuterium`, `LightElements`; `/BSBURN/` serves only the dead `BURSMIX` |
| The outer layers | `/ENVSTRUCT/`, `/ATMSTRUCT/`, `/ENVPRT/`, `/ATMPRT/`, `/ENVCZ/`, `/PULSE1/`, `/PULSE2/`, `/STCH/`, `/JTEST/` | `EnvelopeSolution`; `/STCH/` to `StoreFile`; `/JTEST/` to `OverturnAnal` |
| Outputs at chosen ages | `/ACDPTH/` | `AGEOUT`, `LCLCD` to `Config%io`; the acoustic results to `AcousticAnal` |
| Rotation work arrays | `/INTVAR/`, `/INTVR2/`, `/INTFAC/`, `/VFACT/`, `/TAUKH/`, `/DIFAD2/`, `/DIFAD3/`, `/DIFAD4/`, `/DIFADDT/`, `/EGRIDCHI/`, `/EGRIDDER/` | `RotationTransport` (private) |
| Solver work arrays | `/TRIDI/`, `/SPLIN/`, `/EGRID/` | locals of `numerics` and `ChiGrid` |
| OPAL EOS 1995 | `/A/`, `/AA/`, `/B/`, `/BB/`, `/E/`, `/EE/`, `/EEE/`, `/RMPOPEOS/` | `OpalEos` with `release = '1995'` (its `OpalEosTable`) |
| OPAL EOS 2001 | `/AEOS/`, `/AAEOS/`, `/BEOS/`, `/BBEOS/`, `/EEOS/`, `/EEEOS/`, `/EEEEOS/`, `/RMPOPEOS01/` | `OpalEos`, `'2001'` |
| OPAL EOS 2006 | `/AEOS06/`, `/AAEOS06/`, `/BEOS06/`, `/BBEOS06/`, `/EEOS06/`, `/EEEOS06/`, `/EEEEOS06/` | `OpalEos`, `'2006'` |
| MHD EOS | `/CHE1/`, `/CHE2/`, `/CHE3/`, `/CHE4/`, `/CHE5/`, `/CHEA/`, `/CHEB/`, `/CHEC/`, `/TAB1A/`, `/TAB1B/`, `/TAB1C/`, `/TAB2A/`, `/TAB2B/`, `/TAB2C/`, `/TABX1/`, `/TABX2/`, `/TABX3/`, `/TABX4/`, `/TABX5/`, `/TTTT/`, `/MHDOUT/` | `MhdEos`: one array of tables |
| SCV EOS | `/SCVEOS/` | `ScvEos` |
| OPAL95 opacities | `/LLOT95/`, `/LLOT95A/`, `/LLOT95E/`, `/OP95EXT/`, `/OP95FACT/`, `/OP95INDX/` | `Opal95Opacity` |
| OPAL92 opacities | `/GLLOT/`, `/LLOT/`, `/LLOT4/`, `/LINTPL/`, `/KIPMLL/`, `/GLLOT2/`, `/LLOT2/`, `/LLOT42/`, `/LINTPL2/`, `/KIPMLL2/` | `Opal92Opacity`, two instances |
| LAOL89 opacities | `/NWLAOL/`, `/SLAOL/`, `/NWLAOL2/`, `/SLAOL2/`, `/ZLAOL/`, `/ZSLAOL/` | `Laol89Opacity` (the pure-Z table a third instance) |
| Alexander opacities | `/ALOT/`, `/ALOTALL/`, `/GALOT/`, `/ALOT06/`, `/ALOT06ALL/`, `/GALOT06/` | `Alex95Opacity`, `Alex06Opacity` |
| Kurucz 1990 opacities | `/KRZ/`, `/GKRZ/`, `/INTPL2/`, `/KIPM/`, `/KRZ2/`, `/GKRZ2/`, `/INTPL22/`, `/KIPM2/` | `Kurucz90Opacity`, two instances |
| Atmosphere tables | `/ATMOS2/`, `/ATMOS2C/`, `/FAC/`, `/ALATM01/`, `/ALATM02/`, `/ALATM05/` | `KuruczAtmosphere`, `CastelliAtmosphere`, `AllardAtmosphere` |

The development branch has already removed the blocks of the options it dropped, consolidated others, and made each remaining block a module (87 `…_MOD` modules; no `COMMON` statement is left, its issue 37; [Section 7.3](overview.md)). That is the first half of this map: a module per block makes the data explicit but still global. The second half, done type by type in [Section 7.2](overview.md), moves each module's variables into the derived type above and deletes the module.
