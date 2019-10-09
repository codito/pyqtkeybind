#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Sample PyQt5 app to demonstrate keybinder capabilities."""

import sys

from PyQt5 import QtWidgets
from PyQt5.QtCore import QAbstractNativeEventFilter, QAbstractEventDispatcher

from pyqtkeybind import keybinder


class WinEventFilter(QAbstractNativeEventFilter):
    def __init__(self, keybinder):
        self.keybinder = keybinder
        super().__init__()

    def nativeEventFilter(self, eventType, message):
        ret = self.keybinder.handler(eventType, message)
        return ret, 0


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()

    print("Press Ctrl+Shift+A any where. Ctrl+Shift+E exits the app.")

    # Setup a global keyboard shortcut to print "Hello World" on pressing
    # the shortcut
    keybinder.init()

    def callback():
        print("hello world")
    def exit_app():
        window.close()
    def unregister():
        keybinder.unregister_hotkey(window.winId(), "Shift+Ctrl+A")
        keybinder.register_hotkey(window.winId(), "Shift+Ctrl+A", callback)

    keybinder.register_hotkey(window.winId(), "Shift+Ctrl+A", callback)
    keybinder.register_hotkey(window.winId(), "Shift+Ctrl+E", exit_app)
    keybinder.register_hotkey(window.winId(), "Shift+Ctrl+F", unregister)

    # Install a native event filter to receive events from the OS
    win_event_filter = WinEventFilter(keybinder)
    event_dispatcher = QAbstractEventDispatcher.instance()
    event_dispatcher.installNativeEventFilter(win_event_filter)

    window.show()
    app.exec_()
    keybinder.unregister_hotkey(window.winId(), "Shift+Ctrl+A")
    keybinder.unregister_hotkey(window.winId(), "Shift+Ctrl+E")


if __name__ == '__main__':
    main()
