Quickstart Guide
================

Here we describe the basic classes, functions, and methods that will allow a user to analyze their Lionbolt or NittanyPhysics data without significant effort nor understanding of the underlying machinery.

A user should be able to get a hang of what Terpdose can do and how to use it without necessarily consulting the documentation, ideally relying on the :ref:`tdexamples` section. However, the provided documentation should also be relatively user-friendly for those interested in getting into the details.

Documentation
-------------

.. toctree::
    :maxdepth: 1
    
    LBdata
    xslibrary
    spaceanglevector
    particle
    crosssections

.. _tdexamples:

Examples
--------

.. attention:: This section is WIP. The examples below can be useful but more examples are to be added.

Accessing raw angular fluence data
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python
    
    from Terpdose import Lionbolt
    
    D = Lionbolt ('results.h5') # Initialize the Lionbolt object
    
    # Now suppose that this solve contains a particle named 'electrons'
    
    el = D.electrons # This is a Particle object
    
    angfl = el.angular_fluence () # This is a list of SpaceAngleVector objects. It is a list over the energy groups
    
    # Now run through and print values for an energy group g0
    g0 = 13
    for i in range(0, 16):
        for s in range(0, 400):
            print(f'energy {g0}, angle {i}, spatial dof {s} : {angfl[g0][i, s]}')
            
            # Although angfl[g0] is a SpaceAngleVector object, its entries can be accessed like a numpy array, using [i, s]
            # Total number of angles can also be given by D.electrons.angular.num_angular_dofs
            # Total number of spatial d.o.f.s can also be given by D.mesh.num_spatial_dofs
    
    # Alternatively you can index the spatial dof using an element and local node index, using the mesh
    mesh = D.mesh
    r    = mesh.nodes ()             # This gives the full set of nodes, indexed like [global node, direction]
    NK   = mesh.num_element_nodes () # This array gives the number of nodes in an element
    for i in range(0,16):
        for e in range(mesh.num_elements):
            for k in range(NK[e]):
                s = mesh.offset[e] + k # Use offset arrays to map from [e, k] to s.
                print(f'energy {g0}, angle {i}, element {e}, node {k} : {angfl[g0][i, s]}')
                
                # To get the global node corresponding to s, use connectivity.
                r0 = r[mesh.connectivity[s],:]
                print(f'coordinates of the mesh node (x,y,z) : {r0}')
    
    # If a user wants to get ONLY g0 from the start, perhaps to save memory.
    angfl_A = el.angular_fluence (energies=g0) # Now this is just a single SpaceAngleVector object.
    
    # If a user wants to get a fixed set of energies
    angfl_B = el.angular_fluence (energies=[1, 4, 8])
    
    # A user can similarly specify angles using argument angles=[0, 2, 4, etc.], or angles=0, etc., 
    # the SpaceAngleVector data will still be rank-two however.
    
    # Calculate the fluence of energy group g0
    fl = angfl[g0].fluence()
    
    # Alternatively, a user can try to avoid calculating fluence by trying to read it from results.h5.
    # If the fluence isn't present in results.h5, this will calculate it using angfl[g0].fluence().
    fl = el.fluence (energies=g0)

Deposition calculations
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python
    
    from Terpdose import Lionbolt
    
    D = Lionbolt ('results.h5') # Initialize the Lionbolt object
    
    dose = D.dose_deposition () # Get the dose deposition due to all particles.
    
    # If the user used Lionbolt to calculate and save the dose deposition, this just reads it in.
    # Otherwise, as long as the user has fluence OR angular fluence data saved, this will calculate the dose deposition.
    
    energy = D.energy_deposition () # Energy deposition
    
    charge = D.charge_deposition () # Charge deposition
