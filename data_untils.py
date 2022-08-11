"""Data type modules

Includes: DecimalJSONEncoder class, encode and decode string
        to bytes,json encode,json decode,dbus encode,deep update dict
"""

from collections import Mapping
from typing import Any, Union
import json
from decimal import Decimal

import dbus

DEFAULT_ENCODING = 'utf-8'


def pretty_float(o: Union[float, Decimal]) -> Union[float, Decimal]:
    """
    Pretty round float/Decimal object

    Args:
        o: Union[float, Decimal]

    Returns:
        o: Union[float, Decimal]
    """
    return round(o, 2)


class DecimalJSONEncoder(json.JSONEncoder):
    """
    Decimal JSON Encoder. Convert Decimal to float when json serialize.
    """

    def default(self, o: Any) -> Any:
        if isinstance(o, Decimal):
            return float(o)
        return super().default(o)


def encode(string: str, encoding=DEFAULT_ENCODING) -> bytes:
    """
    Encode string to bytes based on encoding.

    Args:
        string: str
        encoding: str

    Returns:
        result: bytes
    """
    return string.encode(encoding)


def decode(data: bytes, encoding=DEFAULT_ENCODING) -> str:
    """
    Decode bytes to string based on encoding.

    Args:
        data: bytes
        encoding: str

    Returns:
        result: str
    """
    return data.decode(encoding)


def json_encode(data: Any) -> str:
    """
    Encode python object to json string.

    Args:
        data: Any

    Returns:
        json_encoded: str
    """
    json_encoded = json.dumps(data, cls=DecimalJSONEncoder)
    return json_encoded


def json_decode(payload: str) -> Any:
    """
    Decode json payload to python object.

    Args:
        payload: str

    Returns:
        data: Any
    """
    data = json.loads(payload)
    return data


def dbus_encode(string: str) -> list[dbus.Byte]:
    """
    Encode string to dbus Bytes

    Args:
        string: str

    Returns:
        encoded: list[dbus.Byte]
    """
    encoded = [dbus.Byte(char) for char in encode(string)]
    return encoded


def deep_update_dict(data: dict, update: dict):
    """Deep update dictionary.

    Args:
        data: dict
        update: dict

    Returns:
        data: dict

    Example:
        data = {'a': 1, 'b': {'c': 2, 'd': 3}} and update = {'b': {'e': 4}}
        -> result = {'a': 1, 'b': {'c': 2, 'd': 3, 'e': 4}}
    """
    for key, val in update.items():
        if isinstance(val, Mapping):
            data[key] = deep_update_dict(data.get(key, {}), val)
        else:
            data[key] = val
    return data
