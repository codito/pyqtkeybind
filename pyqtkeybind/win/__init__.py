# -*- coding: utf-8 -*-
import ctypes
from ctypes import c_bool, c_int, WINFUNCTYPE, windll
from ctypes.wintypes import UINT

class WinKeyBinder(KeyBinder):
    __keybinds = defaultdict(list)
    __keygrabs = defaultdict(int) # Key grab key -> number of grabs

    def init(self):
        # Register os dependent hooks
        if sys.platform.startswith("win"):
            # http://msdn.microsoft.com/en-us/library/windows/desktop/ms646309%28v=vs.85%29.aspx
            prototype = WINFUNCTYPE(c_bool, c_int, c_int, UINT, UINT)
            paramflags = (1, 'hWnd', 0), (1, 'id', 0),
            (1, 'fsModifiers', 0), (1, 'vk', 0)
            self.RegisterHotKey = prototype(('RegisterHotKey', windll.user32),
                                            paramflags)

            # http://msdn.microsoft.com/en-us/library/windows/desktop/ms646327%28v=vs.85%29.aspx
            prototype = WINFUNCTYPE(c_bool, c_int, c_int)
            paramflags = (1, 'hWnd', 0), (1, 'id', 0)
            self.UnregisterHotKey = prototype(('UnregisterHotKey',
                                               windll.user32), paramflags)

    def register_hotkey(self, wid, keys, callback):
        if not self.__keygrabs[keys] and\
                not self.RegisterHotKey(wid, 0x0, mods, kc):
            return False

        self.__keybinds[keys].append(callback)
        self.__keygrabs[keys] += 1

    def unregister_hotkey(self, wid, modifiers, key):
        pass

    def handler(self, message):
        WM_HOTKEY_MSG = 0x0312
        msg = ctypes.wintypes.MSG.from_address(message.__int__())
        if eventType == "windows_generic_MSG":
            if msg.message == WM_HOTKEY_MSG:
                key = msg.lParam
                for cb in self.__keybinds.get(key, []):
                    try:
                        cb(e)
                    except TypeError:
                        cb()
        return
