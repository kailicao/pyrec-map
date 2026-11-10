## Explanation

**Purpose.** `WRTMIL` writes one model's Milne (homology) invariants $U$ and $V$, with $W$ and the polytropic index $n + 1$, to the Milne output file, every `NPRTPT` shells and the last one.

**How it fits.**
- **Inputs:** the model (`HCOMP`, $\log\rho$, $L/L_\odot$, $\log P$, $\log r$, $m$ in grams `HS1`, `M`, `MODEL`), and through modules the energy rates `SESUM` and `SEG` and the actual gradient `SDEL(2,·)` (`SCRTCH_MOD`), the surface composition and total mass (`COMP_MOD`), `NPRTPT` (`NMLPAR_MOD`), the constants (`CONSTANTS_MOD`) and the unit `IMILNE` (`IOUNITS_MOD`).
- **Who calls it:** [[putstore.f#PUTSTORE|PUTSTORE]] and [[wrtout.f#WRTOUT|WRTOUT]], when `LMILNE` is set and other conditions hold: PUTSTORE only when `LSTATM` or `LSTENV` is set, and WRTOUT only in its pulsation branch (`LPULSE` on a model that is not stored). So `LMILNE` alone writes nothing.

    > **Question** ([[putstore.f#L342-L343]]; [[wrtout.f#L683-L684]]). **`LMILNE` alone writes nothing.** The calls also need `LSTATM` or `LSTENV` (PUTSTORE), or `LPULSE` on a model that is not stored (WRTOUT). Is the Milne output meant to depend on those switches?

- **Output:** the unit `IMILNE` (21, fixed in PARMIN, [[parmin.f#L674]]), opened by [[parmin.f#PARMIN|PARMIN]] in append mode ([[parmin.f#L956-L959]]).

**The method.** At each printed shell:
$$U = \frac{4\pi\rho r^3}{m},\qquad V = \frac{G m \rho}{P r},\qquad W = U\,\frac{m\,(\epsilon_\mathrm{nuc} + \epsilon_7)}{L},\qquad n + 1 = \frac{1}{\nabla},$$
where $\epsilon_\mathrm{nuc}$ is `SESUM` and $\epsilon_7$ is `SEG(7,·)` (the gravitational energy rate, by the column names [[stitch.f|stitch.f]] gives), and $\nabla$ = `SDEL(2,·)`, the actual gradient.

> **Question** ([[#L76]]). **$W$ includes the gravitational term.** $W$ uses $\epsilon_\mathrm{nuc} + \epsilon_7$; is the gravitational energy meant to be in it?

**Changed since `rp_1`.** Declarations only: COMMON blocks to modules (`/SCRTCH/`, `/COMP/`, `/CCOUT1/` to `NMLPAR_MOD`, `/LUOUT/` to `IOUNITS_MOD`, the constants to `CONSTANTS_MOD`), `IMPLICIT NONE`.

## Bugs, by priority

1. **(not reached)** **The file is closed after each model.** ([[#L109]]; [[parmin.f#L956-L959]]) `WRTMIL` ends with `CLOSE(IMILNE)`, but the file is opened only once, in `PARMIN` (MHP 8/25, [[#L36]]). The next call writes to unit 21 unopened, which gfortran, like most compilers, sends to a default file (`fort.21`), so the Milne file holds only the first model written. Only with `LMILNE` (off by default).

    **A possible fix:**

    ```diff
    --- a/src/wrtmil.f
    +++ b/src/wrtmil.f
    @@ -105,7 +105,9 @@
            NP1 = 1.0D0/SDEL(2,M)
            WRITE(IMILNE,10)M,HS1(M),R,P,D,HCOMP(1,M),HL(M),
          *                   U,V,W,NP1
    +C 11/09/26 KC via Claude
    +C code changed to keep IMILNE open, since PARMIN opens it only once
    +C for the run.
           ENDIF
    -      CLOSE(IMILNE)
           RETURN
           END
    ```

    **Checked by running YREC** (Nov 9, 2026; a line added at each suspected path counted how often it was taken, the outputs otherwise unchanged): not reached in any of 34 runs (26 of YREC's cases, from a 0.04 $M_\odot$ brown dwarf and the solar models to 9 $M_\odot$, rotation, and helium burning, and 8 made-up ones): `LMILNE` is off by default ([[nmlpar_mod.f#L58]]) and set in none of YREC's cases or documents. Not run: `LMILNE` on, with two or more models written. Intent: The comment at [[#L36]] says the file is now opened in PARMIN, so the `CLOSE` looks left over from when WRTMIL opened the file itself.

### WRTMIL

Milne invariants $U$, $V$, with $W$ and $n+1 = 1/\nabla$, for selected shells of one model.
