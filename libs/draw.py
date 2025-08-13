# /libs/draw.py
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
Drawing functions for image processing.
"""
import PIL.Image as _Image
import PIL.ImageDraw as _Draw
import qrcode as _qrcode
import qrcode.constants as _qrcode_constants
import qrcode.exceptions as _qrcode_exceptions

from .utils import get_font as _get_font, aime_process as _aime_process,\
    find_chara_name as _find_chara_name, date_process as _date_process,\
    find_rating_background as _find_ra_bg
from .consts import DXPass as _Pass, Icon as _Icon


def draw_basic(base: str | int, chara: str | int, pass_type: _Pass, /) -> _Image.Image:
    """Draw basic character image.
    Params:
        base (str): The base image file name.
        chara (str): The character image file name.
    Returns:
        PIL.Image.Image: The generated image.
    """
    base_image = _Image.open(f"resources/background/CardBase{str(base).zfill(6)}.png")
    chara_image = _Image.open(f"resources/character/CardChara{str(chara).zfill(6)}.png")
    pass_image = _Image.open(pass_type.value)
    base_image.alpha_composite(chara_image, (0, 0))
    base_image.alpha_composite(pass_image, (0, 0))
    return base_image

def draw_rating(rating: int | None, base: _Image.Image, /) -> _Image.Image:
    """Draw DX Rating.
    Params:
        rating (int | None): The rating value. `None` means no rating.
        base (PIL.Image.Image): The input image to draw on.
    Returns:
        PIL.Image.Image: The generated image.
    """
    x = 690

    # Get the background
    if rating is not None:
        rating_background = _Image.open(f"resources/general/Ra{_find_ra_bg(rating)}.png")
        base.alpha_composite(rating_background, (461, 32))
        # Draw the rating digit by digit, starting from the right
        while rating:
            digit = rating % 10
            rating //= 10
            digit_img = _Image.open(f"resources/general/Num{digit}.png")
            base.alpha_composite(digit_img, (x, 52))
            x -= 29
    else:
        base.alpha_composite(_Image.open("resources/general/Ra1.png"), (461, 32))
        for _ in range(5):
            digit_img = _Image.open("resources/general/Num-.png")
            base.alpha_composite(digit_img, (x, 52))
            x -= 29

    return base

def draw_name(name: str, base: _Image.Image, /) -> _Image.Image:
    """Draw Player Name.
    Params:
        name (str): The player name to draw.
        base (PIL.Image.Image): The input image to draw on.
    Returns:
        PIL.Image.Image: The generated image.
    Raises:
        ValueError: If the name is too long (longer than 273 pixels a.k.a. 9.75 `Ａ`s).
    """
    # Prepare for the drawing
    font = _get_font(28)
    space_width = 182 # Length of 6.5 'Ａ's, also the length of available space
    max_width = 273 # 1.5 * SPACE_WIDTH, longer than this will cause an exception
    draw = _Draw.Draw(base)

    # Measure width of name
    name_bbox = draw.textbbox((0, 0), name, font=font, anchor="lt") # (0, 0, width, height)

    # Do not need the rescaling - directly draw
    if name_bbox[2] <= space_width:
        draw.text((470, 118), name, font=font, fill=(0, 0, 0), anchor="lt")
        return base
    # Too long - raise an exception
    if name_bbox[2] > max_width:
        raise ValueError(f"'{name}' is too wide (width: {name_bbox[2]}, max: {max_width})")

    # Draw the name on a temporary image
    pad = 4 # Compensate for the difference caused by different text rendering method
    tmp_w = int(name_bbox[2]) + pad * 2
    tmp_h = int(name_bbox[3]) + pad * 2
    tmp = _Image.new("RGBA", (max(1, tmp_w), max(1, tmp_h)), (0, 0, 0, 0))
    tmp_draw = _Draw.Draw(tmp)
    tmp_draw.text((pad, pad), name, font=font, fill=(0, 0, 0, 255), anchor="lt")

    # Scale the name
    new_w = max(1, space_width + pad * 2)
    new_h = tmp_h
    scaled = tmp.resize((new_w, new_h), _Image.Resampling.LANCZOS)

    # Draw the scaled name
    base.alpha_composite(scaled, (470 - pad, 118 - pad))
    return base

def draw_friend_code(code: int | str | None, base: _Image.Image, /) -> _Image.Image:
    """Draw Friend Code.
    Params:
        code (int | str | None): The friend code to draw. `None` means no code.
        base (PIL.Image.Image): The input image to draw on.
    Returns:
        PIL.Image.Image: The generated image.
    """
    font = _get_font(20)
    draw = _Draw.Draw(base)

    if code is not None:
        # Draw the friend code
        draw.text((628, 156), f"{code}", font=font, fill=(0, 0, 0), anchor="mt")
    else:
        base.alpha_composite(_Image.open("resources/general/NoFriendCode.png"), (533, 160))

    return base


def draw_aime(aime: int | str, base: _Image.Image, /, *, raw: bool = False) -> _Image.Image:
    """Draw Aime ID.
    Params:
        aime (int | str): The Aime ID to draw. `None` means no Aime ID.
        base (PIL.Image.Image): The input image to draw on.
        raw (bool): If True, the Aime ID will be drawn without any processing.
    Returns:
        PIL.Image.Image: The generated image.
    Raises:
        ValueError: If the Aime ID is invalid.
    """
    if isinstance(aime, int) and not raw:
        aime = _aime_process(aime)
    else:
        aime = str(aime)

    font = _get_font(16)
    draw = _Draw.Draw(base)
    if aime is not None:
        draw.text((156, 1006), aime, font=font, fill=(255, 255, 255), anchor="lt")


    return base

def draw_version(version: str, base: _Image.Image, /) -> _Image.Image:
    """Draw Version.
    Params:
        version (str): The version to draw.
        base (PIL.Image.Image): The input image to draw on.
    Returns:
        PIL.Image.Image: The generated image.
    """
    font = _get_font(16)
    draw = _Draw.Draw(base)
    draw.text((425, 1006), version, font=font, fill=(255, 255, 255), anchor="lt")
    return base

def draw_qr_code(data: str | None, base: _Image.Image, /) -> _Image.Image:
    """Draw QR Code. Error correction level: Medium.
    Params:
        data (str | None): The data to encode in the QR code. Dummy QR code will be used if None.
        base (PIL.Image.Image): The input image to draw on.
    Returns:
        PIL.Image.Image: The generated image with the QR code.
    Raises:
        ValueError: If the data overflows. The maximum version is QR Code 6.
    """
    if data is None:
        dummy_qr_code = _Image.open("resources/general/DummyQRCode.png")
        base.alpha_composite(dummy_qr_code, (581, 866))
        return base

    for version in range(1, 7):
        qr = _qrcode.QRCode(
            version=version,
            error_correction=_qrcode_constants.ERROR_CORRECT_M,
            box_size=3,
            border=4,
        )
        try:
            qr.add_data(data)
            qr.make(fit=False)
        except _qrcode_exceptions.DataOverflowError:
            continue
        box_count = len(qr.get_matrix())
        break
    else:
        raise ValueError(f"Data overflow. {len(data.encode('utf-8'))} bytes received.")
    box_size = 5 if version == 1 else 4 if version <= 3 else 3
    offset = (158 - box_count * box_size) // 2

    qr = _qrcode.QRCode(
        version=version,
        error_correction=_qrcode_constants.ERROR_CORRECT_M,
        box_size=box_size,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=False)

    img = qr.make_image(fill_color="black", back_color="white").get_image().convert("RGBA")
    qr_data = img.getdata()
    temp = []
    for pixel in qr_data:
        if pixel >= (255, 255, 255):
            temp.append((255, 255, 255, 0))
        else:
            temp.append(pixel)
    img.putdata(temp)
    base.alpha_composite(img, (556 + offset, 841 + offset))

    return base

def draw_icon(icons: list[_Icon] | None, base: _Image.Image, /) -> _Image.Image:
    """Draw icons.
    Params:
        icons (list[Icon] | None): The list of icons. `None` means no icons.
        base (PIL.Image.Image): The input image to draw on.
    Returns:
        PIL.Image.Image: The generated image.
    Raises:
        ValueError: If too many icons are provided. At most 4 icons are allowed.
    """
    if icons is None:
        return base

    if (count := len(icons)) > 4:
        raise ValueError(f"Icons exceed the limit (4 icons). {count} icons provided.")
    for i, icon in enumerate(icons):
        icon_image = _Image.open(icon.value).convert("RGBA")
        base.alpha_composite(icon_image, (28 + i * 107, 870))
    return base

def draw_chara_name(name: str | int, base: _Image.Image, /, *, search: bool = True) -> _Image.Image:
    """Draw Character Name.
    Params:
        name (str | int): The character ID or name to draw.
        base (PIL.Image.Image): The input image to draw on.
        search (bool): Whether to search for the character name. `True` by default.
    Returns:
        PIL.Image.Image: The generated image.
    Raises:
        ValueError: If the character ID is not found.
    """
    if search:
        chara_name = _find_chara_name(name)
    else:
        chara_name = str(name)
    font = _get_font(15)
    draw = _Draw.Draw(base)

    draw.text((145, 802), chara_name, font=font, fill=(0, 0, 0), anchor="mt")
    return base

def draw_date(date: str | None, base: _Image.Image, /) -> _Image.Image:
    """Draw Date.
    Params:
        date (str): The date to draw.
        base (PIL.Image.Image): The input image to draw on.
    Returns:
        PIL.Image.Image: The generated image.
    """
    date = _date_process(date)

    font = _get_font(15)
    font_date = _get_font(20)
    draw = _Draw.Draw(base)

    draw.text((42, 832), "ブースト期限", font=font, fill=(0, 0, 0), anchor="lt")
    draw.text((156, 831), date, font=font_date, fill=(0, 0, 0), anchor="lt")

    return base
