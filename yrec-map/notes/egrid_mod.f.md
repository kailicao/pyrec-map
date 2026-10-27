## Explanation

**Purpose.** `EGRID_MOD` holds the evenly spaced grid on which angular momentum transport and rotational mixing are solved: the grid variable $\chi$ at the model's shells and at the even points, the even points' masses, the spacing and their number. Shared by 7 routines. It replaces `COMMON/EGRID/` (MHP via Claude, 10/14/26); `JSON` comes from [[dimensions_mod.f#DIMENSIONS_MOD|`DIMENSIONS_MOD`]].

**What its variables hold, who sets them, who reads them.** All are set by [[getgrid.f#GETGRID|`GETGRID`]] for the region `IBEG`…`IEND`:
- `CHI(JSON)`: $\chi = \log m/\delta_m + L/\delta_L - \log P/\delta_P$ at each shell of the region, with the spacings from the mesh tolerances `HPTTOL`.
- `NTOT` (`INTEGER*4`): the number of even points, the number of shells in the region but at least 3.
- `DCHI`: the spacing, $(\chi_\mathrm{last} - \chi_1)/(\mathtt{NTOT}-1)$.
- `ECHI(JSON)`: $\chi$ at the even points, from `CHI(1)` in steps of `DCHI`.
- `ES1(JSON)`: the mass (g) at the even points, interpolated in $\log m$ by [[osplin.f#OSPLIN|`OSPLIN`]].
- Read by [[rotgrid.f#ROTGRID|`ROTGRID`]] and [[mixgrid.f#MIXGRID|`MIXGRID`]], which interpolate quantities between the two grids, [[mixcom.f#MIXCOM|`MIXCOM`]], [[eq2mod.f#EQ2MOD|`EQ2MOD`]], [[seculr.f#SECULR|`SECULR`]] (which passes `NTOT` to the solvers) and [[checkj.f#CHECKJ|`CHECKJ`]] (printing).

**Design.** A blanket `USE EGRID_MOD`. At `rp_1`, SECULR named the third member `EQS1`, harmless with COMMON's storage association.

**Changed since `rp_1`.** New file: `COMMON/EGRID/` as a module.
