## Explanation

**Purpose.** `ESAC06` is `ESAC` (removed since `rp_1`) for the OPAL 2006 equation-of-state tables: it interpolates them in $X$, $T_6$ and $\rho$ and returns nine thermodynamic quantities (`EOS` has room for ten). It is a copy of `ESAC01` (removed since `rp_1`) adapted to the larger 2006 table. The file also holds `SETEOS06`, the tables' one-time setup.

**How it fits.**
- **Who calls it:** [[oeqos06.f#OEQOS06|OEQOS06]] (called from [[eqstat2.f#EQSTAT2|EQSTAT2]] when `LOPALE06` is set), [[rhoofp06.f#RHOOFP06|RHOOFP06]], and [[calcad.f#CALCAD|CALCAD]], which calls it directly for every point of the model and envelope (with `IORDER` = 9, `IRAD` = 1) when `LOPALE06` is set; its call for the atmosphere points is commented out.
- **Who calls `SETEOS06`:** [[setups.f#SETUPS|SETUPS]], once, when `LOPALE06` is set (the table file is opened by [[parmin.f#PARMIN|PARMIN]]).
- **What it calls:** [[quadeos06.f#QUADEOS06|QUADEOS06]], [[t6rinteos06.f#T6RINTEOS06|T6RINTEOS06]], [[gmass06.f#GMASS06|GMASS06]] and [[radsub06.f#RADSUB06|RADSUB06]]; `SETEOS06` calls [[readcoeos06.f#READCOEOS06|READCOEOS06]].
- **Outputs:** in `EOS06MISC_MOD`'s `EOS`: EOS(1) $P$, (2) $E$, (3) $S$, (4) $\partial E/\partial\rho|_T$, (5) $c_V$, (6) $\partial\ln P/\partial\ln\rho$, (7) $\partial\ln P/\partial\ln T$, (8) $\Gamma_1$, (9) $\Gamma_2/(\Gamma_2-1)$; (10), $\Gamma_3-1$ by the commented-out line of [[radsub06.f#L102]], is never computed: The table file holds nine quantities ([[readcoeos06.f#L124-L126]]), no caller asks for more than nine, and `EOS(10)` keeps the 1 that READCOEOS06 sets ([[readcoeos06.f#L89-L91]]); nothing reads it (settled from the code, Nov 9, 2026).
- **Modules:** `AEOS06_MOD` (the tables `XZ`, the grids `T6LIST`, `RHO`, `T6A`, `XA`, the X index `MF` and workspace; its member `M` is now `MIDX`), shared with `READCOEOS06`, `T6RINTEOS06`, `RHOOFP06` and [[eqbound06.f#EQBOUND06|EQBOUND06]]; `EEEOS06_MOD` (workspace `EPL`, `XX`), with `READCOEOS06` and `T6RINTEOS06`; `EOS06MISC_MOD`, which merges the former `/EEOS06/` (the output `EOS`, `ESACT`), `/AAEOS06/` (workspace), `/BEOS06/` (`ZZ`, `IRI`, `INDEX`, `NTA`, `NRA`) and `/BBEOS06/` (the indices `L1`…`K4`, `IP`, `IQ`), with `OEQOS06`, `RADSUB06`, `READCOEOS06`, `RHOOFP06`, `T6RINTEOS06`, `CALCAD` and `EQBOUND06` (which reads `NTA`, `NRA` and starts its search from `K3`, `L2`); `IOUNITS_MOD` (`ISHORT`).

**The table.** 169 densities and 197 temperatures. Two DATA statements, now in `EOS06MISC_MOD` (with `INDEX`; `XA` is in `AEOS06_MOD`), describe its irregular edge: `NTA(l)`, the lowest temperature index for each density, and `NRA(k)`, the highest density index for each temperature.

> **Question** ([[eos06misc_mod.f#L61-L70]]). **Edge tables in two places.** `NTA` and `NRA` are hard-coded (in `EOS06MISC_MOD`); if the table file changes, they must change too. READCOEOS06 already reads, for each density, the number of temperatures in the file (`ICYCUSE`, [[readcoeos06.f#L105-L118]]), and stops if it is below `NTA`. Could `READCOEOS06` derive them from the file?

**The method.** As `ESAC01` and `ESAC`, whose steps were:
1. The tables are read once, before the first call, by `SETEOS06` (it maps `INDEX` into `IRI`, copies `XA` into `XX` and calls `READCOEOS06`); each call takes $Z$ from `ZZ(1)`. The run stops if the tables' $Z$ values differ (the check before label 66, and label 66 itself); only the two cases below use the alternate return.
2. Out of table (alternate return, label 62) if $T_6$ or $\rho$ is outside the grid. (The copies `XXI` and `RI` of the arguments, [[#L237-L238]], are not used: unused?)
3. Bisection for the indices in $X$ (`MF`…`MI`), $\rho$ (`L1`…`L4`) and $T_6$ (`K1`…`K4`).
4. Check that the stencil avoids the table's empty region, where `XZ` holds values above $10^{30}$, and choose a 3×3 or 4×4 stencil (`IP`, `IQ`). If the 3×3 stencil reaches the empty region but the 2×2 one does not, the stencil is moved back by one in both $T_6$ and $\rho$ and used as 3×3, without a new check; otherwise the routine returns "empty region" (label 65).
5. For each quantity, interpolate in $X$ with a quadratic through three tables (`QUADEOS06`; its first argument `IS` is 0 on the first point, so that it computes its abscissa factors, and 1 afterwards); between two overlapping quadratics, blend them linearly:
$$E = E_{\mathrm{low}}\,w + E_{\mathrm{high}}(1-w), \qquad w = (X_{MH} - X)/(X_{MH} - X_{MG}).$$
Then `T6RINTEOS06` interpolates in $T_6$ and $\rho$.
6. Pressure and energy are tabulated scaled: $P = \mathrm{EOS}(1)\cdot T_6\rho$ and $E = \mathrm{EOS}(2)\cdot T_6$. Without radiation, $c_V$, EOS(5), is scaled by $n\,R/m$, with $R = 83.14511$ (the gas constant in units of $10^{12}$ erg per mole per $10^6$ K) and the moles $n$ and mass $m$ from `GMASS06`; with radiation, `RADSUB06` (which takes `IRAD` as an argument) adds the radiation terms. Since RADSUB06 is called only when `IRAD` = 1 ([[#L481-L485]]), its argument is always 1, and its own branch for `IRAD` = 0 never runs (unused?; [[radsub06.f#L74-L103]]). The error messages print their indices.

**Changed since `rp_1`.** The one-time work (the `ITIME` switch in `/LREADCO/`, the table read, the `INDEX`/`XX` setup) moved to the new `SETEOS06`, called from `SETUPS`; the first-call check $X + Z \le 1$ (label 61) is dropped; the DATA for `XA`, `INDEX`, `NTA`, `NRA` moved into the modules; COMMON blocks to modules (four small ones merged into `EOS06MISC_MOD`, `M` renamed `MIDX`), `IMPLICIT NONE`. The question on the shared `ITIME` flag is settled (the flag is gone), and those on `ESAC` that applied here are now stated on this page.

## Bugs, by priority

1. **(harmless in the runs)** **`EOS(2)` and `EOS(5)` rescaled again on every call with `IORDER` < 5.** ([[#L408]]; [[#L477-L485]]) The loop over the quantities sets `EOS(1..IORDER)` only, but the scaling after it multiplies `EOS(IRI(2))` by $T_6$ and, without radiation, `EOS(IRI(5))` by `MOLES*APROP/TMASS` (about 140 for an ionized mixture with $X = 0.7$) whatever `IORDER` is. [[rhoofp06.f#RHOOFP06|RHOOFP06]] calls ESAC06 with `IORDER` = 1 and `IRAD` = 0, up to 13 times per density ([[rhoofp06.f#L91-L115]]), so each of these calls multiplies the value of `EOS(5)` left by an earlier call by that factor again. Only a call with `IORDER` = 9 resets it (OEQOS06 after a density is found, [[oeqos06.f#L102]], and CALCAD); when RHOOFP06 fails, OEQOS06 returns at once ([[oeqos06.f#L95-L97]]), so the growth carries on across calls, and after about 140 such calls `EOS(5)` overflows. With the developers' build options (`-ffpe-trap=invalid,zero,overflow`, `src/Makefile`, line 61) the run stops; in a release build the value becomes infinite and is overwritten by the next call with `IORDER` = 9, so the results are not changed. This matches the comment in RHOOFP06 that its tolerance was loosened "to prevent array value eos(5) from growing without bound and crashing the program" ([[rhoofp06.f#L117-L119]]). Only with `LOPALE06` (off by default, [[nmlpar_mod.f#L122]]; on in most of the test suite).

    **A possible fix:**

    ```diff
    --- a/src/esac06.f
    +++ b/src/esac06.f
    @@ -474,13 +474,15 @@
           call t6rinteos06(slr,slt)
           eos(iv)=esact
       124 continue
    +C 11/09/26 KC via Claude
    +C code changed to scale only the quantities interpolated in this call.
           p0=t6*r
           eos(iri(1))=eos(iri(1))*p0   ! interpolated in p/po
    -      eos(iri(2))=eos(iri(2))*t6   ! interpolated in E/T6
    +      if (iri(2) .le. iorder) eos(iri(2))=eos(iri(2))*t6
           tmass=gmass06(xh,z,moles,eground,fracz,frac)
           if (irad .eq. 1) then
           call radsub06(irad,t6,r,moles,tmass)
    -      else
    +      else if (iri(5) .le. iorder) then
           eos(iri(5))=eos(iri(5))*moles*aprop/tmass
           endif
           return
    ```

    **Checked by running YREC** (Nov 9, 2026; a line added at each suspected path counted how often it was taken, the outputs otherwise unchanged). The path was taken in all 31 of the 34 cases run that use the OPAL 2006 tables, from 531,263 to 510,367,635 times, and the condition (EOS(5) scaled though not interpolated) in most of those calls: in `testsuite/Test_m1p0feh+0p0GS98_base_TAMS`, for example, 10,067,407 of 12,400,539. `EOS(5)` reached $6.30\times10^{42}$ before a scaling, far below the overflow (about $10^{308}$), so no run stopped on it. With the page's fix, `testsuite/Test_3Msolar_GS_rot_gray_OPALSCV_SF2_GS98_OP_CF10_RGp2diffrotI3cz2` and `testsuite/Test_m1p0feh+0p0GS98_base_TAMS` give identical `.track` and `.store` files. Intent: RHOOFP06's comment ([[rhoofp06.f#L117-L119]]) treats the growth as a known symptom, not as intended. The growth is real in every run, and the comment records crashes from it before the tolerance was loosened; a run with more failed density searches could still overflow.

2. **(never occurred)** **The second $X$ quadratic's warning tests the wrong array.** ([[#L452-L458]]) In loop 47 the value just computed is `ESK2(IT,IR)`, but the warning tests `ESK(IT,IR)`, the first quadratic's value, already tested in loop 45. A value of `ESK2` above $10^{20}$ (a stencil reaching the empty region) passes without a message, and a large `ESK` is reported twice.

    **A possible fix:**

    ```diff
    --- a/src/esac06.f
    +++ b/src/esac06.f
    @@ -451,7 +451,9 @@
             do it=k1,k1+ip
               esk2(it,ir)=quadeos06(is,iw,xh,epl(mg,it,ir),epl(mh,it,ir)
          x    ,epl(mi,it,ir),xx(mg),xx(mh),xx(mi))
    -          if(esk(it,ir) .gt. 1.D+20) then
    +C 11/09/26 KC via Claude
    +C code changed to test the second quadratic's value.
    +          if(esk2(it,ir) .gt. 1.D+20) then
               write(ISHORT,'(A," problem it,ir,l3,k3,iq,ip=", 6i5)') ID,
          x    it,ir,l3,k3,iq,ip
               write(ISHORT,'(3e12.4)')  (epl(ms,it,ir),ms=mg,mg+2)
    ```

    **Checked by running YREC** (Nov 9, 2026; a line added at each suspected path counted how often it was taken, the outputs otherwise unchanged). Loop 47 ran in 26 cases, up to 84,320,569 times, at $T_6$ from 0.95 to 50.7 and $X$ from 0.2 to 0.4, but the second quadratic's value never exceeded $10^{20}$, so the missed warning never mattered. No fix was run, since it changes only a warning. What would reach it: an $X$ stencil of four tables whose second quadratic reaches the empty region of the table. Intent: none found.

3. **(not reached)** **The message at label 66 swaps `IP` and `IQ`.** ([[#L498-L499]]) The heading reads `iq,ip,k3,l3,…`, but the values are written as `ip,iq,k3,l3,…`.

    **A possible fix:**

    ```diff
    --- a/src/esac06.f
    +++ b/src/esac06.f
    @@ -495,8 +495,10 @@
        66 write(ISHORT,*)ID," Z does not match Z in EOSdata* files you ",
          . "are using (66)"
           write(ISHORT,'("mf,zz(mf)=",i5,e12.4)') mf,zz(mf)
    +C 11/09/26 KC via Claude
    +C code changed to print IQ and IP in the order of the heading.
           write(ISHORT,'("  iq,ip,k3,l3,xh,t6,r,z= ",4i5,4e12.4)')
    -     x ip,iq,k3,l3,xh,t6,r,z
    +     x iq,ip,k3,l3,xh,t6,r,z
           stop
     
           end
    ```

    **Checked by running YREC** (Nov 9, 2026; a line added at each suspected path counted how often it was taken, the outputs otherwise unchanged). The message at label 66 was never reached in the 31 runs with the OPAL 2006 tables: `z` is taken from `zz(1)` ([[#L258]]), and every table of the shipped file has the same $Z$, so only a file whose tables differ in $Z$ reaches it, and the run then stops. No fix was run, since it changes only a message. Intent: none found.

4. **(cannot be reached)** **The check on `IORDER` warns and goes on.** ([[#L230-L232]]) The check copied from `ESAC01` writes "iorder cannot exceed 9" and continues. The file holds nine quantities, so with `IORDER` = 10 the loop would read `XZ(·,10,·,·)`, which READCOEOS06 leaves at $10^{35}$ ([[readcoeos06.f#L79-L88]]), and T6RINTEOS06 would stop the run with "Interpolation indices out of range" ([[t6rinteos06.f#L97-L101]]). No caller passes more than 9 today.

    **A possible fix:**

    ```diff
    --- a/src/esac06.f
    +++ b/src/esac06.f
    @@ -227,8 +227,11 @@
           save
     
           blank=' '
    +C 11/09/26 KC via Claude
    +C code changed to stop on an IORDER above 9, as on a wrong IRAD.
           if (iorder .gt. 9 ) then
              write (ISHORT,'(A, " iorder cannot exceed 9")') ID
    +         stop
           endif
           if ((irad .ne. 0) .and. (irad .ne. 1)) then
              write (ISHORT,'(A, " Irad must be 0 or 1")') ID
    ```

    **Checked by running YREC** (Nov 9, 2026; a line added at each suspected path counted how often it was taken, the outputs otherwise unchanged). The warning never fired, and cannot at 7be4133: Every call passes `IORDER` = 1 ([[rhoofp06.f#L91-L115]]) or 9 ([[oeqos06.f#L80]], [[calcad.f#L262]]). No fix was run, since it is a stop. Intent: none found.

### ESAC06

Interpolates the OPAL 2006 EOS tables in $X$, $T_6$, $\rho$ (as `ESAC01`); results in `EOS06MISC_MOD`'s `EOS`. Also used by `CALCAD` for the adiabatic exponents of the whole model.

### SETEOS06

The OPAL 2006 tables' one-time setup, moved out of `ESAC06`'s first call: maps `INDEX` into `IRI`, copies `XA` into `XX` and calls `READCOEOS06`. `SETUPS` calls it when `LOPALE06` is set.
