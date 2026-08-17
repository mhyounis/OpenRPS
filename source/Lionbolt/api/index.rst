.. _lionboltapi:

The Lionbolt API
================

The Lionbolt API largely revolves around particular derived types and their type-bound procedures. Below, we list the major players and describe their components and procedures, informing the user both what they do and how to work with them.

Note that several of these types rely on other types defined in the same modules for the sole purpose of serving these parent types (Ex: MeshClass depends on MeshElement and MeshFace). We speak about these child types in the pages for the original type. The priority is more user-facing types, i.e., types with which the user will directly have to interact.

.. toctree::
    :maxdepth: 1
    
    meshclass
    angularclass
    fieldgeometry
    externalbeam
    spaceanglevector
    linearoperatorclass