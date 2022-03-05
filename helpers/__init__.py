import string
import sys

if sys.platform == 'darwin':
    PLATFORM = 'darwin'
else:
    PLATFORM = 'windows'


KEY_HEADERS = list(string.printable[:-6])
KEY_HEADERS += ["esc", "enter", "delete", "ctrl", "left", "up", "right", "down", "backspace", "tab", "space", "windows", "alt", "shift", 'insert', 'menu', 'lock', 'screen', 'end', 'pause', 'home']
KEY_HEADERS.append('state')
KEY_HEADERS.append('platform')

MOUSE_HEADERS = ["left_single", "left_double", "right_single", "right_double", "middle_single", "middle_double",
                 "x_single", "x_double", "x2_single", "x2_double"]
MOUSE_HEADERS.append('state')
MOUSE_HEADERS.append('platform')
