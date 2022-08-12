"""_summary_
"""
import logging

from optparse import Option
from .characteristic import Characteristic
from typing import Optional
from ble_server.dbus_utils import parse_dbus_to_json, parse_json_to_dbus

logger = logging.getLogger(__name__)


class TestCharacteristic(Characteristic):
    """
    Dummy test characteristic. Allows writing arbitrary bytes to its value, and
    contains "extended properties", as well as a test descriptor.

    """
    TEST_CHRC_UUID = '12345678-1234-5678-1234-56789abcdef1'
    # create a characteristic object to send a signal
    characteristic: Optional[Characteristic] = None

    def __init__(self, bus, index, service):
        Characteristic.__init__(
            self, bus, index,
            self.TEST_CHRC_UUID,
            ['read', 'write', 'writable-auxiliaries'],
            service)
        self.value = 0
        # self.add_descriptor(TestDescriptor(bus, 0, self))
        # self.add_descriptor(
        #         CharacteristicUserDescriptionDescriptor(bus, 1, self))

    def ReadValue(self, options):
        self.value += 1
        value_to_read = "hello drake nguyen " + str(self.value)
        self.characteristic.NotifyValue(value_to_read)
        dbus_value = parse_json_to_dbus(value_to_read)
        return dbus_value

    def WriteValue(self, value, options):
        value_json = parse_dbus_to_json(value)
        logger.debug(value_json)

    def add_characteristic(self, characteristic: Characteristic):
        self.characteristic = characteristic
