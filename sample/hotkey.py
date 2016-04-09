import sys

from PyQt5 import QtWidgets
from PyQt5.QtCore import QAbstractNativeEventFilter, QAbstractEventDispatcher

from pyqtkeybind import keybinder


class WinEventFilter(QAbstractNativeEventFilter):
    def __init__(self, keybinder):
        self.keybinder = keybinder
        super().__init__()

    def nativeEventFilter(self, eventType, message):
        self.keybinder.handler(message)
        return False, 0


def main():
    app = QtWidgets.QApplication(sys.argv)

    print("Press Shift+F3 any where. Ctrl+C exits the app.")

    # Setup a global keyboard shortcut to print "Hello World" on pressing
    # Shift-F3
    keybinder.init()
    callback = lambda: print("hello world")
    keybinder.register_hotkey(None, "Shift-F3", callback)

    # Install a native event filter to receive events from the OS
    win_event_filter = WinEventFilter(keybinder)
    event_dispatcher = QAbstractEventDispatcher.instance()
    event_dispatcher.installNativeEventFilter(win_event_filter)

    window = QtWidgets.QMainWindow()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()
