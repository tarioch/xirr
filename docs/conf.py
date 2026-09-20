import os
import shutil
import sys

from sphinx.ext import apidoc

# -- Path setup --------------------------------------------------------------

__location__ = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(__location__, "../src"))

# -- Run sphinx-apidoc -------------------------------------------------------
# Read the Docs does not run `sphinx-apidoc` itself, generating the module
# reference here builds it for every sphinx-build.
output_dir = os.path.join(__location__, "api")
module_dir = os.path.join(__location__, "../src/xirr")
shutil.rmtree(output_dir, ignore_errors=True)
apidoc.main(["--implicit-namespaces", "-f", "-o", output_dir, module_dir])

# -- General configuration ---------------------------------------------------

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinx.ext.viewcode",
    "sphinx.ext.napoleon",
    "sphinx_rtd_theme",
]

templates_path = ["_templates"]
source_suffix = ".rst"
master_doc = "index"

project = "xirr"
copyright = "2021, Patrick Ruckstuhl"

try:
    from xirr import __version__ as release
except ImportError:
    release = ""
version = release

exclude_patterns = ["_build", "Thumbs.db", ".DS_Store", ".venv"]
pygments_style = "sphinx"

# -- Options for HTML output -------------------------------------------------

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
html_show_sphinx = False
htmlhelp_basename = "xirr-doc"

# -- External mapping --------------------------------------------------------

python_version = ".".join(map(str, sys.version_info[0:2]))
intersphinx_mapping = {
    "python": ("https://docs.python.org/" + python_version, None),
}
