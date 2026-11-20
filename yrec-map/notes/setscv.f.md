## Explanation

**Purpose.** Builds the equation-of-state table for the envelope's mixture from the SCV (Saumon–Chabrier–Van Horn, by the module's name `SCVEOS_MOD`, "MHP 5/97") tables of pure hydrogen, pure helium and metals, which [`SETUPS`](https://github.com/yreclab/yrec/blob/7be4133/src/setups.f#L16-L396) has read. It adds the entropy of mixing, and computes by finite differences the derivatives the structure equations need. (The header comment, "evaluate the EOS with the new tables and call eqstat … and compare," describes an earlier purpose; the routine calls neither.)

**How it fits.**
- **Who calls it:** [`STARIN`](starin.f.md#starin), once the starting model's envelope composition is known.
- **Inputs, through modules:** `SCVEOS_MOD` (the tables `TABLEX` (hydrogen), `TABLEY` (helium), `TABLEZ` (metals) on a grid of temperatures `TLOGX(63)` and up to 76 pressures `NPTSX(I)`), and `COMP_MOD` (`XENV`, `ZENV`).
- **What it calls:** [`INTER3`](inter3.f.md#inter3), three-point Lagrange interpolation weights (`FT`) and their derivatives (`FTD`).
- **Outputs, through `SCVEOS_MOD`:** column 12 of `TABLEX` and `TABLEY`, `SMIX` (the entropy of mixing), and `TABLENV(63, 76, 12)`, the mixture's table; also the interpolation indices `IDTSCV` (named `IDT` at `rp_1`) and `IDP` left from the last point. It is read by [`EQSCVE`](eqscve.f.md#eqscve) and [`EQSCVG`](eqscvg.f.md#eqscvg), through [`EQSTAT`](eqstat.f.md#eqstat), when `LSCV` is true.

**The method.** The table columns are used, in the code's notation, as $`\log P`$ (1), the ionization fractions (2, 3), $`\log\rho`$ (4), $`\log S`$ (5), $`\partial\ln\rho/\partial\ln T`$ (7), $`\partial\ln\rho/\partial\ln P`$ (8) and $`\partial\ln S/\partial\ln T`$ (9); we read this from the formulas.

1. **$`dU/dT`$ of each pure table** (column 12; the loop's comment, "READ IN EQUATION OF STATE TABLES FOR HYDROGEN AND HELIUM" ([line 37](https://github.com/yreclab/yrec/blob/7be4133/src/setscv.f#L37)), is left from the reading, now done in SETUPS, [setups.f, lines 368–393](https://github.com/yreclab/yrec/blob/7be4133/src/setups.f#L368-L393)), from the two expressions for $`c_P`$ in the comments,
   
   $$\displaystyle c\_P = S\left(\frac{\partial\ln S}{\partial\ln T}\right)\_P = \frac{dU}{dT} + \frac{P}{\rho T}\\,\frac{(\partial\ln\rho/\partial\ln T)^2}{\partial\ln\rho/\partial\ln P}.$$
2. **Entropy of mixing.** With $`Y = 1 - X`$ (`XENV`), the mixture's density $`\rho_\mathrm{mix} = 1/((1-Y)/\rho_X + Y/\rho_Y)`$, the number densities of hydrogen and helium particles and of their electrons from the ionization fractions, and $`\beta = (m_H/m_{He})\,Y/(1-Y)`$, $`\gamma`$ the ratio of particles per nucleus, the code computes
   
   $$\displaystyle S\_\mathrm{mix} = \frac{k}{m\_H}\\,\frac{2(1-Y)}{1+x\_2+3x\_1}\left\[\ln(1+\beta\gamma) - \frac{n\_{e,H}}{n}\ln(1+\delta) + \beta\gamma\ln\Bigl(1+\frac{1}{\beta\gamma}\Bigr) - \frac{n\_{e,He}}{n}\ln\Bigl(1+\frac1\delta\Bigr)\right\],$$
   
   with $`n`$ = `TNUM` the sum of the hydrogen and helium number densities (`HNUM` + `HENUM`), $`n_{e,H}`$, $`n_{e,He}`$ their electron number densities (`HNUME`, `HENUME`, each floored at 1), $`\delta`$ (`DE`) the ratio of electrons from helium to those from hydrogen, scaled by $`\beta\gamma`$ (the last term uses `DEI`, which is $`1/\delta`$ when both are positive); $`x_1`$, $`x_2`$ are `TABLEX(I,J,2)` and `(I,J,3)`. Constants: $`m_H`$ = `CMH`, $`m_{He}`$ = `CMHE` ($`\mathrm{g}`$), $`k`$ = `CBOLTZ` ($`\mathrm{erg\,K^{-1}}`$). This is the code's formula; its source is not cited.

    > **Question** ([lines 53–54](https://github.com/yreclab/yrec/blob/7be4133/src/setscv.f#L53-L54); [line 120](https://github.com/yreclab/yrec/blob/7be4133/src/setscv.f#L120)). **$`Y`$ in the entropy of mixing ignores $`Z`$.** Here $`Y = 1 -`$ `XENV`, so the ratio of helium to hydrogen counts the metals as helium, while step 3 uses $`Y = 1 - X - Z`$. Is this intended (mixing of hydrogen and helium only, the metals left out of the mixture)? With $`Z \approx 0.02`$ the ratio changes by about 7% at $`X = 0.7`$.

3. **The mixture at each $`(T, P)`$**, with $`X`$, $`Y = 1 - X - Z`$, $`Z`$ from `COMP_MOD`: densities add as volumes,
   
   $$\displaystyle \frac1\rho = \frac{X}{\rho\_X} + \frac{Y}{\rho\_Y} + \frac{Z}{\rho\_Z},\qquad \frac{\partial\ln\rho}{\partial\ln P} = \sum\_k X\_k\frac{\rho}{\rho\_k}\left(\frac{\partial\ln\rho}{\partial\ln P}\right)\_k,$$
   
   and the same for $`\partial\ln\rho/\partial\ln T`$; the entropy is $`S = X S_X + Y S_Y + S_\mathrm{mix}`$, and $`c_P`$ follows, with the metals' term added. The radiation pressure `PRAD` $`= aT^4/3`$ is added to `P` and `PL` ([lines 122–126](https://github.com/yreclab/yrec/blob/7be4133/src/setscv.f#L122-L126)), but neither is used afterwards (unused?), nor is `QPT0` ([line 144](https://github.com/yreclab/yrec/blob/7be4133/src/setscv.f#L144), unused?): The table stays on the gas-pressure grid (`TABLENV(I,J,1)` is `TABLEX(I,J,1)`), and [`EQSCVE`](eqscve.f.md#eqscve) adds radiation itself, looking the table up at the gas pressure $`\beta P`$ (settled from the code, Nov 9, 2026: [eqscve.f, lines 52–53](https://github.com/yreclab/yrec/blob/7be4133/src/eqscve.f#L52-L53), [eqscve.f, lines 159–160](https://github.com/yreclab/yrec/blob/7be4133/src/eqscve.f#L159-L160)). Stored: `TABLENV(·,·,1..6)` = $`\log P`$, $`\log\rho`$, $`\partial\ln\rho/\partial\ln T`$, $`\partial\ln\rho/\partial\ln P`$, $`c_P`$, $`dU/dT`$.
4. **Derivatives,** by three-point Lagrange differentiation in $`\ln T`$ and $`\ln P`$: of $`\partial\ln\rho/\partial\ln T`$ in $`\ln P`$ and $`\ln T`$, of $`\partial\ln P/\partial\ln\rho`$ in $`\ln\rho`$, of $`\ln c_P`$ in $`\ln T`$, and of $`dU/dT`$ in $`\ln P`$ and $`\ln T`$; stored in columns 7–12. The derivative of $`\ln c_P`$ in $`\ln P`$, `QCPP`, is computed but not stored ([line 218](https://github.com/yreclab/yrec/blob/7be4133/src/setscv.f#L218), unused?). Of the table, [`EQSCVE`](eqscve.f.md#eqscve) reads columns 1–6 and [`EQSCVG`](eqscvg.f.md#eqscvg) column 1; columns 7–12 are read nowhere at 7be4133.

    **The comment's list of derivatives is stale.** The list before the loop ([lines 173–179](https://github.com/yreclab/yrec/blob/7be4133/src/setscv.f#L173-L179)) names `D LN CP / D LN P`, "D LN DEL(AD)/D LN P," and "D LN DEL(AD)/D LN T," but columns 7–12 hold `QDTP`, `QDTT`, `QPDD`, `QCPT`, `QAP`, and `QAT` ([lines 245–250](https://github.com/yreclab/yrec/blob/7be4133/src/setscv.f#L245-L250)): The derivatives of $`dU/dT`$ (`QAP`, `QAT`: [lines 225–236](https://github.com/yreclab/yrec/blob/7be4133/src/setscv.f#L225-L236)) take the place of those of $`\nabla_\mathrm{ad}`$, and `QCPP`, $`d\ln c_P/d\ln P`$, is computed ([line 218](https://github.com/yreclab/yrec/blob/7be4133/src/setscv.f#L218)) but not stored.

**Changed since `rp_1`.** The module variable `IDT` is renamed `IDTSCV` (in `SCVEOS_MOD`, also used by `EQSCVE` and `EQSCVG`); the unused `/NMLPAR/` is dropped; otherwise declarations only: COMMON blocks to modules, `IMPLICIT NONE`.

## Bugs, by priority

1. **(harmless in the runs)** **`QSMIXT` reads the entropy of mixing beyond the lower row's pressures.** ([lines 150–151](https://github.com/yreclab/yrec/blob/7be4133/src/setscv.f#L150-L151)) The temperature derivative of `SMIX` at row `I`, point `J` takes `SMIX(IDTSCV..IDTSCV+2, J)`, but the first loop sets `SMIX(I',J)` only for `J` up to `NPTSX(I')` ([lines 38–39](https://github.com/yreclab/yrec/blob/7be4133/src/setscv.f#L38-L39)). In the shipped tables (`input/eos/scv/h_tab_i.dat`) `NPTSX` grows with temperature (30 points at $`\log T = 2.10`$, 38 at $`3.54`$, 49 at $`3.62`$, and 76 from $`5.14`$), so at the high-pressure end of a row with more points than the row below, the lower neighbor's value is one that was never set (zero in practice, as a module array). `QSMIXT` enters $`\partial\ln S/\partial\ln T`$ and so $`c_P`$, column 5 ([lines 153–154](https://github.com/yreclab/yrec/blob/7be4133/src/setscv.f#L153-L154), [lines 159–160](https://github.com/yreclab/yrec/blob/7be4133/src/setscv.f#L159-L160)), which EQSCVE interpolates, and EQSCVE can use such points: At its lowest row `IDTSCV` it reads pressures up to `NPTSX(IDTSCV)` ([eqscve.f, lines 102–128](https://github.com/yreclab/yrec/blob/7be4133/src/eqscve.f#L102-L128)), and that row's derivative used row `IDTSCV-1`. Only with `LSCV` (off by default, [nmlpar_mod.f, line 258](https://github.com/yreclab/yrec/blob/7be4133/src/nmlpar_mod.f#L258); on in several test-suite cases, such as `Test_m0p3feh+0p0GS98_scv_ZAMS`).

    **A possible fix,** with the protection the code already uses for `QCPT` ([lines 219–223](https://github.com/yreclab/yrec/blob/7be4133/src/setscv.f#L219-L223)), which takes the neighbor's last point at a lower pressure:

    ```diff
    --- a/src/setscv.f
    +++ b/src/setscv.f
    @@ -147,8 +147,15 @@
     C ENTROPY.  OBEYS ADDITIVE VOLUME RULE, BUT ALSO NEED TO INCLUDE THE
     C ENTROPY OF MIXING.
                 S0 = X*SX + Y*SY + SMIX(I,J)
    -            QSMIXT = FTD(1)*SMIX(IDTSCV,J)+FTD(2)*SMIX(IDTSCV+1,J)+
    -     *               FTD(3)*SMIX(IDTSCV+2,J)
    +C 11/09/26 KC via Claude
    +C code changed to keep the neighbor rows within their own pressures,
    +C as for QCPT below.
    +            QSMIXT = 0.0D0
    +            DO K = 1,3
    +               II = IDTSCV+K-1
    +               JJ = MIN(NPTSX(II),J)
    +               QSMIXT = QSMIXT + FTD(K)*SMIX(II,JJ)
    +            END DO
     C D LN S/ D LN T
                 QST0 = (X*SX*TABLEX(I,J,9) + Y*SY*TABLEY(I,J,9) +
          *              QSMIXT)/S0
    ```

    **Checked by running YREC** (Nov 9, 2026; a line added at each suspected path counted how often it was taken, the outputs otherwise unchanged). In all 32 runs with `LSCV` on, each call of `SETSCV` built 3,720 table points, of which 46 read an unset `SMIX` of a neighboring row, at $`\log T`$ from 2.18 to 5.14 and $`\log P`$ from 10 to 19. A second counting line in `EQSCVE`, where a model point's stencil reads such an entry of row `IDTSCV` (it does not cover the stencils shifted for smoothing), never fired, the $`0.04`$ and $`0.1\,M_\odot`$ cases included. With the page's fix, `testsuite/Test_m0p3feh+0p0GS98_scv_ZAMS` and `examples/run_standard_solar_model/Test_solarcal_noGS_norot` give identical `.track` and `.store` files. Intent: none found; the same code protects `QCPT` ([lines 219–223](https://github.com/yreclab/yrec/blob/7be4133/src/setscv.f#L219-L223)). The wrong entries were never read by a counted stencil in any run, and the fix changed no output, so the table is wrong but no result was; this is fragile code.

2. **(harmless in the runs)** **The same reads in `QDTT` and `QAT`, where a fix is undone.** ([lines 212–213](https://github.com/yreclab/yrec/blob/7be4133/src/setscv.f#L212-L213); [lines 226–231](https://github.com/yreclab/yrec/blob/7be4133/src/setscv.f#L226-L231)) `QDTT` reads `TABLENV(IDTSCV..IDTSCV+2, J, 3)` with no protection, and in the loop for `QAT` the line `QR(K) = TABLENV(ii,jj,6)` with `jj = min(NPTSX(ii),j)` is overwritten by the next, `QR(K) = TABLENV(IDTSCV+K-1,J,6)`, so the protection has no effect. Both read unset entries as `QSMIXT` does (the lower neighbor's entries at the high-pressure end of a row with more points than the row below, which were never set: [suspected bug 1](#b1)), but they go into columns 8 and 12, which nothing reads at 7be4133 (EQSCVE reads columns 1–6). Correct today; wrong as soon as a routine uses these columns.

    **A possible fix:**

    ```diff
    --- a/src/setscv.f
    +++ b/src/setscv.f
    @@ -209,8 +209,15 @@
     C DERIVATIVES OF D LN RHO/ D LN T
                QDTP = TABLENV(I,IDP,3)*FPD(1)+TABLENV(I,IDP+1,3)*FPD(2)
          *           +TABLENV(I,IDP+2,3)*FPD(3)
    -           QDTT = TABLENV(IDTSCV,J,3)*FTD(1)+TABLENV(IDTSCV+1,J,3)*FTD(2)
    -     *           +TABLENV(IDTSCV+2,J,3)*FTD(3)
    +C 11/09/26 KC via Claude
    +C code changed to keep the neighbor rows within their own pressures
    +C in QDTT, and to drop the line that undid it in QAT.
    +           QDTT = 0.0D0
    +           DO K = 1,3
    +              ii = IDTSCV+K-1
    +              jj = min(NPTSX(ii),j)
    +              QDTT = QDTT + TABLENV(ii,jj,3)*FTD(K)
    +           END DO
     C DERIVATIVES OF LN CP
                DO K = 1,3
                   QR(K) = DLOG(TABLENV(I,IDP+K-1,5))
    @@ -225,9 +232,8 @@
     C DERIVATIVES OF DU/DT
                DO K = 1,3
                   ii = IDTSCV+K-1
    -            jj = min(NPTSX(ii),j)
    -            QR(K) = TABLENV(ii,jj,6)
    -              QR(K) = TABLENV(IDTSCV+K-1,J,6)
    +              jj = min(NPTSX(ii),j)
    +              QR(K) = TABLENV(ii,jj,6)
                END DO
                QAT = QR(1)*FTD(1)+QR(2)*FTD(2)+QR(3)*FTD(3)
                DO K = 1,3
    ```

    **Checked by running YREC** (Nov 9, 2026; a line added at each suspected path counted how often it was taken, the outputs otherwise unchanged). As for `QSMIXT` ([suspected bug 1](#b1)), 46 of each call's 3,720 points read unset entries, in all 32 runs with `LSCV` on. With the page's fix, `testsuite/Test_m0p3feh+0p0GS98_scv_ZAMS` and `examples/run_standard_solar_model/Test_solarcal_noGS_norot` give identical `.track` and `.store` files, as expected, since columns 8 and 12 are read nowhere. Intent: The protected lines at [lines 220–229](https://github.com/yreclab/yrec/blob/7be4133/src/setscv.f#L220-L229) show what was meant; [line 230](https://github.com/yreclab/yrec/blob/7be4133/src/setscv.f#L230) undoes them.
