# Rotation and mass loss

*In Python: [[new/pyrec/rotation/__init__.py|`pyrec.rotation`]].*

## 3.10 Rotation: `Distortion`, `RotationLaw`, `RotationTransport`, `WindLaw`, `RotationStep`

**`RotationStep`. Responsibility:** evolve the internal rotation over one model step, as [[getw.f#GETW|`GETW`]] does: without instabilities, $\Omega$ from $j$ and the wind; with them, $N$ diffusion substeps, each with the structure interpolated in time, the wind, mixing of convection zones, and transport of angular momentum and composition.

```fortran
type :: RotationStep
    type(Distortion) :: dist
    type(RotationLaw) :: law
    type(RotationTransport) :: transport
    class(WindLaw), allocatable :: wind        !! Absent: no wind.
contains
    procedure :: run
        !! (star, start, zones, dt, ierr) GETW. Substeps
        !! N = min(ceil(DWMAX/DTDIF), ceil(DTWIND/DTDIF)).
    procedure, private :: midstep   !! (star, start, f) MIDMOD at fraction f.
    procedure, private :: check_j   !! CHECKJ: j > 0, convergence, Omega.
    procedure, private :: check_comp !! CHECKC: 0 <= X <= 1, cut substep.
end type

type :: Distortion
contains
    procedure :: factors   !! (star) FPFT with SHAPE, FUNC: f_P, f_T, <g>.
    procedure :: inertia   !! (star) MOMI, INTMOM: I and dI/dOmega.
    procedure :: quadrupole !! (star) GETQUA: the P2 potential (Zahn 1992).
end type

type :: RotationLaw
contains
    procedure :: omega_from_j  !! (star, lcz) GETROT; zones by WCZIMP.
    procedure :: solid_body    !! (star, jstart, jend) SOLID.
end type

type :: RotationTransport
    !! Diffusion coefficients and velocities on the interfaces (VCIRC);
    !! factors FW, FC, FES, FGSF, FMU, FSS (/VMULT/), Config%rot.
contains
    procedure :: secular
        !! (star, zones, dt, redo, ierr) SECULR: transport of j and of the
        !! composition by meridional circulation, GSF, secular and dynamical
        !! shear; redo : the substep must be shortened (LREDO).
end type

type, abstract :: WindLaw
contains
    procedure(dj_if), deferred :: domega
        !! (star, dt, dw) Change of the surface zone's Omega [rad s-1].
end type
type, extends(WindLaw) :: KawalerWind     !! WIND, COWIND
type, extends(WindLaw) :: MattWind        !! MWIND, MCOWIND, AMCALC
```

**Replaces:** [[getw.f#GETW|`GETW`]], [[midmod.f#MIDMOD|`MIDMOD`]], [[checkj.f#CHECKJ|`CHECKJ`]], [[checkc.f#CHECKC|`CHECKC`]], [[rotmix.f#ROTMIX|`ROTMIX`]], [[bursmix.f#BURSMIX|`BURSMIX`]] and [[bsrotmix.f#BSROTMIX|`BSROTMIX`]] (never run: `LBURS` is false; kept only if KC wants them, [Section 8](overview.md)); [[fpft.f#FPFT|`FPFT`]], [[shape.f#SHAPE|`SHAPE`]], [[func.f#FUNC|`FUNC`]], [[momi.f#MOMI|`MOMI`]], [[intmom.f#INTMOM|`INTMOM`]], [[getqua.f#GETQUA|`GETQUA`]]; [[getrot.f#GETROT|`GETROT`]], [[wczimp.f#WCZIMP|`WCZIMP`]], [[solid.f#SOLID|`SOLID`]] (and the uncalled [[wcz.f|`WCZ`]]); [[seculr.f#SECULR|`SECULR`]], [[vcirc.f#VCIRC|`VCIRC`]], [[setupv.f#SETUPV|`SETUPV`]], [[codiff.f#CODIFF|`CODIFF`]], [[getfc.f#GETFC|`GETFC`]], [[dadcoeft.f#DADCOEFT|`DADCOEFT`]], [[dcoeft.f#DCOEFT|`DCOEFT`]], [[ccoeft.f#CCOEFT|`CCOEFT`]], [[rotgrid.f#ROTGRID|`ROTGRID`]], [[eq2mod.f#EQ2MOD|`EQ2MOD`]], [[ndifcom.f#NDIFCOM|`NDIFCOM`]]; [[wind.f#WIND|`WIND`]], [[cowind.f#COWIND|`COWIND`]], [[mwind.f#MWIND|`MWIND`]], [[mcowind.f#MCOWIND|`MCOWIND`]], [[amcalc.f#AMCALC|`AMCALC`]]. Angular momentum and composition are transported by diffusion equations of the form
$$\rho r^2\,\frac{\partial j}{\partial t} = \frac{1}{r^2}\frac{\partial}{\partial r}\Bigl(\rho r^4 D_J\,\frac{\partial\Omega}{\partial r}\Bigr),$$
with $D_J$ from the instabilities' velocities, solved on the `ChiGrid`. The many work blocks that `SETUPV` and `VCIRC` share (`/INTVAR/`, `/VFACT/`, `/TAUKH/`, `/DIFAD2/`–`/DIFAD4/`) become components of `RotationTransport`, private to it.

## 3.11 Mass loss: `MassLossLaw`, `MassLoss`

**Responsibility:** set the rate $\dot M$ by a law, and apply the change of mass to the model, its convection zone and its angular momentum.

```fortran
type, abstract :: MassLossLaw
contains
    procedure(mdot_if), deferred :: rate
        !! (star) -> real(dp) dM/dt [Msun yr-1], < 0 for loss.
end type
type, extends(MassLossLaw) :: ConstantMassLoss   !! DMDT0
type, extends(MassLossLaw) :: ReimersMassLoss    !! CREIM, LREIMER

type :: MassLoss
    class(MassLossLaw), allocatable :: law
    real(dp) :: comp_acc(NSP)          !! Accreted composition (COMPACC).
contains
    procedure :: apply
        !! (star, dt, ierr) MASSLOSS, MDOT: limit the mass removed, rescale
        !! the mass coordinates, remove J, mix accreted matter in the CZ.
end type
```

**Replaces:** [[massloss.f#MASSLOSS|`MASSLOSS`]], [[mdot.f#MDOT|`MDOT`]]. The argument mismatch between them (MAIN question 2) cannot survive a checked interface; the development branch has already fixed it ("fix a CALL MDOT mismatch", [Section 7.3](overview.md)). `MASSLOSS`'s header calls it "experimental code and valid for Allard atmospheres only"; the design keeps it as it is and says so in the type's docstring.
