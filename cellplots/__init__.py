
# __init__.py

__VERSION__ = __version__ = "0.0.1rc0"

from . import core
from . import _tools as tl

from .core._plot import plot
from .core._umap import umap, umap_manifold