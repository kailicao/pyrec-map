# The compiled tree

*Part of [A new design for YREC](overview.md). Each family's default runs compiled (Numba), and a family in plain Python also works, with a warning. Since compiled code cannot call Python without leaving the compiled chain, a family in plain Python makes everything that calls it run in Python too. This page shows what that reaches: a table per family, a high-level tree of a step's stages, and each family's compiled static methods. All of it is generated from the code, not drawn by hand.*

**How to read it.** A *kernel* is a function Numba compiles; a *chain* is a kernel with every kernel it calls, which Numba compiles together; a *top kernel* is one called from plain Python, at the head of a chain. [C] marks what runs compiled, [P] what runs as plain Python, [C/P] a mix; `<family>` is the family a kernel belongs to; *inline* and *no-NRT* are its Numba options (`inline='always'`, no reference counting). Names are Python's: `module.function`, the object-oriented version's classes under `pyrec_oop/`.

## The families' bindings

The compiled chains call the local families through module globals; in the object-oriented version each is bound to the installed family's static method ([Writing a Numba family](numba.md)). With YREC's defaults installed:

- `opacity_point` -> `pyrec_oop/opacity.Opacity.point` (opacity)
- `eos_point` -> `pyrec_oop/eos.EOS.point` (eos)
- `convection_point` -> `pyrec_oop/convection.Convection.point` (convection)
- `atmosphere_point` -> `qatm._qatm_k` (atmosphere)
- `envelope_point` -> `qenv._qenv_k` (atmosphere)
- `network_point` -> `pyrec_oop/network.Network.point` (network)
- `network_serves` -> `pyrec_oop/network.Network.serves` (network)

The atmosphere's integrands are the Fortran-tracking pyrec's own qatm and qenv kernels, bound as the default class's static methods.

## What falls back when a family is plain

A plain family replaces the family's static methods with Python functions. Every kernel that calls one of them, directly or through others, then runs as Python too; the kernels they call in other families stay compiled, but are now entered from Python at each call (crossings). The stage families have no compiled static method: They are plain Python already, calling compiled kernels, so making one plain changes nothing compiled.

For each family alone: the static methods a plain family replaces (for the Fortran-tracking pyrec, all the family's kernels), how many kernels would then run as Python (those and every kernel that reaches them), the chains entered from plain Python that fall back, the kernels still compiled but then entered from Python, and the Fortran run's time in routines all of whose kernels fall back. `compiled_tree.py --plain FAMILY` gives one family's full what-if.

| Family | Static methods replaced | Kernels in Python | Chains that fall back | Crossings | Fortran time in routines wholly in Python | pyrec's profile, routines affected |
| --- | --- | ---: | --- | ---: | ---: | --- |
| `eos` | `pyrec_oop/eos.EOS.point`, `pyrec_oop/eos.EOS.update_hints` | 12 | `coefft._coefft_nb`, `envint._atm_loop_k`, `envint._env_loop_k` | 12 | 0.04 s (1%) | envint 4.94 s, coefft 4.14 s |
| `opacity` | `pyrec_oop/opacity.Opacity.point` | 11 | `coefft._coefft_nb`, `envint._atm_loop_k`, `envint._env_loop_k` | 12 | 0.04 s (1%) | envint 4.94 s, coefft 4.14 s |
| `atmosphere` | `qatm._qatm_k`, `qenv._qenv_k` | 8 | `envint._atm_loop_k`, `envint._env_loop_k` | 7 | 0.04 s (1%) | envint 4.94 s |
| `network` | `pyrec_oop/network.Network.point`, `pyrec_oop/network.Network.serves` | 3 | `coefft._coefft_nb` | 6 | 0.00 s (0%) | coefft 4.14 s |
| `convection` | `pyrec_oop/convection.Convection.point` | 9 | `coefft._coefft_nb`, `envint._atm_loop_k`, `envint._env_loop_k` | 13 | 0.03 s (1%) | envint 4.94 s, coefft 4.14 s |
| `diffusion` | none: a stage family, plain Python that calls compiled kernels | 0 | none | 0 | | |
| `rotation` | none: a stage family, plain Python that calls compiled kernels | 0 | none | 0 | | |
| `mass_loss` | none: a stage family, plain Python that calls compiled kernels | 0 | none | 0 | | |
| `solver` | none: a stage family, plain Python that calls compiled kernels | 0 | none | 0 | | |
| `timestep` | none: a stage family, plain Python that calls compiled kernels | 0 | none | 0 | | |
| `rezoner` | none: a stage family, plain Python that calls compiled kernels | 0 | none | 0 | | |

The table is for a plain subclass that still calls the default's compiled kernels (as `point = EOS.point.py_func` does). A family written wholly in Python also runs its own routines in Python: the family's share in the next table, for example 82% of the Fortran's time for the EOS.

The time columns: the Fortran run's own time (gprof, 5.47 s sampled in all) in the routines whose kernels would all run as Python, and, for the routines affected, the Fortran-tracking pyrec's time in its warm-run profile (14.0 s inside Python in all; pyrec's `tests/results.md`, Nov 17, 2026). The envelope's integration (envint) and the solver's loop (coefft) are most of pyrec's time and fall back for four of the five local families.

## The families in the run

Each routine on the 1 M☉ run's path counted once. Time: the Fortran run's gprof self time (5.47 s sampled in all); pyrec: its warm-run profile (14.0 s inside Python; a Python function's exclusive time, its kernels' time included), where it names one of the family's routines.

| Family | Routines on the path | Compiled | Fortran self time | In compiled routines | pyrec |
| --- | ---: | ---: | ---: | ---: | --- |
| `eos` | 18 | 15 | 4.47 s (82%) | 4.45 s | readcoeos06 0.66 s, setscv 0.22 s |
| `opacity` | 18 | 9 | 0.42 s (8%) | 0.41 s |  |
| `atmosphere` | 9 | 7 | 0.04 s (1%) | 0.04 s | envint 4.94 s |
| `network` | 10 | 9 | 0.14 s (3%) | 0.14 s |  |
| `convection` | 7 | 3 | 0.05 s (1%) | 0.05 s | mix 0.18 s |
| `rotation` | 1 | 0 | 0.00 s (0%) | 0.00 s | viscos 0.11 s |
| `mass_loss` | 1 | 0 | 0.00 s (0%) | 0.00 s |  |
| `solver` | 5 | 4 | 0.09 s (2%) | 0.09 s | coefft 4.14 s, crrect 0.14 s |
| `timestep` | 3 | 1 | 0.00 s (0%) | 0.00 s |  |
| `rezoner` | 2 | 1 | 0.01 s (0%) | 0.01 s | hpoint 0.15 s |
| `io` | 13 | 1 | 0.01 s (0%) | 0.00 s | putmodel2 1.53 s, stitch 0.16 s, wrtout 0.14 s |
| `utilities` | 17 | 15 | 0.24 s (4%) | 0.24 s |  |
| `driver` | 2 | 1 | 0.00 s (0%) | 0.00 s |  |

The rows `io`, `utilities`, and `driver` are groups of routines outside the families: the input and output, the shared numerical utilities, and the run's driver and setup.

## The high-level tree

The step's stages ([One step](overview.md)) and, under each, the families reached and their top kernels.

Under each stage, what pyrec's plain Python reaches from the stage's routines: those the stage's families wrap, or in the Fortran-tracking pyrec `main.step`'s. The walk follows the calls and skips the routines the run never reaches. Per family it lists the routines that run as plain Python, and the kernels called from Python (top kernels), each heading a chain of kernels. [C] compiled (Numba), [P] plain Python, [C/P] both. In the OOP version, each stage's line ends with what the stage does (`pyrec_oop/model.py`, STAGES).

- **controls. `controls`** (no pyrec routine): the controls, in order
  - (plain Python in the driver; no kernel)
- **start. `numerics.timestep.ages`** (no pyrec routine): start = state.copy()
  - (a copy of the State's arrays; no kernel)
- **mass_loss. `physics.mass_loss`** (massloss): massloss (main.f 721-725)
  - [C] `eos`
    - [C] `eqscve._eqscve_nb` from eqscve: chain of 8 kernels; reaches utilities
    - [C] `eqscvg._eqscvg_nb` from eqscvg: chain of 4 kernels; reaches utilities
    - [C] `eqstat2._eqstat2_k` from eqstat2: chain of 40 kernels; reaches utilities
  - [P] `mass_loss`
    - [P] plain: massloss
  - [C] `utilities`
    - [C] `interp._interp_nb` from interp: chain of 1 kernel
    - [C] `kspline._kspline_nb` from kspline: chain of 1 kernel
    - [C] `ksplint._ksplint_nb` from ksplint: chain of 1 kernel
- **composition. `physics.network.save_start`, `physics.convection.mix`, `numerics.timestep.advance_age`** (mix): the start composition saved; mix: burning, mixing, settling over the step; the age (main.f 726-741)
  - [C] `eos`
    - [C] `eqscve._eqscve_nb` from eqscve: chain of 8 kernels; reaches utilities
    - [C] `eqscvg._eqscvg_nb` from eqscvg: chain of 4 kernels; reaches utilities
    - [C] `eqstat2._eqstat2_k` from eqstat2: chain of 40 kernels; reaches utilities
  - [C/P] `convection` (pyrec: mix 0.18 s)
    - [P] plain: convec, oversh, hsubp
    - [C] `mix._mix_clean_nb` from mix: chain of 1 kernel
    - [C] `mix._mix_zones_mean_nb` from mix: chain of 1 kernel
  - [C] `utilities`
    - [C] `interp._interp_nb` from interp: chain of 1 kernel
    - [C] `kspline._kspline_nb` from kspline: chain of 1 kernel
    - [C] `ksplint._ksplint_nb` from ksplint: chain of 1 kernel
  - [C] `driver`
    - [C] `main._step_save_comp_nb` from main: chain of 1 kernel
- **rezone. `numerics.rezoner`** (hpoint): hpoint (main.f 763-796)
  - [C] `eos`
    - [C] `eqscve._eqscve_nb` from eqscve: chain of 8 kernels; reaches utilities
    - [C] `eqscvg._eqscvg_nb` from eqscvg: chain of 4 kernels; reaches utilities
    - [C] `eqstat2._eqstat2_k` from eqstat2: chain of 40 kernels; reaches utilities
  - [C/P] `opacity`
    - [P] plain: surfopac, op95xtab, alex06tab
    - [C] `condopacp._cinterp3_nb` from cinterp3: chain of 1 kernel
    - [C] `condopacp._condopacp_nb` from condopacp: chain of 4 kernels
    - [C] `condopacp._hunt_nb` from hunt: chain of 1 kernel
    - [C] `condopacpint._condopacpint_nb` from condopacpint: chain of 6 kernels
    - [C] `getalex06._getalex06_nb` from getalex06: chain of 3 kernels; reaches utilities
    - [C] `getopac._getopac_nb` from getopac: chain of 21 kernels; reaches utilities
    - [C] `getopal95._getopal95_nb` from getopal95: chain of 9 kernels; reaches utilities
    - [C] `op952d._op952d_nb` from op952d: chain of 2 kernels
    - [C] `op953d._op953d_nb` from op953d: chain of 2 kernels
  - [C/P] `convection`
    - [P] plain: ovrot, convec, oversh, hsubp
    - [C] `tpgrad._tpgrad_nb` from tpgrad: chain of 3 kernels
  - [P] `rotation` (pyrec: viscos 0.11 s)
    - [P] plain: viscos
  - [P] `solver`
    - [P] plain: physic
  - [C] `rezoner` (pyrec: hpoint 0.15 s)
    - [C] `hpoint._masses_nb` from hpoint: chain of 1 kernel
    - [C] `hpoint._rezone_nb` from hpoint: chain of 15 kernels; reaches utilities
    - [C] `hpoint._transfer_nb` from hpoint: chain of 1 kernel
  - [C] `utilities`
    - [C] `interp._interp_nb` from interp: chain of 1 kernel
    - [C] `intrp2._intrp2_nb` from intrp2: chain of 1 kernel
    - [C] `kspline._kspline_nb` from kspline: chain of 1 kernel
    - [C] `ksplint._ksplint_nb` from ksplint: chain of 1 kernel
    - [C] `osplin._osplin_nb` from osplin: chain of 11 kernels
    - [C] `splinc._splinc_nb` from splinc: chain of 1 kernel
    - [C] `splintd2._splintd2_nb` from splintd2: chain of 1 kernel
- **structure. `numerics.solver` (which calls `network.light_elements_start`, `convection.mix_zones`, `rotation`)** (crrect, lirate88, mixcz, getw, fpft): crrect levels 1-4, with lirate88, step_first_guess, step_store_rates, mixcz, and with rotation getw, fpft in the structure-rotation iteration (main.f 799-1010)
  - [C] `eos`
    - [C] `eqscve._eqscve_nb` from eqscve: chain of 8 kernels; reaches utilities
    - [C] `eqscvg._eqscvg_nb` from eqscvg: chain of 4 kernels; reaches utilities
    - [C] `eqstat2._eqstat2_k` from eqstat2: chain of 40 kernels; reaches utilities
  - [C/P] `opacity`
    - [P] plain: alex06tab
    - [C] `condopacp._cinterp3_nb` from cinterp3: chain of 1 kernel
    - [C] `condopacp._condopacp_nb` from condopacp: chain of 4 kernels
    - [C] `condopacp._hunt_nb` from hunt: chain of 1 kernel
    - [C] `condopacpint._condopacpint_nb` from condopacpint: chain of 6 kernels
    - [C] `getalex06._getalex06_nb` from getalex06: chain of 3 kernels; reaches utilities
    - [C] `getopac._getopac_nb` from getopac: chain of 21 kernels; reaches utilities
    - [C] `getopal95._getopal95_nb` from getopal95: chain of 9 kernels; reaches utilities
    - [C] `op952d._op952d_nb` from op952d: chain of 2 kernels
    - [C] `op953d._op953d_nb` from op953d: chain of 2 kernels
  - [C/P] `atmosphere` (pyrec: envint 4.94 s)
    - [P] plain: surfbc
    - [C] `envint._atm_loop_k` from envint: chain of 78 kernels; reaches convection, eos, opacity, utilities
    - [C] `envint._env_loop_k` from envint: chain of 78 kernels; reaches convection, eos, opacity, utilities
    - [C] `hra._hra_nb` from hra: chain of 1 kernel
  - [C] `network`
    - [C] `engeb._engeb_nb` from engeb: chain of 5 kernels
    - [C] `lirate88._lirate88_rates_nb` from lirate88: chain of 1 kernel
  - [C/P] `convection` (pyrec: mix 0.18 s)
    - [P] plain: convec, oversh, hsubp
    - [C] `mix._mix_clean_nb` from mix: chain of 1 kernel
    - [C] `mix._mix_zones_mean_nb` from mix: chain of 1 kernel
    - [C] `mixcz._mixcz_clean_nb` from mixcz: chain of 1 kernel
    - [C] `mixcz._mixcz_find_zones_nb` from mixcz: chain of 1 kernel
    - [C] `mixcz._mixcz_zones_mean_nb` from mixcz: chain of 1 kernel
    - [C] `tpgrad._tpgrad_nb` from tpgrad: chain of 3 kernels
  - [C] `solver` (pyrec: coefft 4.14 s, crrect 0.14 s)
    - [C] `coefft._coefft_nb` from coefft: chain of 75 kernels; reaches convection, eos, network, opacity, utilities
    - [C] `crrect._crrect_apply_nb` from crrect: chain of 1 kernel
    - [C] `crrect._crrect_largest_nb` from crrect: chain of 1 kernel
    - [C] `hsolve._hsolve_nb` from hsolve: chain of 1 kernel
    - [C] `reduce._reduce_nb` from reduce: chain of 1 kernel
  - [C] `utilities`
    - [C] `interp._interp_nb` from interp: chain of 1 kernel
    - [C] `intrp2._intrp2_nb` from intrp2: chain of 1 kernel
    - [C] `kspline._kspline_nb` from kspline: chain of 1 kernel
    - [C] `ksplint._ksplint_nb` from ksplint: chain of 1 kernel
    - [C] `ratext._ratext_nb` from ratext: chain of 1 kernel
  - [C] `driver`
    - [C] `main._step_first_guess_nb` from main: chain of 1 kernel
    - [C] `main._step_store_rates_nb` from main: chain of 1 kernel
- **zones. `numerics.rezoner.locate_zones`, `physics.network.light_elements_due`, `physics.convection.zones`, `physics.network.light_elements`, `numerics.rezoner.restore_fitting_point`** (findsh, convec, lirate88, liburn, getnewenv, fpft): findsh; convec, lirate88, liburn; getnewenv (main.f 1013-1047)
  - [C] `eos`
    - [C] `eqscve._eqscve_nb` from eqscve: chain of 8 kernels; reaches utilities
    - [C] `eqscvg._eqscvg_nb` from eqscvg: chain of 4 kernels; reaches utilities
    - [C] `eqstat2._eqstat2_k` from eqstat2: chain of 40 kernels; reaches utilities
  - [C/P] `network`
    - [P] plain: safedivexp
    - [C] `liburn._liburn_interior_nb` from liburn: chain of 3 kernels; reaches utilities
    - [C] `liburn._liburn_mass_sums_nb` from liburn: chain of 1 kernel
    - [C] `liburn._liburn_zone_nb` from liburn: chain of 3 kernels; reaches utilities
    - [C] `lirate88._lirate88_rates_nb` from lirate88: chain of 1 kernel
  - [P] `convection`
    - [P] plain: convec, oversh, hsubp
  - [P] `rezoner`
    - [P] plain: findsh
  - [C] `utilities`
    - [C] `interp._interp_nb` from interp: chain of 1 kernel
    - [C] `kspline._kspline_nb` from kspline: chain of 1 kernel
    - [C] `ksplint._ksplint_nb` from ksplint: chain of 1 kernel
    - [C] `ratext._ratext_nb` from ratext: chain of 1 kernel
- **timestep. `numerics.timestep`, `numerics.timestep.counts_model`, `outputs`** (htimer, wrtout): htimer, the model number, the output (wrtout), the history row, the stopping conditions (main.f 1051-1126)
  - [C] `eos`
    - [C] `eqscve._eqscve_nb` from eqscve: chain of 8 kernels; reaches utilities
    - [C] `eqscvg._eqscvg_nb` from eqscvg: chain of 4 kernels; reaches utilities
    - [C] `eqstat2._eqstat2_k` from eqstat2: chain of 40 kernels; reaches utilities
  - [C/P] `opacity`
    - [P] plain: alex06tab
    - [C] `condopacp._cinterp3_nb` from cinterp3: chain of 1 kernel
    - [C] `condopacp._condopacp_nb` from condopacp: chain of 4 kernels
    - [C] `condopacp._hunt_nb` from hunt: chain of 1 kernel
    - [C] `condopacpint._condopacpint_nb` from condopacpint: chain of 6 kernels
    - [C] `getalex06._getalex06_nb` from getalex06: chain of 3 kernels; reaches utilities
    - [C] `getopac._getopac_nb` from getopac: chain of 21 kernels; reaches utilities
    - [C] `getopal95._getopal95_nb` from getopal95: chain of 9 kernels; reaches utilities
    - [C] `op952d._op952d_nb` from op952d: chain of 2 kernels
    - [C] `op953d._op953d_nb` from op953d: chain of 2 kernels
  - [C/P] `atmosphere` (pyrec: envint 4.94 s)
    - [P] plain: tauintnew
    - [C] `envint._atm_loop_k` from envint: chain of 78 kernels; reaches convection, eos, opacity, utilities
    - [C] `envint._env_loop_k` from envint: chain of 78 kernels; reaches convection, eos, opacity, utilities
    - [C] `gettau._gettau_envelope_nb` from gettau: chain of 1 kernel
    - [C] `gettau._gettau_interior_nb` from gettau: chain of 1 kernel
    - [C] `hra._hra_nb` from hra: chain of 1 kernel
  - [C] `network`
    - [C] `eqburn._eqburn_nb` from eqburn: chain of 3 kernels
    - [C] `rates._rates_nb` from rates: chain of 5 kernels
  - [C] `convection`
    - [C] `tpgrad._tpgrad_nb` from tpgrad: chain of 3 kernels
  - [C/P] `timestep`
    - [P] plain: htimer, xtime
    - [C] `ptime._ptime_max_changes_nb` from ptime: chain of 1 kernel
  - [C/P] `io` (pyrec: putmodel2 1.53 s, stitch 0.16 s, wrtout 0.14 s)
    - [P] plain: putstore, wrtlst, putmodel2, stitch
    - [C] `wrtout._wrtout_inertia_nb` from wrtout: chain of 1 kernel
  - [C] `utilities`
    - [C] `interp._interp_nb` from interp: chain of 1 kernel
    - [C] `intrp2._intrp2_nb` from intrp2: chain of 1 kernel
    - [C] `kspline._kspline_nb` from kspline: chain of 1 kernel
    - [C] `ksplint._ksplint_nb` from ksplint: chain of 1 kernel
    - [C] `ratext._ratext_nb` from ratext: chain of 1 kernel

PHYSIC appears under `solver` because the stages still reach pyrec's PHYSIC, through the routines the defaults wrap (HPOINT calls it) and through `families.profiles`, whose code holds both PHYSIC and `pyrec_oop.profiles` (the generator follows both branches); the object-oriented version drops it, its mean molecular weight and its shear limit going to two small modules ([The families' names](names.md)), once the defaults replace those routines.

## Each family's compiled static methods

The local families' hot paths and the kernels they call; a kernel of another family is shown on one line, its tree under its own family. In the generated chains, `eqstat._eqstat_k` (the envelope's EOS call) calls the installed EOS family's `point`, as the tree under `eos` shows.

### `eos`

```text
[C] pyrec_oop/eos.py:EOS
|-- [C] pyrec_oop/eos.EOS.point (inline, no-NRT) <eos>
|   `-- [C] eqstat2._eqstat2_kv (no-NRT) <eos>
|       |-- [C] eqbound06._eqbound06_nb (no-NRT) <eos>
|       |   |-- [C] eqbound06._eqbound06_rsearch_nb (no-NRT) <eos>
|       |   `-- [C] eqbound06._eqbound06_tsearch_nb (no-NRT) <eos>
|       |-- [C] eqrelv._eqrelv_nb (no-NRT) <eos>
|       |   `-- [C] eqrelv._eqrelv_tcolumns_nb (no-NRT) <eos>
|       |-- [C] eqsaha._eqsaha_nb (no-NRT) <eos>
|       |   |-- [C] eqsaha._eqsaha_helium_k_nb (no-NRT) <eos>
|       |   `-- [C] eqsaha._eqsaha_saha_k_nb (no-NRT) <eos>
|       |-- [C] eqscve._eqscve_nb (no-NRT) <eos>
|       |   |-- [C] eqscve._stencil_spline_nb (no-NRT) <eos>
|       |   |   |-- [C] kspline._kspline_nb (inline) <utilities>
|       |   |   `-- [C] ksplint._ksplint_nb (inline) <utilities>
|       |   |-- [C] eqscvg._eqscvg_nb (no-NRT) <eos>
|       |   |   |-- [C] eqscvg._in_t_nb (no-NRT) <eos>
|       |   |   |-- [C] eqscvg._rows_nb (no-NRT) <eos>
|       |   |   `-- [C] interp._interp_nb (inline, no-NRT) <utilities>
|       |   `-- [C] interp._interp_nb (inline, no-NRT) <utilities> (see above)
|       |-- [C] eqstat2._eqstat2_comp_nb (no-NRT) <eos>
|       |-- [C] eqstat2._eqstat2_step_nb (no-NRT) <eos>
|       |-- [C] mu._mu_nb (no-NRT) <eos>
|       |   `-- [C] mu._mu_ions_nb (no-NRT) <eos>
|       `-- [C] oeqos06._oeqos06_s (no-NRT) <eos>
|           `-- [C] oeqos06._oeqos06_nb (no-NRT) <eos>
|               |-- [C] esac06._esac06_nb (no-NRT) <eos>
|               |   |-- [C] esac06._esac06_rindex_nb (no-NRT) <eos>
|               |   |-- [C] esac06._esac06_tindex_nb (no-NRT) <eos>
|               |   |-- [C] esac06._esac06_xindex_nb (no-NRT) <eos>
|               |   |-- [C] esac06._log (no-NRT) <eos>
|               |   |-- [C] gmass06._gmass06_nb (inline, no-NRT) <eos>
|               |   |-- [C] quadeos06._quadeos06_nb (inline, no-NRT) <eos>
|               |   |-- [C] radsub06._radsub06_nb (no-NRT) <eos>
|               |   |   `-- [C] radsub06._radsub06_prad_nb (no-NRT) <eos>
|               |   `-- [C] t6rinteos06._t6rinteos06_nb (inline, no-NRT) <eos>
|               |       `-- [C] quadeos06._quadeos06_nb (inline, no-NRT) <eos> (see above)
|               |-- [C] oeqos06._oeqos06_beta_nb (no-NRT) <eos>
|               |-- [C] oeqos06._oeqos06_derivs_nb (no-NRT) <eos>
|               `-- [C] rhoofp06._rhoofp06_nb (no-NRT) <eos>
|                   |-- [C] esac06._esac06_nb (no-NRT) <eos> (see above)
|                   |-- [C] rhoofp06._rhoofp06_prad_nb (no-NRT) <eos>
|                   |-- [C] rhoofp06._rhoofp06_tindex_nb (no-NRT) <eos>
|                   `-- [C] rhoofp06._rhoofp06_xindex_nb (no-NRT) <eos>
`-- [C] pyrec_oop/eos.EOS.update_hints (inline, no-NRT) <eos>
```

### `opacity`

```text
[C] pyrec_oop/opacity.py:Opacity
`-- [C] pyrec_oop/opacity.Opacity.point (inline, no-NRT) <opacity>
    `-- [C] getopac._getopac_nb (no-NRT) <opacity>
        |-- [C] condopacpint._condopacpint_nb (no-NRT) <opacity>
        |   |-- [C] condopacp._condopacp_nb (no-NRT) <opacity>
        |   |   |-- [C] condopacp._cinterp3_nb (inline, no-NRT) <opacity>
        |   |   |-- [C] condopacp._condopacp_in_rho_nb (no-NRT) <opacity>
        |   |   |   `-- [C] condopacp._cinterp3_nb (inline, no-NRT) <opacity> (see above)
        |   |   `-- [C] condopacp._hunt_nb (inline, no-NRT) <opacity>
        |   `-- [C] condopacpint._condopacpint_weights_nb (no-NRT) <opacity>
        |-- [C] getalex06._getalex06_nb (no-NRT) <opacity>
        |   |-- [C] getalex06._getalex06_stencil_nb (no-NRT) <opacity>
        |   `-- [C] interp._interp_nb (inline, no-NRT) <utilities>
        |-- [C] getopac._getopac_add_conductive_nb (no-NRT) <opacity>
        |-- [C] getopac._getopac_hubbard_lampe_nb (no-NRT) <opacity>
        |-- [C] getopac._getopac_ramp_nb (no-NRT) <opacity>
        `-- [C] getopal95._getopal95_nb (no-NRT) <opacity>
            |-- [C] getopal95._getopal95_stencil_nb (no-NRT) <opacity>
            |-- [C] getopal95._x_stencil_nb (no-NRT) <opacity>
            |   `-- [C] intrp2._intrp2_nb (inline, no-NRT) <utilities>
            |-- [C] interp._interp_nb (inline, no-NRT) <utilities> (see above)
            |-- [C] op952d._op952d_nb (no-NRT) <opacity>
            |   `-- [C] op952d._op952d_extrap_nb (no-NRT) <opacity>
            `-- [C] op953d._op953d_nb (no-NRT) <opacity>
                `-- [C] op953d._op953d_extrap_nb (no-NRT) <opacity>
```

### `atmosphere`

```text
[C] pyrec_oop/atmosphere.py:Atmosphere (its integrands: pyrec's qatm and qenv kernels)
`-- [C] qatm._qatm_k (no-NRT) <atmosphere>
    |-- [C] eqstat._eqstat_forced (no-NRT) <eos>
    |-- [C] eqstat._eqstat_k (no-NRT) <eos> (a chain of 41: it calls the installed EOS.point; see `eos`)
    |-- [C] hra._hra_nb (no-NRT) <atmosphere>
    |-- [C] qenv._getopac_c (no-NRT) <atmosphere>
    |   `-- [C] pyrec_oop/opacity.Opacity.point (inline, no-NRT) <opacity> (a chain of 22; see `opacity`)
    `-- [C] qenv._opac_ok (no-NRT) <atmosphere>
`-- [C] qenv._qenv_k (no-NRT) <atmosphere>
    |-- [C] eqstat._eqstat_forced (no-NRT) <eos>
    |-- [C] eqstat._eqstat_k (no-NRT) <eos> (a chain of 41: it calls the installed EOS.point; see `eos`)
    |-- [C] pyrec_oop/convection.Convection.point (inline, no-NRT) <convection> (a chain of 4; see `convection`)
    |-- [C] qenv._getopac_c (no-NRT) <atmosphere>
    |   `-- [C] pyrec_oop/opacity.Opacity.point (inline, no-NRT) <opacity> (a chain of 22; see `opacity`)
    `-- [C] qenv._opac_ok (no-NRT) <atmosphere>
```

### `network`

```text
[C] pyrec_oop/network.py:Network
|-- [C] pyrec_oop/network.Network.point (inline, no-NRT) <network>
|   `-- [C] engeb._engeb_nb (no-NRT) <network>
|       |-- [C] engeb._engeb_comp_sums_nb (inline) <network>
|       |-- [C] engeb._engeb_fprf_nb (inline) <network>
|       |-- [C] engeb._engeb_r1_nb (inline) <network>
|       `-- [C] engeb._engeb_screen_nb (inline) <network>
`-- [C] pyrec_oop/network.Network.serves (inline, no-NRT) <network>
```

### `convection`

```text
[C] pyrec_oop/convection.py:Convection
`-- [C] pyrec_oop/convection.Convection.point (inline, no-NRT) <convection>
    `-- [C] tpgrad._tpgrad_nb (no-NRT) <convection>
        |-- [C] tpgrad._tpgrad_cubic_nb (no-NRT) <convection>
        `-- [C] tpgrad._tpgrad_derivs_nb (no-NRT) <convection>
```

## How the trees are made

A generator, `compiled_tree.py`, reads the code without importing or running it (Python's `ast`) and writes the trees as Markdown and JSON in about 2 s:

- **Kernels** are found by their Numba decorator, by an assignment that compiles a function, or as a compiled static method of a class; a kernel's calls are the names in its body that resolve, through the module's imports, to other kernels.
- **The object-oriented version's hook** is read from pyrec's `families.py`: the chain modules and their kernels (`CHAINS`), the globals bound to a family's static method (`KERNELS`), and each family's default class. In the chain modules each global is resolved to the default's static method, as the generated chains bind it, and `families.chains().NAME` to the chain's kernel `NAME`.
- **Calls through the installed families** (`families.eqstat`, `families.atmosphere().atmosphere_plain`, …) are resolved to what the default class's attribute reaches, read from its code: a function bound to the attribute, in the class or in `__init__`, or what a plain method's body calls.
- **Families** come from each Fortran routine's file (the overview's table, and the rest of the run's files placed by hand); a compiled static method belongs to its class's family.
- **The run** is YREC's 1 M☉ ZAMS case: the routines it reaches and their time from gprof, and pyrec's profile for the Python's own time.
- **What falls back** is found by marking the family's static methods plain and following every kernel that reaches them.

It is rerun whenever a family, a chain, or the hook changes.

**Its limits.** It follows calls by name: calls through a family's instance (`self.network.burn(...)`, the stage methods), through dictionaries, or through function arguments are not followed, so the stages reach pyrec's routines from the routines each stage's defaults wrap (each default's `WRAPS` table); calls through `families.py`'s accessors are followed. A test that combines the Numba switch with another condition keeps both branches, so the tree shows what can run, not how often. gprof's time cannot be split by caller, so the stages carry no times. The crossings' counts are each routine's calls in the Fortran run from all its callers, an upper bound.
