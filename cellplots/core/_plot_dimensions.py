
# -- import packages: ----------------------------------------------------------
import matplotlib
import ABCParse


# -- set typing: ---------------------------------------------------------------
from typing import Tuple


# -- operational class: --------------------------------------------------------
class PlotDimensions(ABCParse.ABCParse):
    """
    Controller class for setting plot dimensions. Uses the defaults (taken from
    rcParams['figure.figsize']) and unpacks them as [width, height] = [6.4, 4.8]
    and multiplies these values by the given number of rows (nrows) and number of
    columns (ncols) as well as a width and height scaling factor to arrive at the
    overall figure size, in inches.

    https://matplotlib.org/stable/tutorials/introductory/customizing.html#:~:text=%23figure.figsize%3A%20%20%20%20%206.4%2C%204.8%20%20%23%20figure%20size%20in%20inches
    """

    def __init__(
        self,
        rcParams_key="figure.figsize",
        ncols: int = 1,
        nrows: int = 1,
        width: float = 1.0,
        height: float = 1.0,
        *args,
        **kwargs,
    ) -> None:
        """
        Parameters
        ----------
        rcParams: str, default = "figure.figsize"
            Key to access matplotlib.rcParams[rcParams_key]. Modification will likely never
            be necessary and would more likely lead to error.

        """
        self.__parse__(locals(), public=[None])

    @property
    def _DEFAULT_FIGSIZE(self):
        return matplotlib.rcParams[self._rcParams_key]

    @property
    def _DEFAULT_WIDTH(self) -> float:
        return self._DEFAULT_FIGSIZE[0]

    @property
    def _DEFAULT_HEIGHT(self) -> float:
        return self._DEFAULT_FIGSIZE[1]

    @property
    def width(self) -> float:
        return self._DEFAULT_WIDTH * self._ncols * self._width

    @property
    def height(self) -> float:
        return self._DEFAULT_HEIGHT * self._nrows * self._height

    def __call__(
        self,
        ncols: int = 1,
        nrows: int = 1,
        width: float = 1.0,
        height: float = 1.0,
        *args,
        **kwargs,
    ) -> Tuple[float]:
        """
        Parameters
        ----------
        ncols: int, default = 1
            Number of columns to include in the plot. Multiplies the default plot width.

        nrows: int, default = 1
            Number of rows to include in the plot. Multiplies the default plot height.

        width: float, default = 1.0
            Scalar multiplier of plot width.

        height: float, default = 1.0
            Scalar multiplier of plot height.

        Returns
        -------
        [width, height]: Tuple[float]
            Adjusted plot width and height
        """
        self.__update__(locals(), public=[None])

        return self.width, self.height

    def __repr__(self) -> str:
        return f"Plot size: {self.width} x {self.height} (inches)"
