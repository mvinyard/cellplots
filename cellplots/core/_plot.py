# _plot.py

# -- import packages: ----------------------------------------------------------
import ABCParse
import matplotlib.pyplot as plt


# -- import local dependencies: ------------------------------------------------
from ._base_figure_container import BaseFigureContainer


# -- set typing: ---------------------------------------------------------------
from typing import List, Optional, Dict, Tuple


# -- API-facing function: ------------------------------------------------------
def plot(
    nplots: int = 1,
    ncols: int = 1,
    width: float = 1.0,
    height: float = 1.0,
    hspace: float = 0,
    wspace: float = 0,
    width_ratios: Optional[List[float]] = None,
    height_ratios: Optional[List[float]] = None,
    title: Optional[List[str]] = [""],
    x_label: Optional[List[str]] = [""],
    y_label: Optional[List[str]] = [""],
    del_xy_ticks: List[bool] = [False],
    del_x_ticks: List[bool] = [False],
    del_y_ticks: List[bool] = [False],
    title_fontsize: List[float] = [10],
    label_fontsize: List[float] = [8],
    tick_fontsize: List[float] = [6],
    title_kwargs: Optional[List[Dict]] = [{}],
    x_label_kwargs: Optional[List[Dict]] = [{}],
    y_label_kwargs: Optional[List[Dict]] = [{}],
    tick_kwargs: Optional[List[Dict]] = [{}],
    color: Optional[List[Dict]] = [{}],
    delete: Optional[List[List]] = [[]],
    position: Optional[List[Dict[str, List[Tuple[str, float]]]]] = [{}],
    *args,
    **kwargs,
) -> Tuple[plt.Figure, List[plt.Axes]]:
    """
    Parameters
    ----------
    nplots: int, default = 1

    ncols: int, default = 1

    width: float, default = 1.0

    height: float, default = 1.0

    hspace: float, default = 0

    wspace: float, default = 0
    width_ratios: Optional[List[float]], default = None

    height_ratios: Optional[List[float]], default = None

    title: Optional[List[str]], default = [""]

    x_label: Optional[List[str]], default = [""]

    y_label: Optional[List[str]], default = [""]

    del_xy_ticks: List[bool], default = [False]

    del_x_ticks: List[bool], default = [False]

    del_y_ticks: List[bool], default = [False]

    title_fontsize: List[float], default = [10]

    label_fontsize: List[float], default = [8]

    tick_fontsize: List[float], default = [6]

    title_kwargs: Optional[List[Dict]], default = [{}]

    x_label_kwargs: Optional[List[Dict]], default = [{}]

    y_label_kwargs: Optional[List[Dict]], default = [{}]

    tick_kwargs: Optional[List[Dict]], default = [{}]

    color: Optional[List[Dict]], default = [{}]

    delete: Optional[List[List]], default = [[]]

    position: Optional[List[Dict[str, List[Tuple[str, float]]]]], default = [{}]

    *args
    **kwargs

    Returns
    -------
    (fig, axes): Tuple[plt.Figure, List[plt.Axes]]
    """

    KWARGS = ABCParse.function_kwargs(func=BaseFigureContainer, kwargs=locals())
    figure = BaseFigureContainer(**KWARGS)
    figure._configure_canvas(**figure._CANVAS_KWARGS)

    return figure.fig, figure.axes