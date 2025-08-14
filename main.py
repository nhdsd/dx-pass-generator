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
from time import time as _time

from libs.parse import argparser as _argparser
from libs.utils import to_full_width as _to_full_width, is_existing as _is_existing
from libs.draw import draw_rating as _draw_rating, draw_name as _draw_name\
    ,draw_friend_code as _draw_friend_code, draw_aime as _draw_aime, draw_version as _draw_version\
    ,draw_qr_code as _draw_qr_code, draw_icon as _draw_icon, draw_basic as _draw_basic\
    ,draw_chara_name as _draw_chara_name, draw_date as _draw_date\
    ,draw_info_plate as _draw_info_plate

def _main(): # pylint: disable=too-many-branches
    start = _time()
    print("绘制开始！")
    args = _argparser()
    if args.no_override and _is_existing(args.output):
        print(f"[ERROR] 输出文件 '{args.output}' 已存在，如果你想覆盖它，请不要使用 --no-override 选项。")
        raise FileExistsError(f"Output file '{args.output}' already exists.")
    result = _draw_basic(args.background, args.chara, args.pass_type)
    if args.skip_rating:
        print("[2/10] 跳过 DX Rating 绘制。")
    else:
        result = _draw_rating(args.rating, result)
    if args.skip_player_name:
        print("[3/10] 跳过玩家名称绘制。")
    else:
        if args.full_width:
            result = _draw_name(_to_full_width(args.player_name), result)
        else:
            result = _draw_name(args.player_name, result)
    if args.skip_friend_code:
        print("[4/10] 跳过好友码绘制。")
    else:
        result = _draw_friend_code(args.friend_code, result)
    result = _draw_aime(args.aime, result, raw=args.raw_aime)
    result = _draw_version(args.version, result)
    if args.skip_qr_code:
        print("[7/10] 跳过 QR 码绘制。")
    else:
        result = _draw_qr_code(args.qr_code, result, empty=args.empty_qr_code)
    result = _draw_icon(args.icon, result, qr=not args.skip_qr_code)
    if not args.skip_info_plate:
        result = _draw_info_plate(result)
    if args.skip_name:
        print("[9/10] 跳过角色名称绘制。")
    else:
        if args.chara_name is not None:
            result = _draw_chara_name(args.chara_name, result)
        else:
            result = _draw_chara_name(args.chara, result)
    if args.skip_date:
        print("[10/10] 跳过日期绘制。")
    else:
        result = _draw_date(args.date, result)

    result.save(args.output)
    print(f"绘制结束，用时 {_time() - start:.2f} 秒。")

if __name__ == "__main__":
    _main()
