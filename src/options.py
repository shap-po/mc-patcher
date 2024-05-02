from typing import TextIO

# source: https://minecraft.wiki/w/Key_codes
KEY_CODES = {
    'key.keyboard.unknown': 0,
    'key.keyboard.escape': 1,
    'key.keyboard.keypad.1': 2,
    'key.keyboard.keypad.2': 3,
    'key.keyboard.keypad.3': 4,
    'key.keyboard.keypad.4': 5,
    'key.keyboard.keypad.5': 6,
    'key.keyboard.keypad.6': 7,
    'key.keyboard.keypad.7': 8,
    'key.keyboard.keypad.8': 9,
    'key.keyboard.keypad.9': 10,
    'key.keyboard.keypad.0': 11,
    'key.keyboard.keypad.subtract': 12,
    'key.keyboard.keypad.equal': 13,
    'key.keyboard.backspace': 14,
    'key.keyboard.tab': 15,
    'key.keyboard.q': 16,
    'key.keyboard.w': 17,
    'key.keyboard.e': 18,
    'key.keyboard.r': 19,
    'key.keyboard.t': 20,
    'key.keyboard.y': 21,
    'key.keyboard.u': 22,
    'key.keyboard.i': 23,
    'key.keyboard.o': 24,
    'key.keyboard.p': 25,
    'key.keyboard.left.bracket': 26,
    'key.keyboard.right.bracket': 27,
    'key.keyboard.enter': 28,
    'key.keyboard.left.control': 29,
    'key.keyboard.a': 30,
    'key.keyboard.s': 31,
    'key.keyboard.d': 32,
    'key.keyboard.f': 33,
    'key.keyboard.g': 34,
    'key.keyboard.h': 35,
    'key.keyboard.j': 36,
    'key.keyboard.k': 37,
    'key.keyboard.l': 38,
    'key.keyboard.semicolon': 39,
    'key.keyboard.apostrophe': 40,
    'key.keyboard.grave.accent': 41,
    'key.keyboard.left.shift': 42,
    'key.keyboard.backslash': 43,
    'key.keyboard.z': 44,
    'key.keyboard.x': 45,
    'key.keyboard.c': 46,
    'key.keyboard.v': 47,
    'key.keyboard.b': 48,
    'key.keyboard.n': 49,
    'key.keyboard.m': 50,
    'key.keyboard.comma': 51,
    'key.keyboard.period': 52,
    'key.keyboard.slash': 53,
    'key.keyboard.right.shift': 54,
    'key.keyboard.keypad.multiply': 55,
    'key.keyboard.left.alt': 56,
    'key.keyboard.space': 57,
    'key.keyboard.caps.lock': 58,
    'key.keyboard.f1': 59,
    'key.keyboard.f2': 60,
    'key.keyboard.f3': 61,
    'key.keyboard.f4': 62,
    'key.keyboard.f5': 63,
    'key.keyboard.f6': 64,
    'key.keyboard.f7': 65,
    'key.keyboard.f8': 66,
    'key.keyboard.f9': 67,
    'key.keyboard.f10': 68,
    'key.keyboard.num.lock': 69,
    'key.keyboard.scroll.lock': 70,
    'key.keypad.7': 71,
    'key.keypad.8': 72,
    'key.keypad.9': 73,
    'key.keypad.subtract': 74,
    'key.keypad.4': 75,
    'key.keypad.5': 76,
    'key.keypad.6': 77,
    'key.keypad.add': 78,
    'key.keypad.1': 79,
    'key.keypad.2': 80,
    'key.keypad.3': 81,
    'key.keypad.0': 82,
    'key.keypad.decimal': 83,
    'key.keyboard.f11': 87,
    'key.keyboard.f12': 88,
    'key.keyboard.f13': 100,
    'key.keyboard.f14': 101,
    'key.keyboard.f15': 102,
    # 'kana': 112,
    # 'convert': 121,
    # 'noconvert': 123,
    # 'yen': 125,
    # 'numpadequals': 141,
    # 'circumflex': 144,
    # 'at': 145,
    # 'colon': 146,
    # 'underline': 147,
    # 'kanji': 148,
    # 'stop': 149,
    # 'ax': 150,
    # 'unlabled': 151,
    'key.keypad.enter': 156,
    'key.keyboard.right.control': 157,
    # 'numpadcomma': 179,
    'key.keypad.divide': 181,
    # 'sysrq': 183,
    'key.keyboard.right.alt': 184,
    'key.keyboard.pause': 197,
    'key.keyboard.home': 199,
    'key.keyboard.up': 200,
    'key.keyboard.page.up': 201,
    'key.keyboard.left': 203,
    'key.keyboard.right': 205,
    'key.keyboard.end': 207,
    'key.keyboard.down': 208,
    'key.keyboard.page.down': 209,
    'key.keyboard.insert': 210,
    'key.keyboard.delete': 211,
    'key.keyboard.left.win': 219,
    'key.keyboard.right.win': 220,
    # 'apps': 221,
    # 'power': 222,
    # 'sleep': 223,


    'key.mouse.left': -100,
    'key.mouse.right': -99,
    'key.mouse.middle': -98,
    'key.mouse.4': -97,
    'key.mouse.5': -96,
    'key.mouse.6': -95,
    'key.mouse.7': -94,
    'key.mouse.8': -93,
    'key.mouse.9': -92,
    'key.mouse.10': -91,
    'key.mouse.11': -90,
    'key.mouse.12': -89,
    'key.mouse.13': -88,
    'key.mouse.14': -87,
    'key.mouse.15': -86,
    'key.mouse.16': -85,
}
KEY_CODES_INV = {v: k for k, v in KEY_CODES.items()}

# first version that introduced new key codes
NEW_KEY_CODES_VERSION = 1444


def load(fp: TextIO, remove_version: bool = False) -> dict:
    """
    Load options from a Minecraft options.txt file.

    :param fp: A TextIO object representing the options.txt file.
    :return: A dictionary containing the options.
    """
    options = {}

    for line in fp:
        line = line.strip()
        if not line:
            continue

        key, value = line.split(':', 1)
        key = key.strip()
        value = value.strip()

        if value == 'true':
            value = True
        elif value == 'false':
            value = False
        else:
            try:
                value = int(value)
            except ValueError:
                pass

        if key.startswith('key_'):
            value = KEY_CODES_INV.get(value, value)

        options[key] = value

    if remove_version:
        options.pop('version', None)

    return options


def dump(obj: dict, fp: TextIO = None) -> str:
    """
    Dump options to a Minecraft options.txt file format.

    :param obj: A dictionary containing the options.
    :param fp: (Optional) A TextIO object to write the options to. If not provided, the function returns the options as a string.
    :return: Returns the options as a string.
    """
    lines = []

    version = obj.get('version')
    is_old_version = (not version or version < NEW_KEY_CODES_VERSION)

    for key, value in obj.items():
        if is_old_version and key.startswith('key_'):
            value = KEY_CODES.get(value, value)
        if isinstance(value, bool):
            value = str(value).lower()

        lines.append(f'{key}:{value}')

    options_str = '\n'.join(lines)

    if fp:
        fp.write(options_str)
    return options_str
