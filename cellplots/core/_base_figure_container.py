from typing import List, Dict, Optional, Tuple
import ABCParse
import abc


from ._figure_generator import FigureGenerator
from ._ax_labels import AxLabels
from ._spine_modifiers import AxSpineModifier


class BaseFigureContainer(ABCParse.ABCParse):
    def __init__(
        self,
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
    ):

        self.__parse__(locals(), public=[None])

    @property
    def _CANVAS_KWARGS(self):
        self._PARAMS.update(self._PARAMS["kwargs"])

        PARAMS = ABCParse.function_kwargs(
            func=self._configure_canvas, kwargs=self._PARAMS
        )
        return PARAMS

    def _configure_canvas(
        self,
        nplots: int = 1,
        ncols: int = 1,
        width: float = 1.0,
        height: float = 1.0,
        hspace: float = 0,
        wspace: float = 0,
        width_ratios: Optional[List[float]] = None,
        height_ratios: Optional[List[float]] = None,
        *args,
        **kwargs,
    ):

        self._AX_LABELS = AxLabels()

        # STEP 0: intake
        self.__update__(locals(), public=[None])
        # STEP 1: Generate the figure canvas
        self._generate_figure()
        # STEP 3: Now do modifications to axes
        self._make_figure_modifications()

    @property
    def _FIGURE_GENERATOR_KWARGS(self):
        return ABCParse.function_kwargs(
            func=FigureGenerator, kwargs=self._PARAMS
        )

    # -- STEP 1/3: generate canvas of fig, axes
    def _generate_figure(self):
        self._FIG_GEN = FigureGenerator(**self._FIGURE_GENERATOR_KWARGS)
        self.fig, self.axes = self._FIG_GEN()

    #     # -- STEP 2/3: do plotting
    #     @abc.abstractmethod
    #     def forward(self):
    #         ...
    # MOVED TO __CALL__

    # -- STEP 3/3: make modifications to fig, axes canvas
    def _make_figure_modifications(self):
        """Make modifications to axes, labels, etc."""

        _init_kw = ABCParse.function_kwargs(func=AxLabels, kwargs=self._PARAMS)

        _call_kw = ABCParse.function_kwargs(
            func=AxLabels.__call__, kwargs=self._PARAMS
        )

        nplots = self._PARAMS["nplots"]
        _IGNORE = ["args"]

        init_kw = {}
        for k, v in _init_kw.items():
            if not k in _IGNORE:
                if len(v) < nplots:
                    v += v * (nplots - len(v))
            init_kw[k] = v

        call_kw = {}
        for k, v in _call_kw.items():
            if not k in _IGNORE:
                if len(v) < nplots:
                    v += v * (nplots - len(v))
                call_kw[k] = v

        for en, ax in enumerate(self.axes):

            ax_init_kw = {k: v[en] for k, v in init_kw.items()}
            ax_call_kw = {k: v[en] for k, v in call_kw.items()}

            ax_labels = AxLabels(**ax_init_kw)
            ax_labels(ax, **ax_call_kw)

        # coordinates modifying spine colors
        SPINE_COLOR_MODS = self._PARAMS["color"]
        N_COLOR_MODS = len(SPINE_COLOR_MODS)
        if N_COLOR_MODS:

            for en, ax in enumerate(self.axes):
                if en < N_COLOR_MODS:
                    SPINE_MODIFIER = AxSpineModifier()
                    spines = list(SPINE_COLOR_MODS[en].keys())
                    colors = list(SPINE_COLOR_MODS[en].values())
                    SPINE_MODIFIER.color(self.axes[en], spines=spines, colors=colors)

        # coordinates deleting spines

        SPINE_DELETIONS = self._PARAMS["delete"]
        if SPINE_DELETIONS == "all":
            for en, ax in enumerate(self.axes):
                SPINE_MODIFIER = AxSpineModifier()
                SPINE_MODIFIER.delete_all(ax)

        else:

            N_DELETE = len(SPINE_DELETIONS)
            if N_DELETE:

                for en, ax in enumerate(self.axes):
                    SPINE_MODIFIER = AxSpineModifier()
                    if en < N_DELETE:
                        SPINE_MODIFIER.delete(self.axes[en], spines=SPINE_DELETIONS[en])

        # coordinates repositioning spines
        SPINE_REPOSITIONING = self._PARAMS["position"]
        N_REPOSITION = len(SPINE_REPOSITIONING)
        if N_REPOSITION:

            for en, ax in enumerate(self.axes):
                SPINE_MODIFIER = AxSpineModifier()
                if en < N_REPOSITION:
                    spines = list(SPINE_REPOSITIONING[en].keys())
                    position = list(SPINE_REPOSITIONING[en].values())
                    if position == "all":
                        position = ["top", "bottom", "right", "left"]
                    SPINE_MODIFIER.reposition(
                        self.axes[en], spines=spines, position=position
                    )

    def __call__(self, *args, **kwargs):

        """
        Specific plotting kwargs are passed in __call__, while figure setup and Figure modifiers options are passed
        in __init__

        STEP 2: do plotting (variable pending inherented class)
        """