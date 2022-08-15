"""Helper function of battery"""

from ..constants import BATTERY_PATH2, BATTERY_PATH3, BATTERY_PROVIDER_PATH
from .battery_provider import Battery

try:
    from gi.repository import GObject
except ImportError:
    import gobject as GObject


def add_late_battery():
    global app
    global bus
    app.add_battery(Battery(bus, BATTERY_PATH3, 70, 'Protocol 2'))


def drain_battery(battery):
    new_percentage = 100
    if battery.percentage is not None:
        new_percentage = battery.percentage - 5
        if new_percentage < 0:
            new_percentage = 0

    battery.set_percentage(new_percentage)

    if new_percentage <= 0:
        return False

    return True


def register_provider_cb():
    print('Battery Provider registered')

    # Battery added early right after RegisterBatteryProvider succeeds
    app.add_battery(Battery(bus, BATTERY_PATH2, None))
    # Battery added later
    GObject.timeout_add(5000, add_late_battery)


def register_provider_error_cb(error):
    print('Failed to register Battery Provider: ' + str(error))
    mainloop.quit()


def unregister_provider_cb():
    print('Battery Provider unregistered')


def unregister_provider_error_cb(error):
    print('Failed to unregister Battery Provider: ' + str(error))


def unregister_battery_provider(battery_provider_manager):
    battery_provider_manager.UnregisterBatteryProvider(
        BATTERY_PROVIDER_PATH,
        reply_handler=unregister_provider_cb,
        error_handler=unregister_provider_error_cb)


def remove_battery(app, battery):
    app.remove_battery(battery)
