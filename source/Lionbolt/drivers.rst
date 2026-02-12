User-Defined Drivers
====================

.. show like a concept map??

At the moment, user-defined drivers are a WIP feature.

Lionbolt has been designed such that the user can opt to use the input file to carry out a solve, or, they can design their own 'driver,' i.e., their own solution sequence, relying on Lionbolt routines. To understand how to construct your own driver, read this page.

The Modular Structure of Lionbolt
---------------------------------

Lionbolt is deliberately intended to be highly modular, with inspiration from the GEANT4 project [CITE]. That is, it is intended that with minimal understanding of the workings of particular routines, but with a thorough understanding of the available set of routines, users can link together various procedures in order to create highly specialized solution sequences. As such, Lionbolt's routines are divided into 'public API' and 'internal' routines. The public API routines are those which are meant to be called in a particular, physically motivated sequence, from some main program file. They are named intuitively and generally ask for minimal, object-oriented input (e.g., ``CreateBeam``, which asks for a set of instructions contained within a particular derived type, and then the energy grid and an object of the type ``LinacType``, which can then be propagated to perform actions that typically require a beam to be specified, like creation of an external beam source). Module procedures are also leveraged to allow the input to be flexible.

Linear Operators in Lionbolt
----------------------------

A major player in Lionbolt is the linear operator class (see LinearOperatorClass.f90). This class is then extended to define a particular linear operator, i.e., the Boltzmann operator, the transport operator, etc. This class comes with its own matrix-vector routine ('MatVec') as well as a matrix inverse routine ('MatInv'), and then the extension should define the routines as well as all objects needed to execute these routines. Furthermore, the class comes with its own readiness flags as well as a character for the name of the operator. Now, these linear operators act upon flattened space-angle vectors. An important contradiction to note is the definition of the scattering operator, whose inverse is generally undefined in the Boltzmann transport equation. As such, it could be more logical to have separated the linear operators into 'integro-differential operators' and integral operators, where the former (including the full Boltzmann operator and the transport operator) do come with their own MatInv routine, while the latter do not. Nevertheless, this appears at the moment less practical than just defining a scattering inverse routine that calls an error and terminates the program.

For instance, a linear operator is initialized by, e.g., a subroutine like AssembleBoltzmann. This subroutine accepts up to three inputs: a MeshType object, an AngularType object, and a CSType object, clearly representing the space, angle, and physics/energy parts of the operator. A user can initialize the operator by providing particular combinations (that are required due to the coupling of coordinates in Boltzmann transport). One can build only the spatial part, i.e., give the MeshType object. Or, one can build the space and angle part, giving the MeshType object and AngularType object. One can build the physics part, giving both the AngularType and the CSType. On the other hand, one can build the entire operator by providing all parts. Note that providing a particular input repeatedly results in re-writing of the operator.

The reason for structuring the operator assembly modules as such is to facilitate iteration. For instance, if performing a polyenergetic Boltzmann transport solve, one will typically rely on 'energy iteration,' which allows for iteratively solving for the energy index descending in energy by assuming no up-scatter in energy (a perfectly valid assumption in the rest frame of the medium, which is necessarily assumed). In this case, it is useful to assemble the space-angle portions separately from assembling the physics portion, which can be updated compactly during an energy group loop.

If and when Lionbolt generalizes to other transport problems and thus operators, new structures to the corresponding assembly routines will be determined independently.

Running Your Own Driver
-----------------------

Public API
----------

.. toctree::
    :maxdepth: 1
    
    public/CreateBeam