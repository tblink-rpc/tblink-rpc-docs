# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
# sys.path.insert(0, os.path.abspath('.'))


# -- Project information -----------------------------------------------------

project = 'TbLink RPC'
copyright = '2021, Matthew Ballance'
author = 'Matthew Ballance'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.doctest',
    'sphinx.ext.todo',
    'sphinx.ext.coverage',
    'sphinx.ext.imgmath',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
    'sphinx.ext.intersphinx',
#    'sphinxcontrib.makedomain',
    'sphinx.ext.inheritance_diagram',
#    'cairosvgconverter',
    'breathe',
    'sphinx_issues',
    'sphinxarg.ext',
    'sphinxcontrib.spelling',
    'sphinxcontrib.openapi'
]


if "DOXYDOCS_DIR_CPP" in os.environ.keys():
    doxydocs_dir_cpp=os.environ["DOXYDOCS_DIR_CPP"]
else:
    doxtdocs_dir_cpp="../doxydocs_cpp"

if "DOXYDOCS_DIR_SV" in os.environ.keys():
    doxydocs_dir_sv=os.environ["DOXYDOCS_DIR_SV"]
else:
    doxtdocs_dir_sv="../doxydocs_sv"

breathe_projects = { "tblink_rpc_cpp": os.path.join(doxydocs_dir_cpp, "xml"), 
                    "tblink_rpc_sv": os.path.join(doxydocs_dir_sv, "xml") 
                    }
breathe_default_project = "tblink_rpc_cpp"

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']
