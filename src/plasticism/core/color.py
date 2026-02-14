import math
import numpy as np

from pygame.color import Color

def oklab_to_rgb(L: float, a: float, b: float, clamp: bool=True, decimals: int=3) -> tuple[float, float, float]:
    """
    Converts an OKLab color to an RGB color.

    :param L: Lightness `[0.0, 1.0]`
    :param a: a* `[-0.4, 0.4]`
    :param b: b* `[-0.4, 0.4]`
    :param clamp: Whether to clamp the output to [0.0, 1.0)
    :param decimals: Number of decimal places to round to
    :return: Color in RGB format [0.0, 1.0) if clamp
    """

    # OKLab to linear LMS
    # M1^{-1}
    M1_inv = np.array([
        [1.0, 0.3963377774, 0.2158037573],
        [1.0, -0.1055613458, -0.0638541728],
        [1.0, -0.0894841775, -1.2914855480]
    ])
    
    lab_vector = np.array([L, a, b])
    lms_linear = M1_inv @ lab_vector
    
    lms = lms_linear ** 3
    
    # linear LMS to linear sRGB
    # M2^{-1}
    M2_inv = np.array([
        [4.0767416621, -3.3077115913, 0.2309699292],
        [-1.2684380046, 2.6097574011, -0.3413193965],
        [-0.0041960863, -0.7034186147, 1.7076147010]
    ])
    
    rgb_linear = M2_inv @ lms
    
    # linear sRGB to sRGB
    def gamma_correction(x: float) -> float:
        if x <= 0.0031308:
            return 12.92 * x
        else:
            return 1.055 * (x ** (1/2.4)) - 0.055
    
    rgb = np.array([gamma_correction(val) for val in rgb_linear])
    
    if clamp:
        rgb = np.clip(rgb, 0.0, 1.0)
    
    rgb_01 = tuple(round(val, decimals) for val in rgb)
    
    return rgb_01

def oklch_to_rgb(L: float, C: float, H: float, clamp: bool=True, decimals: int=3) -> tuple[float, float, float]:
    """
    Converts an OKLCH color to an RGB color.

    :param L: Lightness `[0.0, 1.0]`
    :param C: Chroma `[0.0, 0.4]`
    :param H: Hue `[0.0, 360.0]`
    :param clamp: Whether to clamp the output to [0.0, 1.0)
    :param decimals: Number of decimal places to round to
    :return: Color in RGB format [0.0, 1.0) if clamp
    """

    # OKLCH to OKLab
    H_rad = math.radians(H)
    a = C * math.cos(H_rad)
    b = C * math.sin(H_rad)
    
    return oklab_to_rgb(L, a, b, clamp=clamp, decimals=decimals)

def oklch_to_rgb_int8(L: float, C: float, H: float) -> tuple[int, int, int]:
    rgb_01 = oklch_to_rgb(L, C, H, clamp=True)
    return tuple((round(val * 255) for val in rgb_01))  # type: ignore

def oklab_to_rgb_int8(L: float, a: float, b: float) -> tuple[int, int, int]:
    rgb_01 = oklab_to_rgb(L, a, b, clamp=True)
    return tuple((round(val * 255) for val in rgb_01))  # type: ignore


class Oklch(Color):
    def __init__(self, L: float, C: float, H: float, a: int = 255):
        self._L = L
        self._C = C
        self._H = H
        self.a = a
        self.update_oklch()
    
    def update_oklch(self):
        super().__init__(*oklch_to_rgb_int8(self.L, self.C, self.H), self.a)

    @property
    def L(self) -> float:
        return self._L
    @L.setter
    def L(self, value: float):
        self._L = value
        self.update_oklch()

    @property
    def C(self) -> float:
        return self._C
    @C.setter
    def C(self, value: float):
        self._C = value
        self.update_oklch()

    @property
    def H(self) -> float:
        return self._H
    @H.setter
    def H(self, value: float):
        self._H = value
        self.update_oklch()

    @property
    def oklch(self) -> tuple:
        return (self.L, self.C, self.H)

    def __repr__(self) -> str:
        return f"Oklch({self.L}, {self.C}, {self.H}, {self.a})"