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
