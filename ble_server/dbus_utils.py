""" Encode and decode dbus data.
"""

from typing import Any


# convert from json to dbus data
# for ReadValue
def parse_json_to_dbus(data: str | Any) -> bytearray:
    dbus_data = bytearray(data, encoding="utf8")
    return dbus_data

# convert from dbus to json data
# for WriteValue function


def parse_dbus_to_json(data: bytearray) -> str:
    data_convert = bytes(data).decode("utf-8")
    return data_convert
