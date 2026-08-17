.. _ouputlionbolt:

Output
======

A single Lionbolt solve puts out two files: a 'standard out' file (``.out``) file and an HDF5 file (``.h5``) file. These files are named and located according to the user input file. For instance, if the user's input file is ``mysolve.in``, the outputs will be named ``mysolve.out`` and ``mysolve.h5``. The contents of these files are described below.

The Standard Out File
---------------------

::
    
    mysolve.out

This file will contain basic, human-readable information that allows the user to track the progress of the calculation. This includes solve start / stop time, total time, solve type, number of cores, scratch directory and files, in addition to live updates (that can be useful for diagnosis of issues), such as the point at which the program enters some subroutine or begins some major task like discretizing a coordinate, and finally, any warnings and errors that arise.

This file also contains quantities that may be of interest to the user for more convenient interpretation of their results. For instance, the physics library used in the solve is always printed, and that allows a user to directly and consecutively read off attenuation coefficients for the materials present in their solve.

The HDF5 File
-------------

::
    
    mysolve.h5

This is an 'HDF5' file :cite:`HDF5`. It attempts to thread the needle between efficient data storage and ease of access. That is, Boltzmann transport is notorious for outputting significant quantities of data, on the order of 100s of GBs sometimes, so it was not practical to output the data in a file type other than binary. However, it is also not practical to output data without some semblence of human-readability. The HDF5 file format is essentially a categorized binary file which can easily be accessed and read via packages installable to various major programming languages, such as Fortran, C/C++, python, and more. There are also websites which allow you to upload your HDF5 file and view its categories, for instance, https://myhdf5.hdfgroup.org/.

The Lionbolt HDF5 file is organized in a particular manner, which **at the moment**, will not be described in these docs. However, the pattern is rather straightforward, and so the user is recommended to use a website or other program to explore the structure of various output files.

Furthermore, user-friendly access as well as post-processing of Lionbolt's HDF5 output files is the entire function of the :ref:`Terpdose <terpdose>` python package. The user is **highly** recommended to use Terpdose unless they intend to post-process Lionbolt data beyond what Terpdose can do.

References
----------

.. bibliography::
    :filter: docname in docnames
    :style: unsrt