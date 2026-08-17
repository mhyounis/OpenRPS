LinearOperatorClass
===================

This is an **abstract** type, meaning of course that it can not be used to define an allocated object, but instead serves as a common base across various types ('extensions' of this type) that share several similarities.

In Lionbolt, this type works to eventually define the various operators whose operations are the focus of Lionbolt. The base consists of pointers to the objects describing space (:ref:`meshclass`), angle (:ref:`angularclass`), and cross section (:ref:`xstype`) discretization, in addition to a matrix multiplication procedure, a matrix inversion procedure, a build procedure (which is actually a generic interface to several different build procedures that assemble important parts of the operator but allow for re-assembly without deleting the entire object), and finally a destroy procedure. The multiply and inverse procedures specifically apply to objects of the :ref:`spaceanglevector` type. 

.. attention:: You should generally not interact with the linear operators except to build, multiply, invert, and destroy, or to assign specific objects (mentioned with the existing concrete extensions). If you attempt to assign any other objects then you open yourself up to unhandled errors.

Build, Apply, Destroy
---------------------

The build routines turn an uninitiated LinearOperator declaration into an object that can be used to multiply and invert on a :ref:`spaceanglevector` object. Notably, you can ONLY build with objects that are targets. See below for an example of how to use the build routines:

.. code-block:: fortran
    
    Type (BoltzmannOp)             :: Op ! BoltzmannOp can be replaced with any operator
    Type (MeshClass),       Target :: mesh
    Type (AngularClass),    Target :: angular
    Type (XSType),          Target :: XS
    Type (SpaceAngleVector)        :: v
    
    <Initialize and populate mesh, angular, XS, and v>
    
    ! Now there are four valid ways to call build. 
    ! If any of these are re-called then the operator is updated with the new quantities
    call Op%Build (mesh, angular, XS) ! Builds entire object in one go
    call Op%Build (mesh)              ! Builds only mesh and space-related attributes of the operator
    call Op%Build (mesh, angular)     ! Builds only angular-related attributes of the operator. (mesh is required here)
    call Op%Build (angular, XS)       ! Builds only cross-section-related attributes of the operator. (angular is required here)
    
    ! Now apply to v
    call Op%MatVec (v)
    
    ! Or invert on v
    call Op%MatInv (v)
    
    ! Destroy
    call Op%Destroy ()

Existing Concrete Extensions
----------------------------

The following operators are implemented.

.. data:: TransportOp
    
    The transport operator $T = \mathbf{\hat{k}}\cdot\nabla + \Sigma_{t}$. Access the guess vector (for GMRES inversion) using :mod:`%xg`.

.. data:: ScatteringOp
    
    The scattering operator $K = \int d\Omega' \ \Sigma_{s}(\mathbf{\hat{k}}'\rightarrow\mathbf{\hat{k}})\times$. If you want to perform delta-down scattering, then you can access a unique build procedure, :mod:`BuildDeltaDown (XSdd(:))`, where :mod:`XSdd (:)` is a rank-1 real array containing the delta-down cross sections per material. You can do this without destroying, and additionally, you can switch back to full angular scattering by rebuilding with :mod:`XS`.

.. data:: BoltzmannOp
    
    The Boltzmann operator $L = T - K$, or, if :mod:`%Tprecond = .TRUE.`, this is actually $T^{-1}L = 1 - T^{-1}K$, the preconditioned Boltzmann operator. While building, if your :mod:`AngularClass` object is $S_{N}$, :mod:`%Tprecond` is automatically set to :mod:`.TRUE.`, but can nonetheless be manually changed.
    
    Note also, this operator will contain instances of T and K, via objects :mod:`T` and :mod:`K`. It is not recommended to have separate instances of these operators if doing a full Boltzmann solve (except in the case of carrying a spare $K$ operator for coupling between particles/energy groups).