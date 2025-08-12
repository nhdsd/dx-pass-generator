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
from libs.parse import argparser as _argparser
from libs.utils import to_full_width as _to_full_width
from libs.draw import draw_rating as _draw_rating, draw_name as _draw_name\
    ,draw_friend_code as _draw_friend_code, draw_aime_and_version as _draw_aime_and_version\
    ,draw_qr_code as _draw_qr_code, draw_icon as _draw_icon, draw_basic as _draw_basic\
    ,draw_chara_name as _draw_chara_name, draw_date as _draw_date

def _main():
    args = _argparser()
    result = _draw_basic(args.background, args.chara, args.pass_type)
    result = _draw_rating(args.rating, result)
    if args.full_width:
        result = _draw_name(_to_full_width(args.player_name), result)
    else:
        result = _draw_name(args.player_name, result)
    result = _draw_friend_code(args.friend_code, result)
    result = _draw_aime_and_version(args.aime, args.version, result)
    result = _draw_qr_code(args.qr_code, result)
    result = _draw_icon(args.icon, result)
    result = _draw_chara_name(args.chara, result)
    result = _draw_date(args.date, result)
    result.save("output.png")

if __name__ == "__main__":
    _main()
