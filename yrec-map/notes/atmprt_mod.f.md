## Explanation

**Purpose.** `ATMPRT_MOD` holds the state at the last point of the atmosphere integration (or the fitting point of a tabulated atmosphere), for the envelope integration and the output. It replaces `COMMON/ATMPRT/` (MHP via Claude, 10/14/26), where the optical depth was named `TAU`; it is now `TAUL`.

**What its variables hold, who sets them, who reads them.**
- `TAUL` ($`\log\tau`$), `AP` ($`\log P`$), `AT` ($`\log T`$): set by [`QATM`](https://github.com/yreclab/yrec/blob/7be4133/src/qatm.f#L6-L125) at each point of the atmosphere integration; `AP` and `AT` also by the table routines [`SURFP`](surfp.f.md#surfp), [`KCSURFP`](kcsurfp.f.md#kcsurfp), and [`ALSURFP`](alsurfp.f.md#alsurfp).
- `AD` ($`\log\rho`$), `AO` (the opacity), `AFXION(3)` (the ionization fractions): set by `QATM` only when the model is stored or written for pulsation (`LSAVE`, `LPUMOD`).
- Read by [`ENVINT`](envint.f.md#envint), which writes them with the stored model, and by [`MASSLOSS`](massloss.f.md#massloss) (`AP`, `AT`) and the table routines.

**Changed since `rp_1`.** New file: `COMMON/ATMPRT/` as a module, `TAU` renamed `TAUL`.
