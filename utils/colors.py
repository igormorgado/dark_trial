#!/usr/bin/env python

import numpy as np
from typing import Tuple, Callable, List

def luminance_standard(r: float, g: float, b: float) -> float:
    return 0.2126*r + 0.7152*g + 0.0722*b

def luminance_perceived(r: float, g: float, b: float) -> float:
    return 0.299*r + 0.587*g + 0.114*b

def luminance_perceived2(r: float, g: float, b: float) -> float:
    return 0.299*r*r + 0.587*g*g + 0.114*b*b

def contrast_ratio (r1: float, g1: float, b1: float,
                    r2: float, g2: float, b2: float,
                    luminance: Callable = luminance_standard) -> float:
    """WCAG 2.0 constrast standards
    AAA  7+
    AA   4.5+
    AA18 3+
    """
    l1 = luminance(r1, g1, b1)
    l2 = luminance(r2, g2, b2)
    ratio = (l1 + 0.05) / (l2 + 0.05)
    return max(ratio, 1/ratio)

def relative_luminance(r: float, g: float, b: float) -> float:
    """Returns the relative luminance from a normalized linear RGB tuple"""
    T = np.array([[0.4124, 0.3576, 0.1805],
                  [0.2126, 0.7152, 0.0722],
                  [0.0193, 0.1192, 0.9505]], dtype=float)
    D95 = T @ [r, g, b]
    return D95[1]


def channel_linear(color_channel: float, alpha: float = 0.055) -> float:
    """Convert a sRGB color channel to linear space"""
    assert(0 <= color_channel <= 1)
    
    if color_channel <= 0.04045:
        return color_channel / 12.92
    else:
        return ((color_channel + alpha) / (1 + alpha)) ** 2.4

def hex2srgb(hexcolor: str) -> Tuple[float, float, float]:
    """Convert HEX color to normalized linear sRGB"""

    hexcolor = hexcolor.strip("#")
    r = hexcolor[0:2]
    g = hexcolor[2:4]
    b = hexcolor[4:6]
    return (channel_linear(int(r, 16)/255.0),
            channel_linear(int(g, 16)/255.0),
            channel_linear(int(b, 16)/255.0))

def hexspace_generator():
    for r in range(256):
        for g in range(256):
            for b in range(256):
                yield f"{r:02x}{g:02x}{b:02x}"

def contrasts(color: str,
              black: str = "121212",
              white: str = "e3e3e3") -> Tuple[float, float]:

    return (contrast_ratio(*hex2srgb(black), *hex2srgb(color)),
            contrast_ratio(*hex2srgb(white), *hex2srgb(color)))

def good_contrast(color: str,
                  black: str = "#121212",
                  white: str = "#e3e3e3",
                  threshold: float = 4.5) -> bool:

    contrast = contrasts(color, black, white)

    return (contrast[0] >= threshold) and (contrast[1] >= threshold)

def candidates(colorspace,
               black: str = "121212",
               white: str = "e3e3e3", 
               threshold: float = 3.0) -> List[str]:
    return [color
            for color in colorspace
            if good_contrast(color, black=black, white=white, threshold=threshold)]

rgb_colorspace = hexspace_generator()
black = "000000"
white = "ffffff"
#print("Computing large colorspace")
#large_colorspace = candidates(rgb_colorspace, black=black, white=white, threshold=3.0)
#print("Computing AA colorspace")
#aa_colorspace = candidates(large_colorspace, black=black, white=white, threshold=4.5)
#print("Computing proto AAA colorspace")
#aaa_colorspace = candidates(aa_colorspace, black=black, white=white, threshold=4.5825)
#computed_contrasts = [(contrasts(color, black=black, white=white), f"#{color}") for color in aaa_colorspace]
#coordinates, colors = zip(*computed_contrasts)
#x, y = zip(*coordinates)
#plt.scatter(x,y,color=colors)






