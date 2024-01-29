__doc__ = """Configuration file for the Sphinx documentation builder."""

# -- project info: ------------------------------------------------------------

project = 'cellplots'
copyright = '2023, Michael E. Vinyard'
author = 'Michael E. Vinyard'
release = '0.0.1'

# -- config: ------------------------------------------------------------------
import os
import sys

sys.path.insert(0, os.path.abspath('../../'))

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.coverage',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx.ext.autosectionlabel',
    'nbsphinx',
    'sphinx_copybutton',
    'sphinx_favicon',
    'sphinx_design',
    'myst_parser',
]

templates_path = ['_templates']
exclude_patterns = []


# -- html output options: -----------------------------------------------------

html_theme = 'pydata_sphinx_theme'
html_static_path = ['_static']
html_css_files = ['css/custom.css']


html_theme_options = {
    "github_url": "https://github.com/mvinyard/cellplots",
    "twitter_url": "https://twitter.com/vinyard_m",
    "logo": {
      "image_light": "cellplots.logo.light.png",
      "image_dark": "cellplots.logo.dark.png",
   },
}
autoclass_content = 'init'

favicons = [{"rel": "icon", "href": "scdiffeq.favicon.png"}]

# -- notes: -------------------------------------------------------------------
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html
