#!/usr/bin/env python3
"""
text_attr.py
-------------
Terminal text styling utility.

Usage as module:
    from text_attr import print
    print("Hello World", attr="bold+red")

Usage as CLI:
    python3 text_attr.py <text-to-print> [attr_string]
    Example: python3 text_attr.py 'Hello World' bold+red

Attributes:
    bold, italic, underline
    <color-name>, <r;g;b>, rand_color
    bg:<color-name>, bg:<r;g;b>, bg:rand_color

Environment variable:
    NO_COLOR=1 disables color output
"""

import json
import os
import random
import sys
import re

# GLOBAL CACHE
_COLORS = {
         'black': '0;0;0',           'white': '255;255;255',
         'red': '255;0;0',           'darkred': '139;0;0',
         'lightred': '255;102;102',  'green': '0;255;0',
         'darkgreen': '0;100;0',     'lightgreen': '144;238;144',
         'blue': '0;0;255',          'darkblue': '0;0;139',
         'lightblue': '173;216;230', 'skyblue': '135;206;235',
         'steelblue': '70;130;180',  'yellow': '255;255;0',
         'gold': '255;215;0',        'khaki': '240;230;140',
         'lemon': '255;250;205',     'cyan': '0;255;255',
         'aqua': '127;255;212',      'teal': '0;128;128',
         'magenta': '255;0;255',     'violet': '238;130;238',
         'orchid': '218;112;214',    'purple': '128;0;128',
         'indigo': '75;0;130',       'orange': '255;165;0',
         'darkorange': '255;140;0',  'coral': '255;127;80',
         'tomato': '255;99;71',      'salmon': '250;128;114',
         'brown': '165;42;42',       'chocolate': '210;105;30',
         'sienna': '160;82;45',      'tan': '210;180;140',
         'pink': '255;192;203',      'hotpink': '255;105;180',
         'olive': '128;128;0',       'lightpink': '255;182;193',
         'gray': '128;128;128',      'darkgray': '64;64;64',
         'lightgray': '211;211;211', 'silver': '192;192;192',
         'navy': '0;0;128',          'maroon': '128;0;0',
         }

_builtin_print = print  # Save reference of original built-in print function


def _get_color(string):
    """
    Return 255;255;255 like string from predefined dictionary or return
    the passed arg if in the form of 255;255;255 otherwise return false
    """
    if string in _COLORS: return _COLORS[string]
    pattern = r"^\s*(?:25[0-5]|2[0-4]\d|1?\d{1,2})\s*;\s*(?:25[0-5]|2[0-4]\d|1?\d{1,2})\s*;\s*(?:25[0-5]|2[0-4]\d|1?\d{1,2})\s*$"
    if re.match(pattern, string): return string
    return False

def print(*args, attr=None, sep=' ', end='\n', file=None, flush=False):
    """
    Custom print function with optional terminal styling.
    Works like built-in print but supports `attr`.
    """
    if file is None:
        file = sys.stdout   # default value of file arg

    text = sep.join(str(arg) for arg in args)

    # ---- NO_COLOR MODE ----
    if os.getenv("NO_COLOR") or not attr:
        _builtin_print(text, end=end, file=file, flush=flush)
        return

    esc = "\033["
    reset = f"{esc}0m"
    style_codes = []
    fg_code = ""
    bg_code = ""

    # Parse attributes
    attrs = [i.replace(" ", "").lower() for i in attr.split("+")]
    for attr in attrs:
        if attr == "bold":
            style_codes.append("1")
        elif attr == "italic":
            style_codes.append("3")
        elif attr == "underline":
            style_codes.append("4")
        elif attr == "rand_color":
            col = _COLORS[random.choice(list(_COLORS))]
            fg_code = f"38;2;{col}"
        elif attr == "bg:rand_color":
            col = _COLORS[random.choice(list(_COLORS))]
            bg_code = f"48;2;{col}"
        elif attr.startswith("bg:") and _get_color(attr[3:]):
            col = _get_color(attr[3:])
            bg_code = f"48;2;{col}"
        elif _get_color(attr):
            col = _get_color(attr)
            fg_code = f"38;2;{col}"

    # Combine escape codes
    final_code = ""
    if style_codes:
        final_code += f"{esc}{';'.join(style_codes)}m"
    if fg_code:
        final_code += f"{esc}{fg_code}m"
    if bg_code:
        final_code += f"{esc}{bg_code}m"

    # Print styled text
    _builtin_print(f"{final_code}{text}{reset}", end=end, file=file, flush=flush)


# ---------------------------
# Show help
# ---------------------------
def show_help():
    """
    Display verbose help for text_attr module and CLI usage.
    """
    _builtin_print("""
TEXT_ATTR MODULE / CLI - Terminal Text Styling Utility
=====================================================

1. MODULE USAGE
---------------
Import the module and use the `print` function with the optional `attr` argument:

    from text_attr import print

    print("Hello World", attr="bold+red")
    print("Warning!", attr="bg:200;200;55 + italic")
    print("Info with background", attr="blue+bg:yellow")

Parameters:
    attr (str): styling attributes, joined by '+'
    sep, end, file, flush: same as built-in print

2. CLI USAGE
------------
Run from terminal:

    python3 text_attr.py <text-to-print> [attr_string]
    Example: python3 text_attr.py 'Hello World' bold+red

3. SUPPORTED ATTRIBUTES
-----------------------
Text styles:
    bold       - Bold text
    italic     - Italic text
    underline  - Underlined text

Foreground colors:
    <color-name>   - Any color defined in your JSON database
    <r;g;b>        - RGB color code e.g. 255;0;200
    rand_color     - Pick a random color from the JSON database

Background colors:
    bg:<color-name>    - Background with a specific color
    bg:<r;g;b>         - RGB color code e.g. 255;0;200
    bg:rand_color      - Random background color


Examples:
    "bold + red"
    "200;200;55 + underline"
    "bg:200;200;55 + italic"
    "underline + blue + bg:yellow"
    "italic + rand_color"
    "bold + bg:rand_color"

4. ENVIRONMENT VARIABLES
------------------------
NO_COLOR=1      Disable all color output (useful for scripts or CI pipelines)

5. NOTES
---------
- Try 'python3 text_attr.py --color' to show all available color names.
- Original Python print can still be accessed via `_builtin_print(...)`.
- Works on Windows, macOS, Linux terminals that support ANSI escape codes.
""")

if __name__ == "__main__":
    if "--help" in sys.argv:
        show_help()
    elif "--color" in sys.argv:
        count=1
        for i in _COLORS:
            print(f" {count}. {i}")
            count+=1
    elif len(sys.argv) == 2:
        print(sys.argv[1])
    elif len(sys.argv) == 3:
        print(sys.argv[1], attr=sys.argv[2])
    else:
        _builtin_print("Usage: python3 text_attr.py <text-to-print> [attr_string]")
        _builtin_print("Example: python3 text_attr.py 'Hello World' bold+red")
        print("Try '", end="")
        print(f"python3 {sys.argv[0]} --help", attr="green", end="")
        print("' for more info.")
        sys.exit(1)