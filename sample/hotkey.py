#!/usr/bin/env python
"""Sample QtPy app to demonstrate keybinder capabilities."""

import sys
from typing import Callable, Optional

from qtpy import QtWidgets
from qtpy.QtCore import QAbstractNativeEventFilter, QAbstractEventDispatcher
import qtpy

from pyqtkeybind import keybinder


class WinEventFilter(QAbstractNativeEventFilter):
    def __init__(self, keybinder):
        self.keybinder = keybinder
        super().__init__()

    def nativeEventFilter(self, eventType, message):
        ret = self.keybinder.handler(eventType, message)
        return ret, 0


class EventDispatcher:
    """Install a native event filter to receive events from the OS"""

    def __init__(self, keybinder) -> None:
        self.win_event_filter = WinEventFilter(keybinder)
        self.event_dispatcher = QAbstractEventDispatcher.instance()
        self.event_dispatcher.installNativeEventFilter(self.win_event_filter)


class QtKeyBinder:
    def __init__(self, win_id: Optional[int]) -> None:
        keybinder.init()
        self.win_id = win_id

        self.event_dispatcher = EventDispatcher(keybinder=keybinder)

    def register_hotkey(self, hotkey: str, callback: Callable) -> None:
        keybinder.register_hotkey(self.win_id, hotkey, callback)

    def unregister_hotkey(self, hotkey: str) -> None:
        keybinder.unregister_hotkey(self.win_id, hotkey)


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()

    print("Using {} {}.\n".format(qtpy.API_NAME, qtpy.QT_VERSION))

    print("Sample app for pyqtkeybind:")
    print("\tPress Ctrl+Shift+A or Print Screen any where to trigger a callback.")
    print("\tCtrl+Shift+F unregisters and re-registers previous callback.")
    print("\tCtrl+Shift+E exits the app.")

    # Set up a global keyboard shortcut to print "Hello World" on pressing
    # the shortcut
    sample_key_binder = QtKeyBinder(win_id=None)

    def callback():
        print("hello world")

    def exit_app():
        window.close()

    def unregister():
        sample_key_binder.unregister_hotkey("Ctrl+Shift+A")
        print("unregister and register previous binding")
        sample_key_binder.register_hotkey("Ctrl+Shift+A", callback)

    sample_key_binder.register_hotkey("Ctrl+Shift+A", callback)
    sample_key_binder.register_hotkey("Print Screen", callback)
    sample_key_binder.register_hotkey("Ctrl+Shift+E", exit_app)
    sample_key_binder.register_hotkey("Ctrl+Shift+F", unregister)

    window.show()
    app.exec_()
    sample_key_binder.unregister_hotkey("Ctrl+Shift+A")
    sample_key_binder.unregister_hotkey("Ctrl+Shift+F")
    sample_key_binder.unregister_hotkey("Ctrl+Shift+E")
    sample_key_binder.unregister_hotkey("Print Screen")


if __name__ == "__main__":
    main()
