# -*- coding: utf-8 -*-
import sys
from collections import defaultdict

import ctypes
from ctypes import c_bool, c_int, WINFUNCTYPE, windll
from ctypes.wintypes import UINT

from .keybindutil import keys_from_string


class WinKeyBinder(object):
    __keybinds = defaultdict(list)
    __keygrabs = defaultdict(int)   # Key grab key -> number of grabs

    def init(self):
        # Register os dependent hooks
        if sys.platform.startswith("win"):
            # http://msdn.microsoft.com/en-us/library/windows/desktop/ms646309%28v=vs.85%29.aspx
            prototype = WINFUNCTYPE(c_bool, c_int, c_int, UINT, UINT)
            paramflags = (1, 'hWnd', 0), (1, 'id', 0), (1, 'fsModifiers', 0), (1, 'vk', 0)
            self.RegisterHotKey = prototype(('RegisterHotKey', windll.user32), paramflags)

            # http://msdn.microsoft.com/en-us/library/windows/desktop/ms646327%28v=vs.85%29.aspx
            prototype = WINFUNCTYPE(c_bool, c_int, c_int)
            paramflags = (1, 'hWnd', 0), (1, 'id', 0)
            self.UnregisterHotKey = prototype(('UnregisterHotKey', windll.user32), paramflags)

    def register_hotkey(self, wid, keys, callback):
        mods, kc = keys_from_string(keys)
        if wid == None:
            wid = 0x0
        # print(wid)
        # print(mods)
        # print(kc)
        
        # Add MOD_NOREPEAT
        # mods = mods | 0x4000
        # TODO keys get notified twice, fix it

        # High word = Key code, Low word = Modifiers
        # https://msdn.microsoft.com/en-us/library/windows/desktop/ms646279%28v=vs.85%29.aspx
        key_index = kc << 16 | mods
        if not self.__keygrabs[key_index] and\
                not self.RegisterHotKey(c_int(wid), 0x1, UINT(mods | 0x4000), UINT(kc)):
            print("Couldn't register hot key!")
            return False

        self.__keybinds[key_index].append(callback)
        self.__keygrabs[key_index] += 1

    def unregister_hotkey(self, wid, modifiers, key):
        if not self.UnregisterHotKey(c_int(wid), 0x1):
            print("Couldn't unregister hot key!")
            return False
        return True

    def handler(self, eventType, message):
        WM_HOTKEY_MSG = 0x0312
        msg = ctypes.wintypes.MSG.from_address(message.__int__())
        if eventType == "windows_generic_MSG":
            if msg.message == WM_HOTKEY_MSG:
                key = msg.lParam
                print(key & 0xffff)
                print(key >> 16)
                if (0x1000 & (key & 0xffff) != 0):
                    return
                for cb in self.__keybinds.get(key, []):
                    cb()
        return
