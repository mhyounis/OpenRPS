.. _LBval:

Validation
==========

The validation of Lionbolt is interwoven with the validation of NittanyPhysics. That is, one of the best ways to validate a cross section library is to see the resulting transport it predicts. However, this obviously relies on Lionbolt's space-angle machinery. That said, we do not provide results of space-angle validation, however, various driver files can be found within the files of Lionbolt. These driver files will be used in the future to minimally validate any changes to existing space-angle code. Still, physics solves can be taken as equally meaningful validation, as without the appropriate results from the space-angle operators, the results would not be physically accurate.

Lionbolt with NittanyPhysics cross sections has been validated against EGSnrc :cite:`EGSnrc`, specifically the 521ICRU physics dataset. The following validation studies demonstrate several capabilities of Lionbolt - full 3D mesh solves as well as slab solves, homogeneous media as well as heterogeneous media, high Z and low Z materials, high incident energies and low incident energies, and photon and electron transport.

The validation cases mentioned in this page can be run by the user by navigating to ``$LIONBOLT/validation/`` (where ``$LIONBOLT`` is the Lionbolt main directory). Furthermore, one can re-purpose validation input files listed below as templates, or they can re-run and analyze the validation cases themselves. To plot the validation against the given EGSnrc results file, just use the script ``$LIONBOLT/validation/plot_validation.py``, providing as input the folder containing the validation case, for example::
    
    $LIONBOLT/validation/plot_validation.py $LIONBOLT/validation/electrons_incident/Al_521keV_0deg
    
then look for the figure ``$LIONBOLT/validation/electrons_incident/Al_521keV_0deg/comparison.png`` (which also includes Lockwood experimental data :cite:`Lockwood1980` where available).

Electrons Incident
------------------

We note, disagreements found in heavier metal media are likely due to the complete absence of radiative scattering and relaxation cascades in NittanyPhysics (which is likely to be one of the first things added to NittanyPhysics in the near future, at which time of course we will re-validate the presented validation cases).

We also note that currently NittanyPhysics does not generate photons sourced by electrons (although electrons can be sourced by photons). This is also going to be implemented and validated shortly.

We provide the comparison figures for each of the documented validation cases here.

Electron beam normally incident on Al slab, 521 keV
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/assets/validation/electrons_incident/Al_521keV_0deg.png
    :width: 75%
    :align: center

Electron beam normally incident on Al slab, 6 MV polychromatic spectrum
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/assets/validation/electrons_incident/Al_6MV_0deg.png
    :width: 75%
    :align: center
    
    Note, the polychromatic spectrum used is simply a photon spectrum that was re-purposed for electrons. This is simply meant to benchmark the discretization parameters required to get agreeing solves, whether or not the context is physically perfect.

Electron beam normally incident on Au slab, 1 MeV
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/assets/validation/electrons_incident/Au_1MeV_0deg.png
    :width: 75%
    :align: center

Electron beam normally incident on Au slab, 10 MeV
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/assets/validation/electrons_incident/Au_10MeV_0deg.png
    :width: 75%
    :align: center
    
    Note, this disagreement is due to the absence of radiative scattering (Bremsstrahlung) and atomic relaxation mechanisms in NittanyPhysics. These remain WIP but will be validated as soon as possible. This solve thus demonstrates that you should be wary of using the current version of NittanyPhysics for high-Z, high energy solves.

Electron beam normally incident on Al/Au/Al slab, 1 MeV
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/assets/validation/electrons_incident/AlAuAl_1MeV_0deg.png
    :width: 75%
    :align: center

Photons Incident
----------------

6 MV polychromatic X-ray beam incident on typical water tank phantom
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/assets/validation/photons_incident/water_tank_6MV_depth_comparison.png
    :width: 75%
    :align: center

.. figure:: /_static/assets/validation/photons_incident/water_tank_6MV_Lionbolt_YZ.png
    :width: 75%
    :align: center
    
.. figure:: /_static/assets/validation/photons_incident/water_tank_6MV_EGSnrc_YZ.png
    :width: 75%
    :align: center

1 MeV monoenergetic X-ray beam incident on typical water tank phantom
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/assets/validation/photons_incident/water_tank_1MeV_depth_comparison.png
    :width: 75%
    :align: center

.. figure:: /_static/assets/validation/photons_incident/water_tank_1MeV_Lionbolt_YZ.png
    :width: 75%
    :align: center
    
    Note, the color scale is artificially saturated by mesh node artifacts. These can occur when your mesh is not sufficiently refined, as in the case of this validation which, due to the softness of the incident X-rays, required an exceedingly small mesh size near the surface. At the moment, the local machine on which these calculations were carried out is simply not strong enough to produce sufficiently refined solves (which also happens to be the reason that no :mod:`PROBLEM GENERAL` solves were done with electrons).
    
.. figure:: /_static/assets/validation/photons_incident/water_tank_1MeV_EGSnrc_YZ.png
    :width: 75%
    :align: center

6 MeV monoenergetic X-ray beam incident on typical water tank phantom
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/assets/validation/photons_incident/water_tank_6MeV_depth_comparison.png
    :width: 75%
    :align: center

.. figure:: /_static/assets/validation/photons_incident/water_tank_6MeV_Lionbolt_YZ.png
    :width: 75%
    :align: center
    
.. figure:: /_static/assets/validation/photons_incident/water_tank_6MeV_EGSnrc_YZ.png
    :width: 75%
    :align: center

X-ray beam normally incident on Pb slab, 10 MeV
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/assets/validation/photons_incident/Pb_10MeV_0deg.png
    :width: 75%
    :align: center
    
    Note, this disagreement is again due to the absence of radiative scattering (Bremsstrahlung) and atomic relaxation mechanisms in NittanyPhysics. These remain WIP but will be validated as soon as possible. 

.. bibliography::
    :filter: docname in docnames
    :style: unsrt