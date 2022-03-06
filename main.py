import sys
import time
import csv
import mouse
import keyboard
from typing import Union, Any, List
import json

import helpers
from helpers.Database import Database
import threading


class Handler:
    def __init__(self):
        self.running = True
        hook = keyboard.hook(lambda y: self.safe_call(lambda: self.keyboard_callback(y)))
        if not sys.platform == 'darwin':
            mouse.hook(lambda y: self.safe_call(lambda: self.mouse_callback(y)))

        self.lock = threading.Lock()

    def keyboard_callback(self, key: keyboard.KeyboardEvent) -> None:
        if not self.running: return
        global db
        if key.name is None:
            return

        insertion_key = key.name.lower().split()[-1]
        if "option" in insertion_key:
            insertion_key = "alt"

        if insertion_key in helpers.SPECIAL_MAP.keys():
            insertion_key = helpers.SPECIAL_MAP[insertion_key]

        db.insert(table="keys", key=insertion_key, down=int(key.event_type == keyboard.KEY_DOWN), time=str(key.time))

    def mouse_callback(self, event: Union[mouse.ButtonEvent, mouse.MoveEvent, mouse.WheelEvent]) -> None:
        if not self.running: return

        global db
        if isinstance(event, mouse.ButtonEvent):
            db.insert(table="mouse_buttons", button=event.button, event=event.event_type, time=event.time)
        # elif isinstance(event, mouse.MoveEvent):
        #     db.insert(table="mouse_move", x=event.x, y=event.y, time=event.time)
        # elif isinstance(event, mouse.WheelEvent):
        #     db.insert(table="mouse_wheel", delta=event.delta, time=event.time)

    def key_parse(self) -> dict:
        global db

        # converts each row from database response to dictionary, only returning values within check_rate
        keys = [dict(i) for i in
                db.execute(f"SELECT * FROM keys WHERE {time.time()} - time <= {config['check_rate']}").fetchall()]

        # used for filtering rows by key
        uniq_keys = []

        # supposedly sorts by key
        keys = sorted(keys, key=lambda x: x["key"])
        # get all keys pressed
        for i in keys:
            if i["key"] == "command":
                uniq_keys.append("ctrl")
            else:
                uniq_keys.append(i["key"])

        # filter out duplicates
        uniq_keys = list(set(uniq_keys))

        # return value, key: amount
        frequency = {k: 0 for k in uniq_keys}

        for key in uniq_keys:
            for row in keys:
                if row["key"] == "command":
                    row["key"] = "ctrl"
                if row["key"] not in helpers.KEY_HEADERS:
                    row["key"] = "other"
                # only downpress
                if row["key"] == key and row["down"] == 1:
                    frequency[key] += 1

        # return json.dumps(frequency)
        return frequency


    def mouse_button_parse(self) -> dict:
        global db
        # converts each row from database response to dictionary, only returning values within check_rate
        buttons = [dict(i) for i in db.execute(
            f"SELECT * FROM mouse_buttons WHERE {time.time()} - time <= {config['check_rate']}").fetchall()]

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

        return frequency

    def add_rows_to_csv(self, filename: str, headers: List[str], rows: dict, state: str) -> bool:
        if len(rows) == 0:
            rows["state"] = helpers.EMPTY
        else:
            rows["state"] = state

        rows["platform"] = helpers.PLATFORM
        try:
            with open(filename, "r") as file:
                write_header = len(file.readlines()) == 0
        except FileNotFoundError:
            write_header = True
        with open(filename, "a", newline="\n") as file:
            writer = csv.DictWriter(file, fieldnames=headers)
            if write_header:
                writer.writeheader()
            try:
                writer.writerow(rows)
                return True
            except:
                return False


    def safe_call(self, func: callable) -> Any:
        """
        Assures thread-safe reads/writes to the database

        :param func: the unsafe function
        :return: Return value of func
        """
        ret = None
        try:
            self.lock.acquire(True)
            ret = func()
        finally:
            self.lock.release()
        return ret



CONFIG_FILE = "config.json"

with open(CONFIG_FILE, 'r') as config:
    config = json.load(config)

DATABASE_FILE = config["database_file"]
db = Database(DATABASE_FILE)

handler = Handler()

#  lambda function allows for passing safe_call into the keyboard hook instead of the keyboard callback directly
keyboard.hook(lambda y: handler.safe_call(lambda: handler.keyboard_callback(y)))
if not sys.platform == 'darwin':
    mouse.hook(lambda y: handler.safe_call(lambda: handler.mouse_callback(y)))

state = helpers.DISTRACTED

while True:
    time.sleep(config["check_rate"])
    key_resp = handler.safe_call(handler.key_parse)
    if not helpers.PLATFORM == 'darwin':
        mouse_resp = handler.safe_call(handler.mouse_button_parse)
    else:
        mouse_resp = {}
    handler.add_rows_to_csv(config["key_data_file"], helpers.KEY_HEADERS, key_resp, state)
    handler.add_rows_to_csv(config["mouse_data_file"], helpers.MOUSE_HEADERS, mouse_resp, state)
