"""_summary_
"""

import dbus
import argparse
import threading
import dbus.mainloop.glib

from ble_server.utils import find_adapter,\
    register_ad_cb, register_ad_error_cb, shutdown,\
    register_app_cb, register_app_error_cb
from ble_server.constants import BLUEZ_SERVICE_NAME,\
    LE_ADVERTISING_MANAGER_IFACE, GATT_MANAGER_IFACE
from ble_server.advertisement.test_advertisement import TestAdvertisement
from ble_server.application.appication import Application
from ble_server.services.test_sevice import TestService
from ble_server import agent
from ble_server.characteristics.test_signal_characteristic import TestSendSignalCharacteristic
from ble_server.characteristics.test_characteristic import TestCharacteristic

try:
    from gi.repository import GObject  # python3
except ImportError:
    import gobject as GObject  # python2

mainloop = None


def main(timeout=0):
    global mainloop

    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

    bus = dbus.SystemBus()

    adapter = find_adapter(bus)
    if not adapter:
        print('LEAdvertisingManager1 interface not found')
        return

    adapter_props = dbus.Interface(bus.get_object(BLUEZ_SERVICE_NAME, adapter),
                                   "org.freedesktop.DBus.Properties")

    adapter_props.Set("org.bluez.Adapter1", "Powered", dbus.Boolean(1))

    ad_manager = dbus.Interface(bus.get_object(BLUEZ_SERVICE_NAME, adapter),
                                LE_ADVERTISING_MANAGER_IFACE)

    test_advertisement = TestAdvertisement(bus, 0)

    # agent
    agent_path = agent.constants.AGENT_PATH
    agent_obj = agent.agent.Agent(bus, agent_path)

    obj = bus.get_object(BLUEZ_SERVICE_NAME, "/org/bluez")
    manager = dbus.Interface(obj, "org.bluez.AgentManager1")
    manager.RegisterAgent(
        agent_path, agent.constants.AgentCapability.NO_INPUT_NO_OUTPUT.value)

    manager.RequestDefaultAgent(agent_path)
    print("Agent registered")

    mainloop = GObject.MainLoop()

    ad_manager.RegisterAdvertisement(test_advertisement.get_path(), {},
                                     reply_handler=register_ad_cb,
                                     error_handler=register_ad_error_cb)

    if timeout > 0:
        threading.Thread(target=shutdown, args=(timeout, mainloop)).start()
    else:
        print('Advertising forever...')

    # initilize app
    service_manager = dbus.Interface(
        bus.get_object(BLUEZ_SERVICE_NAME, adapter),
        GATT_MANAGER_IFACE)

    app = Application(bus)

    # create instance of service
    test_service = TestService(bus, 0)

    # create instances characteristics
    test_characteristic = TestCharacteristic(bus, 0, test_service)
    test_send_dignal_characteristic = TestSendSignalCharacteristic(
        bus, 1, test_service)

    # add test_send_dignal_characteristic to test_characteristic to test send
    # signal
    test_characteristic.add_characteristic(test_send_dignal_characteristic)

    # add characteristics to service
    test_service.add_characteristic(test_characteristic)
    test_service.add_characteristic(test_send_dignal_characteristic)

    # add services to app
    app.add_service(test_service)

    service_manager.RegisterApplication(app.get_path(), {},
                                        reply_handler=register_app_cb,
                                        error_handler=register_app_error_cb)

    mainloop.run()  # blocks until mainloop.quit() is called

    ad_manager.UnregisterAdvertisement(test_advertisement)
    print('Advertisement unregistered')
    dbus.service.Object.remove_from_connection(test_advertisement)


if __name__ == "__main__":
    # Create a parser.
    parser = argparse.ArgumentParser()
    parser.add_argument('--timeout', default=0, type=int, help="advertise " +
                        "for this many seconds then stop, 0=run forever " +
                        "(default: 0)")
    args = parser.parse_args()

    main(args.timeout)
