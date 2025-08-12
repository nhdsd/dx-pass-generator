# /main.py
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
Main entry point for the application.
"""
from libs.utils import to_full_width as _to_full_width
from libs.draw import draw_rating as _draw_rating, draw_name as _draw_name\
    ,draw_friend_code as _draw_friend_code, draw_aime_and_version as _draw_aime_and_version\
    ,draw_qr_code as _draw_qr_code, draw_icon as _draw_icon, draw_basic as _draw_basic\
    ,draw_chara_name as _draw_chara_name, draw_date as _draw_date
from libs.consts import Icon as _Icon, DXPass as _Pass

BACKGROUND: int = 500001
CHARA: int = 550105
NAME: str = "AAAAAAAA"
RATING: int = 15000
FRIENDCODE = None
AIME = 12345678901234567890
VERSION = "[maimaiDX]1.55-0291"
QRCODE = "C:\\7sRef\\System256\\metaverse\\finalhope"
ICONS = _Icon.LEVEL | _Icon.MASTER | _Icon.RATING
DATE = None

def _main():
    result = _draw_basic(BACKGROUND, CHARA, _Pass.GOLD)
    result = _draw_rating(RATING, result)
    result = _draw_name(_to_full_width(NAME), result)
    result = _draw_friend_code(FRIENDCODE, result)
    result = _draw_aime_and_version(AIME, VERSION, result)
    result = _draw_qr_code(QRCODE, result)
    result = _draw_icon(ICONS, result)
    result = _draw_chara_name(CHARA, result)
    result = _draw_date(DATE, result)
    result.save("output.png")

if __name__ == "__main__":
    _main()
