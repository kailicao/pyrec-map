## Explanation

**Purpose.** `IOUNITS_MOD` holds the Fortran logical unit numbers of every input and output file, shared by 57 routines. It replaces `COMMON/IOUNITS/` (MHP via Claude, 10/14/26), which had gathered, on 9/25/26, the unit numbers once scattered over `COMMON/LUOUT/`, `/LUNUM/`, `/ALEX06/`, `/ACDPTH/`, `/NEWOPAC/`, `/LOPAL95/`, `/ATMOS2/`, `/ALATM03/`, `/OPALEOS/` and `/SCV2/` (the dead `IDYN`, `ILLDAT`, `ISCOMP`, `IKUR` of `/LUNUM/` removed). All members are `INTEGER*4`.

**What its variables hold, who sets them, who reads them.** [[parmin.f#PARMIN|`PARMIN`]] assigns every number (its comments name the files; they can be changed only in the code) and opens most of the files; the routines that read or write a file use its unit.
- Run control: `IOWR` = 6 (the status output, the screen; the [[main.f#(file level)|main program]] sets it to 9 before calling PARMIN, which overwrites it), `ISTAND` = 14 and `IRUN` = 13 (the `CONTROL` and `PHYSICS` namelists, read by PARMIN).
- Models: `IFIRST` = 12 (the starting model), `ILAST` = 11 (the last model), `ISTOR` = 23 (saved models).
- Outputs: `ISHORT` = 20 (all diagnostic information, the `.short` file), `ITRACK` = 19 (the track), `IDEBUG` = 18 (debugging), `IMILNE` = 21 (Milne's invariant variables, written by [[wrtmil.f#WRTMIL|`WRTMIL`]]), `IMODPT` = 22 (shell-by-shell output), `ISNU` = 33 (neutrino fluxes), `ISOUND` = 500 (the sound-speed profile, written by [[wrtmod.f#WRTMOD|`WRTMOD`]] with `LSOUND`), `IOPMOD`, `IOPENV`, `IOPATM` = 24, 25, 26 (interior, envelope and atmosphere for a pulsation code, also opened by [[pdist.f#PDIST|`PDIST`]]), `ICLCD` = 91 (the acoustic-depth output, assigned only with `LACOUT`).
- Input tables: `IFERMI` = 15 (Fermi–Dirac tables, read by [[setups.f#SETUPS|`SETUPS`]]), `IOATM` = 38 (Kurucz atmospheres, SETUPS), `IOATMA` = 66 (Allard atmospheres, [[alfilein.f#ALFILEIN|`ALFILEIN`]]), `ILIV95` = 48 (OPAL95 opacities, [[ll95tbl.f#LL95TBL|`LL95TBL`]]), `IALEX06` = 90 (Alexander 2006 opacities, [[readalex06.f#READALEX06|`READALEX06`]]), `IOPUREZ` = 62 (the pure-CN opacities, [[rdzlaol.f#RDZLAOL|`RDZLAOL`]]), `IcondOpacP` = 75 (Potekhin conductive opacities, [[condopacp.f#CONDOPACP|`CONDOPACP`]]), `IOPALE` = 49 (OPAL 2006 equation of state, [[readcoeos06.f#READCOEOS06|`READCOEOS06`]]), `ISCVH`, `ISCVHE`, `ISCVZ` = 72, 73, 74 (the SCV equation of state, SETUPS).
- `IJLAST`: the unit to which [[wrtout.f#WRTOUT|`WRTOUT`]] writes the model with `LJLAST` (acoustic-depth output), but assigned nowhere; the branch never runs, since `LACOUT` cannot be turned on (see [[acdpth_mod.f#ACDPTH_MOD|`ACDPTH_MOD`]]).

**Design.** A blanket `USE IOUNITS_MOD`. Unit numbers are fixed in PARMIN rather than allocated, so a new file must pick a free number by hand (ISOUND's 500 stands apart).

**Changed since `rp_1`.** New file: the unit numbers of ten COMMON blocks, and of `/IOUNITS/` into which they were merged, as one module; the dead units `IDYN`, `ILLDAT`, `ISCOMP`, `IKUR` (and PARMIN's unshared `ILSTBN`, `ISTOBN`, `IFSTBN`) removed.

## Questions for the experts

1. **A unit with no number.** `IJLAST` is used by WRTOUT's acoustic-depth branch but assigned nowhere, so the branch would write to unit 0 if it ever ran. Assign it in PARMIN with `ICLCD`, or remove it with the branch?
