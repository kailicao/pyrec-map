# The pilot: opacity

*Part of [A new design for YREC](overview.md). The opacity was the first family built: Its default wraps the Fortran-tracking pyrec's opacity routines, and the run's output stayed byte-identical with theirs. This page shows the family's code beside the code it wraps.*

**What it wraps:** [getopac.f](../../yrec-map/notes/getopac.f.md) and the routines it calls, [getopal95.f](../../yrec-map/notes/getopal95.f.md), [getalex06.f](../../yrec-map/notes/getalex06.f.md), [gtpurz.f](../../yrec-map/notes/gtpurz.f.md), and [condopacpint.f](../../yrec-map/notes/condopacpint.f.md) (each page shows the Fortran beside the Fortran-tracking pyrec). Its interface: [The families](families.md).

## The family's code

The base class, `OpacityBase`, fixes the interface: a static method `point` over one point, in $`\log\rho`$ and $`\log T`$ (YREC's `DL` and `TL`), returning $`\kappa`$, $`\log\kappa`$, its two logarithmic derivatives, and a status; `kernel_args()` and `kernel_args_out()` (the kernel's data read in, and the saved guesses written back); `serves(log_temperature, x, z)` (whether `point` covers the points at that $`T`$, X, and Z, at any density); `plain(...)` (the family's own code for the rest). `__call__` evaluates arrays without a model.

The default, `Opacity`, is YREC's: the molecular tables of Ferguson et al. 2005 (YREC's ALEX06 tables) below `TMOLMAX` ($`\log T`$ = 4.1 by default), OPAL 1995 above `TMOLMIN` (4.0), a linear ramp in $`\log T`$ between, then Potekhin's conductive opacity (or the Hubbard-Lampe fit) added as $`1/\kappa = 1/\kappa_\mathrm{rad} + 1/\kappa_\mathrm{cond}`$.

```python
class Opacity(OpacityBase):
    def __init__(self):
        self._ga = np.zeros(2, dtype=np.int64)       # alot06_mod's IT, ID
        self._guess = np.zeros(3, dtype=np.int64)    # condopacp's IZ, IT, IR

    @staticmethod
    @accel.njit(inline="always", _nrt=False)
    def point(log_density, log_temperature, x, z, fxion, data):
        d = data
        return _getopac_nb(log_density, log_temperature, x, z, fxion, d.tmolmin, d.tmolmax, d.lcondopacp,
                           d.capalex06, ..., d.guess)

    def kernel_args(self):
        return _getopac.data_in(self._ga, self._guess)

    def kernel_args_out(self, data) -> None:
        _getopac.data_out(data)

    def serves(self, log_temperature, x, z) -> bool:
        return _getopac.fast_path(0.0, log_temperature, x, z)

    def plain(self, log_density, log_temperature, x, z, fxion):
        return _getopac.getopac(float(log_density), float(log_temperature), float(x), float(z), 0.0, 0.0, 0.0, 0.0,
                                fxion)
```

Its names beside YREC's: [The families' names](names.md).

## Beside the Fortran-tracking pyrec

| The family | What it is in the Fortran-tracking pyrec |
| --- | --- |
| `Opacity.point` | getopac's kernel, `_getopac_nb`, unchanged, called on the family's data |
| `kernel_args()` | `getopac.data_in`: the kernel's 33 arguments after ($`\log\rho`$, $`\log T`$, X, Z, the ionization) as one named tuple, `getopac.OpacityData`, read from pyrec's modules |
| `kernel_args_out()` | `getopac.data_out`: the saved guesses written back to pyrec's modules |
| `serves` | `getopac.fast_path`: the paths the kernel covers in the solar run |
| `plain` | pyrec's `getopac` itself: the other paths (a new X or Z for the molecular table, the helium-burning blend, condopacp's first call) |

The chains that reach the opacity (the solver's loop over the shells; the envelope's integrands) call it as `opacity_point(dl, tl, x, z, fxion, data)`, a module global. In the Fortran-tracking pyrec it is bound to `getopac._getopac_point`, a short adapter onto the same unchanged kernel; in the object-oriented version it is bound to `Opacity.point` in generated copies of the chains ([Writing a Numba family](numba.md)). So the two versions' chains are the same source and differ only in the binding.

## Evaluated without a model

`Opacity()(log_density, log_temperature, x, z)` evaluates arrays of points: a compiled loop generated for the family's kernel, the points `serves` rejects or the kernel stops on handed to `plain`, and NaN where neither serves. On a grid of 91 values of $`\log T`$ (3.5–8.0) by 141 of $`\log\rho`$ (−12 to 2), 12,831 points, at the ZAMS surface's X = 0.7195962833311453 and Z = 0.01649314, fully ionized, `point` served every point and no value was NaN; $`\log\kappa`$ ranged from −5.59 to 5.46.

| Evaluation (12,831 points) | Per call | Per point |
| --- | --- | --- |
| the compiled family | 15.7 ms | 1.2 µs |
| a plain-Python subclass (`point = Opacity.point.py_func`), with its warning | 59 ms | 4.6 µs |
| pyrec's `getopac` called point by point | 100 ms | 7.8 µs |

The three gave the same bits on the whole grid. The plain subclass is only about 4 times slower here because its Python `point` still calls getopac's compiled kernel; an opacity written wholly in Python would be much slower.

## Bit for bit

Every whole run of the 1 M☉ ZAMS case with the opacity family's kernel bound into the generated chains wrote output byte-identical to YREC's, and so did a run with pyrec's own binding. The warm runs with the family took as long as the unmodified pyrec, within the machine's noise (15.6–16.9 s against 14.4–18.2 s, the two Python versions interleaved on a shared machine; not a comparison with the Fortran). The same holds now that every family is wrapped and the `Model` drives each step ([State](state.md), the copy test).

## The compiled chain

The opacity's static method and what it calls, from [the generated tree](tree.md) (shortened):

```text
[C] pyrec_oop/opacity.py:Opacity (the family's default class: its compiled static methods)
`-- [C] pyrec_oop/opacity.Opacity.point (inline, no-NRT) <opacity>
    `-- [C] getopac._getopac_nb (no-NRT) <opacity>
        |-- [C] condopacpint._condopacpint_nb (no-NRT) <opacity>
        |   |-- [C] condopacp._condopacp_nb (no-NRT) <opacity>
        |   `-- [C] condopacpint._condopacpint_weights_nb (no-NRT) <opacity>
        |-- [C] getalex06._getalex06_nb (no-NRT) <opacity>
        |-- [C] getopac._getopac_add_conductive_nb (no-NRT) <opacity>
        |-- [C] getopac._getopac_hubbard_lampe_nb (no-NRT) <opacity>
        |-- [C] getopac._getopac_ramp_nb (no-NRT) <opacity>
        `-- [C] getopal95._getopal95_nb (no-NRT) <opacity>
```

It is called by `qenv._getopac_c` (the envelope's integrands) and by `coefft._coefft_nb` (the solver's loop). Were the opacity a plain-Python family, 11 kernels would run as Python: `Opacity.point`, the solver's loop, and nine of the envelope's (its two integration loops and the kernels between them and the opacity). A plain subclass of the default would still enter getopac's compiled kernel from Python at every point ([The compiled tree](tree.md)).
