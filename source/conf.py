# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys

print("CONF.PY LOADED")

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project   = 'OpenRPS'
copyright = '2026, Muhsin H. Younis'
author    = 'Muhsin H. Younis'
release   = 'v1.0.1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

templates_path    = ['_templates']
exclude_patterns  = []
suppress_warnings = []

sys.path.insert(0, os.path.abspath("."))  # points to source/

extensions = [
    'sphinx.ext.autodoc',
    # 'sphinx.ext.autosummary',
    'sphinxcontrib.bibtex',
    'sphinx_math_dollar',
    'sphinx.ext.mathjax',
    # 'numpydoc',
    'sphinx.ext.napoleon'
]

# autosummary_generate = True

# -- mathjax ---------------------------------------------------
# Added by Muhsin H. Younis, 2026
math_number_all = True
mathjax3_config = {
    'tex': {
        'tags': 'ams',  # Use AMS numbering rules
        'tagSide': 'right',  # Explicitly force numbers to the right
    }
}

# -- BibTeX ---------------------------------------------------
# Added by Muhsin H. Younis, 2026
bibtex_bibfiles = [
    '_bibtex/references.bib'
    ]
bibtex_default_style = 'aps'

suppress_warnings.append('bibtex.duplicate_citation')
suppress_warnings.append('bibtex.duplicate_label')

# -- Code style ---------------------------------------------------
# Added by Muhsin H. Younis, 2026
pygments_style = 'vs'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme       = 'sphinx_rtd_theme'
html_static_path = ['_static']

html_logo = '_static/assets/logos/OpenRPS.png'

html_css_files = ['styles/style.css']

# -- autodoc ------------------------------------------------
# Added by Muhsin H. Younis, 2026
numpydoc_class_members_toctree = False
numpydoc_show_class_members    = False
napoleon_numpy_docstring       = True
autodoc_default_options        = { 'members': True, }
add_module_names               = False
autodoc_typehints              = 'description'