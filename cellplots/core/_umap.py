

# -- import libraries: --------------------------------------------------------
from abc import abstractmethod
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import anndata
import adata_query
import matplotlib

# -- import local dependencies ------------------------------------------------
from ._base_figure_container import BaseFigureContainer
from ._group_count_zorder import GroupCountZOrder
from .. import _tools as tl

# -- set typing: --------------------------------------------------------------
from typing import Optional, Union, Dict, List


# -- Operational base class: --------------------------------------------------
class BaseUMAP(BaseFigureContainer):
    def __init__(
        self,
        ax: Optional[plt.Axes] = None,
        delete: Optional[str] = "all",
        del_xy_ticks: List[bool] = [True],
        *args,
        **kwargs,
    ) -> None:
        """
        Parameters
        ----------
        ax: Optional[plt.Axes], default = None
        
        delete: Optional[str], default = "all"
        
        del_xy_ticks: List[bool], default = [True]
        
        Returns
        -------
        None
        """
        super().__init__(*args, **kwargs)

        self.__parse__(locals(), public=[None], ignore=["ax"])
        self._configure_axes(ax)

    def _configure_axes(self, ax: plt.Axes) -> None:

        if ax is None:
            self._configure_canvas(**self._CANVAS_KWARGS)
        else:
            self.axes = [ax]

    @abstractmethod
    def forward(self):
        ...

    def __call__(self, adata: anndata.AnnData, *args, **kwargs):
        """
        Parameters
        ----------
        adata: anndata.AnnData

        Returns
        -------
        """
        self.__update__(locals(), public=[None])


# -- Operational API-facing class: --------------------------------------------
class UMAP(BaseUMAP):
    def __init__(
        self,
        use_key: str = "X_umap",
        rasterized: bool = True,
        zorder_boost: int = 0,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)

        self.__parse__(locals(), public=[None])

    def _get_highest_zorder(self, ax):
        return max([_.zorder for _ in ax.get_children()])
    
    @property
    def _GROUPBY(self):
        if hasattr(self, "_groupby"):
            return self._groupby
        return None
    @property
    def s(self):
        if hasattr(self, "_s"):
            return self._s
        return matplotlib.rcParams["lines.markersize"] ** 2
    
    @property
    def _HIGHEST_PLOTTED_ZORDER(self):
        return max([self._get_highest_zorder(ax) for ax in self.axes])

    @property
    def _GROUPED(self) -> bool:
        return (not self._GROUPBY is None)

    @property
    def _N_GROUPS(self):
        return len(self._GROUPED_DATA)

    def _from_adata(self, adata: anndata.AnnData, groupby: Optional[str] = None):
        if self._GROUPED:
            return adata_query.fetch(adata, key=self._use_key, groupby=self._GROUPBY)
        return {"all": adata_query.fetch(adata, key=self._use_key)}

    @property
    def _GROUPED_DATA(self):
        return self._from_adata(self._adata, self._GROUPBY)

    @property
    def _ZORDER_CONTROLLER(self):
        if not hasattr(self, "_zorder_controller"):
            self._zorder_controller = GroupCountZOrder()
        return self._zorder_controller

    @property
    def _ZORDER(self):
        if self._GROUPED:
            ZORDER = self._ZORDER_CONTROLLER(
                self._adata, groupby=self._GROUPBY, force=self._force_zorder
            )
            return ZORDER[self._CURRENT_LABEL] + self._zorder_boost
        return self._HIGHEST_PLOTTED_ZORDER + 1 + self._zorder_boost

    @property
    def _quantitatively_colored(self) -> bool:
        return any(
            [
                isinstance(self._PARAMS["c"], type_check)
                for type_check in [pd.Series, np.ndarray, List]
            ]
        )
    
    @property
    def _CMAP(self):

        if "c" in self._PARAMS:
            if isinstance(self._PARAMS["c"], str):
                return {"c": self._PARAMS["c"]}
            elif self._quantitatively_colored:
                numerical_cmap = {}
                for attr in ["c", "vmin", "vmax", "cmap"]:
                    if attr in self._PARAMS:
                        numerical_cmap[attr] = self._PARAMS[attr]
                return numerical_cmap
            
        # if hasattr(self, "_cmap") and (not self._GROUPED):
        if hasattr(self, "_cmap") and isinstance(self._cmap, Dict):
            return {"c": self._cmap[self._CURRENT_LABEL]}
        return {"c": "lightgrey"} # {}

    @property
    def _UMAP_CLEANER(self):
        if hasattr(self, "_clean_stdev"):
            if not hasattr(self, "_umap_cleaner"):
                self._umap_cleaner = tl.CleanUMAP(n_stdev=self._clean_stdev)
            return self._umap_cleaner

    def forward(
        self,
        X_umap: np.ndarray,
        label: str,
        en: int,
    ):

        self._CURRENT_LABEL = label
        self._CUREENT_ITER = en

        if hasattr(self, "_clean_stdev"):
            X_umap = X_umap[self._UMAP_CLEANER(X_umap)]

        KWARGS = {
            "label": self._CURRENT_LABEL,
            "zorder": self._ZORDER,
            "s": self.s,
            "ec": self._ec,
            "alpha": self._alpha,
            "rasterized": self._rasterized,
        }
        KWARGS.update(self._CMAP)

        for ax in self.axes:
            ax.scatter(X_umap[:, 0], X_umap[:, 1], **KWARGS)
            
    def _format_return(self):
        if hasattr(self, "fig"):
            return (self.fig, self.axes)
        return self.axes

    def __call__(
        self,
        adata: anndata.AnnData,
        groupby: Optional[str] = None,
        s: Optional[int] = None,
        c: Optional[str] = None,
        alpha: float = 1,
        ec: str = "None",
        cmap: Optional[Union[Dict, str]] = None,
        clean_stdev: Optional[float] = None,
        force_zorder: Optional[Dict[str, int]] = {},
        *args,
        **kwargs,
    ):
        """
        Parameters
        ----------
        adata: anndata.AnnData

        groupby: Optional[str], default = None
            Column of adata.obs by which to group (and subsequently color) cells.

        cmap: Optional[
                  Union[
                      Dict,
                      str,
                      matplotlib.colors.LinearSegmentedColormap,
                      matplotlib.colors.ListedColormap,
                  ]
              ], default = None
              Colormap by which to color cells or groups of plotted cells.

        Returns
        -------
        (fig, axes): Tuple[plt.Figure, List[plt.Axes]]
        """
        self.__update__(locals(), public=[None])
        
        for en, (label, X_umap) in enumerate(self._GROUPED_DATA.items()):
            self.forward(X_umap, en=en, label=label)

        return self.axes # self._format_return()
    
# -- API-facing function: ----
def umap(
    adata: anndata.AnnData,
    groupby: Optional[str] = None,
    s: float = None,
    c: Optional[str] = None,
    alpha: float = 1,
    ec: str = "None",
    cmap: Optional[Union[Dict, str]] = None,
    clean_stdev: Optional[float] = None,
    force_zorder: Optional[Dict[str, int]] = {},
    ax: Optional[plt.Axes] = None,
    delete: Optional[str] = "all",
    del_xy_ticks: List[bool] = [True],
    *args,
    **kwargs,
):

    umap_figure = UMAP(ax=ax, delete=delete, del_xy_ticks=del_xy_ticks)
    umap_figure(
        adata=adata,
        groupby=groupby,
        s=s,
        c=c,
        alpha=alpha,
        ec=ec,
        cmap=cmap,
        clean_stdev=clean_stdev,
        force_zorder=force_zorder,
        *args,
        **kwargs,
    )
    return umap_figure.axes

    
def umap_manifold(
    adata,
    groupby=None,
    c_background="k",
    c_cover="w",
    s_background=120,
    s_cover=60,
    clean_stdev=3,
    ax = None,
    *args,
    **kwargs
):

    if isinstance(c_background, str):
        kwargs = {"c": c_background}
    elif isinstance(c_background, Dict):
        kwargs = {"cmap": c_background}

    umap_figure = UMAP(ax = ax)
    axes = umap_figure(
        adata=adata,
        groupby=groupby,
        alpha=1,
        s=s_background,
        clean_stdev=clean_stdev,
        **kwargs
    )
        
    zorder_boost = int(umap_figure._HIGHEST_PLOTTED_ZORDER + 1)
    
    updated_axes = []
    for ax in axes:
        umap_figure_cover = UMAP(ax=ax, zorder_boost=zorder_boost)
        ax_ = umap_figure_cover(
            adata, groupby=groupby, c=c_cover, s=s_cover, clean_stdev=clean_stdev
        )[0]
        updated_axes.append(ax_)

    return updated_axes