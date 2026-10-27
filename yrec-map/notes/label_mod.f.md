## Explanation

**Purpose.** `LABEL_MOD` holds the envelope's $X$ and $Z$ of the current run, used to label the output, shared by 6 routines. It replaces `COMMON/LABEL/` (MHP via Claude, 10/14/26).

**What its variables hold, who sets them, who reads them.**
- `XENV0`, `ZENV0` (`REAL*8`): set by the [[main.f#(file level)|main program]] at the start of each run `NK` from the namelist arrays `XENV0A(NK)`, `ZENV0A(NK)`, and by [[rscale.f#RSCALE|`RSCALE`]] when the run rescales the composition (`RESCAL(2,NK)`, `RESCAL(3,NK)`; RSCALE then also sets `ZENV` from `ZENV0`, "DBG 4/95 bug fix"). Written in the headers of the output by [[wrthead.f#WRTHEAD|`WRTHEAD`]], [[wrtmod.f#WRTMOD|`WRTMOD`]] and [[wrtout.f#WRTOUT|`WRTOUT`]].
- Initial values 0.7D0 and 0.02D0, moved from PARMIN's `DATA XENV0, ZENV0/0.7,0.02/`; they are overwritten before any use.

**Design.** A blanket `USE LABEL_MOD`; [[parmin.f#PARMIN|`PARMIN`]] still uses the module, though it no longer reads or writes either member (at `rp_1` it wrote them to the `.short` file). The module header says its literals are copied verbatim, but the `DATA` statement's single-precision `0.7` and `0.02` became `0.7D0` and `0.02D0`; harmless, since the defaults are never used, and the two are in no namelist, unlike what the header says.

**Changed since `rp_1`.** New file: `COMMON/LABEL/` as a module, with its defaults moved from PARMIN (now in double precision); PARMIN no longer writes them.
