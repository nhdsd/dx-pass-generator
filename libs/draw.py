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
from math import ceil
import PIL.Image as _Image
import PIL.ImageDraw as _Draw
import qrcode as _qrcode
import qrcode.constants as _qrcode_constants
import qrcode.exceptions as _qrcode_exceptions

from .utils import get_font as _get_font, aime_process as _aime_process,\
    find_chara_name as _find_chara_name, date_process as _date_process,\
    find_rating_background as _find_ra_bg, open_image as _open_image,\
    text_width_validate as _text_width_validate
from .consts import DXPass as _Pass, Icon as _Icon


def draw_basic(base: int, chara: int, pass_type: _Pass, /) -> _Image.Image:
    """Draw basic character image.
    Params:
        base (str): The base image file name.
        chara (str): The character image file name.
    Returns:
        PIL.Image.Image: The generated image.
    """
    base_image = _open_image(f"resources/background/CardBase{str(base).zfill(6)}.png")
    chara_image = _open_image(f"resources/character/CardChara{str(chara).zfill(6)}.png")

    pass_image = _open_image(pass_type.value[0])
    icon_image = _open_image(pass_type.value[0][:-4] + "Icon.png")
    serial_image = _open_image("resources/general/SerialCode.png")
    print("[1/10] 绘制背景、角色和 DX Pass 基底...")
    base_image.alpha_composite(chara_image, (0, 0))
    base_image.alpha_composite(pass_image, (0, 0))
    base_image.alpha_composite(icon_image, pass_type.value[1])
    base_image.alpha_composite(serial_image, (141, 1000))
    return base_image

# pylint: disable=line-too-long, too-many-locals
def draw_basic_holographic(base: int, chara: int, pass_type: _Pass, /, *, holo: str) -> _Image.Image:
    """Draw basic character image.
    Params:
        base (str): The base image file name.
        chara (str): The character image file name.
    Returns:
        PIL.Image.Image: The generated image.
    """
    print("[WARN] 镭射效果是实验性功能。")
    base_image = _open_image(f"resources/background/CardBase{str(base).zfill(6)}.png")
    chara_image = _open_image(f"resources/character/CardChara{str(chara).zfill(6)}.png")

    black_image = _Image.new("RGBA", (768, 1052), (255, 255, 255, 255))
    chara_mask = _Image.eval(_Image.alpha_composite(
        black_image,
        _open_image(f"resources/holograph/CardCharaMask{str(chara).zfill(6)}.png")
    ).convert("L"), lambda px: 255 - px)
    frame_mask = _Image.eval(_Image.alpha_composite(
        black_image,
        _open_image("resources/general/HoloFrame.png")
    ).convert("L"), lambda px: 255 - px)
    base_mask = _Image.eval(
        _Image.open("resources/general/HoloBase.png").convert("L"),
        lambda px: 255 - px
    )

    holo_img = _open_image(holo)
    chara_holo = holo_img.copy()
    chara_holo.putalpha(chara_mask)

    frame_holo = holo_img.copy()
    frame_holo.putalpha(frame_mask)

    base_holo = holo_img.copy()
    base_holo.putalpha(base_mask)

    base_image.alpha_composite(base_holo, (0, 0))
    pass_image = _open_image(pass_type.value[0])
    icon_image = _open_image(pass_type.value[0][:-4] + "Icon.png")
    serial_image = _open_image("resources/general/SerialCode.png")
    print("[1/10] 绘制背景、角色和 DX Pass 基底...")
    base_image.alpha_composite(chara_image, (0, 0))
    base_image.alpha_composite(chara_holo, (0, 0))
    base_image.alpha_composite(pass_image, (0, 0))
    base_image.alpha_composite(frame_holo, (0, 0))
    base_image.alpha_composite(icon_image, pass_type.value[1])
    base_image.alpha_composite(serial_image, (141, 1000))
    return base_image


def draw_rating(rating: int | None, base: _Image.Image, /, *, override: int | None) -> _Image.Image:
    """Draw DX Rating.
    Params:
        rating (int | None): The rating value. `None` means no rating.
        base (PIL.Image.Image): The input image to draw on.
        override (int | None): The override rating value. `None` means no override.
    Returns:
        PIL.Image.Image: The generated image.
    """
    print("[2/10] 绘制 DX Rating...")
    x = 690

    # Get the background
    if rating is not None:

        rating_bg = _open_image(f"resources/general/Ra{_find_ra_bg(override or rating)}.png")
        base.alpha_composite(rating_bg, (461, 32))
        # Draw the rating digit by digit, starting from the right
        if rating < 0:
            print("[ERROR] DX Rating 值不可以是负数。")
            raise ValueError(f"Rating must be non-negative, but got {rating}.")
        while rating:
            digit = rating % 10
            rating //= 10
            digit_img = _open_image(f"resources/general/Num{digit}.png")
            base.alpha_composite(digit_img, (x, 52))
            x -= 29
    else:
        print("[2/10] DX rating 将被隐藏。")
        rating_bg = _open_image(f"resources/general/Ra{_find_ra_bg(override or 0)}.png")
        base.alpha_composite(rating_bg, (461, 32))
        for _ in range(5):
            digit_img = _open_image("resources/general/Num-.png")
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
    print("[3/10] 绘制玩家名...")
    base.alpha_composite(_open_image("resources/general/Player.png"), (457, 107))
    font = _get_font(28)
    space_width = 182 # Length of 6.5 'Ａ's, also the length of available space
    max_width = 273 # 1.5 * SPACE_WIDTH, longer than this will cause an exception
    draw = _Draw.Draw(base)

    # Measure width of name
    # We are not using utils.text_width_validate because player name is scalable
    name_bbox = draw.textbbox((0, 0), name, font=font, anchor="lt") # (0, 0, width, height)

    # Do not need the rescaling - directly draw
    if name_bbox[2] <= space_width:
        draw.text((470, 118), name, font=font, fill=(0, 0, 0), anchor="lt")
        return base
    # Too long - raise an exception
    if name_bbox[2] > max_width:
        print(f"[ERROR] 文本过宽，超出限制值 {name_bbox[2] - max_width} 像素。")
        raise ValueError(f"Text '{name}' is too wide (width: {name_bbox[2]}, max: {max_width})")

    print("[3/10] 文本较长，需要横向压缩...")
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
    print("[4/10] 绘制好友码...")
    base.alpha_composite(_open_image("resources/general/Friend.png"), (457, 148))
    max_width = 195
    font = _get_font(20)
    _text_width_validate(f"{code}", font, max_width)
    draw = _Draw.Draw(base)

    if code is not None:
        # Draw the friend code
        draw.text((628, 156), f"{code}", font=font, fill=(0, 0, 0), anchor="mt")
    else:
        print("[4/10] 好友码将被隐藏。")
        base.alpha_composite(_open_image("resources/general/NoFriendCode.png"), (533, 160))

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

    print("[5/10] 绘制 Aime ID...")
    max_width = 270
    font = _get_font(16)
    _text_width_validate(aime, font, max_width)
    draw = _Draw.Draw(base)
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
    print("[6/10] 绘制版本...")
    max_width = 190
    font = _get_font(16)
    _text_width_validate(version, font, max_width)
    draw = _Draw.Draw(base)
    draw.text((425, 1006), version, font=font, fill=(255, 255, 255), anchor="lt")
    return base

def draw_qr_code(data: str | None, base: _Image.Image, /, *, empty: bool = False) -> _Image.Image:
    """Draw QR Code. Error correction level: Medium.
    Params:
        data (str | None): The data to encode in the QR code. Dummy QR code will be used if None.
        base (PIL.Image.Image): The input image to draw on.
    Returns:
        PIL.Image.Image: The generated image with the QR code.
    Raises:
        ValueError: If the data overflows. The maximum version is QR Code 6.
    """
    print("[7/10] 绘制二维码...")
    base.alpha_composite(_open_image("resources/general/QRCodeBase.png"), (556, 841))
    if empty:
        print("[7/10] 二维码绘制将只保留空白背景。")
        return base

    if data is None:
        print("[7/10] 二维码将使用占位符绘制。")
        dummy_qr_code = _open_image("resources/general/DummyQRCode.png")
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
        print("[ERROR] 尝试让二维码编码的内容过多。")
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

def draw_icon(icons: list[_Icon] | None, base: _Image.Image, /, *, qr: bool = True) -> _Image.Image:
    """Draw icons.
    Params:
        icons (list[Icon] | None): The list of icons. `None` means no icons.
        base (PIL.Image.Image): The input image to draw on.
    Returns:
        PIL.Image.Image: The generated image.
    Raises:
        ValueError: If too many icons are provided. At most 4 icons are allowed.
    """
    print("[8/10] 绘制增益图标...")
    if icons is None:
        print("[8/10] 无增益图标。")
        return base

    if (count := len(icons)) > 4 + 0 if qr else 2:
        print("[ERROR] 图标数量超出限制。过多图标会向右溢出。")
        raise ValueError(f"Icons exceed the limit. {count} icons provided.")
    for i, icon in enumerate(icons):
        icon_image = _open_image(icon.value).convert("RGBA")
        base.alpha_composite(icon_image, (28 + i * 107, 870))
    return base

def draw_info_plate(base: _Image.Image, /) -> _Image.Image:
    """Draw Info Plate.
    Params:
        base (PIL.Image.Image): The input image to draw on.
    Returns:
        PIL.Image.Image: The generated image.
    """
    base.alpha_composite(_open_image("resources/general/Name.png"), (0, 790))
    return base

def draw_chara_name(name_or_id: str | int, base: _Image.Image, /) -> _Image.Image:
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
    print("[9/10] 绘制角色名...")
    if isinstance(name_or_id, int):
        name = _find_chara_name(name_or_id)
    else:
        print("[9/10] 使用自定义角色名...")
        name = name_or_id

    max_width = 220
    for size in (15, 14, 13, 12):
        font = _get_font(size)
        text_width = font.getbbox(name, anchor="lt")[2]
        if text_width > max_width:
            continue
        break
    else:
        print(f"[ERROR] 文本过宽，超出限制值 {ceil(text_width) - max_width} 像素。")
        raise ValueError(f"Text '{name}' is too wide (width: {ceil(text_width)}, max: {max_width})")
    draw = _Draw.Draw(base)

    draw.text((145, 802 + int(size==12)), name, font=font, fill=(0, 0, 0), anchor="mt")
    return base

def draw_date(date: str, base: _Image.Image, /) -> _Image.Image:
    """Draw Date.
    Params:
        date (str): The date to draw.
        base (PIL.Image.Image): The input image to draw on.
    Returns:
        PIL.Image.Image: The generated image.
    """
    print("[10/10] 绘制到期日期...")
    date = _date_process(date)

    font = _get_font(15)
    font_date = _get_font(20)
    draw = _Draw.Draw(base)

    draw.text((42, 832), "ブースト期限", font=font, fill=(0, 0, 0), anchor="lt")
    draw.text((156, 831), date, font=font_date, fill=(0, 0, 0), anchor="lt")

    return base
