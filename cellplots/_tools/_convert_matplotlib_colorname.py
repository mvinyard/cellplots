
import ABCParse
import matplotlib.colors

class MatplotlibColorNameConverter(ABCParse.ABCParse):
    def __init__(self, *args, **kwargs):
        self.__parse__(locals(), public=[None])

    @property
    def single_letter_codes(self):
        return {
            "b": "blue",
            "g": "green",
            "r": "red",
            "c": "cyan",
            "m": "magenta",
            "y": "yellow",
            "k": "black",
            "w": "white",
        }

    @property
    def color_name(self):
        if self._color in self.single_letter_codes:
            return self.single_letter_codes[self._color]
        return self._color

    def _to_hex(self, color_name):
        return matplotlib.colors.mcolors.cnames.get(color_name, None)

    def __call__(self, color: str, *args, **kwargs) -> str:
        self.__update__(locals(), public=[None])
        return self._to_hex(self.color_name)


# -- API-facing function: -----------------------------------------------------
def convert_matplotlib_colorname(color: str) -> str:
    """
    Parameters
    ----------
    color: str

    Returns
    -------
    hex_code: str
    """
    return MatplotlibColorNameConverter()(color)
