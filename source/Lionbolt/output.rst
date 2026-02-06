Output
======

A single Lionbolt solve puts out two files: a 'standard out' file (``.out <.out>``) file and an HDF5 file (``.h5 <.h5>``) file. These files are named and located according to the user input file. For instance, if the user's input file is ``mysolve.in``, the outputs will be named ``mysolve.out`` and ``mysolve.h5``. The contents of these files are described below.

The Standard Out File
---------------------

This file will contain basic, user-readable information that allows the user to track the progress of the calculation. This includes solve start / stop time, total time, solve type, number of cores, scratch directory and files, in addition to live updates (that can be useful for diagnosis of issues), such as the point at which the program enters some subroutine or begins some major task like discretizing a coordinate, and finally, any warnings and errors that arise.

This file also contains quantities that may be of interest to the user for more convenient interpretation of their results. For instance, the physics library used in the solve is always printed, and that allows a user to directly and consecutively read off attenuation coefficients for the materials present in their solve, to possibly use intuition to understand something they've observed in the solve.

The HDF5 File
-------------

This file is where most of the raw results of the run will be stored. As such, this file is typically very large.

The layout of the HDF5 file is detailed below





The user is recommended, for navigating over categories and inspecting attributes (such as discrete ordinate or spherical harmonic index, as well as energy group bounds), to use an HDF5 file viewer. A great viewer that can be accessed online is https://myhdf5.hdfgroup.org/.

Finally, access and post-processing of Lionbolt's HDF5 output files is the entire function of the :ref:`Terpdose <terpdose>` Python package. The user is highly recommended to use Terpdose unless they intend to post-process Lionbolt data beyond what Terpdose can do.