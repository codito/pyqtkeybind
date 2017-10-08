import sys

from PyQt5 import QtWidgets
from PyQt5.QtCore import QAbstractNativeEventFilter, QAbstractEventDispatcher

from pyqtkeybind import keybinder


class WinEventFilter(QAbstractNativeEventFilter):
    def __init__(self, keybinder):
        self.keybinder = keybinder
        super().__init__()

    def nativeEventFilter(self, eventType, message):
        self.keybinder.handler(eventType, message)
        return False, 0


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()

    print("Press Shift+F3 any where. Ctrl+C exits the app.")

    # Setup a global keyboard shortcut to print "Hello World" on pressing
    # Shift-F3
    keybinder.init()
    callback = lambda: print("hello world")
    keybinder.register_hotkey(window.winId(), "Shift-F3", callback)

    # Install a native event filter to receive events from the OS
    win_event_filter = WinEventFilter(keybinder)
    event_dispatcher = QAbstractEventDispatcher.instance()
    event_dispatcher.installNativeEventFilter(win_event_filter)

    window.show()
    app.exec_()
    keybinder.unregister_hotkey(window.winId(), 0x0, 0x0)


if __name__ == '__main__':
    main()
