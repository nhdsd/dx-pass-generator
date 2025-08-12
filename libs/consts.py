# /libs/consts.py
# -*- coding: utf-8 -*-
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Constants for image processing.
"""
from enum import Enum as _Enum

class RatingNum(_Enum):
    """File names of the DX Rating sprites."""
    # Digits of the DX Rating
    NUM1 = "resources/general/Num1.png"
    NUM2 = "resources/general/Num2.png"
    NUM3 = "resources/general/Num3.png"
    NUM4 = "resources/general/Num4.png"
    NUM5 = "resources/general/Num5.png"
    NUM6 = "resources/general/Num6.png"
    NUM7 = "resources/general/Num7.png"
    NUM8 = "resources/general/Num8.png"
    NUM9 = "resources/general/Num9.png"
    NUM0 = "resources/general/Num0.png"

class RatingBackground(_Enum):
    """File names of the DX Rating sprites."""
    # Background
    WHITE = "resources/general/Ra1.png" # 0 - 999
    BLUE = "resources/general/Ra2.png" # 1000 - 1999
    GREEN = "resources/general/Ra3.png" # 2000 - 3999
    YELLOW = "resources/general/Ra4.png" # 4000 - 6999
    RED = "resources/general/Ra5.png" # 7000 - 9999
    PURPLE = "resources/general/Ra6.png" # 10000 - 11999
    BRONZE = "resources/general/Ra7.png" # 12000 - 12999
    SILVER = "resources/general/Ra8.png" # 13000 - 13999
    GOLD = "resources/general/Ra9.png" # 14000 - 14499
    PLATINUM = "resources/general/Ra10.png" # 14500 - 14999
    RAINBOW = "resources/general/Ra11.png" # 15000 - + inf (Theoretical Rating: ~16550)

    @classmethod
    def get_bg_name(cls, rating: int) -> str:
        """
        Get the background name for a given rating.
        Params:
            rating (int): The rating value.
        Returns:
            str: The background name for the given rating.
        """
        if not isinstance(rating, int):
            raise TypeError(f"Expected int, but got {type(rating).__name__}.")
        if rating < 0:
            raise ValueError(f"Rating must be non-negative, but got {rating}.")
        thresholds = (1000, 2000, 4000, 7000, 10000, 12000, 13000, 14000, 14500, 15000)
        index = sum(int(rating >= threshold) for threshold in thresholds)
        return tuple(cls)[index].value

class DXPass(_Enum):
    """DX Pass types."""
    BRONZE = "resources/general/BronzeBase.png"
    SILVER = "resources/general/SilverBase.png"
    GOLD = "resources/general/GoldBase.png"
    FREEDOM = "resources/general/FreedomBase.png"

    @classmethod
    def get_pass_name(cls, pass_type: str) -> str:
        """
        Get the DX Pass name for a given type.
        Params:
            pass_type (str): The DX Pass type.
        Returns:
            str: The DX Pass name for the given type.
        """
        if not isinstance(pass_type, str):
            raise TypeError(f"Expected str, but got {type(pass_type).__name__}.")
        return cls[pass_type.upper()].value

class Icon(_Enum):
    """Icon types."""
    FREEDOM = "resources/general/IconFreedom.png"
    LEVEL = "resources/general/IconLevel.png"
    RATING = "resources/general/IconRating.png"
    MASTER = "resources/general/IconMaster.png"
    POWER1 = "resources/general/IconPower1.png"
    POWER2 = "resources/general/IconPower2.png"
    POWER3 = "resources/general/IconPower3.png"
    POWER4 = "resources/general/IconPower4.png"

    def __or__(self, other: "Icon") -> list["Icon"]:
        if not isinstance(other, Icon):
            raise TypeError(f"Expected Icon, but got {type(other).__name__}.")
        return [self, other]

    def __ror__(self, other: list["Icon"]) -> list["Icon"]:
        if not isinstance(other, list) or not all(isinstance(i, Icon) for i in other):
            raise TypeError(f"Expected list of Icon, but got {type(other).__name__}.")
        return other + [self]

class IconPreset(_Enum):
    """Icon preset types."""
    GOLD = Icon.LEVEL | Icon.MASTER | Icon.RATING
    FREEDOM = Icon.FREEDOM | Icon.MASTER | Icon.RATING

    # Before maimai DX Splash PLUS...
    OLD_BRONZE = Icon.POWER1
    OLD_SILVER = Icon.POWER2
    OLD_GOLD = Icon.POWER3 | Icon.MASTER | Icon.RATING
    OLD_PLATINUM = Icon.POWER4 | Icon.MASTER | Icon.RATING
