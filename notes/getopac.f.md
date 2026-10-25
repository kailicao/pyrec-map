## Explanation

**Purpose.** `GETOPAC` is YREC's opacity routine: for a given $\rho$, $T$, $X$, $Z$ it chooses among the low-temperature (molecular) tables and the interior tables, ramps between them, handles metal-rich helium-burning cores, and adds conductive opacity. It returns $\kappa$ and its logarithmic derivatives.

**How it fits.**
- **Who calls it:** seven routines: [[coefft.f#COEFFT|COEFFT]], [[envint.f#ENVINT|ENVINT]], [[physic.f#PHYSIC|PHYSIC]], [[qatm.f#QATM|QATM]], [[qenv.f#QENV|QENV]], [[sconvec.f#SCONVEC|SCONVEC]] and [[starin.f#STARIN|STARIN]].
- **Inputs:** `DL`, `TL` ($\log\rho$, $\log T$), `X`, `Z`, and `FXION` (ionization fractions, passed on to the conductive opacity).
- **What it calls:** low-temperature tables: [[getalex06.f#GETALEX06|GETALEX06]] (Ferguson–Alexander 2006), [[yalo3d.f#YALO3D|YALO3D]] (Alexander 1995), [[kurucz.f#KURUCZ|KURUCZ]] and [[kurucz2.f#KURUCZ2|KURUCZ2]] (Kurucz 1990, one or two $Z$); interior tables: [[getopal95.f#GETOPAL95|GETOPAL95]] (OPAL 1995), [[yllo3d.f#YLLO3D|YLLO3D]] and [[yllo3d2.f#YLLO3D2|YLLO3D2]] (OPAL 1992), [[gtlaol.f#GTLAOL|GTLAOL]] and [[gtlaol2.f#GTLAOL2|GTLAOL2]] (Los Alamos 1989); [[gtpurz.f#GTPURZ|GTPURZ]] (pure-metal table); and [[condopacpint.f#CONDOPACPINT|CONDOPACPINT]] (Potekhin conductive opacity).
- **Outputs:** `O` ($\kappa$), `OL` ($\log\kappa$), `QOD` $=\partial\log\kappa/\partial\log\rho$, `QOT` $=\partial\log\kappa/\partial\log T$.
- **COMMON blocks:** `/NEWOPAC/` (the table choice flags `LALEX06`, `LALEX95`, `LKUR90`, `LOPAL95`, `LOPAL92`, `LLAOL89`, `L2Z`, the tables' $Z$ values, and the ramp limits `TMOLMIN`, `TMOLMAX`), set by [[parmin.f#PARMIN|PARMIN]] and the opacity setup routines; `/NWLAOL/` (`LPUREZ`); `/MISCOPAC/` (`LcondOpacP`); `/OPTAB/` (`OPTOL`); `/COMP/` (`ZENV`); `/LUOUT/`.

**The method.**
1. **Molecular opacity** for $\log T \le$ `TMOLMAX`, from the first table enabled in the order Alexander 2006, Alexander 1995, Kurucz. With two Kurucz tables (`L2Z`), $\log\kappa$ and its derivatives are interpolated linearly in $Z$. If `KURUCZ` or `KURUCZ2` fails (it takes the alternate return), no molecular value is kept and the interior tables are used alone, even below `TMOLMIN`.
2. **Interior opacity**, unless $\log T <$ `TMOLMIN` and a molecular value was found:
   - for $Z > 0.1$ and $\log T > 7.7$ (helium-burning cores), linear interpolation in $Z$ between the interior table at $Z_\mathrm{tab}$ (0.1 for OPAL 1995) and the pure-metal table at $Z = 1$: $\log\kappa = \log\kappa_{Z=1} + (Z-1)\,\dfrac{\log\kappa_\mathrm{tab} - \log\kappa_{Z=1}}{Z_\mathrm{tab} - 1}$; the run stops if no pure-$Z$ table is loaded;
   - the run stops if $Z > 0.12$ below that temperature, or if $Z$ differs from the envelope's `ZENV` beyond `OPTOL` with a single-$Z$ table (neither `L2Z` nor OPAL 1995, which interpolates in $Z$ itself);
   - otherwise OPAL 1995, OPAL 1992 or LAOL 1989, the last two with linear interpolation between two $Z$ tables if `L2Z`.
3. **Ramp** for `TMOLMIN` ≤ $\log T \le$ `TMOLMAX`: with $w = (\log T - \mathrm{TMOLMIN})/(\mathrm{TMOLMAX} - \mathrm{TMOLMIN})$, $\kappa = w\,\kappa_\mathrm{int} + (1-w)\,\kappa_\mathrm{mol}$, and the derivatives likewise.
4. **Conduction.** Potekhin's opacity if `LcondOpacP` is set and it succeeds; otherwise, for $\log T \ge 4.2$ and $\log\rho \ge 2\log T - 13$, the Hubbard–Lampe fit as coded:
$$\log\kappa_c = \log(1 - 0.6X) - 14.6196 - (3.5853 + 0.1386\log\rho)\log\rho + (5.1324 - 0.3219\log T)\log T + 0.3901\log\rho\log T.$$
5. **Combination:** $1/\kappa = 1/\kappa_\mathrm{rad} + 1/\kappa_c$, and
$$\frac{\partial\log\kappa}{\partial\log\rho} = \frac{\kappa_c\,\partial\log\kappa_\mathrm{rad} + \kappa_\mathrm{rad}\,\partial\log\kappa_c}{\kappa_\mathrm{rad} + \kappa_c},$$
and the same in $\log T$.

## Questions for the experts

1. **Undefined `ZIT`.** In the helium-burning branch, if neither `LOPAL95`, `LOPAL92` nor `LLAOL89` is set, `ZIT` and the interior values are undefined. The final trap ("NO OPACITY TABLE CHOSEN") is not reached on that path. Add it there too?
2. **Ramp in $\kappa$, not $\log\kappa$.** The ramp is linear in $\kappa$, while the derivatives (which are of $\log\kappa$) are averaged with the same weights. The derivatives are then not exactly those of the ramped $\kappa$. Acceptable?
3. **Conduction where no table applies.** Below $\log T = 4.2$ or at low density the routine returns without conduction, which is fine; but when Potekhin is enabled and fails, Hubbard–Lampe is used without a message. Should the fallback be reported?
4. **`FXION` used only by conduction.** Fine, but its meaning differs by equation of state (`EQSAHA` versus SCV); does `CONDOPACPINT` depend on which one supplied it?

### GETOPAC

Chooses, ramps and combines the molecular, interior, pure-metal and conductive opacities (method above).
