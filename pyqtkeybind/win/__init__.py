# -*- coding: utf-8 -*-
import sys
from collections import defaultdict

import ctypes
from ctypes import c_bool, c_int, WINFUNCTYPE, GetLastError
from ctypes.wintypes import UINT

from .keybindutil import keys_from_string


class WinKeyBinder(object):
    __keybinds = defaultdict(list)
    __keygrabs = defaultdict(int)   # Key grab key -> number of grabs

    def init(self):
        # Register os dependent hooks
        if sys.platform.startswith("win"):
            self.user32 = ctypes.WinDLL('user32', use_errno=True, use_last_error=True)
            # http://msdn.microsoft.com/en-us/library/windows/desktop/ms646309%28v=vs.85%29.aspx
            prototype = WINFUNCTYPE(c_bool, c_int, c_int, UINT, UINT)
            paramflags = (1, 'hWnd', 0), (1, 'id', 0), (1, 'fsModifiers', 0), (1, 'vk', 0)
            self.RegisterHotKey = prototype(('RegisterHotKey', self.user32), paramflags)

            # http://msdn.microsoft.com/en-us/library/windows/desktop/ms646327%28v=vs.85%29.aspx
            prototype = WINFUNCTYPE(c_bool, c_int, c_int)
            paramflags = (1, 'hWnd', 0), (1, 'id', 0)
            self.UnregisterHotKey = prototype(('UnregisterHotKey', self.user32), paramflags)

    def register_hotkey(self, wid, keys, callback):
        mods, kc = keys_from_string(keys)
        if wid is None:
            wid = 0x0

        # High word = Key code, Low word = Modifiers
        # https://msdn.microsoft.com/en-us/library/windows/desktop/ms646279%28v=vs.85%29.aspx
        # Add MOD_NOREPEAT = 0x4000 to mods, so that keys don't get notified twice
        # This requires VISTA+ operating system
        key_index = kc << 16 | mods
        if not self.__keygrabs[key_index] and\
                not self.RegisterHotKey(c_int(wid), key_index, UINT(mods | 0x4000), UINT(kc)):
            print("Couldn't register hot key!")
            return False

        self.__keybinds[key_index].append(callback)
        self.__keygrabs[key_index] += 1
        return True

    def unregister_hotkey(self, wid, keys):
        mods, kc = keys_from_string(keys)
        key_index = kc << 16 | mods

        self.__keybinds.pop(key_index)
        self.__keygrabs.pop(key_index)

        if not self.UnregisterHotKey(c_int(wid), key_index):
            err = "Couldn't unregister hot key '{0}'. Error code = {1}."\
                .format(keys, GetLastError())
            print(err)
            return False
        return True

    def handler(self, eventType, message):
        WM_HOTKEY_MSG = 0x0312
        msg = ctypes.wintypes.MSG.from_address(message.__int__())
        if eventType == "windows_generic_MSG":
            if msg.message == WM_HOTKEY_MSG:
                key = msg.lParam
                for cb in self.__keybinds.get(key, []):
                    try:
                        cb()
                    finally:
                        return True
        return False
