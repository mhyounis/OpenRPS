Plotting
========

Documentation
-------------

.. toctree::
    :maxdepth: 1
    
    geometric
    grids
    interpolation

Examples
--------

.. attention:: This section is WIP.

Plotting dose deposition in a slice
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Terpdose comes with a script, :ref:`plot_deposition`, which allows a user to do this providing all arguments in the command line. However, for further customization one can use the following example as a guide:

.. code-block:: python
    
    from Terpdose import *
    
    D = Lionbolt ('results.h5')
    
    mesh = D.mesh # The mesh in our problem, requested by several functions, is accessible as the 'mesh' attribute of the Lionbolt class.
    
    dmap = D.dose_deposition
    
    # Say your mesh is a 30 x 30 x 30 cm^3 cube with its base at the origin, beam along Z-axis.
    # The following is an example of the grid geometry one can create:
    geo  = Plane (
        n      = [100, 100],        # 100 points along each axis
        origin = [0.0,  0.0, 15.0], # Plane is going to be centered at 15 along the Z-axis
        ax1    = [0.0, 15.0,  0.0], # Take first in-plane axis to be along the Y-axis, half-length is 15.0 for a 30.0 cm cube side length
        ax2    = [0.0,  0.0, 15.0], # Take first in-plane axis to be along the Z-axis, half-length is 15.0 for a 30.0 cm cube side length
    )
    # This plane now describes the YZ plane that covers an entire slice of the water tank.
    
    # OPTION 1 - Create the Grid yourself (good for reuse, as the Grid can be expensive to generate)
    grid = Grid (mesh=mesh, geo=geo)
    
    # Now interpolate dmap onto the grid
    dmap_grid = GridInterpolation (grid, dmap)
    
    # OPTION 2 - Do not create a Grid
    # Now must feed mesh to the interpolation function
    dmap_grid = GeoInterpolation (mesh, geo, dmap)
    
    # Result is np.float64 [100, 100]. This can now be plotted however you wish, with geo.xyz OR grid.xyz being the set of grid position vectors