## Explanation

**Purpose.** Decides when to write a model for pulsation calculations: it "calculates the distance the star has travelled in the HR diagram; if far enough, output pulsation model." When the accumulated distance passes a threshold, it opens three new output files named after the run and the model number, and sets `LPULSE` so that the output routines write the model to them.

**How it fits.**
- **Inputs:** the previous point (`POL1` $=\log L$, `POT1` $=\log T_\mathrm{eff}$, `POA1` = age) and the running total `POLEN`; the current `BL` ($\log L/L_\odot$), `TEFFL`, `MODELN`, the run index `NK` and the age `DAGE` (arguments); the weights `POA`, `POB`, `POC` and the threshold `POMAX` in [[nmlpar_mod.f#NMLPAR_MOD|NMLPAR_MOD]] (namelist `CONTROL`, read by [[parmin.f#PARMIN|PARMIN]]); the base file names `FPMOD`, `FPENV`, `FPATM` (arguments, since MHP 8/25).
- **Who calls it:** the main program in [[main.f|main.f]], after each model when `LPOUT` is set.
- **Outputs:** `POLEN` and the previous point updated; `LPULSE` in `NMLPAR_MOD`; the units `IOPMOD`, `IOPENV`, `IOPATM` (from [[iounits_mod.f#IOUNITS_MOD|IOUNITS_MOD]]) opened as `<FPMOD>NN_MMMM` and so on, with `NN` = `NK` (the main program's loop over runs, `DO 200 NK = 1, NUMRUN`) and `MMMM` the model number; a line to `IOWR` and `ISHORT`. While `LPULSE` is true, [[wrtmod.f#WRTMOD|WRTMOD]] writes the model to `IOPMOD` and passes `LPULPT` on to [[envint.f#ENVINT|ENVINT]], which writes the atmosphere and envelope to `IOPATM` and `IOPENV` from the points [[qatm.f#QATM|QATM]] and [[qenv.f#QENV|QENV]] store.

    > **Question** ([[#L94]]; [[#L103]]; [[#L112]]). **`STATUS='NEW'`.** The files are opened as new, so rerunning a model sequence in the same directory stops at the first existing pulsation file. Is the stop meant to protect earlier pulsation files, or should they be opened with `STATUS='UNKNOWN'` (and rewound), as PARMIN opens the other outputs?


**The method.** The squared step in the HR diagram and in age, with weights $a, b, c$, is accumulated:
$$\ell^2 \mathrel{+}= (a\,\Delta\log L)^2 + (b\,\Delta\log T_\mathrm{eff})^2 + (c\,\Delta t)^2 .$$
When $\ell^2 \ge$ `POMAX`, the files are opened and $\ell^2$ is reset to zero; otherwise the three units are closed and `LPULSE` is set false.

**`POMAX` bounds a squared distance.** `POLEN` adds the squares of the weighted steps, $(\mathtt{POA}\,\Delta\log L)^2 + (\mathtt{POB}\,\Delta\log T_\mathrm{eff})^2 + (\mathtt{POC}\,\Delta\mathrm{age})^2$ ([[#L76-L79]]; printed as "LEN SQ"), and is compared with `POMAX` ([[#L83]]), so the default `POMAX` = 0.1 means a distance of about 0.32. YREC's documentation describes none of `POMAX`, `POA`, `POB`, and `POC`; it could say that the threshold is a squared distance.

**From YREC's documentation.** [Control Options](https://yrec.readthedocs.io/en/latest/namelist_control.html) (Output): `LPULSE` writes pulsation output, to `FPMOD` (the interior), `FPENV` (the envelope) and `FPATM` (the atmosphere), and needs `LSTATM` and `LSTENV` for the outer two; `IPVER` chooses its format.

**Changed since `rp_1`.** `NK` and `DAGE` are now arguments (from `/ZRAMP/` and `/THEAGE/` before; main.f is the only caller); the other COMMON blocks to modules, `IMPLICIT NONE`; the unused `/PULSE/` members and dead `/LUNUM/` units dropped.

## Bugs, by priority

1. **(not reached)** **Two different lines under the same labels.** ([[#L119-L122]]) The same format writes the step's differences (`TM1`–`TM3`) to `IOWR` but their weighted squares (`TMP1`–`TMP3`) to `ISHORT`, under the same labels "D L," "D Te," "D AGE," so the two files disagree and the `ISHORT` line is mislabeled. Only with `LPOUT` (off by default).

    **A possible fix:** a choice for the developers: write the same quantities to both units, or give the weighted squares their own labels.

    **Checked by running YREC** (Nov 9, 2026; a line added at each suspected path counted how often it was taken, the outputs otherwise unchanged): Not reached in any of 34 runs: 26 of YREC's cases, from a 0.04 $M_\odot$ brown dwarf and the solar models to 9 $M_\odot$, rotation, and helium burning, and 8 made-up ones. PDIST runs only with `LPOUT` on; its default is false, no case sets it, and no document offers it. `LPOUT` is in the namelist group that PARMIN reads ([[parmin.f#L355]]), so any case with it on reaches this line at every model. The fix (measurement only: the differences written to `ISHORT` as well) was not run. Intent: none found.
