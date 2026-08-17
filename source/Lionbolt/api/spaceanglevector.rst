.. _spaceanglevector:

SpaceAngleVector
================

Objects of this type can be acted upon by objects of the linear operator class. They are therefore generally meant to contain sources and angular fluences. In order to initialize them, use:

.. code-block:: fortran
    
    Type (MeshClass)        :: mesh
    Type (AngularClass)     :: angular
    Type (SpaceAngleVector) :: v
    
    <Initialize and populate mesh and angular>
    
    v = SpaceAngleVector (mesh, angular)

Note that this will allocate an array of length :mod:`mesh%NENK * angular%NI`, where :mod:`NENK` is the number of spatial degrees of freedom (i.e., the total number of nodes in the elemental mesh, thus including nodes whose spatial position is identical if they reside in different elements), and :mod:`NI` is the number of angular degrees of freedom (i.e. for $S_{N}$, :mod:`Nmu * Nphi` or :mod:`2 * (L + 1)**2`).

To access values of the array keep in mind that they will generally be stored in the following way:

.. code-block:: fortran
    
    value(e,k,i) = v%v(mesh%offset(e) + k + (i - 1) * angular%NI)

where on the LHS we have the value of some map at the element :mod:`e`, node (within the element) :mod:`k`, and angular index :mod:`i`. Since in general not every element will have the same number of nodes, we use the mesh offset array :mod:`mesh%offset(e)`, where :mod:`mesh%offset(e) + k` gives the index of the node :mod:`(e,k)` in the spatial degrees of freedom indexing system.