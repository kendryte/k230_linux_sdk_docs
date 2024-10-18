# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import sys, os
import datetime

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = os.getenv('PROJECT') or 'K230 Linux SDK'
copyright = str(datetime.datetime.now().year) + ' ' + (os.getenv('COPYRIGHT') or 'Canaan Inc')
author = os.getenv('AUTHOR') or 'Canaan'
# release = '0.1'
root_doc = os.getenv('ROOT_DOC') or 'index'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx_copybutton',
    'myst_parser',
    'sphinx_multiversion'
]
html_title = 'K230 Linux SDK'
templates_path = ['_templates']
exclude_patterns = []

language = 'zh_CN'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

myst_heading_anchors = 7
suppress_warnings = ["myst.header"]

html_copy_source = True
html_show_sourcelink = False

html_favicon = 'favicon.ico'

# html_show_sphinx = False
# html_theme = 'alabaster'
html_theme = "sphinx_book_theme"
html_static_path = ['_static']

# if want to add top nav for canann, enable this.
html_css_files = ['topbar.css', 'custom-theme.css']


locale_dirs = ['locale']

html_theme_options = {
    #"use_edit_page_button": True,
    "primary_sidebar_end": ["versionsFlex.html"],
    "footer_start": ["Fleft.html"],
	"footer_center": ["Footer.html"],
	"footer_end" : ["Fright.html"]
}

