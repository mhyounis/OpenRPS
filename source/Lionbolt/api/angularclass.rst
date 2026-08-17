.. _angularclass:

AngularClass
============

Objects of this type carry information about angular discretization. At the moment, only $S_{N}$ angular discretization is implemented, so we will describe only how to initialize that.

One can initialize an object of this type using:

.. code-block:: fortran
    
    Type (AngularClass) :: angular
    Integer             :: L       ! Angular discretization parameter (described below)
    Character (*)       :: solver  ! Solver type for the operators eventually built from this ('SI' or 'GMRES')
    Logical             :: slab    ! Whether or not this is for a slab calculation 
    
    angular = AngularClass (L, solver, slab)

Note, the integer :mod:`L` corresponds to the Legendre order which fully integrates the polar angle in the discrete ordinates set. That is, if :mod:`Nmu` is the number of polar angles and :mod:`Nphi` is the number of azimuthal angles, then :mod:`Nmu = L + 1` and :mod:`Nphi = 2 * (L + 1)`.

Also, it may be rather clunky to include solver information in the angular object. The two options are :mod:`SI` and :mod:`GMRES`. We emphasize that this is where you'll set the solvers to be used when inverting a given operator that this object is used to build. This could be changed in the future.

There are no type-bound procedures at the moment.