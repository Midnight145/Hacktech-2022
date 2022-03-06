import string
import sys

if sys.platform == 'darwin':
    PLATFORM = 'darwin'
else:
    PLATFORM = 'windows'

DISTRACTED = "distracted"
FOCUSED = "focused"
EMPTY = "unresponsive"
UNRESPONSIVE = EMPTY

SPECIAL_MAP = {'!': "excla", '"': 'dquote', '#': 'pound', '$': 'dollar', '%': 'percent', '&': 'ampersand',
               '\'': 'squote', '(': 'lparen', ')': 'rparen', '*': 'asterisk', '+': 'plus', ',': 'comma', '-': 'minus',
               '.': 'period', '/': 'fslash', ':': 'colon', ';': 'semicolon', '<': 'lthan','=': 'equals', '>': 'gthan',
               '?': 'question', '@': 'at', '[': 'lbracket', ']': 'rbracket','\\': 'backslash','^': 'caret',
               '_': 'uscore', '`': 'backtick', '{': 'lbrace', '|': 'pipe', '}': 'rbrace', '~': 'tilde'}

KEY_HEADERS = list(string.printable.replace(string.ascii_uppercase, '')[:-6])
KEY_HEADERS += ["esc", "enter", "delete", "ctrl", "left", "up", "right", "down", "backspace", "tab", "space", "windows",
                "alt", "shift", 'insert', 'menu', 'lock', 'screen', 'end', 'pause', 'home', "other"]
KEY_HEADERS.append('state')
KEY_HEADERS.append('platform')
for i in range(len(KEY_HEADERS)):
    if KEY_HEADERS[i] in SPECIAL_MAP.keys():
        KEY_HEADERS[i] = SPECIAL_MAP[KEY_HEADERS[i]]

MOUSE_HEADERS = ["left_single", "left_double", "right_single", "right_double", "middle_single", "middle_double",
                 "x_single", "x_double", "x2_single", "x2_double"]
MOUSE_HEADERS.append('state')
MOUSE_HEADERS.append('platform')
