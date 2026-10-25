# Input, output and analysis

*In Python: [[new/pyrec/io/__init__.py|`pyrec.io`]].*

## 3.14 Input, output and analysis

**Model files.** `ModelFile` is the base; each format is a subclass with `read(star, ierr)` and `write(star, cfg, ierr)`, so that `STARIN` and the writers no longer branch on the format.

```fortran
type, abstract :: ModelFile
    character(len=:), allocatable :: path
contains
    procedure(read_if), deferred :: read      !! (star, ierr)
    procedure(write_if), deferred :: write    !! (star, cfg, ierr)
end type
type, extends(ModelFile) :: Model2File   !! GETMODEL2, PUTMODEL2, WRTLST
type, extends(ModelFile) :: Yrec7File    !! GETYREC7, PUTYREC7 (read only?)
type, extends(ModelFile) :: StoreFile    !! PUTSTORE; stitched: STITCH
```

**Writers.** `Logger` owns the `.short` file and the levels of its messages ([Section 6.2](fortran.md)), and `ShortWriter` writes each model's block in it; `TrackWriter` writes the track and the per-model summary ([[wrthead.f#WRTHEAD|`WRTHEAD`]], [[wrtout.f#WRTOUT|`WRTOUT`]], [[pindex.f#PINDEX|`PINDEX`]]); `PulsationWriter` decides when and writes the pulsation models ([[pdist.f#PDIST|`PDIST`]], [[wrtmod.f#WRTMOD|`WRTMOD`]]). **Analyses** read a model and never change it: `AcousticAnal` ([[calcad.f#CALCAD|`CALCAD`]], acoustic depths $t = \int dr/c_s$), `MilneAnal` ([[wrtmil.f#WRTMIL|`WRTMIL`]], the homology invariants $U$, $V$), `OverturnAnal` ([[gettau.f#GETTAU|`GETTAU`]], [[tauint.f#TAUINT|`TAUINT`]], [[tauintnew.f#TAUINTNEW|`TAUINTNEW`]], [[taucal.f#TAUCAL|`TAUCAL`]], the convective overturn time $\tau_\mathrm{cz}$ that the wind and the output need).

**Replaces:** [[getmodel2.f#GETMODEL2|`GETMODEL2`]], [[getyrec7.f#GETYREC7|`GETYREC7`]], [[putmodel2.f#PUTMODEL2|`PUTMODEL2`]], [[putyrec7.f|`PUTYREC7`]] (never called), [[wrtlst.f#WRTLST|`WRTLST`]], [[putstore.f#PUTSTORE|`PUTSTORE`]], [[stitch.f#STITCH|`STITCH`]], and the writers and analyses named above. `PUTSTORE`, "mostly a clone of wrtlst.f and putmodel2.f", becomes `StoreFile%write` calling the shared `Model2File` code for the model part. The small helpers [[alfilein.f#SORT_SHELL|`SORT_SHELL`]], [[condopacp.f#CINTERP3|`CINTERP3`]], [[condopacp.f#HUNT|`HUNT`]], [[liburn.f#SAFEDIVEXP|`SAFEDIVEXP`]], [[slopes.f#SAFEDIVIDE|`SAFEDIVIDE`]] and [[nulosses.f#AZBAR|`AZBAR`]] move to `numerics` or stay private to their type.
