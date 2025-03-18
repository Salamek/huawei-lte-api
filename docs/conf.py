# Configuration file for the Sphinx documentation builder.

# -- Project information -----------------------------------------------------

project = 'Huawei LTE API'
copyright = '2021, Salamek'
author = 'Salamek'

# -- General configuration ---------------------------------------------------

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
]

templates_path = ['_templates']

exclude_patterns = []

# -- Options for HTML output -------------------------------------------------

html_theme = 'alabaster'
html_static_path = ['_static']
