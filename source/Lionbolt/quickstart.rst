.. _quickstart:

Quickstart Guide
================

Lionbolt can be downloaded from GitHub at https://github.com/mhyounis/Lionbolt, or by running the command::
    
    git clone https://github.com/mhyounis/Lionbolt

in the destination directory. Note that Lionbolt is only compatible with Linux, including Windows Subsystem for Linux (WSL).

Before installing, recognize that the user has three ways to use Lionbolt.

1. The user can provide an input file and allow Lionbolt to proceed as a program with a standard solution procedure. This is the **most user-friendly** option. The input file is sufficiently flexible that no features are obscured in this method, and in general this is intended to be the method of choice for most users.
2. The user can provide a 'driver.' This is essentially the user's own solution sequence in the form of a Fortran program file which relies on the Lionbolt API available through the Lionbolt library. The API was designed for user-friendliness and object-orientation motivated by the physics of the problem.
3. The user can build the Lionbolt API as a standalone library and link it to another larger codebase or program.

Now, methods #1 and #2 follow the same :ref:`installation instructions <program_lionbolt>` as one another. Method #3 follows :ref:`a different set of instructions <library_lionbolt>`.

Conversely, to *operate* both methods #2 and #3 requires an understanding of the Lionbolt API (whereas method #1 requires only understanding the input file). To learn about the Lionbolt API, the user is directed towards :ref:`lionboltapi`. In the quickstart page, however, we will focus on the user-friendly, input file-based method, method #1.

To post-process and visualize Lionbolt results, it is strongly recommended to also install :ref:`Terpdose <terpdose>`. Terpdose will be used extensively in this quickstart guide.

Quick Installation
------------------

For more information the user can visit :ref:`installation instructions <program_lionbolt>`, however here we detail a very brief way to install Lionbolt via the submit script.

The requirements of Lionbolt are detailed in the ``environment.yaml`` file in the main Lionbolt directory. While one has the ability to thus design their environment around these requiremenets however they want, this file can be used to automatically create a minimal conda environment named 'lblt,' which has all Lionbolt (and NittanyPhysics) requirements satisfied. This can be done using::
    
    conda env create -f environment.yaml

It is recommended to add the Lionbolt directory to your ``PATH``, for access to the Lionbolt submit script from any working directory, otherwise the absolute path to ``Lionbolt.py`` or your input file will need to provided upon use. 

Assuming the user has ``Lionbolt.py`` in their path, they can compile Lionbolt at any time using::
    
    Lionbolt.py -b
    
To clean Lionbolt, one may use::
    
    Lionbolt.py -c

Examples
--------

See the validation folder (``$LIONBOLT/validation/``) or the examples folder (``$LIONBOLT/examples``) for various calculations that you can run (``$LIONBOLT`` is the Lionbolt main directory, you can of course set this as an environment variable if you want). For a lightweight run you can consider the Lockwood aluminum slab validation case, ``$LIONBOLT/validation/electrons_incident/Al_521keV_0deg/lb.in``, and for a more demanding calculation you can do a full 3D space water tank phantom calculation, ``$LIONBOLT/validation/photons_incident/water_tank_6MV``. See also the :ref:`validation page <LBval>` and the :ref:`gallery <gall>` for more example calculations that you can try running.

To run any given calculation, the most convenient way is to use the Lionbolt submit script with the path of the file. If you use this script, note that any directories specified in the input file will be relative to the directory containing the input file (which I find most convenient). Anyway, if your input file is ``lb.in``, just do::
    
    Lionbolt.py lb.in

.. _creation-of-a-mesh:

Creating a mesh
---------------

Lionbolt currently only acceps `gmsh`_ :cite:`Geuzaine2009` formatted meshes, thus, you are recommended to use gmsh to create a mesh. Furthermore, it must be noted that at the moment Lionbolt can only treat convex geometries. Both of these restrictions will be relaxed sooner rather than later.

We will not discuss a gmsh tutorial here, however, several template gmsh ``.geo`` files are provided with the full 3D solves scattered among the ``validation`` and ``examples`` folders. To find these (and the meshes themselves), simply search the Lionbolt directory for the extensions ``.geo`` and ``.msh``.

Material assignment
~~~~~~~~~~~~~~~~~~~

We must note that material assignments in Lionbolt are based on 'physical tags' given to volumes in gmsh. The physical tag must correspond to the material index in your solve. If no physical tag is provided, Lionbolt assumes there is one uniform material in the mesh. If you indicate that there are multiple materials in the solve and this is not corroborated by your mesh, you will receive an error message and the program will terminate.

(OPTIONAL) Beam definition
~~~~~~~~~~~~~~~~~~~~~~~~~~

Lastly, you are recommended to provide the outline of the beam(s) you intend to use within the mesh. That is to say, construct the beam's intersection with your medium as its own set of volumes such that gmsh creates mesh elements fully within the beam and those fully without. This is not *required*, however, it allows for the external beam source to be more appropriately defined. Since collimated beams are modeled as discontinuous, having the beam outline in your geometry means that the discontinuous finite element method can much better represent your source. If it is not provided and the beam's cutoff region intersects several finite elements, then quadrature within those finite elements will essentially assume a polynomial decay of the beam from a finite value (at the node(s) within the beam) to zero (at the node(s) outside the beam). This will have adverse effects on the shape of your source as well as its overall normalization, as Lionbolt does not apply any correction factors to account for beams that deviate from their ideal shape in the mesh.

.. _gmsh: https://gmsh.info/

.. bibliography::
    :filter: docname in docnames
    :style: unsrt