from typing import Tuple, Optional, List, Dict, Union

import ABCParse
import matplotlib.pyplot as plt


class BaseSpineModifier(ABCParse.ABCParse):
    def __init__(self, *args, **kwargs):
        self.__parse__(locals())

    def _select_axes(self, kwargs, ignore=[]):
        ignore += ["self", "args", "kwargs", "ax"]
        return {k: v for k, v in kwargs.items() if not k in ignore and not v is None}


class SpineDeleter(BaseSpineModifier):
    def __init__(self):
        super().__init__()

    @property
    def _SPINES_TO_DELETE(self):
        _axes = self._select_axes(self._PARAMS)
        return [k for k, v in _axes.items() if v == True]

    def forward(self, ax, spine):
        ax.spines[spine].set_visible(False)

    def __call__(
        self,
        ax,
        top: Optional[bool] = None,
        bottom: Optional[bool] = None,
        right: Optional[bool] = None,
        left: Optional[bool] = None,
    ):
        self.__update__(locals(), public=[None])

        for spine in self._SPINES_TO_DELETE:
            self.forward(ax, spine)


class SpineColorModifier(BaseSpineModifier):
    def __init__(self):
        super().__init__()

    @property
    def _SPINES_TO_RECOLOR(self) -> Dict:
        return self._select_axes(self._PARAMS, ignore=["position_type", "amount"])

    def forward(self, ax, spine, color):
        ax.spines[spine].set_color(color)

    def __call__(
        self,
        ax: plt.Axes,
        top: Optional[str] = None,
        bottom: Optional[str] = None,
        right: Optional[str] = None,
        left: Optional[str] = None,
    ):
        self.__update__(locals(), public=[None])

        for spine, color in self._SPINES_TO_RECOLOR.items():
            self.forward(ax, spine, color)


class SpinePositionModifier(BaseSpineModifier):
    def __init__(self):
        super().__init__()

    @property
    def _SPINES_TO_REPOSITION(self) -> Dict:
        return self._select_axes(self._PARAMS)

    def forward(self, ax, spine, position_type, amount):
        ax.spines[spine].set_position((position_type, amount))

    def __call__(
        self,
        ax: plt.Axes,
        top: Optional[Tuple[str, float]] = None,
        bottom: Optional[Tuple[str, float]] = None,
        right: Optional[Tuple[str, float]] = None,
        left: Optional[Tuple[str, float]] = None,
    ):
        self.__update__(locals(), public=[None])

        for spine, (position_type, amount) in self._SPINES_TO_REPOSITION.items():
            self.forward(ax, spine, position_type, amount)

            
class AxSpineModifier(ABCParse.ABCParse):
    
    """
    Container modifier to control all above modifiers for a single ax.
    """
    
    def __init__(self):
        self._DELETE = SpineDeleter()
        self._COLOR = SpineColorModifier()
        self._POSITION = SpinePositionModifier()

    def forward(self, ax, mod):
        if hasattr(self, f"_{mod}"):
            modifier = getattr(self, f"_{mod.upper()}")
            PASSED = getattr(self, f"_{mod}")
            modifier(ax, **PASSED)

    def __call__(
        self,
        ax: plt.Axes,
        delete: Optional[Dict] = None,
        color: Optional[Dict] = None,
        position: Optional[Dict] = None,
    ):
        self.__update__(locals(), public=[None])

        for mod in ["delete", "color", "position"]:
            self.forward(ax, mod)
