"""_summary_
"""

from .service import Service
from ..characteristics.test_characteristic import TestCharacteristic


class TestService(Service):
    """
    Dummy test service that provides characteristics and descriptors that
    exercise various API functionality.

    """
    TEST_SVC_UUID = '12345678-1234-5678-1234-56789abcdef0'

    def __init__(self, bus, index):
        Service.__init__(self, bus, index, self.TEST_SVC_UUID, True)
        # self.add_characteristic(TestEncryptCharacteristic(bus, 1, self))
        # self.add_characteristic(TestSecureCharacteristic(bus, 2, self))
