
import ABCParse
from typing import Tuple

class HexToRGB(ABCParse.ABCParse):
    def __init__(self, *args, **kwargs):
        self.__parse__(locals(), public=[None])

    @property
    def _HEX_CODE(self):
        return self._hex_code.lstrip("#")

    @property
    def R(self):
        return self._forward(self._HEX_CODE[0:2])

    @property
    def G(self):
        return self._forward(self._HEX_CODE[2:4])

    @property
    def B(self):
        return self._forward(self._HEX_CODE[4:6])

    def _forward(self, hex_slice: str, divisor=255.0):
        return int(hex_slice, 16) / divisor

    def __call__(self, hex_code: str, *args, **kwargs) -> Tuple:

        self.__update__(locals(), public=[None])

        return tuple([self.R, self.G, self.B])


# -- API-facing function: -----------------------------------------------------
def hex_to_rgb(hex_code: str) -> Tuple[float]:

    """
    Convert a hex color code to an RGB tuple with values in the range [0, 1].
    Parameters
    ----------
    hex_code: str
        String representing the hex color code. Can start with '#' or not.

    Returns
    -------
    RGB: Tuple[float]
        RGB tuple with float values in the range [0, 1].
    """
    converter = HexToRGB()
    return converter(hex_code=hex_code)
