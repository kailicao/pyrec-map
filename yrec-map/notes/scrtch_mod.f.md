## Explanation

**Purpose.** `SCRTCH_MOD` holds the local physics of the interior at each shell, as computed in the last pass of the structure equations: energy generation, opacity, temperature gradients, ionization, convective velocity. Many routines read it later in the step (mixing, burning, regridding, output). Shared by 16 routines. It replaces `COMMON/SCRTCH/` (MHP via Claude, 10/14/26); `JSON` comes from `DIMENSIONS_MOD`.

**What its variables hold, who sets them, who reads them.** [[coefft.f#COEFFT|`COEFFT`]] stores all of them at each shell `IM`; [[physic.f#PHYSIC|`PHYSIC`]] stores `SO`, `SDEL` and `SVEL` again when it recomputes the physics.
- `SESUM(JSON)`: the sum of the nuclear energy generation's five terms `EG(1)`…`EG(5)` (0 below the cutoff temperature `TCUT(1)`); `SEG(7,JSON)`: those five as fractions of `SESUM`, then the neutrino term `EG(6)` and the gravitational term `HHC` (`EGRAV`) (`SEG(6)`, `SEG(7)`). Read by [[hpoint.f#HPOINT|`HPOINT`]] (which interpolates them, through [[osplin.f#OSPLIN|`OSPLIN`]], to the grid at the start of the step), [[midmod.f#MIDMOD|`MIDMOD`]], [[wrtmil.f#WRTMIL|`WRTMIL`]], the setup of rotation (`FRACNUC` in `ROTDER_MOD`) and the output ([[putstore.f#PUTSTORE|`PUTSTORE`]], [[stitch.f#STITCH|`STITCH`]], [[wrtmod.f#WRTMOD|`WRTMOD`]]).
- `SO(JSON)`: the opacity. Read by `HPOINT`, `MIDMOD`, [[viscos.f#VISCOS|`VISCOS`]] and the output (`PUTSTORE`, `STITCH`, `WRTMOD`, [[wrtout.f#WRTOUT|`WRTOUT`]]).
- `SDEL(3,JSON)`: $\nabla_\mathrm{rad}$, $\nabla$, $\nabla_\mathrm{ad}$. [[rotmix.f#ROTMIX|`ROTMIX`]] replaces `SDEL(2,·)` for a while and restores it. Read by the burning and mixing routines ([[liburn.f#LIBURN|`LIBURN`]], [[liburn2.f#LIBURN2|`LIBURN2`]], [[microdiff_mte.f#MICRODIFF_MTE|`MICRODIFF_MTE`]], [[setup_grsett.f#SETUP_GRSETT|`SETUP_GRSETT`]], `ROTMIX`), [[gettau.f#GETTAU|`GETTAU`]], `HPOINT`, `MIDMOD`, `PHYSIC` and the output.
- `SVEL(JSON)`: the convective velocity (cm/s); read by `GETTAU`, `HPOINT`, `MIDMOD` and the output.
- `SBETA(JSON)`, `SETA(JSON)`, `SFXION(3,JSON)`, `SCP(JSON)`: $\beta$ (gas over total pressure), the degeneracy parameter $\eta$, the three ionization fractions and $c_P$, for the stored model (`PUTSTORE`, `STITCH`).
- `LOCONS(JSON)`: whether conduction dominates the opacity (`LOCOND`); set by `COEFFT` and read by no routine.

**Design.** A blanket `USE SCRTCH_MOD` in each routine.

**Changed since `rp_1`.** New file: `COMMON/SCRTCH/` as a module.
