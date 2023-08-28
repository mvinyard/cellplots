
from ._base_figure_container import BaseFigureContainer

class UMAP(BaseFigureContainer):
    def __init__(self, delete="all", del_xy_ticks=[True], *args, **kwargs):
        super().__init__()

        self.__parse__(locals(), public=[None])

        self._configure_canvas(**self._CANVAS_KWARGS)

    def __call__(self, x, y, *args, **kwargs):

        for ax in self.axes:
            ax.scatter(x, y, *args, **kwargs)