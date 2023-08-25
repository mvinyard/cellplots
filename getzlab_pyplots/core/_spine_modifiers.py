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
    
    def __init__(self, *args, **kwargs)->None:
        
        """
        Parameters
        ----------
        
        Returns
        -------
        None
        """
    
        self._DELETE = SpineDeleter()
        self._COLOR = SpineColorModifier()
        self._POSITION = SpinePositionModifier()
    
    
    # -- Spine repositioning functions: ----------------------------------------
    def reposition(self, ax: plt.Axes, spines: List = [], position: List[Tuple[str, float]] = ())->None:
        
        """
        Parameters
        ----------
        ax: plt.Axes
        
        spines: List[str], default = []
            Include any or all of ['top', 'bottom', 'left', 'right']
            
        position: List[Tuple[str, float]], default = [()]
            
        Returns
        -------
        None
        """
        
        self._POSITION(ax, **{i:j for i, j in zip(spines, position)})

    # -- Spine color functions: ------------------------------------------------
    def color(self, ax: plt.Axes, spines: List  = [], colors: List = [])->None:
        
        """
        Parameters
        ----------
        ax: plt.Axes
        
        spines: List[str], default = []
            Include any or all of ['top', 'bottom', 'left', 'right']
            
        colors: List[str], default = []
            Colors corresponding in respective order to the passed list of spines.
            
        Returns
        -------
        None
        """
        
        self._COLOR(ax, **{i:j for i, j in zip(spines, colors)})    
    
    # -- Spine deleting functions: ---------------------------------------------
    def delete(self, ax: plt.Axes, spines: List[str] = [], all_spines: bool = False)->None:
        
        """
        Parameters
        ----------
        ax: plt.Axes
        
        spines: List[str], default = []
            Include any or all of ['top', 'bottom', 'left', 'right']
            
        all_spines: bool, default = False
            If True, delete all spines of ax.
            
        Returns
        -------
        None, deletes indicated spines.
        """        
        if all_spines:
            self.delete_all(ax)
        self._DELETE(ax, **{spine: True for spine in spines})
        
    def delete_all(self, ax: plt.Axes)->None:
        """
        Parameters
        ----------
        ax
        
        Returns
        -------
        None, deletes all spines.
        """
        spines = ['top', 'bottom', 'right', 'left']
        self._DELETE(ax, **{spine: True for spine in spines})
        
    def forward(self, ax: plt.Axes, mod: str)->None:
        if hasattr(self, f"_{mod}"):
            modifier = getattr(self, f"_{mod.upper()}")
            PASSED = getattr(self, f"_{mod}")
            modifier(ax, **PASSED)

    # -- Calling API: ----------------------------------------------------------
    def __call__(
        self,
        ax: plt.Axes,
        delete: Optional[Dict] = None,
        color: Optional[Dict] = None,
        position: Optional[Dict] = None,
    )->None:
        """
        Parameters
        ----------
        ax: plt.Axes [required]
        
        delete: Optional[Dict], default = None
        
        color: Optional[Dict], default = None
        
        position: Optional[Dict], default= None
        
        Returns
        -------
        None
        """
        
        self.__update__(locals(), public=[None])

        for mod in ["delete", "color", "position"]:
            self.forward(ax, mod)
