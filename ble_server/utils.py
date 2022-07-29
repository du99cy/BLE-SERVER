import dbus
import time

from .exceptions import *
from .constants import *

def register_ad_cb():
    print('Advertisement registered')


def register_ad_error_cb(error,mainloop):
    print('Failed to register advertisement: ' + str(error))
    mainloop.quit()


def find_adapter(bus):
    remote_om = dbus.Interface(bus.get_object(BLUEZ_SERVICE_NAME, '/'),
                               DBUS_OM_IFACE)
    objects = remote_om.GetManagedObjects()

    for o, props in objects.items():
        if LE_ADVERTISING_MANAGER_IFACE in props:
            return o

    return None


def shutdown(timeout,mainloop):
    print('Advertising for {} seconds...'.format(timeout))
    time.sleep(timeout)
    mainloop.quit()

def register_app_cb():
    print('GATT application registered')


def register_app_error_cb(error,mainloop):
    print('Failed to register application: ' + str(error))
    mainloop.quit()
