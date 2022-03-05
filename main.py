import time
import csv
import mouse
import keyboard
from typing import Union, Any
import json

import helpers
from helpers.Database import Database
import threading


def keyboard_callback(key: keyboard.KeyboardEvent) -> None:
    global db
    db.insert(table="keys", key=key.name.lower(), down=int(key.event_type == keyboard.KEY_DOWN),
                  time=str(key.time))


def mouse_callback(event: Union[mouse.ButtonEvent, mouse.MoveEvent, mouse.WheelEvent]) -> None:
    global db
    if isinstance(event, mouse.ButtonEvent):
        db.insert(table="mouse_buttons", button=event.button, event=event.event_type, time=event.time)
    # elif isinstance(event, mouse.MoveEvent):
    #     db.insert(table="mouse_move", x=event.x, y=event.y, time=event.time)
    # elif isinstance(event, mouse.WheelEvent):
    #     db.insert(table="mouse_wheel", delta=event.delta, time=event.time)


def key_parse() -> dict:
    global db

    # converts each row from database response to dictionary, only returning values within check_rate
    keys = [dict(i) for i in db.execute(f"SELECT * FROM keys WHERE {time.time()} - time <= {config['check_rate']}").fetchall()]

    # used for filtering rows by key
    uniq_keys = []

    # supposedly sorts by key
    keys = sorted(keys, key=lambda x: x["key"])

    # get all keys pressed
    for i in keys:
        if i == "command":
            uniq_keys.append("ctrl")
        else:
            uniq_keys.append(i["key"])

    # filter out duplicates
    uniq_keys = list(set(uniq_keys))

    # return value, key: amount
    frequency = {k: 0 for k in uniq_keys}

    for key in uniq_keys:
        for row in keys:
            # only downpress
            if row["key"] == "command":
                row["key"] = "ctrl"
            if row["key"] == key and row["down"] == 1:
                frequency[key] += 1

    # return json.dumps(frequency)
    return frequency


def mouse_button_parse() -> dict:
    global db
    # converts each row from database response to dictionary, only returning values within check_rate
    buttons = [dict(i) for i in db.execute(f"SELECT * FROM mouse_buttons WHERE {time.time()} - time <= {config['check_rate']}").fetchall()]

    # used for filtering row by button
    uniq_buttons = []

    # get all buttons pressed
    for i in buttons:
        uniq_buttons.append(i["button"])

    # remove duplicates
    uniq_buttons = list(set(uniq_buttons))

    # modified button names
    uniq_modified = []
    for i in uniq_buttons:
        uniq_modified.append(i + "_single")
        uniq_modified.append(i + "_double")

    # return value, button: amount
    # dict comprehension guarantees default value
    frequency = {k: 0 for k in uniq_modified}

    for button in uniq_buttons:
        for row in buttons:
            # single click handling
            if row["button"] == button and row["event"] == mouse.DOWN:
                frequency[button + "_single"] += 1
            # double click handling
            elif row["button"] == button and row["event"] == mouse.DOUBLE:
                frequency[button + "_double"] += 1

    # return json.dumps(frequency)
    return frequency


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


def add_rows_to_csv(filename: str, headers: list[str], rows: dict, state: str) -> None:
    rows["state"] = state
    try:
        with open(filename, "r") as file:
            write_header = len(file.readlines()) == 0
    except FileNotFoundError:
        write_header = True
    with open(filename, "a", newline="\n") as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        if write_header:
            writer.writeheader()
        print(rows)
        writer.writerow(rows)


def safe_call(func: callable) -> Any:
    """
    Assures thread-safe reads/writes to the database

    :param func: the unsafe function
    :return: Return value of func
    """
    ret = None
    try:
        lock.acquire(True)
        ret = func()
    finally:
        lock.release()
    return ret


lock = threading.Lock()
CONFIG_FILE = "config.json"

with open(CONFIG_FILE, 'r') as config:
    config = json.load(config)


DATABASE_FILE = config["database_file"]
db = Database(DATABASE_FILE)

#  lambda function allows for passing safe_call into the keyboard hook instead of the keyboard callback directly
keyboard.hook(lambda y: safe_call(lambda: keyboard_callback(y)))
mouse.hook(lambda y: safe_call(lambda: mouse_callback(y)))

print(safe_call(key_parse))
print(safe_call(mouse_button_parse))
state = "distracted"

while True:
    time.sleep(config["check_rate"])
    key_resp = safe_call(key_parse)
    mouse_resp = safe_call(mouse_button_parse)
    add_rows_to_csv(config["key_data_file"], helpers.KEY_HEADERS, key_resp, state)
    add_rows_to_csv(config["mouse_data_file"], helpers.MOUSE_HEADERS, mouse_resp, state)
