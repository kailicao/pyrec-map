## Explanation

**Purpose.** Decides when to write a model for pulsation calculations: it "calculates the distance the star has travelled in the HR diagram; if far enough, output pulsation model". When the accumulated distance passes a threshold, it opens three new output files named after the run and the model number, and sets `LPULSE` so that the output routines write the model to them.

**How it fits.**
- **Inputs:** the previous point (`POL1` $=\log L$, `POT1` $=\log T_\mathrm{eff}$, `POA1` = age) and the running total `POLEN`; the current `BL` ($\log L/L_\odot$), `TEFFL`, `MODELN`; the age `DAGE` in `/THEAGE/`; the weights `POA`, `POB`, `POC` and the threshold `POMAX` in `/PO/` (namelist `CONTROL`, read by [[parmin.f#PARMIN|PARMIN]]); the base file names `FPMOD`, `FPENV`, `FPATM` (arguments, since MHP 8/25).
- **Who calls it:** the main program in [[main.f|main.f]], after each model when `LPOUT` is set.
- **Outputs:** `POLEN` and the previous point updated; `LPULSE` in `/PULSE/`; the units `IOPMOD`, `IOPENV`, `IOPATM` (from `/LUNUM/`) opened as `<FPMOD>NN_MMMM` and so on, with `NN` = `NK` (from `/ZRAMP/`; the main program's loop over runs, `DO 200 NK = 1, NUMRUN`) and `MMMM` the model number; a line to `IOWR` and `ISHORT`. While `LPULSE` is true, [[wrtmod.f#WRTMOD|WRTMOD]] writes the model to `IOPMOD` and passes `LPULPT` on to [[envint.f#ENVINT|ENVINT]], which writes the atmosphere and envelope to `IOPATM` and `IOPENV` from the points [[qatm.f#QATM|QATM]] and [[qenv.f#QENV|QENV]] store.

**The method.** The squared step in the HR diagram and in age, with weights $a, b, c$, is accumulated:
$$\ell^2 \mathrel{+}= (a\,\Delta\log L)^2 + (b\,\Delta\log T_\mathrm{eff})^2 + (c\,\Delta t)^2 .$$
When $\ell^2 \ge$ `POMAX`, the files are opened and $\ell^2$ is reset to zero; otherwise the three units are closed and `LPULSE` is set false.

## Questions for the experts

1. **`POMAX` is a squared distance.** The sum is of squares (printed as "LEN SQ"), so `POMAX` = 0.1 means a distance of about 0.32. Is the namelist documentation clear about this?
2. **Two different lines.** The same format writes the step's differences (`TM1`–`TM3`) to `IOWR` but their weighted squares (`TMP1`–`TMP3`) to `ISHORT`, under the same labels "D L", "D Te", "D AGE".
3. **`STATUS='NEW'`.** The files are opened as new, so rerunning a model sequence in the same directory stops at the first existing pulsation file.
