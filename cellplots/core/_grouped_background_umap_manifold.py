

# -- import packages: ----------------------------------------------------------
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import pandas as pd
import ABCParse
import anndata


# -- import local depenendencies: ----------------------------------------------
from .. import _tools as tl


# -- set typing: ---------------------------------------------------------------
from ._base_figure_container import BaseFigureContainer as FigureContainer
from typing import Optional, List, Dict
from ._group_count_zorder import GroupCountZOrder
from ._umap import UMAP


# -- controller class: ---------------------------------------------------------
class GroupedBackgroundUMAPManifold(ABCParse.ABCParse):
    def __init__(
        self,
        umap_fig: Optional[FigureContainer] = None,
        clean_stdev: float = 3.5,
        sizes=[80, 40],
        cover_color="w",
        rasterized=True,
        *args,
        **kwargs
    ):

        self.__parse__(locals(), public=[None])
        self._cells_plotted = {}

    @property
    def _UMAP_KWARGS(self):
        
        PARAMS = self._PARAMS.copy()
        PARAMS.update(self._PARAMS['kwargs'])
        PARAMS.pop("kwargs")
        
        return ABCParse.function_kwargs(FigureContainer, kwargs = PARAMS)
    
    @property
    def UMAP(self):
        if self._umap_fig is None:
            self._umap_fig = UMAP(**self._UMAP_KWARGS)
        return self._umap_fig
        
    @property
    def _GROUPED(self):
        return self._obs_df.groupby(self._groupby)

    @property
    def _ZORDER_DICT(self) -> Dict:
        if not hasattr(self, "_zorder_dict"):
            self._group_count_zorder = GroupCountZOrder()
            self._zorder_dict = self._group_count_zorder(self._adata, self._groupby)
        return self._zorder_dict

    def forward(self, adata_group, group, en):

        xu = tl.clean_umap_coordinates(adata_group, n_stdev=self._clean_stdev)
        
        if self._cmap_arg is None:
            color = self._cmap[en]
        else:
            color = self._cmap[group]
            
        self.UMAP(
            xu[:, 0],
            xu[:, 1],
            s=self._sizes[0],
            color=color,
            ec="None",
            rasterized=self._rasterized,
            zorder=self._ZORDER_DICT[group],
        )
        self.UMAP(
            xu[:, 0],
            xu[:, 1],
            s=self._sizes[1],
            c=self._cover_color,
            ec="None",
            rasterized=self._rasterized,
            zorder=self._ZORDER_DICT[group],
        )
        self._cells_plotted[group] = {
            "available": adata_group.shape[0],
            "plotted": xu.shape[0],
        }

    @property
    def _STATS(self) -> pd.DataFrame:

        cells_plotted = pd.DataFrame(self._cells_plotted)
        cells_plotted.loc["pct"] = (
            cells_plotted.loc["plotted"] / cells_plotted.loc["available"]
        )
        return cells_plotted
    
    @property
    def fig(self):
        return self.UMAP.fig
    
    @property
    def axes(self):
        return self.UMAP.axes

    def __call__(
        self,
        adata: anndata.AnnData,
        groupby: str,
        cmap: Optional[Dict] = None,
        *args,
        **kwargs
    ):
        
        """
        
        """

        self.__update__(locals(), public=[None], ignore=["adata"])

        self._adata = adata.copy()
        self._obs_df = self._adata.obs.copy()
        
        if cmap is None:
            self._cmap_arg = None
            self._cmap = cm.tab20.colors
        else:
            self._cmap_arg = self._cmap

        for en, (group, group_df) in enumerate(self._GROUPED):
            self.forward(self._adata[group_df.index], group, en)


# -- API-facing function: ------------------------------------------------------
def grouped_background_umap_manifold(
    adata: anndata.AnnData,
    groupby: str,
    cmap: Optional[Dict] = None,
    clean_stdev: float = 3.5,
    sizes=[80, 40],
    cover_color="w",
    umap_fig: Optional[FigureContainer] = None,
    rasterized=True,
    *args,
    **kwargs,
):
    manifold = GroupedBackgroundUMAPManifold(
        umap_fig=umap_fig,
        clean_stdev=clean_stdev,
        sizes=sizes,
        cover_color=cover_color,
        rasterized=rasterized,
        *args,
        **kwargs,
    )
    manifold(adata = adata, groupby = groupby, cmap = cmap)
    return manifold
