#!/usr/bin/env python3
# SPDX-License-Identifier: LGPL-2.1-or-later

import dbus
import dbus.exceptions
import dbus.mainloop.glib
import dbus.service

from ..constants import BATTERY_PROVIDER_IFACE, BATTERY_PROVIDER_PATH, DBUS_PROP_IFACE

try:
    from gi.repository import GObject
except ImportError:
    import gobject as GObject


class InvalidArgsException(dbus.exceptions.DBusException):
    _dbus_error_name = 'org.freedesktop.DBus.Error.InvalidArgs'


class Battery(dbus.service.Object):
    """
    org.bluez.BatteryProvider1 interface implementation
    """

    def __init__(self, bus, dev, percentage, source=None):
        self.path = BATTERY_PROVIDER_PATH + '/dev_' + dev
        self.dev_path = '/org/bluez/hci0/dev_' + dev
        self.bus = bus
        self.percentage = percentage
        self.source = source
        dbus.service.Object.__init__(self, bus, self.path)

    def get_battery_properties(self):
        properties = {}
        if self.percentage is not None:
            properties['Percentage'] = dbus.Byte(self.percentage)
        if self.source is not None:
            properties['Source'] = self.source
        properties['Device'] = dbus.ObjectPath(self.dev_path)
        return properties

    def get_properties(self):
        return {BATTERY_PROVIDER_IFACE: self.get_battery_properties()}

    def get_path(self):
        return dbus.ObjectPath(self.path)

    def set_percentage(self, percentage):
        if percentage < 0 or percentage > 100:
            print('percentage not valid')
            return

        self.percentage = percentage
        print('battery %s percentage %d' % (self.path, self.percentage))
        self.PropertiesChanged(
            BATTERY_PROVIDER_IFACE, self.get_battery_properties())

    @dbus.service.method(DBUS_PROP_IFACE,
                         in_signature='s',
                         out_signature='a{sv}')
    def GetAll(self, interface):
        if interface != BATTERY_PROVIDER_IFACE:
            raise InvalidArgsException()

        return self.get_properties()[BATTERY_PROVIDER_IFACE]

    @dbus.service.signal(DBUS_PROP_IFACE, signature='sa{sv}')
    def PropertiesChanged(self, interface, properties):
        return
