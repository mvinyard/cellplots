
# -- import packages: ---------------------------------------------------------
import matplotlib.colors
import ABCParse


# -- import local dependencies: -----------------------------------------------
from ._hex_to_rgb import hex_to_rgb


# -- set typing: --------------------------------------------------------------
from typing import List, Optional, Tuple


# -- Controlling class: -------------------------------------------------------
class CustomColorMap(ABCParse.ABCParse):
    """Custom colormap from min/max/[center] values."""
    def __init__(self, *args, **kwargs):
        self.__parse__(locals(), public=[None])

    def to_RGB(self, hex_code) -> Tuple[float]:

        return hex_to_rgb(hex_code)

    @property
    def _CMAP_MAX(self) -> Tuple[float]:
        return hex_to_rgb(self._max_color)

    @property
    def _CMAP_MIN(self) -> Tuple[float]:
        return hex_to_rgb(self._min_color)

    @property
    def _colors(self) -> List[Tuple[float]]:
        colors = [self._CMAP_MIN, self._CMAP_MAX]
        if hasattr(self, "_center_color"):
            colors.insert(1, hex_to_rgb(self._center_color))
        return colors

    @property
    def cmap(self) -> matplotlib.colors.LinearSegmentedColormap:
        return matplotlib.colors.LinearSegmentedColormap.from_list(
            self._name, self._colors
        )

    def __call__(
        self,
        max_color: str,
        min_color: str = "#FFFFFF",
        center_color: str = None,
        name: Optional[str] = "custom_cmap",
        *args,
        **kwargs
    ) -> matplotlib.colors.LinearSegmentedColormap:
        self.__update__(locals(), public=[None])

        return self.cmap


# -- API-facing function: -----------------------------------------------------
def custom_cmap(
    max_color: str,
    min_color: str = "#FFFFFF",
    center_color: Optional[str] = None,
    name: Optional[str] = "custom_cmap",
) -> matplotlib.colors.LinearSegmentedColormap:
    """
    Compose a custom colormap passing min, max, and optionally,
    center color values as hex codes.

    Parameters
    ----------
    max_color: str
        Maximum color.

    min_color: str, default = "#FFFFFF"
        Minimum color. If not provided, the default is white.

    center_color: Optional[str], default = None
        Can be optionally provided to specify a mid-point color.

    name: Optional[str], default = "custom_cmap"
        Colormap name. Propogated into the LinearSegmentedColormap object.

    Returns
    -------
    cmap: matplotlib.colors.LinearSegmentedColormap
    """
    return CustomColorMap()(
        max_color=max_color,
        min_color=min_color,
        center_color=center_color,
        name=name,
    )
