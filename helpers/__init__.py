import string

KEY_HEADERS = list(string.printable[:-6])
KEY_HEADERS += ["esc", "enter", "delete", "ctrl", "left", "up", "right", "down", "backspace", "tab", "space", "windows", "alt"]
KEY_HEADERS.append('state')

MOUSE_HEADERS = ["left_single", "left_double", "right_single", "right_double", "middle_single", "middle_double",
                 "x_single", "x_double", "x2_single", "x2_double", "state"]