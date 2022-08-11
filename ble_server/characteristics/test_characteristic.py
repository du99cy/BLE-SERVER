"""_summary_
"""

from optparse import Option
from .characteristic import Characteristic
from typing import Optional


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
        self.characteristic.NotifyValue(
            "hello drake nguyen " + str(self.value))
        return self.value

    def WriteValue(self, value, options):
        print('TestCharacteristic Write: ' + repr(value))
        self.value = value

    def add_characteristic(self, characteristic: Characteristic):
        self.characteristic = characteristic
