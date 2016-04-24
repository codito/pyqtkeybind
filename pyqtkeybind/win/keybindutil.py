# -*- coding: utf-8 -*-

from ctypes.wintypes import UINT
from PyQt5.QtGui import QKeySequence
from PyQt5.QtCore import Qt

from .keycodes import KeyTbl, ModsTbl


def keys_from_string(keys):
    keysequence = QKeySequence(keys)
    ks = keysequence[0]

    print("ks : " + hex(ks))
    # Calculate the modifiers
    mods = Qt.NoModifier
    qtmods = Qt.NoModifier
    if (ks & Qt.ShiftModifier == Qt.ShiftModifier):
        mods |= ModsTbl.index(Qt.ShiftModifier)
        qtmods |= Qt.ShiftModifier.real
    if (ks & Qt.AltModifier == Qt.AltModifier):
        mods |= ModsTbl.index(Qt.AltModifier)
        qtmods |= Qt.AltModifier.real
    if (ks & Qt.ControlModifier == Qt.ControlModifier):
        mods |= ModsTbl.index(Qt.ControlModifier)
        qtmods |= Qt.ControlModifier.real

    # Calculate the keys
    qtkeys = ks ^ qtmods
    print("mods: " + hex(qtmods))
    print("keys: " + hex(qtkeys))
    keys = KeyTbl.index(qtkeys)

    return mods, keys
