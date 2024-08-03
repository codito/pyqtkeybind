import os
import sys
from collections import defaultdict
from struct import unpack

import qtpy
import xcffib
import xcffib.xproto
from xcffib import ffi

from .keybindutil import *


# class X11KeyBinder(KeyBinder):
class X11KeyBinder(object):
    conn = None
    wid = None

    def _get_conn_root_window(self):
        # Get the X11 connection and update keyboard mappings
        if qtpy.API == "pyqt5":
            import sip
            from PyQt5.QtX11Extras import QX11Info

            qt_conn = QX11Info.connection()
            ptr = sip.unwrapinstance(qt_conn)
            self.conn = xcffib.wrap(ptr)
            self.wid = QX11Info.appRootWindow()
            print("qx11 wid: ", self.wid)

            display = os.environ["DISPLAY"]
            conn = xcffib.connect(display=display)

            # Get the root window
            setup = conn.get_setup()
            self.wid = setup.roots[0].root
            print("wid: ", self.wid)

            # print("pref_screen: ", self.conn.pref_screen, conn.pref_screen)
            print("fd: ", self.conn.get_file_descriptor(), conn.get_file_descriptor())
            print(
                "screenptr: ",
                self.conn.get_screen_pointers(),
                conn.get_screen_pointers(),
            )
        else:
            display = os.environ["DISPLAY"]
            self.conn = xcffib.connect(display=display)

            # Get the root window
            setup = self.conn.get_setup()
            self.wid = setup.roots[0].root

    def init(self):
        self._get_conn_root_window()
        update_keyboard_mapping(self.conn, None)

    def register_hotkey(self, wid, key_string, callback):
        # return bind_global_key(self.conn, "KeyPress", key_string, callback)
        # if wid and not qtpy.API == "pyqt5":
        #     self.wid = wid
        print("wid: ", self.wid)
        return bind_key(self.conn, "KeyPress", self.wid, key_string, callback)

    def unregister_hotkey(self, wid, key_string):
        return unbind_global_key(self.conn, self.wid, key_string)

    def handler(self, eventType, message):
        e = self._parse_keypress_event(message)

        if e.is_valid():
            return run_keybind_callbacks(e)
        return False

    def _parse_keypress_event(self, message):
        # Try unpack the message as a xcb_key_press_event.
        # Each xcb event is 36 bytes, last 4 bytes are padding for keypress,
        # hence set the size to be unpacked as 32.
        message.setsize(32)
        return X11KeyPressEvent(message.asstring())


class X11KeyPressEvent(object):
    def __init__(self, data):
        (
            self.response_type,
            self.detail,
            self.sequence,
            self.time,
            self.root,
            self.event,
            self.child,
            self.root_x,
            self.root_y,
            self.event_x,
            self.event_y,
            self.state,
            self.same_screen,
        ) = unpack("=BBHIIIIhhhhHBx", data)

    def is_valid(self):
        # Response type of a KeyPress event is 2, KeyRelease event has a
        # response type 3
        return self.response_type == 0x2
