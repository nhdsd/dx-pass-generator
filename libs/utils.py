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
from contextlib import redirect_stderr

import PIL.ImageFont as _ImageFont
from fontTools.ttLib import TTFont as _TTFont


with open("resources/font/SEGA_MARUGOTHICDB.ttf", "rb") as _ttf:
    _FONT_BINARY = _BIO(_ttf.read())

# Sega's font file is somehow broken, producing annoying warning message.
# This suppresses the warning.
with _SIO() as _stdout:
    with redirect_stderr(_stdout):
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
        raise ValueError(f"Rating must be non-negative, but got {rating}.")
    thresholds = (1000, 2000, 4000, 7000, 10000, 12000, 13000, 14000, 14500, 15000)
    return 1 + sum(int(rating >= threshold) for threshold in thresholds)

def text_validate(text: str) -> None:
    """Validate the input text.
    Params:
        text (str): The input text to validate.
    Raises:
        ValueError: If the text contains invalid characters.
    """
    for char in text:
        if ord(char) not in _FONT_CMAP:
            raise ValueError(f"Invalid character '{char}' (U+{ord(char):04X}) found in text.")

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
        raise ValueError(f"Invalid Aime ID '{aime}' found. Use string if it is not an Aime ID.")
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
        raise ValueError(f"Character ID '{chara_id}' not found.") from e

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
        raise ValueError(f"Invalid date: {date_str}.")

    return date.strftime("%Y/%m/%d")
