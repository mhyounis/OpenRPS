.. _meshclass:

MeshClass
=========

Objects of this type carry information about the spatial discretization. How it is initialized is vastly different in the general (3D) case and the slab (1D) case, however, how it ends up being used in Lionbolt is entirely identical. After describing how a user can work with this object in both cases, we will discuss some of its important attributes, and then describe at a basic level what information it contains, primarily for developers.

General
-------

In the general case, one may initialize their mesh using:

.. code-block:: fortran
    
    Type (MeshClass) :: mesh
    
    mesh = MeshClass ('/path/to/GMSH/mesh.msh')
    
    ! OR
    
    call mesh%FromFile ('/path/to/GMSH/mesh.msh')

Notably, at the moment only meshes created in GMSH are compatible with Lionbolt. 

Now, however, while your mesh has been initialized, it is not yet ready for use. To make it ready for use, you must then use:

.. code-block:: fortran
    
    call mesh%PostProcess ()

This is inconvenient but currently necessary, however it will likely be changed in the future. It is needed because we must perform geometric and finite-element analysis on this mesh, i.e., determination of element volumes, face areas, creation of various shape function inner products, etc., yet you are given the freedom to translate and scale your mesh using:

.. code-block:: fortran
    
    Real (8) :: dx ! Translation in x
    Real (8) :: dy ! Translation in y
    Real (8) :: dz ! Translation in z
    Real (8) :: Sx ! Scale factor in x
    Real (8) :: Sy ! Scale factor in y
    Real (8) :: Sz ! Scale factor in z
    
    call mesh%translate ([ dx, dy, dz ])
    call mesh%scale     ([ Sx, Sy, Sz ])

These operations generally change the results of geometric and finite element analysis in a manner not always trivial to account for. In the future, we may make it so that translating or scaling can be done after post-processing, in which case post-processing will be absorbed into the initialization routines, but the translation and scale routines will become a time sink as we will need to modify the results of post-processing.

If one wishes to empty a mesh object such that it can be regenerated, they can use the destroy procedure:

.. code-block:: fortran
    
    call mesh%Destroy ()

Slab
----

In the slab case one must add slabs one-by-one to build up a geometry. For example:

.. code-block:: fortran
    
    Type (MeshClass) :: mesh
    Integer          :: num_elements ! Number of elements in this slab
    Real (8)         :: thickness    ! Thickness of this slab in cm
    Integer          :: mat_index    ! Index of the material (according to one's physics library) corresponding to this slab
    Character (*)    :: structure    ! Structure of the mesh ('linear' for constant sized elements, 
                                     !                        'logarithmic' for logarithmically sized elements, 
                                     !                         shallower depths are larger. Case insensitive)
    
    call mesh%AddSlab (num_elements, thickness, mat_index, structure)
    
    ... ! More slabs can be added

After one is finished constructing their geometry, they must finalize the object using the post-process procedure:

.. code-block:: fortran
    
    call mesh%PostProcess ()

If one wishes to empty a mesh object such that it can be regenerated, they can use the destroy procedure:

.. code-block:: fortran
    
    call mesh%Destroy ()

Useful Objects
--------------

The following are some of the more important user-facing attributes belonging to the mesh class:

.. code-block:: fortran
    
    Integer               :: NK
    Integer               :: NF
    Integer               :: NBF
    Integer               :: NE
    Integer               :: NENK
    Integer,  Allocatable :: offset       (:)
    Integer,  Allocatable :: connectivity (:)
    Real (8), Allocatable :: rg           (:,:)

We discuss each term individually.

:mod:`NK` is the number of global nodes in the mesh.

:mod:`NF` is the number of global faces in the mesh.

:mod:`NBF` is the number of boundary faces in the mesh.

:mod:`NE` is the number of elements in the mesh.

:mod:`NENK` is the number of spatial degrees of freedom in the mesh. In other words, each node in each element, despite being shared by multiple elements, counts as its own degree of freedom.

:mod:`offset` is the 'offset' array. Since not every element has the same number of nodes, we need a map from element and node index to spatial degree of freedom. Specifically, :mod:`offset(e) + k` gives the index of the node :mod:`(e,k)` in the spatial degrees of freedom indexing system.

:mod:`connectivity` is the 'connectivity' array. Specifically, :mod:`connectivity(sdof)` gives the global node index of a spatial dof :mod:`sdof`.

:mod:`rg` is the global mesh. It is indexed as :mod:`rg(iDir,kg)`, where :mod:`iDir` is the Cartesian direction and :mod:`kg` is the global node index.

For Developers
--------------

.. attention:: This section is WIP.