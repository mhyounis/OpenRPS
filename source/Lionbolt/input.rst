.. _user-input:

User Input
==========

The Lionbolt input file is intended to be structured with some degree of freedom. Besides the :ref:`problem-key`, there is absolutely no requirement on the order in which various headers are defined. However, ordering of duplicate subheaders does in general matter, and determines important properties of the solve, for one example, the order in which to transport particles (see the :ref:`particles-header` header), or the order in which slabs are stacked (see the :ref:`mesh-header` header).

Note the following generally:

- The input file is case insensitive, except for material names, and partially so for particle names (see below).
- Use # to make a comment in the input file.
- Blank lines are not read, anywhere.
- The number of spaces/tabs leading/following a line does not matter.
- If using the Lionbolt submit script, then file paths in the input file can be absolute OR relative to the directory containing the input file itself (which can be useful). If they are not using the submit script, then as usual, the relative paths given in an input file must be relative to the directory from which the user is executing Lionbolt.

In the following guide, the keys which activate some option are listed first like :mod:`KEY`, but if the key demands variable inputs then they are listed afterwards like :mod:`val1 val2 val3`, then formatted like :mod:`KEY` :mod:`val1 val2 val3`. If the other inputs are fixed options, they will be denoted like :mod:`[ opt1 | opt2 | opt 3 ]`. Required options are designated with ``REQUIRED``. Options that are required depending on a particular option are designated like ``REQUIRED IF : PROBLEM GENERAL``.

Input Headers
-------------

.. _problem-key:

PROBLEM
~~~~~~~

This key indicates the problem type to be solved by Lionbolt.

.. code-block::
    
    PROBLEM [ GENERAL | SLAB ]

:mod:`PROBLEM` :mod:`[ GENERAL | SLAB ]` ``REQUIRED``

.. container:: vbarlb
    
    :mod:`GENERAL` indicates to perform a full, 5D phase space solve (3D geometry, 2D angular space), while :mod:`SLAB` indicates to perform an infinite slab, 2D phase space solve (1D geometry, 1D angular space).

.. _mesh-header:

MESH
~~~~

This header defines the mesh to use for the problem.

.. code-block::
    
    MESH
        GMSH         path/to/mesh/file.msh
        TRANSLATE    Tx Ty Tz
        SCALE        Sx Sy Sz
        SLAB
            THICKNESS    T
            ELEMENTS     N
            STRUCTURE    [ LINEAR | LOGARITHMIC ]
            MATERIAL     mat
        END
    END

:mod:`GMSH` :mod:`path/to/mesh/file.msh` ``REQUIRED IF : PROBLEM GENERAL``

.. container:: vbarlb
    
    Specifies a 3D mesh. :mod:`path/to/mesh/file.msh` specifies the path (absolute or relative) to the file. To understand how to construct the mesh file, index material domains, etc., see the :ref:`creation-of-a-mesh` section in the :ref:`Quickstart <quickstart>` page. To understand how to define the materials themselves (if you are using NittanyPhysics cross sections), see the :ref:`materials-header` header.

:mod:`TRANSLATE` :mod:`Tx Ty Tz`

.. container:: vbarlb
    
    Translates the user's mesh, with translation vector :mod:`Tx Ty Tz`. 
    
    If both :mod:`TRANSLATE` and :mod:`SCALE` keys are present, translation is applied before scaling.

:mod:`SCALE` :mod:`Sx Sy Sz`

.. container:: vbarlb

    Scales the user's mesh, with scaling vector :mod:`Sx Sy Sz`. 
    
    If both :mod:`TRANSLATE` and :mod:`SCALE` keys are present, translation is applied before scaling.

:mod:`SLAB` ``REQUIRED IF : PROBLEM SLAB``

.. container:: vbarlb
    
    This subheader is used to specify a slab to be used in the solution. Importantly, multiple slabs can be stacked, and their thicknesses, mesh structure, elements, and material specifications will be used to construct the individual slabs.
    
    :mod:`THICKNESS` :mod:`T` ``REQUIRED``
    
    .. container:: vbarlb
        
        Thickness of this slab.
        
    :mod:`ELEMENTS` :mod:`N` ``REQUIRED``
    
    .. container:: vbarlb
        
        Number of mesh elements in this slab.
        
    :mod:`STRUCTURE` :mod:`[ LINEAR | LOGARITHMIC ]` ``REQUIRED``
    
    .. container:: vbarlb
        
        Spacing of the mesh elements. Linear gives linearly spaced mesh elements, logarithmic gives logarithmically spaced elements (more elements at shallower depths).
        
    :mod:`MATERIAL` :mod:`mat`
    
    .. container:: vbarlb
        
        Index of the material for this slab. To understand how to define the materials themselves, see the :ref:`materials-header` header.
        
        By default, it a material index is not provided, material 1 is taken.

.. _materials-header:

MATERIALS
~~~~~~~~~

This header defines the materials to be used in the problem. Note, the material definitions given here are entirely used to construct the cross section library with :ref:`nittanyphysics`. If the user wants to provide their own cross section library (this is WIP as of now), they do not need a materials header, however they will still need to be careful with how the materials in their mesh definition relate to the materials in their provided library.

In general, the user should ensure that the number of materials specified here match up with the materials specified in the mesh, whether in a mesh file or in the :mod:`SLAB` subheaders in :ref:`mesh-header`.

.. code-block::
    
    MATERIALS
        <MATERIAL NAME>
            DENSITY rho
            Atom    NAtoms
        END
    END

:mod:`<MATERIAL NAME>` ``REQUIRED``

.. container:: vbarlb
    
    The user-defined name for a material, used for certain printouts. Spaces are allowed. Case is respected.
    
    Any number of material subheaders can be provided, as long as they match up with the number of materials specified in the mesh.

    :mod:`DENSITY` :mod:`rho` ``REQUIRED``
    
    .. container:: vbarlb
        
        The density of the material, in grams per cubic centimeter
    
    :mod:`Atom` :mod:`NAtoms` ``REQUIRED``
    
    .. container:: vbarlb
        
        :mod:`Atom` is the first atom of the material (given by atomic symbol), and :mod:`NAtoms` is the number of this atom in the material. Material cross sections are then created using a mass-weighted mixture of these atoms.
        
        For materials with multiple atom types, any number of these lines can be provided.
        
        In the future, :mod:`Atom` will be generalized to allow for special molecule/material names that are given specialized cross sections in :ref:`NittanyPhysics`.
    
    .. :mod:`ZEFF`
    
    .. .. container:: vbarlb
        
    ..     User can here either provide the effective atomic number manually, or give the keys X, Y, Z, to use formulae to calculate the Zeff based on the atoms and numbers of atoms provided.
        
    ..     By default, Zeff is just taken as the total number of protons in the material.

ANGULAR
~~~~~~~

.. code-block::
    
    ANGULAR
        PNSCATTERING L
    END

:mod:`PNSCATTERING` :mod:`L` ``REQUIRED``

.. container:: vbarlb
    
    The global Legendre order that is used in the $P_{N}$ scattering treatment, and thus defines the angular discretization regardless of discretization method (of which currently only $S_{N}$ is implemented). 
    
    Note that the angular discretization *method* for a given particle is specified in :ref:`particles-header`, where different particles can have different discretization methods.

.. _particles-header:

PARTICLES
~~~~~~~~~

.. code-block::
    
    PARTICLES
        <PARTICLE NAME>
            PHYSICS     [ PHOTONS | ELECTRONS ]
            GRID        [ LINEAR | LOGARITHMIC | EXPONENTIAL | Emin:Emax:G | fname ]
            MIN         Emin
            MAX         Emax
            GROUPS      G
            ANGULAR     [ SN ]
            SOLVER      [ GMRES | SI ]
            NOSCATTER
        END
    END
    
.. later: ANGULAR [ SN | PN ] L, and remove the global angular block. But will have to figure out mapping between orders. Just gotta do the derivation

:mod:`<PARTICLE NAME>` ``REQUIRED``

.. container:: vbarlb
    
    The particle to be solved. Multiple such subheaders can be provided, and this will also determine the particle coupling. That is, a particle will be coupled only to the particles which have been solved *before* it, assuming that these particles couple in the first place. Note however, particle names can not be repeated. Still, physical properties of particles (i.e., whether the particle assumes photon physics or electron physics, etc.) *can* be repeated (see :mod:`PHYSICS` below).
    
    Also note, the particle name provided is case-sensitive in the standard out file, however, it is always lowercase in the HDF5 file.
    
    :mod:`PHYSICS` :mod:`[ PHOTONS | ELECTRONS ]` ``REQUIRED IF : USING NITTANYPHYSICS AND PARTICLE NAME IS NOT AN IMPLEMENTED NITTANYPHYSICS PARTICLE``
    
    .. container:: vbarlb
        
        This is the name of the particle that is used to generate the physics of the particle being specified. It is only required when :mod:`<PARTICLE NAME>` does not correspond to one of the options of this :mod:`PHYSICS` option, i.e., particles implemented in NittanyPhysics.
        
    :mod:`GRID` :mod:`[ LINEAR | LOGARITHMIC | EXPONENTIAL | Emin:Emax:G | fname ]` ``REQUIRED``
    
    .. container:: vbarlb
        
        One either specifies the spacing of the energy grid using :mod:`[ LINEAR | LOGARITHMIC | EXPONENTIAL ]` (in which case they then need to supply :mod:`MIN`, :mod:`MAX`, and :mod:`GROUPS`, see the options below), OR, they can specify a (linear) grid using its min, max, and number of groups formatted like :mod:`Emin:Emax:G`, OR, they can provide a file with their own energy grid points in rows (this file must be sorted in descending order, i.e., highest energies first). 
    
    :mod:`MIN` :mod:`Emin` ``REQUIRED IF : GRID IS [ LINEAR | LOGARITHMIC | EXPONENTIAL ]``
    
    .. container:: vbarlb
        
        The minimum energy of the energy grid.
    
    :mod:`MAX` :mod:`Emax` ``REQUIRED IF : GRID IS [ LINEAR | LOGARITHMIC | EXPONENTIAL ]``
    
    .. container:: vbarlb
        
        The maximum energy of the energy grid.
    
    :mod:`GROUPS` :mod:`G` ``REQUIRED IF : GRID IS [ LINEAR | LOGARITHMIC | EXPONENTIAL ]``
    
    .. container:: vbarlb
        
        The number of groups (bins) in the energy grid (note, number of grid points is therefore :mod:`G` plus one).
    
    :mod:`ANGULAR` :mod:`SN` ``REQUIRED``
    
    .. container:: vbarlb
        
        The angular discretization method for this particle. Currently only the discrete ordinates method ($S_{N}$) is implemented, but in the future, the real spherical harmonics expansion ($P_{N}$) will be implemented.
        
    :mod:`SOLVER` :mod:`[ GMRES | SI ]` ``REQUIRED``
        
    .. container:: vbarlb
        
        The iterative solver to be used for space-angle inversion of the Boltzmann transport equation -- the Generalized Minimal Residual Method :cite:`Saad1986` (GMRES), or Source Iteration :cite:`Battista2019` (SI). 
        
        At the moment, there is no specific plan to implement any more solvers, but this is something that could be done very simply in Lionbolt due to the structure of the program. If any solvers are implemented soon, they will likely come from SPARSKIT :cite:`SPARSKIT`, which would be very readily implemented as the file :mod:`third_party/iters.f` contains all of SPARSKIT's iterative solvers in a form with which Lionbolt is designed to easily interface, as the implementation of GMRES used by Lionbolt is in this file.
        
    :mod:`NOSCATTER`
    
    .. container:: vbarlb
        
        An optional input that takes zero scattering cross section for the given particle. Useful for studying primary beams.

.. _beam-header:

BEAM
~~~~

This block defines a *beam*, which is a particle source. Multiple beams can be specified by using multiple such blocks.

.. code-block::
    
    BEAM
        PARTICLE    IND
        [ POLYCHROMATIC | MONOCHROMATIC ] [ FILE NAME | [ gs | ngs E0 dE ] ]
        [ SPHERICAL | PLANAR ]
        AXIS        [ k0x k0y k0z | theta ]
        ORIGIN      R0x R0y R0z
        CUTOUT      [ RECTANGLE | CIRCLE | NONE ]    p1 p2 ...
        WEIGHT      w
    END

:mod:`PARTICLE` :mod:`IND` ``REQUIRED``

.. container:: vbarlb
    
    :mod:`IND` is The index of the particle (according to your :ref:`particles-header` header) which this beam sources. The first particle must be sourced at least once, but other particles may or may not have one or multiple sources.

:mod:`[ POLYCHROMATIC | MONOCHROMATIC ]` :mod:`[ FILE NAME | [ gs | ngs E0 dE ] ]` ``REQUIRED``

.. container:: vbarlb
    
    Information about the energy spectrum of the source. 
    
    If using :mod:`POLYCHROMATIC`, then one must specify a file name :mod:`FILE NAME`. The file must be formatted as so: simply have two columns which describe a discretized energy spectrum. The first column is the energy points (in MeV), and the second column is the (relative) value of the counts **per MeV**. The spectrum will be normalized by Lionbolt, but importantly it is still an **energy distribution** rather than an absolute count of particles.
    
    If using :mod:`MONOCHROMATIC`, then one must specify either:
        * The set of groups :mod:`gs` to populate, noting that they are populated such that the number of particles per unit energy is constant.
        * (**WIP** - still working out how to best refine the grid after inserting the manually specified groups) The number of groups :mod:`ngs` among which to split the energy range from :mod:`E0 - dE/2` to :mod:`E0 + dE/2`. Note, if this option is selected, then the group(s) defined by this input will be forced into your energy grid, maintaining the total number of groups, with any gridpoints that are too close to the newly created gridpoints spread out to half the distance to the next over gridpoint (in short, do not rely on your gridpoint structure being exactly, e.g., :mod:`LINEAR`, :mod:`LOGARITHMIC`). Furthermore, with this option you cannot use a custom energy grid (like :mod:`GRID fname` in the :mod:`PARTICLES` block).

:mod:`[ SPHERICAL | PLANAR ]` ``REQUIRED``

.. container:: vbarlb
    
    Whether to use a point-source/'spherical' angular distribution (particles are sourced radially from a point) or a planar angular distribution (particles are sourced along a single direction).

:mod:`AXIS` :mod:`[ k0x k0y k0z | theta ]` ``REQUIRED IF : PROBLEM GENERAL``

.. container:: vbarlb
    
    The axis of this beam. If using :mod:`PROBLEM GENERAL` then all three components of the direction vector must be provided. Note, if the vector is not normal then Lionbolt will normalize it.
    
    If using :mod:`PROBLEM SLAB` then only the angle of incidence :mod:`theta` is specified (in degrees). By default in the slab case (where this key is not required), 0 angle of incidence is used.
    
:mod:`ORIGIN` :mod:`R0x R0y R0z` ``REQUIRED IF : PROBLEM GENERAL``

.. container:: vbarlb
    
    The origin of the beam. 

:mod:`CUTOUT` :mod:`[ RECTANGLE | CIRCLE | NONE ]` :mod:`p1 p2 ...` ``REQUIRED IF : PROBLEM GENERAL``

.. container:: vbarlb
    
    Information about the cutout of the beam. The number and meaning of requested parameters :mod:`p1 p2 ...` depends on the beam cutout.
    
    The cutout normal vector is always the beam axis. Furthermore, the beam axis will be used in the definition of a beam coordinate system, which is initially defined by rotating the lab coordinate system such that the z-axis is along the beam axis. Further rotations can be applied in this frame depending on the cutout. The options and parameters are listed below.
    
    .. may want to be much more explicit about beam coordinate system. Maybe use Euler angle reasoning in direct terms of beam axis and the intrinsic rotation angles, or use figures. Maybe when I have more cutouts.
    
    :mod:`RECTANGLE` gives a rectangular beam cutout. There are four parameters, in order.
    
        1. Distance from beam origin at which cutout is defined.
        
        2. Angle of rotation about beam axis (fully defining beam coordinate system).
        
        3. Length of cutout along beam x-axis
            
        4. Length of cutout along beam y-axis.
    
    :mod:`CIRCLE` gives a circular beam cutout. There are two parameters, in order.
    
        1. Distance from beam origin at which cutout is defined.
        
        2. Radius of cutout at this distance.
    
    :mod:`NONE` gives a wide-open collimator. There are no parameters.

:mod:`WEIGHT` :mod:`w`

.. container:: vbarlb
    
    It is difficult to discuss this briefly, so you are referred to :ref:`a discussion of beam normalization in the Lionbolt theory page <normalization>`. However, note that this option only matters at all if multiple beams are being used (whether or not they describe the same particle), and also that the default for this option is always 1.

POSTPROCESSING
~~~~~~~~~~~~~~

Rather than use Terpdose to generate post-processing quantities like dose, one can generate them with Lionbolt and save them to the HDF5 output file. This can prevent a user from having to re-generate such quantities when using them within Terpdose (Terpdose will, when asked for a particular post-processing quantity, first check to see if it's already been written).

.. code-block::
    
    POSTPROCESSING
        FLUENCE
        UNCOLLIDED
        ENERGY
        DOSE
        CHARGE
    END
    
:mod:`FLUENCE`

.. container:: vbarlb
    
    Create and save fluence maps for all energies and all particles.

:mod:`UNCOLLIDED`

.. container:: vbarlb
    
    Create and save uncollided angular fluence and fluence maps for all energies and all particles (ONLY IF their fully solved counterparts are being written in the first place).

:mod:`ENERGY`

.. container:: vbarlb
    
    Create and save an energy deposition map.

:mod:`DOSE`

.. container:: vbarlb
    
    Create and save a dose deposition map.

:mod:`CHARGE`

.. container:: vbarlb
    
    Create and save a charge deposition map.

OPTIONS
~~~~~~~

Options don't live in any block. These are keys that can get picked up anywhere.

.. code-block::
    
    STORAGELIMITED
    MEMORYLIMITED
    DEBUG

:mod:`STORAGELIMITED`

.. container:: vbarlb
    
    This stops the program from saving angular fluences, which can take up a significant amount of disk storage (on the order of 10s - 100s of GB for realistic discretization parameters). Note, if you use this option without explicitly specifying some post-processing, your solve will essentially output nothing that you can actually work with.
    
    Lionbolt does not have as many post-processing capabilities as Terpdose, so you should generally be aware of whether your application will need angular fluences or perhaps only fluences or deposition maps, prior to running your input file.

:mod:`MEMORYLIMITED`

.. container:: vbarlb
    
    This tells the program not to store angular fluences of previous energy groups and particles in memory, but rather, to write them to disk (as they must be later used for coupling). 
    
    AT THE MOMENT this option is useless, as Lionbolt ALWAYS writes these quantities to disk, so leaving it off will not change anything. Lionbolt will be able to store these arrays in memory once MPI is implemented (as not using this option is really only appropriate on HPC clusters).

:mod:`DEBUG`

.. container:: vbarlb
    
    This puts more profiling information in the standard output file. Can be useful for developers or those interested in profiling.

.. later add raytracing, when its validated.

Example Input Files
-------------------

Below, we give several valid input files which can give you some ideas about compatibilities and typical settings.

An input file that would allow the user to perform coupled photon-electron transport in water.

.. code-block::
    
    PROBLEM GENERAL
    
    MESH
        GMSH     path/to/mesh/file.msh
    END
    
    MATERIALS
        WATER
            DENSITY 1.0 # g / cc
            H   2
            O   1
        END
    END
    
    ANGULAR
        PNSCATTERING    15
    END
    
    PARTICLES
        PHOTONS
            GRID         0.001:5.4:25
            ANGULAR      SN
            SOLVER       SI
        END
        ELECTRONS
            GRID         0.001:5.4:50
            ANGULAR      SN
            SOLVER       GMRES
        END
    END
    
    BEAM
        PARTICLE 1 # The particle sourced by this beam is the first one listed in PARTICLES
        POLYCHROMATIC    path/to/linac/spectrum.txt
        AXIS             0.0  0.0 -1.0                 # Gives a beam pointing straight down the z-axis. Reference frame is that of the mesh.
        ORIGIN           0.0  0.0  130.0               # Localizes the origin of the beam
        CUTOUT           RECTANGLE 100.0 10.0 10.0 0.0 # Cutout with its parameters
        SPHERICAL                                      # Point source, generates fluence radially outwards from the origin.
    END
    
    STORAGELIMITED
    DEBUG

References
----------

.. bibliography::
    :filter: docname in docnames
    :style: unsrt