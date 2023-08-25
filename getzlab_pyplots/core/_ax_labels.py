
import matplotlib.pyplot as plt
import matplotlib
import ABCParse


from typing import Optional, Dict


class AxLabels(ABCParse.ABCParse):
    def __init__(
        self,
        title_fontsize: float = 10,
        label_fontsize: float = 8,
        tick_fontsize: float = 6,
        title_kwargs: Dict = {},
        x_label_kwargs: Dict = {},
        y_label_kwargs: Dict = {},
        tick_kwargs: Dict = {},
    ):
        
        """
        Parameters
        ----------
        title_fontsize: float, default = 10
        
        label_fontsize: float, default = 8
        
        tick_fontsize: float, default = 6
        
        title_kwargs: Dict, default = {}
        
        x_label_kwargs: Dict, default = {}
        
        y_label_kwargs: Dict, default = {}
        
        tick_kwargs: Dict, default = {}
        
        Returns
        -------
        None, instantiates class.
        """

        self.__parse__(locals(), public=[None])

    def _set_title(self):
        self.ax.set_title(
            self._title, fontsize=self._title_fontsize, **self._title_kwargs
        )

    def _set_x_label(self):
        self.ax.set_xlabel(
            self._x_label, fontsize=self._label_fontsize, **self._x_label_kwargs
        )

    def _set_y_label(self):
        self.ax.set_ylabel(
            self._y_label, fontsize=self._label_fontsize, **self._y_label_kwargs
        )

    def _set_tick_params(self):
        self.ax.tick_params(
            axis="both",
            which="both",
            labelsize=self._tick_fontsize,
            **self._tick_kwargs,
        )        
        
    def _rm_ticks(self):
        
        if self._del_xy_ticks or self._del_x_ticks:
            self.ax.set_xticks([])
        if self._del_xy_ticks or self._del_y_ticks:
            self.ax.set_yticks([])

    def _forward(self):
        
        
        self._set_title()
        self._set_x_label()
        self._set_y_label()
        self._set_tick_params()
        self._rm_ticks()

    def __call__(
        self,
        ax: plt.Axes,
        title: Optional[str] = "",
        x_label: Optional[str] = "",
        y_label: Optional[str] = "",
        del_xy_ticks: bool = False,
        del_x_ticks: bool = False,
        del_y_ticks: bool = False,
        *args,
        **kwargs,
    ):
        
        """
        Parameters
        ----------
        ax: plt.Axes [ required ]
        
        title: Optional[str], default = ""
        
        x_label: Optional[str], default = ""
        
        y_label: Optional[str], default = ""
        
        del_xy_ticks: bool, default = False
        
        del_x_ticks: bool, default = False
        
        del_y_ticks: bool, default = False
        
        
        Returns
        -------
        None, modifies passed ax according to specified parameters.
        """
        # consider an API-facing function akin to `format_ax_labels`
        
        self.__update__(locals(), public = ['ax'])

        self._forward()
