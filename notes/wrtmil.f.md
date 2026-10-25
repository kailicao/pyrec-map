## Explanation

**Purpose.** `WRTMIL` writes one model's Milne (homology) invariants $U$ and $V$, with $W$ and the polytropic index $n + 1$, to the Milne output file, every `NPRTPT` shells and the last one.

**How it fits.**
- **Inputs:** the model (`HCOMP`, $\log\rho$, $L/L_\odot$, $\log P$, $\log r$, $m$ in grams `HS1`, `M`, `MODEL`), and through COMMON blocks the energy rates `SESUM` and `SEG` and the actual gradient `SDEL(2,·)` (`SCRTCH`), the surface composition and total mass (`COMP`), and `NPRTPT` (`CCOUT1`).
- **Who calls it:** [[putstore.f#PUTSTORE|PUTSTORE]] and [[wrtout.f#WRTOUT|WRTOUT]], when `LMILNE` is set and other conditions hold: PUTSTORE only when `LSTATM` or `LSTENV` is set, and WRTOUT only in its pulsation branch (`LPULSE` on a model that is not stored). So `LMILNE` alone writes nothing.
- **Output:** the unit `IMILNE` (21), opened by [[parmin.f#PARMIN|PARMIN]] in append mode.

**The method.** At each printed shell:
$$U = \frac{4\pi\rho r^3}{m},\qquad V = \frac{G m \rho}{P r},\qquad W = U\,\frac{m\,(\varepsilon_\mathrm{nuc} + \varepsilon_7)}{L},\qquad n + 1 = \frac{1}{\nabla},$$
where $\varepsilon_\mathrm{nuc}$ is `SESUM` and $\varepsilon_7$ is `SEG(7,·)` (the gravitational energy rate, by the column names [[stitch.f|stitch.f]] gives), and $\nabla$ = `SDEL(2,·)`, the actual gradient.

## Questions for the experts

1. **The file is closed after each model.** `WRTMIL` ends with `CLOSE(IMILNE)`, but the file is opened only once, in `PARMIN` (MHP 8/25). The next call writes to unit 21 unopened, which most compilers send to a default file such as `fort.21`. Should the `CLOSE` go?
2. **$W$ includes the gravitational term.** $W$ uses $\varepsilon_\mathrm{nuc} + \varepsilon_7$; is the gravitational energy meant to be in it?
3. **Hard-coded unit.** `IMILNE = 21` is fixed in `PARMIN`.
4. **`LMILNE` alone writes nothing.** The calls also need `LSTATM` or `LSTENV` (PUTSTORE), or `LPULSE` on a model that is not stored (WRTOUT). Is the Milne output meant to depend on those switches?

### WRTMIL

Milne invariants $U$, $V$, with $W$ and $n+1 = 1/\nabla$, for selected shells of one model.
