# Suspected bugs

This page lists the suspected bugs in YREC (commit 7be4133) that running it showed to change a star's evolution, stop a run, or write wrong output: 23 and 15 of the 199 suspected bugs on this site. Each was first read from the code, one file at a time, and then checked by running YREC (Nov 9–10, 2026). A bug marked **Checked by KC** is one I (Kaili Cao, KC) have checked myself; the others are an AI's reading of the code and of the runs. Each links to its write-up on its file's page: the code, the reasoning, the full result, and, for most, a possible fix.

**How each was checked.** A line added at each suspected path counted how often it was taken, and how often the condition that makes it wrong actually held, with the outputs otherwise unchanged. This was done in 34 runs: 26 of YREC's own cases, one or more per kind of physics, from a 0.04 M☉ brown dwarf to 9 M☉, with rotation, diffusion, and helium burning, and 8 made-up cases; a ninth, for `getfc.f` bug 1, was run on Nov 10 (all nine at the end of this page). Most bugs whose condition held were then run with their possible fix alone, on one or two cases, and compared with the same case unfixed; where no fix was run, the write-up says why. Because YREC's iterations amplify any change, every comparison is judged against a **null change** on the same case: nearly every opacity (all with 3 ≤ log T ≤ 9 and −6 ≤ log ρ ≤ 9.75) multiplied by 1 + 10⁻¹⁰. A fix's effect counts as real only when it is clearly larger than that, about five times or more.

**What the runs showed**, for each bug below:

- **(changes results, large)**: The fix moves the track far beyond the null change.
- **(changes results, small)**: The fix's effect is clearly beyond the null change, but small.
- **(stops the run)**: A run stopped there.
- **(wrong output)**: The fix changes what is written, not the star.


## Bugs that change results or stop the run: 23

### Opacities

- **(changes results, large)** **Checked by KC** (Nov 10, 2026). **[`getopal95.f` bug 2](../yrec-map/getopal95.f.html#b2): Empty temperatures in the OP tables above $\log T = 8.0$.** In a made-up case, `examples/run_from_zahb_to_tahb/ZAHB_m1p0feh+0p0_TAHB` with `FLIV95` set to `op05/AAG2021zx0.0187.tab`, log L moves by up to 0.27 dex, against 1.4e-6 for the null change.
- **(changes results, large)** **Checked by KC** (Nov 10, 2026). **[`ll95tbl.f` bug 1](../yrec-map/ll95tbl.f.html#b1): The $X = 1 - Z$ tables at $Z$ = 0.06 and 0.08 overwrite the $X = 0$ tables at $Z$ = 0.08 and 0.10.** In `testsuite/Test_m0p95feh+0p0_GN93_TAHB`, the fix moves log L by up to 0.36 dex, against 1.7e-7 for the null change, and the track ends at 0.0943 Gyr instead of 0.1293.
- **(changes results, small)** **Checked by KC** (Nov 10, 2026). **[`condopacpint.f` bug 1](../yrec-map/condopacpint.f.html#b1): The mixture's derivatives are multiplied by $\log K$.** In `testsuite/Test_m0p3feh+0p0GS98_scv_ZAMS`, the fix moves log L by up to 1.4e-5 dex, against 1e-9 for the null change; on the rotating 3 M☉ giant the change is within the noise.
- **(changes results, small)** **Checked by KC** (Nov 10, 2026). **[`condopacpint.f` bug 2](../yrec-map/condopacpint.f.html#b2): The temperature derivative is taken from the density derivatives.** With this fix alone, `testsuite/Test_m0p3feh+0p0GS98_scv_ZAMS` moves log L by up to 5.0e-6 dex, against 1e-9 for the null change; on the rotating 3 M☉ giant the change is within the noise.
- **(changes results, small)** **Checked by KC** (Nov 10, 2026). **[`condopacpint.f` bug 3](../yrec-map/condopacpint.f.html#b3): A sign in the extrapolation below $\log\rho = -6$.** In `examples/run_from_dbl_to_zams/Test_m0040_feh0_noGS_ZAMS`, the fix moves log L by up to 2.4e-4 dex, against 2.5e-5 for the null change, and the end age shifts from 8,681 to 8,692 Gyr.

### Angular-momentum loss and mass loss

- **(changes results, large)** **Checked by KC** (Nov 10, 2026). **[`massloss.f` bug 1](../yrec-map/massloss.f.html#b1): The Reimers rate is in g/s, read as $M_\odot$/yr.** A made-up case: `testsuite/Test_m3p0feh+0p0GS98_std25_TAMS` with `LMDOT` and `LREIMER` on; unfixed, the 3 M☉ star falls to 0.11 M☉ and fails to converge, and with the fix it keeps its mass.
- **(stops the run)** **Checked by KC** (Nov 10, 2026). **[`mdot.f` bug 2](../yrec-map/mdot.f.html#b2): A stop without a message when there is no surface convection zone.** A made-up case: `testsuite/Test_m3p0feh+0p0GS98_std25_TAMS` with Reimers mass loss on and `massloss.f` bug 1 fixed ends here at model 129, at `STOP 911` with no message; the 1 M☉ giant-branch case does too, at model 6,599.

### Rotation: the structure of a rotating star

- **(changes results, large)** **Checked by KC** (Nov 10, 2026). **[`getqua.f` bug 1](../yrec-map/getqua.f.html#b1): A wrong index in $d\rho/dr$.** In `testsuite/Test_3Msolar_GS_rot_gray_OPALSCV_SF2_GS98_OP_CF10_RGp2diffrotI3cz2`, the fix moves log L by up to 0.42 dex, against 0.0076 for the null change, with 1,919 models instead of 1,853.

### The time step and rezoning

- **(changes results, large)** **Checked by KC** (Nov 10, 2026). **[`hpoint.f` bug 3](../yrec-map/hpoint.f.html#b3): `ALPHAE` taken as a depth in $\log_{10}P$.** In `examples/run_from_zahb_to_tahb/ZAHB_m0p8feh+0p0_TAHB`, an approximate version of the fix (`ALPHAE/CLN`) moves log L by up to 0.334 dex, against 2.0e-7 for the null change, and the run ends at 0.2356 Gyr instead of 0.2297.

### Input: namelists, tables, and the starting model

- **(stops the run)** **Checked by KC** (Nov 10, 2026). **[`starin.f` bug 4](../yrec-map/starin.f.html#b4): 0/0 with one core point.** A made-up case: `testsuite/Test_solarGS98_kurucz` with `FCORE` = 1.0 stops in its first second in TPGRAD, at `STOP 912`; with the fix, it runs to its end.
- **(changes results, small)** **Checked by KC** (Nov 10, 2026). **[`parmin.f` bug 2](../yrec-map/parmin.f.html#b2): `ISETMIX` = 2 and `ISETISO` = 2 do nothing.** A made-up case: `testsuite/Test_solarAAG21_dif` with `ISETMIX` = `ISETISO` = 2 and its custom mixture on; the fix moves log L by up to 0.0025 dex on the pre-main sequence, against 0.00023 for the null change.

### Nuclear reactions, energy generation, and neutrinos

- **(changes results, small)** **Checked by KC** (Nov 10, 2026). **[`engeb.f` bug 1](../yrec-map/engeb.f.html#b1): The Itoh branch replaces the temperature derivative by the density derivative.** In `testsuite/Test_m2p0_feh+0p0_vzams150_IES2_TAMS`, the fix moves log L by up to 1.83e-5 dex, against 1.58e-8 for the null change, with the same models and end age.
- **(changes results, small)** **Checked by KC** (Nov 10, 2026). **[`engeb.f` bug 2](../yrec-map/engeb.f.html#b2): Relative derivatives added to absolute ones in the Itoh branch.** With this fix alone, `testsuite/Test_m2p0_feh+0p0_vzams150_IES2_TAMS` moves log T_c by 3.5e-7 dex, against 1.72e-8 for the null change; in `IES1` the change is within the noise.
- **(changes results, small)** **Checked by KC** (Nov 10, 2026). **[`engeb.f` bug 3](../yrec-map/engeb.f.html#b3): The alpha captures' temperature derivatives.** In `testsuite/Test_m0p95feh+0p0_GN93_TAHB`, the fix moves log L by up to 2.76e-5 dex, against 1.67e-7 for the null change; in the rotating 3 M☉ giant the change is within the noise.
- **(changes results, small)** **Checked by KC** (Nov 10, 2026). **[`sneut.f` bug 1](../yrec-map/sneut.f.html#b1): A typo in `tfac2`.** In `testsuite/Test_m2p0_feh+0p0_vzams150_IES2_TAMS`, the fix moves log L by up to 7.95e-5 dex, against 1.58e-8 for the null change, with the same 546 models and end age.
- **(changes results, small)** **Checked by KC** (Nov 10, 2026). **[`neutrino.f` bug 1](../yrec-map/neutrino.f.html#b1): Metals other than C and O are left out.** In the 1 M☉ run to helium ignition the fractions summed to 0.984 to 0.991 in 33,460,185 calls; the fix changes the last neutrino luminosity from 0.845 to 0.876 L☉ (null change: 0.846), with log L within the noise and central log T a little beyond it.

### Convection, overshoot, and the mixing of composition

- **(changes results, small)** **Checked by KC** (Nov 10, 2026). **[`convec.f` bug 2](../yrec-map/convec.f.html#b2): A merger keeps the upper zone's top.** In `testsuite/Test_m9p0feh+0p0GS98_base_TAHB`, 22 of the 130 mergers cut the overshot core back by one or two shells; the fix moves log L by up to 1.45e-3 dex, against 7.0e-6 for the null change.
- **(changes results, small)** **Checked by KC** (Nov 10, 2026). **[`tpgrad.f` bug 2](../yrec-map/tpgrad.f.html#b2): With spots, the derivatives of the gradient are those of the unspotted one.** In the spotted 1 M☉ case the derivatives were taken 974,865 times with S = 0.878 to 0.99982; the fix moves log L by up to 0.00055 dex, against 0.000051 for a null change.

### Rotation: angular-momentum transport and rotational mixing

- **(changes results, small)** **Checked by KC** (Nov 10, 2026). **[`getfc.f` bug 1](../yrec-map/getfc.f.html#b1): The factor ½ in $\alpha$.** In a made-up case, `testsuite/Test_m2p0_feh+0p0_vzams150_IES1_TAMS` with `LVFC` on, surface N-14 moves by up to 0.0039 dex, against 7e-6 for the null change, and the main sequence lasts 1.357 Gyr instead of 1.344.
- **(changes results, small)** **Checked by KC** (Nov 10, 2026). **[`getw.f` bug 1](../yrec-map/getw.f.html#b1): `THP` and `WMST` recomputed from a stale `OMEGA` after the first substep.** In `testsuite/Test_m0p8feh+0p0GS98_rotp8p0d0p1mag1e4std_TAMS`, the fix moves central log T by up to 0.0015 dex, against 0.0002 for the null change; the solar case stays within the noise.
- **(changes results, small)** **Checked by KC** (Nov 10, 2026). **[`vcirc.f` bug 2](../yrec-map/vcirc.f.html#b2): `CC` is never set.** In `testsuite/Test_m2p0_feh+0p0_vzams150_IES2_TAMS`, the fix moves log L by up to 0.0056 dex and central log T by 0.0055, against about 2e-8 for the null change, with the same 546 models.

### The equation of state

- **(changes results, small)** **Checked by KC** (Nov 10, 2026). **[`eqscvg.f` bug 1](../yrec-map/eqscvg.f.html#b1): H$_2$ counted as one hydrogen nucleus.** In `examples/run_from_dbl_to_zams/Test_m0040_feh0_noGS_ZAMS`, the fix moves log L by up to 0.0035 dex, against 2.5e-5 for the null change, and the run ends at 7,928 Gyr instead of 8,681 Gyr.

### Output

- **(changes results, small)** **Checked by KC** (Nov 10, 2026). **[`stitch.f` bug 1](../yrec-map/stitch.f.html#b1): The integration steps are not restored.** In `testsuite/Test_m0p1feh+0p0GS98_spot25_ZAMS`, the fix moves log L by up to 5.8e-5 dex, against 9.4e-9 for the null change, and the last model is at 16.677 Gyr instead of 16.714.

## Bugs that write wrong output: 15

Each changes only what is written (a printed line, a label, a stored column), not the star.

| Bug | What is wrong | What the runs showed |
| --- | --- | --- |
| [`chkcal.f` bug 1](../yrec-map/chkcal.f.html#b1) | The first cycle prints an "Old BL" and "Old RL" that were never set. **Checked by KC** (Nov 10, 2026). | In `examples/run_standard_solar_model/Test_solarcal_noGS_norot`, the first cycle printed the old luminosity and radius before `BLP` and `RLP` were set; nothing computed reads these two printed lines. |
| [`envint.f` bug 2](../yrec-map/envint.f.html#b2) | Wrong $c_P$ in a print. **Checked by KC** (Nov 10, 2026). | In a made-up case, `testsuite/Test_m1p0feh+0p0GS98_base_TAMS` with `LSTCH` off, the line was written 626 times, each with `QCPP` = 0; with the fix the track is identical, and only that line of the `.store` file changes. |
| [`envint.f` bug 4](../yrec-map/envint.f.html#b4) | A stale summary when the envelope is skipped. **Checked by KC** (Nov 10, 2026). | The envelope was skipped once in four runs; in the rotating 3 M☉ case and `testsuite/Test_m2p0_feh+0p0_vzams150_IES2_TAMS`, the fix changes only the `.short` file's summary. |
| [`parmin.f` bug 1](../yrec-map/parmin.f.html#b1) | The wrong message for a rescale-and-evolve card. **Checked by KC** (Nov 10, 2026). | In `examples/run_from_seed_to_start/m10000gs98z001000_prems`, the wrong message was printed once; with format 551 restored, the track and `.store` file are identical, and only the `.short` file changes. |
| [`parmin.f` bug 6](../yrec-map/parmin.f.html#b6) | Long paths are cut to 256 characters without a word. **Checked by KC** (Nov 10, 2026). | Checked by reading the code: a 201-character output folder cuts a case's names to 256 characters without a message; in the round of Nov 9, two fix runs lost their files this way. |
| [`putmodel2.f` bug 1](../yrec-map/putmodel2.f.html#b1) | The caller's luminosities are left in erg s⁻¹. **Checked by KC** (Nov 10, 2026). | Luminosities in erg/s reached HTIMER and the `ISNU` fractions in 27 runs; with the fix, `testsuite/Test_m0p95feh+0p0_GN93_TAHB` gives an identical track, and only its `.short` file differs. |
| [`putstore.f` bug 2](../yrec-map/putstore.f.html#b2) | Atmosphere 5 has no label. **Checked by KC** (Nov 10, 2026). | A made-up case: `testsuite/Test_solarGS98_kurucz` with `KTTAU` = 5 and the Castelli-Kurucz table writes `ATM` without its own value at both stores; with the fix, the track is identical. |
| [`putstore.f` bug 4](../yrec-map/putstore.f.html#b4) | The old header calls the triple-α column "3HE." **Checked by KC** (Nov 10, 2026). | The header was written in 14 runs; with the fix, `examples/run_from_dbl_to_zams/Test_m0040_feh0_noGS_ZAMS` gives an identical track and a `.store` file within 2%, as expected for a label. |
| [`starin.f` bug 5](../yrec-map/starin.f.html#b5) | The warning prints an unset variable. **Checked by KC** (Nov 10, 2026). | In `examples/class_exercises/exercise_4/Grid_m4p0feh+0p0GS98_std25_TAMS`, a mixing length of 1.853 against the run's 1.708 printed no warning; with the test fixed it prints, and only the `.short` file differs. |
| [`stitch.f` bug 2](../yrec-map/stitch.f.html#b2) | β of the interior is read from the envelope's array. **Checked by KC** (Nov 10, 2026). | In 17 runs the interior's written beta came from the envelope's array; with the fix, `testsuite/Test_m0p3feh+0p0GS98_scv_ZAMS` and `testsuite/Test_solarM22M_difkur` have identical tracks, and only their `.store` files change. |
| [`stitch.f` bug 3](../yrec-map/stitch.f.html#b3) | The atmosphere's gravity is the last point's. **Checked by KC** (Nov 10, 2026). | Every atmosphere line writes the last envelope point's gravity (all 113 at 5.950E+02 in `testsuite/Test_m0p3feh+0p0GS98_scv_ZAMS`, model 7); with the fix, that case's track is identical and its `.store` file within 2%. |
| [`wrtmod.f` bug 1](../yrec-map/wrtmod.f.html#b1) | A typo in $d\rho/dr$. **Checked by KC** (Nov 10, 2026). | In seven solar cases with `LPULSE`, such as `testsuite/Test_solarGS98_dif`, `QPR1` differed from `QPR2` by -5.6% to +10.3% on every shell; with the fix, `testsuite/Test_solarGS98_allard` and `testsuite/Test_solarM22M_difkur` have identical tracks and `.store` files. |
| [`wrtmod.f` bug 2](../yrec-map/wrtmod.f.html#b2) | The pulsation model's shell list is never set. **Checked by KC** (Nov 10, 2026). | In all nine runs with `LPULSE`, such as `testsuite/Test_solarGS98_dif`, `IDM` was 0 every time, so the pulsation model was written with 0 shells; no fix was run. |
| [`wrtmod.f` bug 3](../yrec-map/wrtmod.f.html#b3) | Debugging prints. **Checked by KC** (Nov 10, 2026). | The prints ran at every call in 10 runs; with them removed, `testsuite/Test_solarAAG21_dif` and `testsuite/Test_solarGS98_allard` have identical tracks and `.store` files. |
| [`wrtout.f` bug 2](../yrec-map/wrtout.f.html#b2) | The summary gives the neutrino fluxes and capture rates in erg. **Checked by KC** (Nov 10, 2026). | With the labels corrected, `testsuite/Test_m0p3feh+0p0GS98_scv_ZAMS` and `testsuite/Test_3Msolar_GS_rot_gray_OPALSCV_SF2_GS98_OP_CF10_RGp2diffrotI3cz2` have identical tracks; only their `.short` files differ. |

## The other 161

The other suspected bugs are listed, file by file, in the tables of the home page's [Files by topic](../index.html#files-by-topic) (the fragile column), and each is on its file's page, marked with what the runs showed: *harmless in the runs* (the condition held, but the fix's effect stayed within the noise), *never occurred* (the code ran, but the faulty condition never held), *not reached* (no case run reached the code), *cannot be reached* (a guard makes it impossible at 7be4133), or *withdrawn*. No fix among them changed any case run clearly beyond the null change (about five times or more; a few come within twice it), so they can wait, to go in in batches and be checked against YREC's full test suite. For tools, every suspected bug, these included, is listed in [bugs.json](bugs.json): its file, number, what the runs showed, its write-up, and the lines of code it cites.

## One of YREC's sample cases

`sample_cases/UpperMS/Sample_m9p0feh+0p0GS98_none_TAHB` stops before its target: It fails to converge at 30.06 Myr, with central $Y$ at $1.46\times10^{-3}$ against its stop target of $10^{-4}$ (`END_YCEN(1)` and `END_YCEN(2)`, lines 35 and 52 of its `.nml1`). This is YREC's own `KNOWN_ISSUES.md` issue 40: From a central $Y$ of about $2\times10^{-3}$, the envelope's luminosity correction at one shell alternates in sign and grows by about 8% per iteration; with `HTOLER(5,2)` ten times looser, the run stops four models later. The test suite's deck for the same star had its target raised to $2\times10^{-3}$ for this reason on Nov 2, 2026 (`testsuite/Test_m9p0feh+0p0GS98_base_TAHB.nml1`, lines 35–38), and the sample case kept $10^{-4}$. Not a bug in the code: at most the same one-line change to the sample case.

## The made-up cases

Every other case is one of YREC's own, named by its path at 7be4133. Each made-up case is shown with its changes marked (follow its name) and can be downloaded from there. Each starts from one of YREC's cases, changes as few settings as possible, and takes each changed value from YREC's documentation, another of its cases, or a table's README; apart from these changes, only the output names differ.

| Pair | YREC case it starts from | What was changed, and its source | Bugs it reaches |
| --- | --- | --- | --- |
| [`castelli-kttau5`](namelists/castelli-kttau5.html) | `testsuite/Test_solarGS98_kurucz` (a solar model with Kurucz atmospheres) | `KTTAU` = 5 and `FATM` = `atmos/CastelliKurucz/atmk2004p00.tab`, as `input/atmos/CastelliKurucz/README` asks for these tables | [`setups.f` bug 1](../yrec-map/setups.f.html#b1), [`kcsurfp.f` bug 1](../yrec-map/kcsurfp.f.html#b1), [`putstore.f` bug 2](../yrec-map/putstore.f.html#b2) |
| [`custom-mix`](namelists/custom-mix.html) | `testsuite/Test_solarAAG21_dif` (a solar model with the AAG21 mixture and diffusion) | `ISETMIX` = 2 and `ISETISO` = 2, with the case's own commented custom-mixture block switched on (`docs/source/namelist_control.md`) | [`parmin.f` bug 2](../yrec-map/parmin.f.html#b2) |
| [`fcore-default`](namelists/fcore-default.html) | `testsuite/Test_solarGS98_kurucz` | `FCORE` at the code's default, 1.0 (`nmlpar_mod.f`; `docs/source/namelist_physics.md` offers `LCORE` and `FCORE` with no recommended value) | [`starin.f` bug 4](../yrec-map/starin.f.html#b4) |
| [`getfc-1`](namelists/getfc-1.html) | `testsuite/Test_m2p0_feh+0p0_vzams150_IES1_TAMS` (a 2 M☉ star rotating at 150 km/s on the ZAMS, to the TAMS) | `LVFC` on (`docs/source/namelist_physics.md`, "Experimental options"); YREC's own namelists call it "Not recommended" | [`getfc.f` bug 1](../yrec-map/getfc.f.html#b1) |
| [`getopal95-2`](namelists/getopal95-2.html) | `examples/run_from_zahb_to_tahb/ZAHB_m1p0feh+0p0_TAHB` (a 1 M☉ core helium-burning model, from the ZAHB) | `FLIV95` = `opacity/atomic/op05/AAG2021zx0.0187.tab`, the table `input/opacity/atomic/README` recommends for the AAG21 mixture | [`getopal95.f` bug 2](../yrec-map/getopal95.f.html#b2) |
| [`lstch-off`](namelists/lstch-off.html) | `testsuite/Test_m1p0feh+0p0GS98_base_TAMS` (a 1 M☉ star from the ZAMS to the TAMS) | `LSTCH` at its default (off) with `LSTATM` on (`docs/source/namelist_control.md`) | [`envint.f` bug 2](../yrec-map/envint.f.html#b2) |
| [`numderiv`](namelists/numderiv.html) | `testsuite/Test_m1p0feh+0p0GS98_base_TAMS` | `LNumDeriv` on (`docs/source/microphysics.md`, `docs/source/namelist_physics.md`) | [`eqstat.f` bug 1](../yrec-map/eqstat.f.html#b1) |
| [`reimers-rgb`](namelists/reimers-rgb.html) | `testsuite/Test_m1p0feh+0p0GS98_base_HeIgnite` (a 1 M☉ star up the giant branch to helium ignition) | `LMDOT` and `LREIMER` on, as the case's own comment offers, with the default coefficient | [`massloss.f` bug 1](../yrec-map/massloss.f.html#b1), [`mdot.f` bug 2](../yrec-map/mdot.f.html#b2), [`htimer.f` bug 1](../yrec-map/htimer.f.html#b1) |
| [`reimers-3msun`](namelists/reimers-3msun.html) | `testsuite/Test_m3p0feh+0p0GS98_std25_TAMS` (a 3 M☉ main-sequence star) | `LMDOT` and `LREIMER` on, as in `reimers-rgb` | [`massloss.f` bug 1](../yrec-map/massloss.f.html#b1), [`mdot.f` bug 2](../yrec-map/mdot.f.html#b2), [`dburn.f` bug 1](../yrec-map/dburn.f.html#b1) |

No made-up case was built for `getopal95.f` bug 1: It needs a cool hydrogen-poor surface, which none of YREC's cases or documents use, and which YREC cannot build faithfully from the models it ships.
