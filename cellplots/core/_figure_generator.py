
from ._plot_dimensions import PlotDimensions


import math
import matplotlib
import ABCParse
import inspect
import matplotlib.pyplot as plt

from typing import List

class FigureGenerator(ABCParse.ABCParse):
    """Base interface for working with matplotlib and GridSpec to format multi-panel figures."""

    _plot_count = 0

    def __init__(
        self,
        nplots: int = 1,
        ncols: int = 1,
        width: float = 1.0,
        height: float = 1.0,
        hspace: float = 0,
        wspace: float = 0,
        width_ratios: List[float] = None,
        height_ratios: List[float] = None,
        *args,
        **kwargs,
    ):
        self._configure(locals())

    def _configure(self, kwargs):
        self.__parse__(kwargs, public=[None])

        for attr in ["nrows", "ncols"]:
            self._PARAMS.update({attr: getattr(self, attr)})

        self._PLOT_DIMENSIONS = PlotDimensions(
            **ABCParse.function_kwargs(func=PlotDimensions, kwargs=self._PARAMS)
        )

    @property
    def ncols(self):
        return self._ncols

    @property
    def nrows(self):
        return math.ceil(self._nplots / self.ncols)

    @property
    def width(self):
        return self._PLOT_DIMENSIONS.width

    @property
    def height(self):
        return self._PLOT_DIMENSIONS.height

    @property
    def fig(self):
        if not hasattr(self, "_fig"):
            self._fig = plt.figure(figsize=(self.width, self.height))
        return self._fig

    @property
    def grid_structure(self):
        if not hasattr(self, "_grid_structure"):
            self._grid_structure = matplotlib.gridspec.GridSpec(
                nrows=self.nrows,
                ncols=self.ncols,
                width_ratios=self._width_ratios,
                height_ratios=self._height_ratios,
                hspace=self._hspace,
                wspace=self._wspace,
            )
        return self._grid_structure

    @property
    def _AxesDict(self):
        if not hasattr(self, "_axes_dict"):
            self._axes_dict = {}
            for ax_i in range(self.nrows):
                self._axes_dict[ax_i] = {}
                for ax_j in range(self.ncols):
                    self._plot_count += 1
                    self._axes_dict[ax_i][ax_j] = self.fig.add_subplot(
                        self.grid_structure[ax_i, ax_j]
                    )
                    if self._plot_count >= self._nplots:
                        break
        return self._axes_dict

    @property
    def axes(self):
        if not hasattr(self, "_axes"):
            self._axes = []
            for i, row in self._AxesDict.items():
                for j, col in row.items():
                    self._axes.append(self._AxesDict[i][j])
        return self._axes

    def __call__(self):
        return self.fig, self.axes
