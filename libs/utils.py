# /libs/utils.py
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
Some utility functions for image processing.
"""
import datetime as _datetime
import json as _json
from io import BytesIO as _BIO, StringIO as _SIO
from contextlib import redirect_stderr as _redirect_stderr
from math import ceil
import os as _os
from random import choice as _choice

import PIL.Image as _Image
import PIL.ImageFont as _ImageFont
from fontTools.ttLib import TTFont as _TTFont

def not_found_err(file: str) -> None:
    """Create a FileNotFoundError with a custom message.
    Params:
        file (str): The file that was not found.
    """
    print(f"[ERROR] 找不到文件 '{file}'。请检查资源文件完整性。")

def open_image(image: str) -> _Image.Image:
    """Open an image file.
    Params:
        image (str): The image file name.
    Returns:
        PIL.Image.Image: The opened image.
    """
    try:
        return _Image.open(image)
    except FileNotFoundError:
        not_found_err(image)
        raise

try:
    with open("resources/font/SEGA_MARUGOTHICDB.ttf", "rb") as _ttf:
        _FONT_BINARY = _BIO(_ttf.read())
except FileNotFoundError as e:
    not_found_err(e.filename)
    raise

# Sega's font file is somehow broken, producing annoying warning message.
# This suppresses the warning.
with _SIO() as _stdout:
    with _redirect_stderr(_stdout):
        _FONT_CMAP = _TTFont(_FONT_BINARY).getBestCmap()

def to_full_width(text: str) -> str:
    """Convert half-width characters to full-width characters.
    Params:
        text (str): The input text to convert.
    Returns:
        str: The converted text with full-width characters.
    """
    # !: U+0021, ~: U+007E
    return ''.join(chr(ord(c) + 0xFEE0) if '!' <= c <= '~' else c for c in text)

def find_rating_background(rating: int) -> int:
    """Find the background image index for the given rating.
    Params:
        rating (int): The rating value.
    Returns:
        int: The background image index.
    Raises:
        ValueError: If the rating is negative.
    """
    if rating < 0:
        print("[ERROR] DX Rating 值不可以是负数。")
        raise ValueError(f"Rating must be non-negative, but got {rating}.")
    thresholds = (1000, 2000, 4000, 7000, 10000, 12000, 13000, 14000, 14500, 15000)
    return 1 + sum(int(rating >= threshold) for threshold in thresholds)

def text_validate(text: str) -> str:
    """Validate the input text.
    Params:
        text (str): The input text to validate.
    Raises:
        ValueError: If the text contains invalid characters.
    """
    for char in text:
        if ord(char) not in _FONT_CMAP:
            print(f"[ERROR] '{char}' (U+{ord(char):04X}) 无法被字体文件正常渲染。简体字的支持情况十分不乐观！")
            raise ValueError(f"Invalid character '{char}' (U+{ord(char):04X}) found in text.")
    return text

def aime_process(aime: int) -> str:
    """Process the Aime ID.
    Params:
        aime (int): The Aime ID to process.
    Returns:
        str: The processed Aime ID. zfill will be used if the ID is less than 20 digits.
    Raises:
        ValueError: If the Aime ID is too long (more than 20 digits).
    """
    if aime > 1e20 - 1:
        print("[ERROR] Aime ID 不可超过 20 位。如果你确实想输入这一文本，使用 --raw-aime。")
        raise ValueError(f"Invalid Aime ID '{aime}' found. Use --raw-aime to prevent processing.")
    s = str(aime)
    if len(s) < 20:
        s = s.zfill(20)
    return '  '.join(s[i:i + 4] for i in range(0, 20, 4))

def get_font(size: int) -> _ImageFont.FreeTypeFont:
    """Get the PIL font with given size.
    Params:
        size (int): The font size.
    Returns:
        PIL.ImageFont.FreeTypeFont: The PIL font with the given size.
    """
    _FONT_BINARY.seek(0)
    return _ImageFont.truetype(_FONT_BINARY, size)

def find_chara_name(chara_id: str | int) -> str:
    """Find the character name from the character ID.
    Params:
        chara_id (str): The character ID to find.
    Returns:
        str: The character name. If not found, returns the original ID.
    """
    try:
        with open("resources/index/chara.json", "r", encoding="utf-8") as f:
            data = _json.load(f)
            return data[str(chara_id).zfill(7)]
    except KeyError as e:
        print("[ERROR] 无法从角色名索引中找到给定的角色名。自定义的角色请使用 -n/--name 指定名称。")
        raise ValueError(f"Character ID '{chara_id}' not found.") from e
    except FileNotFoundError as e:
        not_found_err(e.filename)
        raise

def date_process(date_str: str | None) -> str:
    """Process the input date.
    Params:
        date (str | None): The input date to process.
    Returns:
        str: The validated date in the format YYYY/MM/DD.
        If the input is None, returns the date 14 days ahead in the format YYYY/MM/DD.
    Raises:
        ValueError: If the date is not in the correct format.
    """
    if date_str is None:
        print("[10/10] 将使用默认到期日期。")
        return (_datetime.datetime.now().date() + _datetime.timedelta(days=14)).strftime("%Y/%m/%d")
    valid = False
    try:
        date = _datetime.datetime.strptime(date_str, "%Y%m%d")
        valid = True
    except ValueError:
        pass
    try:
        date = _datetime.datetime.strptime(date_str, "%Y-%m-%d")
        valid = True
    except ValueError:
        pass
    try:
        date = _datetime.datetime.strptime(date_str, "%Y-%m-%d")
        valid = True
    except ValueError:
        pass
    try:
        date = _datetime.datetime.strptime(date_str, "%Y/%m/%d")
        valid = True
    except ValueError:
        pass

    if not valid:
        print("[ERROR] 无法解析日期，请使用 YYYYMMDD、YYYY-MM-DD 或 YYYY/MM/DD 格式，并检查这一天是否真的存在。")
        raise ValueError(f"Invalid date: {date_str}.")

    return date.strftime("%Y/%m/%d")

def text_width_validate(text: str, font: _ImageFont.FreeTypeFont, max_width: int) -> str:
    """Validate the width of the text.
    Params:
        text (str): The input text to validate.
        font (PIL.ImageFont.FreeTypeFont): The font to use for measuring text width.
        max_width (int): The maximum allowed width.
    Returns:
        str: The validated text.
    Raises:
        ValueError: If the text is too wide.
    """

    text_width = font.getbbox(text, anchor="lt")[2]
    if text_width > max_width:
        print(f"[ERROR] 文本过宽，超出限制值 {ceil(text_width) - max_width} 像素。")
        raise ValueError(f"Text '{text}' is too wide (width: {ceil(text_width)}, max: {max_width})")
    return text

def random_chara() -> int:
    """Randomly choose a character image.
    Returns:
        int: The ID of the randomly chosen character image.
    """
    print("[1/10] 随机选取角色...")
    files = [f[10:-4] for f in _os.listdir("resources/character/") if f.endswith((".png"))]
    if not files:
        print("[ERROR] 随机选取角色失败。请检查资源文件完整性。")
        raise ValueError("No valid image files found in directory: resources/character/")
    chosen_file = _choice(files)
    return int(chosen_file)

def random_background() -> int:
    """Randomly choose a background image.
    Returns:
        int: The ID of the randomly chosen background image.
    """
    print("[1/10] 随机选取背景...")
    files = [f[10:-4] for f in _os.listdir("resources/background/") if f.endswith((".png"))]
    if not files:
        print("[ERROR] 随机选取背景失败。请检查资源文件完整性。")
        raise ValueError("No valid image files found in directory: resources/background/")
    chosen_file = _choice(files)
    return int(chosen_file)
