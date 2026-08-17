.. _terpdose:

Terpdose
========

Terpdose is a python package for post-processing, plotting, and otherwise working with Lionbolt and NittanyPhysics data. It is highly recommended to use Terpdose with Lionbolt, as Lionbolt produces large data files. Access and manipulation of this data is much easier with Terpdose.

Installation is as simple as::
    
    pip install Terpdose

If you cannot obtain Terpdose from PyPi for whatever reason, then you can download it from GitHub at https://github.com/mhyounis/Terpdose, and manually pip install it.

The pages below describe the various classes around which Terpdose is designed.

Primarily, users will be interested in starting with Lionbolt and XSLibrary classes. These read the HDF5 files produced by Lionbolt and NittanyPhysics respectively. From these objects, all data can be accessed, along with several class-bound methods relating to post-processing. More in the pages below.

.. toctree::
    :caption: Contents
    :maxdepth: 1
    
    quickstart/index
    plotting/index
    advanced/index
    scripts/index
