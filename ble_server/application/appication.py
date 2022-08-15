"""Application base module."""

import dbus
import dbus.service

from ..battery.battery_utils import drain_battery

from ..exceptions import *
from ..constants import *

try:
    from gi.repository import GObject
except ImportError:
    import gobject as GObject


class Application(dbus.service.Object):
    """
    org.bluez.GattApplication1 interface implementation
    """

    def __init__(self, bus):
        self.path = '/'
        self.services = []
        self.batteries = []
        dbus.service.Object.__init__(self, bus, self.path)
        # self.add_service(HeartRateService(bus, 0))
        # self.add_service(BatteryService(bus, 1))
        # self.add_service(TestService(bus, 2))

    def get_path(self):
        return dbus.ObjectPath(self.path)

    def add_service(self, service):
        self.services.append(service)

    def add_battery(self, battery):
        self.batteries.append(battery)
        self.InterfacesAdded(battery.get_path(), battery.get_properties())
        GObject.timeout_add(1000, drain_battery, battery)

    def remove_battery(self, battery):
        self.batteries.remove(battery)
        self.InterfacesRemoved(battery.get_path(), [BATTERY_PROVIDER_IFACE])

    @dbus.service.method(DBUS_OM_IFACE, out_signature='a{oa{sa{sv}}}')
    def GetManagedObjects(self):
        response = {}
        print('GetManagedObjects')

        for service in self.services:
            response[service.get_path()] = service.get_properties()
            chrcs = service.get_characteristics()
            for chrc in chrcs:
                response[chrc.get_path()] = chrc.get_properties()
                descs = chrc.get_descriptors()
                for desc in descs:
                    response[desc.get_path()] = desc.get_properties()

        for battery in self.batteries:
            response[battery.get_path()] = battery.get_properties()

        return response

    @dbus.service.signal(DBUS_OM_IFACE, signature='oa{sa{sv}}')
    def InterfacesAdded(self, object_path, interfaces_and_properties):
        return

    @dbus.service.signal(DBUS_OM_IFACE, signature='oas')
    def InterfacesRemoved(self, object_path, interfaces):
        return
