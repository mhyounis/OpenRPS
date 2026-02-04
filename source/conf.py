# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Younis Radiation Physics Suite'
copyright = '2026, Muhsin H. Younis'
author = 'Muhsin H. Younis'
release = '0.1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = []

templates_path = ['_templates']
exclude_patterns = []

sys.path.insert(0, os.path.abspath("."))  # points to source/

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
]

autosummary_generate = True

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

html_logo = '_static/logos/YRPSlogo_opt4_alt1.png'

html_css_files = ['styles/yrps_style.css']