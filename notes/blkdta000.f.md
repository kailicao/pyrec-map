## Explanation

**Purpose.** A `BLOCK DATA` unit (unnamed) that sets the initial values of COMMON blocks used by the OPAL equation-of-state routines: the hydrogen abundances of the tables, the number of temperatures in each density row, and the order in which the EOS quantities are returned.

**How it fits.**
- **Who uses it:** no one calls it; the linker includes it. The blocks it initializes are read by [[esac.f#ESAC|ESAC]], [[readco.f#READCO|READCO]], [[rhoofp.f#RHOOFP|RHOOFP]], [[t6rinterp.f#T6RINTERP|T6RINTERP]], [[eqbound.f#EQBOUND|EQBOUND]] and [[radsub.f#RADSUB|RADSUB]].
- **COMMON blocks:** `/A/` (the tables `XZ` and their grids; here only `XA`), `/B/` (`INDEX`, `NTA`), `/AA/` (declared, nothing set).

**What it sets.**
- `XA` = 0, 0.2, 0.4, 0.6, 0.8: the hydrogen mass fractions of the tables ($M_X = 5$).
- `NTA(1:77)`: for each of the 77 density values, the number of temperatures the table has (56 for the first 37, 54 for the next 7, then fewer, down to 7). The tables are thus not rectangular.
- `INDEX` = 1, …, 10: the order of the EOS quantities in the output array. [[esac.f#ESAC|ESAC]]'s header explains how to change it to return only $\Gamma_1$, for example.

The array sizes (`MX=5`, `MV=10`, `NR=77`, `NT=56`) must match those in the routines that use the blocks.

## Questions for the experts

1. **Which EOS tables.** The values belong to one version of the OPAL EOS tables (the original one, probably, since the 2001 and 2006 versions have their own files, `esac01.f`, `esac06.f`). Are they still used, or only the 2006 path?
2. **`/AA/`.** It is declared here but no value is set. Can the declaration go?

### BLOCK_DATA

Initial values for `/A/` (`XA`) and `/B/` (`NTA`, `INDEX`) of the OPAL EOS routines.
