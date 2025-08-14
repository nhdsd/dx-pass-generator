# /libs/parse.py
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
Parser of the command line input.
"""
import argparse as _argparse

from .utils import text_validate as _text_validate, random_background as _rand_background,\
    random_chara as _random_chara
from .consts import DXPass as _Pass, Icon as _Icon

def argparser() -> _argparse.Namespace:
    """
    Parse the command line input.
    Returns:
        argparse.Namespace: The parsed arguments.
    """
    def _parse_int_or_str(value: str) -> int | str:
        try:
            return int(value)
        except ValueError:
            return value

    def _parse_pass_type(value: str) -> _Pass:
        try:
            return _Pass[value.upper()]
        except KeyError as e:
            raise ValueError(f"Invalid pass type: {value}") from e

    def _parse_icon_type(value: str) -> _Icon:
        try:
            return _Icon[value.upper()]
        except KeyError as e:
            raise ValueError(f"Invalid icon type: {value}") from e

    class _SkipNameDate(_argparse.Action):
        def __call__(self, parser, namespace, values, option_string=None):
            setattr(namespace, "skip_info_plate", True)
            setattr(namespace, "skip_name", True)
            setattr(namespace, "skip_date", True)

    class _SkipAll(_argparse.Action):
        def __call__(self, parser, namespace, values, option_string=None):
            setattr(namespace, "skip_info_plate", True)
            setattr(namespace, "skip_name", True)
            setattr(namespace, "skip_date", True)
            setattr(namespace, "skip_player_name", True)
            setattr(namespace, "skip_rating", True)
            setattr(namespace, "skip_friend_code", True)
            setattr(namespace, "skip_qr_code", True)

    parser = _argparse.ArgumentParser(description="Generate a maimai DX pass image.")

    parser.add_argument(
        "-l", "--pass-level",
        dest="pass_type",
        type=_parse_pass_type,
        help="The pass type. Accepts: 'Bronze', 'Silver', 'Gold'(Default), 'Freedom'",
        default=_Pass.GOLD
    )

    parser.add_argument(
        "-c", "--chara",
        dest="chara",
        type=int,
        help="The character ID. Random by default.",
        default=_random_chara()
    )

    parser.add_argument(
        "-b", "--background",
        dest="background",
        type=int,
        help="The background ID. Random by default.",
        default=_rand_background()
    )

    parser.add_argument(
        "-H", "--holographic",
        dest="holographic",
        action="store_true",
        help="Enable holographic display.",
        default=False
    )
    parser.add_argument(
        "--holo-from",
        dest="holo_from",
        type=str,
        help="Holographic frame source.",
        default="resources/general/Laser.png"
    )


    parser.add_argument(
        "-n", "--name",
        dest="chara_name",
        type=_text_validate,
        help="Override the character name displayed.",
        default=None
    )
    parser.add_argument(
        "--skip-name",
        dest="skip_name",
        action="store_true",
        help="Skip the character name display.",
        default=False
    )

    parser.add_argument(
        "-p", "--player-name",
        dest="player_name",
        type=_text_validate,
        help=("The player name. 'maimai' by default. Half-width characters will be converted "
              "to full-width characters. --half-width and --full-width control this."),
        default="maimai"
    )
    parser.add_argument(
        "--skip-player-name",
        dest="skip_player_name",
        action="store_true",
        help="Skip the player name display.",
        default=False
    )

    full_width = parser.add_mutually_exclusive_group()
    full_width.add_argument(
        "--full-width",
        dest="full_width",
        action="store_true",
        help="Use full-width characters in the name. This is the default."
    )
    full_width.add_argument(
        "--half-width",
        dest="full_width",
        action="store_false",
        help="Use half-width characters in the name. This reserves existing full-width characters."
    )
    parser.set_defaults(full_width=True)

    parser.add_argument(
        "-r", "--rating",
        dest="rating",
        type=int,
        help="The rating. If not specified, the friend code will be displayed as '-----'",
        default=None
    )
    parser.add_argument(
        "--override-rating",
        dest="override_rating",
        type=int,
        help="Override the rating display with the value here.",
        default=None
    )
    parser.add_argument(
        "--skip-rating",
        dest="skip_rating",
        action="store_true",
        help="Skip the rating display.",
        default=False
    )

    parser.add_argument(
        "-f", "--friend-code",
        dest="friend_code",
        type=_text_validate,
        help="The friend code. If not specified, the friend code will be displayed as '-----'.",
        default=None
    )
    parser.add_argument(
        "--skip-friend-code",
        dest="skip_friend_code",
        action="store_true",
        help="Skip the friend code display.",
        default=False
    )

    parser.add_argument(
        "-a", "--aime",
        dest="aime",
        type=_parse_int_or_str,
        help=("The Aime ID. Empty by default. If the input is integer, the program would "
              "validate it and add the spacing every 4 digits. To prevent this, use --raw-aime."),
        default=""
    )
    parser.add_argument(
        "--raw-aime",
        dest="raw_aime",
        action="store_true",
        help="Prevent the processing of the Aime ID.",
        default=False
    )

    parser.add_argument(
        "-v", "--version",
        dest="version",
        type=_text_validate,
        help="The version text. Empty by default.",
        default=""
    )

    parser.add_argument(
        "-q", "--qr-code",
        dest="qr_code",
        type=str,
        help="The QR code text. If not specified, the dummy QR code will be used.",
        default=None
    )
    parser.add_argument(
        "--empty-qr-code",
        dest="empty_qr_code",
        action="store_true",
        help="Use an empty QR code.",
        default=False
    )
    parser.add_argument(
        "--skip-qr-code",
        dest="skip_qr_code",
        action="store_true",
        help="Skip the QR code display.",
        default=False
    )

    parser.add_argument(
        "-i", "--icon",
        dest="icon",
        type=_parse_icon_type,
        help="The icons. Empty by default. Use multiple this option to specify more than one icon.",
        default=None,
        nargs="*"
    )

    parser.add_argument(
        "-d", "--date",
        dest="date",
        type=str,
        help="The date text. If not specified, we will use the date 14 days later.",
        default=None
    )
    parser.add_argument(
        "--skip-date",
        dest="skip_date",
        action="store_true",
        help="Skip the date display.",
        default=False
    )

    parser.add_argument(
        "--skip-name-date",
        action=_SkipNameDate,
        help="Skip the name and date display, as well as the background of the area.",
        default=False,
        nargs=0
    )
    parser.set_defaults(skip_info_plate=False)
    parser.add_argument(
        "--skip-all",
        action=_SkipAll,
        help="Skip all displays.",
        default=False,
        nargs=0
    )

    parser.add_argument(
        "-o", "--output",
        dest="output",
        type=str,
        help="The output file path. If not specified, the output will be saved to 'output.png'.",
        default="output.png"
    )
    parser.add_argument(
        "--no-override",
        action="store_true",
        help="Do not override existing files.",
        default=False
    )

    return parser.parse_args()
