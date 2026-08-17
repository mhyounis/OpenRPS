.. _installation_lionbolt:

Installation
============

.. _program_lionbolt:

Requirements
------------

The requirements of Lionbolt are detailed in the ``environment.yaml`` file in the main Lionbolt directory. While one has the ability to thus design their environment around these requiremenets however they want, this file can be used to automatically create a minimal conda environment named 'lblt,' which has all Lionbolt (and NittanyPhysics) requirements satisfied. This can be done using::
    
    conda env create -f environment.yaml

Building Lionbolt as a Program
------------------------------

Lionbolt comes with a submit script that can handle building, cleaning, and supplying the input file or injecting the user-defined driver. At the moment it is not designed for submission on HPC clusters, as Lionbolt is not currently MPI-capable (this will come in a future update).

In the following we assume that the user has the Lionbolt directory in their environment path, and that the directory is assigned in the environment variable ``$LIONBOLT``. In order to build Lionbolt, you can run the submit script with the flag ``-b``::
    
    Lionbolt.py -b

or, alternatively, you can just provide your input file or driver like::

    Lionbolt.py your_input.in
    Lionbolt.py your_driver.f90

and if Lionbolt is not already built, the submit script will automatically build it. Note that Lionbolt determines whether you are doing a driver or a main program solve based on the extension of the input to the submit script, i.e., ``.in`` gets treated as an input file for a main program solve and ``.f90`` gets treated as a driver file.

In order to remove all Lionbolt build files one can provide the flag ``-c`` to the submit script::
    
    Lionbolt.py -c

Note if one also provides an input/driver file with the ``-c`` flag, then Lionbolt will be rebuilt and run after cleaning. 

To control the number of threads used for OpenMP / MPI (WIP), you can use the flag ``-n``. This should be done upon running a file::
    
    Lionbolt.py your_input.in -n 1
    Lionbolt.py your_driver.f90 -n 1

to enforce a single thread, for example.

Alternatively, one can of course remove the ``build/`` folder manually with, e.g.::
    
    rm -rf build

Now, if one chooses to forego the Lionbolt submit script, the treatment for an input file and a driver is asymmetric. To run the input file, build as usual::
    
    cmake -S $LIONBOLT -B $LIONBOLT/build
    
    cmake --build $LIONBOLT/build -j

Then run like::
    
    $LIONBOLT/build/Lionbolt your_input.in

On the other hand, to run a driver, the driver must be given upon compiling the program. When compiling use the ``-DDRIVER_FILE`` flag::
    
    cmake -S $LIONBOLT -B $LIONBOLT/build  -DDRIVER_FILE=your_driver.f90
    
    cmake --build $LIONBOLT/build -j

Then run like::
    
    $LIONBOLT/build/Lionbolt

with the option to include any other inputs that you may be expecting within your driver using Fortran's typical ``get_command_line`` intrinsic.

.. _library_lionbolt:

Building Lionbolt as a Library
------------------------------

Building Lionbolt as a library for your program is a little more complicated, however, it is of course also largely dependent on your program's ``CMakeLists`` / ``Makefile`` structure. Thus, rather than provide instructions, here we detail the structure of the Lionbolt ``CMakeLists``, so that user will understand how to generate the Lionbolt API library for their own use. It will be up to them to link this library to their build.

The Lionbolt ``CMakeLists`` generates the following::
    
    PrivateLionbolt (library)
    |
    LionboltAPI (library)
    |
    Lionbolt (executable)

where `|` denotes a linkage.

The LionboltAPI consists of only one module, ``LionboltAPI``, in one file, ``LionboltAPI.f90``. This module is just a series of ``use`` statements, declaring the use of a set of modules present in ``PrivateLionbolt``. The set of modules in ``PrivateLionbolt`` contain routines which were designed to be visible via ``LionboltAPI`` (see :ref:`lionboltapi`), as well as some genuinely private routines (referred to in these docs as 'internal routines', see :ref:`internal_lionbolt`) that are relied upon by those visible routines. Then, the ``Lionbolt`` executable is linked only to ``LionboltAPI``. The term ``PrivateLionbolt`` thus only refers to the fact that this library is private to the ``Lionbolt`` executable. In principle an interested user can of course link ``PrivateLionbolt`` to their build as well but this is not recommended as these routines have not been designed for user-friendliness.

Nevertheless, the user should thus configure their build so that it links the library ``LionboltAPI``. Then, they can access the Lionbolt API with the declaration::
    
    use LionboltAPI

The user will also want to consider linking the ``core`` or ``NittanyAPI`` modules, both found in NittanyPhysics, which are indeed privately linked in Lionbolt's ``CMakeLists.txt``.

Using a Local Version of NittanyPhysics
---------------------------------------

Everytime a given version of Lionbolt is compiled, it pulls a specific version of NittanyPhysics from GitHub. To override this, either for development or because you don't want compilation to demand internet access, you can set the following environment variables. One indicates to Lionbolt's build procedure that you wish to use a local version of NittanyPhysics, and the other defines the file path of NittanyPhysics::
    
    export LB_NP_DEV_OVERRIDE=1
    export NITTANY="/path/to/your/NittanyPhysics"