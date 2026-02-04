.. _user-input:

User Input
==========

The Lionbolt input file is intended to be structured with some degree of freedom. Besides the :ref:`problem-key`, there is absolutely no requirement on the order in which various headers are defined. However, ordering of duplicate subheaders does in general matter, and determines important properties of the solve, for one example, the order in which to transport particles (see the :ref:`particles-header` header), or the order in which slabs are stacked (see the :ref:`mesh-header` header).

Note the following generally:

- The input file is case insensitive
- Use # to make a comment in the input file
- Blank lines are not read, anywhere

In the following guide, the keys which activate some option are listed first like :mod:`KEY`, but if the key demands variable inputs then they are listed afterwards like :mod:`val1 val2 val3`, then formatted like :mod:`KEY` :mod:`val1 val2 val3`. If the other inputs are fixed options, they will be denoted like :mod:`[ opt1 | opt2 | opt 3 ]`. Required options are designated with ``REQUIRED``. Options that are required depending on a particular option are designated like ``REQUIRED : PROBLEM GENERAL``.

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

This key defines the mesh to use for the problem.

.. code-block::
    
    MESH
        GMSH         /absolute/path/to/mesh/file.msh
        TRANSLATE    Tx Ty Tz
        SCALE        Sx Sy Sz
        SLAB
            THICKNESS    T
            ELEMENTS     N
            STRUCTURE    [ LINEAR | LOGARITHMIC ]
            MATERIAL     mat
        END
    END

:mod:`GMSH` :mod:`/absolute/path/to/mesh/file.msh` ``REQUIRED IF : PROBLEM GENERAL``

.. container:: vbarlb
    
    Specifies a 3D mesh. :mod:`/absolute/path/to/mesh/file.msh` specifies the absolute path to the file. To understand how to construct the mesh file, such that you can specify the beam, index material domains, etc., see the :ref:`creation-of-a-mesh` section in the :ref:`Quickstart <quickstart>` page. To understand how to define the materials themselves, see the :ref:`materials-header`.

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
        
        Index of the material for this slab. To understand how to define the materials themselves, see the :ref:`materials-header`.
        
        By default, it a material index is not provided, material 1 is taken.

.. _materials-header:

MATERIALS
~~~~~~~~~

This key defines the materials to be used in the problem. Note, the material definitions given here are entirely used to construct the cross section library with :ref:`nittanyphysics`. If the user wants to provide their own cross section library (WIP), they do not need a materials header.

In general, the user should ensure that the number of materials specified here match up with the materials specified in the mesh, whether in a mesh file or in the :mod:`SLAB` subheaders in :ref:`mesh-header`.

.. code-block::
    
    MATERIALS
        [MATERIAL NAME]
            DENSITY rho
            Atom    NAtoms
        END
    END

:mod:`[MATERIAL NAME]` ``REQUIRED``

.. container:: vbarlb
    
    The user-defined name for a material, used for certain printouts. Spaces are allowed. Case is respected.
    
    Any number of material subheaders can be provided, as long as they match up with the number of materials specified in the mesh.

:mod:`DENSITY` :mod:`rho` ``REQUIRED``

.. container:: vbarlb
    
    The density of the material, in grams per cubic centimeter

:mod:`Atom` :mod:`NAtoms` ``REQUIRED``

.. container:: vbarlb
    
    :mod:`Atom` is the first atom of the material (given by atomic symbol), and :mod:`NAtoms` is the number of this atom in the material. Material cross sections are then created using a mass-weighted mixture of these atoms.
    
    For materials with multiple atom types, any number of these lines can be provided
    
    In the future, :mod:`Atom` will be generalized to allow for special molecule/material names that are given specialized cross sections in :ref:`NittanyPhysics`.

ANGULAR
~~~~~~~

.. code-block::
    
    ANGULAR
        PNSCATTERING L
    END

:mod:`PNSCATTERING` :mod:`L` ``REQUIRED``

.. container:: vbarlb
    
    The global Legendre order that is used in the :math:`P_{N}` scattering treatment, and thus defines the angular discretization regardless of discretization method (of which currently only :math:`S_{N}` is implemented). 
    
    Note that the angular discretization method for a given particle is specified in :ref:`particles-header`, where different particles can have different discretization methods.

.. _particles-header:

PARTICLES
~~~~~~~~~

.. code-block::
    
    PARTICLES
        [ ELECTRONS | PHOTONS ]
            STRUCTURE   
            ANGULAR     [ SN ]
            SOLVER      [ GMRES | SI ]
            NOSCATTER
        END
    END

:mod:`[ ELECTRONS | PHOTONS ]` ``REQUIRED``

.. container:: vbarlb
    
    The particle to be solved. Multiple such subheaders can, of course, be provided, and this will also determine the particle coupling. That is, during a solution, a particle will be coupled only to the particles which have been solved before it, assuming that coupling cross sections are nonzero for these particles.
    
    Furthermore, note that a particle can be specified any number of times, as long as it is non-consecutively. In this case, the particle is not considered to couple to its previous instances, but this can be useful for studying, for instance, Bremsstrahlung production (to first order) in coupled photon-electron transport, by specifying :mod:`PHOTONS` then :mod:`ELECTRONS` then :mod:`PHOTONS`.
    
    In the future, protons and positrons will be implemented.
    
    :mod:`STRUCTURE` ``REQUIRED``
    
    .. container:: vbarlb
        
        sfdsdgedsg
        
    :mod:`ANGULAR` :mod:`SN` ``REQUIRED``
    
    .. container:: vbarlb
        
        The angular discretization method for this particle. Currently only the discrete ordinates method (:math:`S_{N}`) is implemented, but in the future, the real spherical harmonics expansion     (:math:`P_{N}`) will be implemented.
        
    :mod:`SOLVER` :mod:`[ GMRES | SI ]` ``REQUIRED``
        
    .. container:: vbarlb
        
        The iterative solver to be used for space-angle inversion of the Boltzmann transport equation -- the Generalized Minimal Residual Method [CITE] (GMRES), or Source Iteration [CITE] (SI). 
        
        At the moment, there is no specific plan to implement any more solvers, but this is something that could be done very simply in Lionbolt due to the structure of the program. If any solvers are implemented soon, they will likely come from SPARSKIT [CITE], which would be very readily implemented as the file :mod:`third_party/iters.f` contains all of SPARSKIT's iterative solvers in a form with which Lionbolt is designed to easily interface, as the implementation of GMRES used by Lionbolt is in this file.
        
    :mod:`NOSCATTER`
    
    .. container:: vbarlb
        
        An optional input that takes zero scattering cross section for the given particle. Useful for studying primary beams.

BEAM
~~~~




Example Input File
------------------

Below, we give an input file that would allow the user to perform coupled photon-electron transport in a 30 x 30 x 30 cm water tank.

.. code-block::
    
    PROBLEM GENERAL
    
    MESH
        GMSH     /absolute/path/to/mesh/file.msh
        SCALE    30.0 30.0 30.0
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
            STRUCTURE    0.001:5.4:25
            ANGULAR      SN
            SOLVER       GMRES
            NOSCATTER
        END
    END
    
    BEAM
        POLYCHROMATIC    /absolute/path/to/linac/spectrum.txt
        AXIS             0.0  0.0 -1.0
        ORIGIN           0.0  0.0  130.0
        CUTOUT           RECTANGLE 100.0 10.0 10.0 0.0
        SPHERICAL
    END
    
    STORAGELIMITED
    DEBUG