
# -- import packages: ----------------------------------------------------------
import numpy as np
import ABCParse
import anndata


# -- Operational class: --------------------------------------------------------
class CleanUMAP(ABCParse.ABCParse):
    def __init__(self, n_stdev: int = 3) -> None:

        self.__parse__(locals(), public=[None])

    @property
    def y_mu(self):
        return self.mu[1]

    @property
    def x_mu(self):
        return self.mu[0]

    @property
    def x_sigma(self):
        return self.sigma[0] * self._n_stdev

    @property
    def y_sigma(self):
        return self.sigma[1] * self._n_stdev

    @property
    def xbounds(self):
        return (self.x_mu - self.x_sigma, self.x_mu + self.x_sigma)

    @property
    def ybounds(self):
        return (self.y_mu - self.y_sigma, self.y_mu + self.y_sigma)

    @property
    def filtered_idx(self):

        x_filt = np.abs(self.xu[:, 0].toarray() - self.x_mu) < self.x_sigma
        y_filt = np.abs(self.xu[:, 1].toarray() - self.y_mu) < self.y_sigma
        return np.all([x_filt, y_filt], axis=0)

    def __call__(self, xu: np.ndarray):

        self.__update__(locals())

        self.mu, self.sigma = self.xu.mean(0), self.xu.std(0)

        return self.filtered_idx

def clean_umap_coordinates(
    adata: anndata.AnnData, use_key: str = "X_umap", n_stdev: int = 3,
) -> np.ndarray:

    """
    Parameters
    ----------
    adata: anndata.AnnData [required]

    use_key: str, default = "X_umap"

    Returns
    -------
    X_umap_clean: np.ndarray
        Filtered UMAP coordinates.
    """

    xu = adata.obsm[use_key]

    clean_umap = CleanUMAP(n_stdev = n_stdev)
    clean_idx = clean_umap(xu=xu)

    return xu[clean_idx]
