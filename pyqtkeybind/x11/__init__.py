# -*- coding: utf-8 -*-

import sys
from collections import defaultdict

from PyQt5.QtX11Extras import QX11Info
import xcffib
import xcffib.xproto
from xcffib import ffi
from struct import unpack
import sip

from .keybindutil import *

# class X11KeyBinder(KeyBinder):
class X11KeyBinder(object):
    conn = None

    def init(self):
        # Get the X11 connection and update keyboard mappings
        qt_conn = QX11Info.connection()
        ptr = sip.unwrapinstance(qt_conn)
        self.conn = xcffib.wrap(ptr)
        update_keyboard_mapping(self.conn, None)

    def register_hotkey(self, wid, key_string, callback):
        if wid is None:
            wid = QX11Info.appRootWindow()

        return bind_global_key(self.conn, "KeyPress", key_string, callback)

    def unregister_hotkey(self, wid, key_string):
        if wid is None:
            wid = QX11Info.appRootWindow()

        return unbind_global_key(self.conn, wid, key_string)

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
        self.response_type, self.detail, self.sequence, self.time,\
            self.root, self.event, self.child, self.root_x, self.root_y,\
            self.event_x, self.event_y, self.state,\
            self.same_screen = unpack("=BBHIIIIhhhhHBx", data)

    def is_valid(self):
        # Response type of a KeyPress event is 2, KeyRelease event has a
        # response type 3
        return self.response_type == 0x2
