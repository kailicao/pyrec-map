# Made-up cases for checking suspected bugs

The namelist pairs (`.nml1` and `.nml2`) used to check this site's suspected bugs by running YREC 7be4133 where none of YREC's own cases reaches them (Nov 9–10, 2026); the bugs, what the runs showed, and every case are on [the bug page](../index.html). Each pair has a page beside it (`<pair>.html`, made by `scripts/namelist_viewer.py`) showing its two files with the settings that differ from its YREC case marked.

**A made-up case is defensible** when it starts from one of YREC's own cases, changes as few settings as possible, takes each changed value from YREC's documentation, another of its cases, or a table's README, and says at the head of its `.nml1` (and `.nml2`) which star it represents, what was changed and why, and which bugs it reaches. Where no defensible case reaches a bug, the bug's write-up says so.

**Running one:** as the YREC case it starts from, with `YREC_INPUT`, `YREC_START`, and `YREC_OUTPUT` set to YREC's `input/`, `startmodels/`, and an output folder. YREC's file names hold 256 characters, and a longer output path silently truncates them.

- `castelli-kttau5`: [`setups.f` bug 1](../../yrec-map/setups.f.html#b1), [`kcsurfp.f` bug 1](../../yrec-map/kcsurfp.f.html#b1), [`putstore.f` bug 2](../../yrec-map/putstore.f.html#b2); the Kurucz solar model with `KTTAU` = 5 and a Castelli-Kurucz table, as that folder's README asks.
- `custom-mix`: [`parmin.f` bug 2](../../yrec-map/parmin.f.html#b2); the AAG21 solar model with its own commented custom-mixture block switched on.
- `fcore-default`: [`starin.f` bug 4](../../yrec-map/starin.f.html#b4); the Kurucz solar model with `FCORE` at the code's default.
- `getfc-1`: [`getfc.f` bug 1](../../yrec-map/getfc.f.html#b1); the 2 M☉ rotating main-sequence case with `LVFC` on, a documented option that YREC's own namelists call "Not recommended."
- `getopal95-2`: [`getopal95.f` bug 2](../../yrec-map/getopal95.f.html#b2); the 1 M☉ helium-burning case with the AAG21 opacity table.
- `lstch-off`: [`envint.f` bug 2](../../yrec-map/envint.f.html#b2); `LSTCH` at its default (off) with `LSTATM` on.
- `numderiv`: [`eqstat.f` bug 1](../../yrec-map/eqstat.f.html#b1); `LNumDeriv` on, as the documentation offers.
- `reimers-rgb`, `reimers-3msun`: Reimers mass loss switched on, as the cases' own comment offers, for 1 M☉ up the giant branch ([`massloss.f` bug 1](../../yrec-map/massloss.f.html#b1), [`mdot.f` bug 2](../../yrec-map/mdot.f.html#b2), [`htimer.f` bug 1](../../yrec-map/htimer.f.html#b1)) and 3 M☉ on the main sequence ([`massloss.f` bug 1](../../yrec-map/massloss.f.html#b1), [`mdot.f` bug 2](../../yrec-map/mdot.f.html#b2), [`dburn.f` bug 1](../../yrec-map/dburn.f.html#b1)).

No made-up case was built for [`getopal95.f` bug 1](../../yrec-map/getopal95.f.html#b1): It needs a cool hydrogen-poor surface, which none of YREC's cases or documents use, and which YREC cannot build faithfully from the models it ships.
