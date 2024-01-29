

# -- import packages: ----------------------------------------------------------
import anndata


# -- set typing: ---------------------------------------------------------------
from typing import Optional, Dict


# -- Controller class: ---------------------------------------------------------
class GroupCountZOrder:
    def __init__(self, *args, **kwargs):
        """
        Would be more efficient to pass a pre-grouped object but this is simpler.
        """

    @property
    def _GROUPED(self):
        return self._df.groupby(self._groupby)

    @property
    def _GROUPED_SIZE(self):
        return self._GROUPED.size()

    def forward(self):
        
        ITERABLE = self._GROUPED_SIZE.sort_values(ascending=False).index
        GROUP_ORDER = {}
        
        for i, group in enumerate(ITERABLE):
            if group in self._force:
                GROUP_ORDER[group] = self._force[group]
            else:
                GROUP_ORDER[group] = int(i + 1)

        return GROUP_ORDER

    def __call__(
        self,
        adata: anndata.AnnData,
        groupby: str,
        force: Optional[Dict] = {},
        *args,
        **kwargs,
    ):

        self._df = adata.obs.copy()
        self._groupby = groupby
        self._force = force

        return self.forward()


# -- API-facing function: ------------------------------------------------------
def group_count_z_order(
    adata: anndata.AnnData,
    groupby: str,
    force: Optional[Dict] = {},
    *args,
    **kwargs,
):
    
    zorder_dict = GroupCountZOrder()
    return zorder_dict(
        adata = adata,
        groupby = groupby,
        force = force,
    )
