import string

KEY_HEADERS = list(string.printable[:-6])
KEY_HEADERS += ["esc", "enter", "delete", "ctrl", "left", "up", "right", "down", "backspace", "tab", "space", "windows", "alt", "shift"]
KEY_HEADERS.append('state')

MOUSE_HEADERS = ["left", "right", "middle", "x1", "x2"]