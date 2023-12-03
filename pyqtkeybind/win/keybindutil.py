import ctypes
from ctypes import windll
from typing import Tuple

import qtpy
from qtpy.QtGui import QKeySequence
from qtpy.QtCore import Qt

from .keycodes import KeyTbl, ModsTbl


def keys_from_string(keys: str) -> Tuple[int, int]:

    keysequence = QKeySequence(keys)
    if qtpy.QT5:
        ks = keysequence[0]

        # Calculate the modifiers
        mods = 0
        qtmods = Qt.NoModifier
        if ks & Qt.ShiftModifier == Qt.ShiftModifier:
            mods |= ModsTbl.index(Qt.ShiftModifier)
            qtmods |= int(Qt.ShiftModifier)
        if ks & Qt.AltModifier == Qt.AltModifier:
            mods |= ModsTbl.index(Qt.AltModifier)
            qtmods |= int(Qt.AltModifier)
        if ks & Qt.ControlModifier == Qt.ControlModifier:
            mods |= ModsTbl.index(Qt.ControlModifier)
            qtmods |= int(Qt.ControlModifier)

        # Calculate the keys
        qtkeys = ks ^ qtmods

        # Pyside2 PySide2.QtCore.Qt.KeyboardModifiers need to be cast to type int
        calculated_keys = qtkeys if qtpy.API == "pyqt5" else int(qtkeys)

    else:
        assert qtpy.QT6
        ks_comb = keysequence[0]
        ks_modifiers = ks_comb.keyboardModifiers()
        calculated_keys = ks_comb.key()

        # Calculate the modifiers
        mods = 0
        if ks_modifiers & Qt.ShiftModifier:
            mods |= ModsTbl.index(Qt.ShiftModifier)
        if ks_modifiers & Qt.AltModifier:
            mods |= ModsTbl.index(Qt.AltModifier)
        if ks_modifiers & Qt.ControlModifier:
            mods |= ModsTbl.index(Qt.ControlModifier)

    try:
        keys = KeyTbl[calculated_keys]
        if keys == 0:
            keys = _get_virtual_key(calculated_keys)
    except ValueError:
        keys = _get_virtual_key(calculated_keys)
    except IndexError:
        keys = KeyTbl.index(calculated_keys)
        if keys == 0:
            keys = _get_virtual_key(calculated_keys)

    return mods, keys


def _get_virtual_key(qtkeys: int) -> int:
    """Use the system keyboard layout to retrieve the virtual key.

    Fallback when we're unable to find a keycode in the mappings table.
    """
    user32 = ctypes.WinDLL("user32", use_last_error=True)
    thread_id = 0

    # Key table doesn't have an entry for this keycode
    # Attempt to retrieve the VK code from system
    keyboard_layout = user32.GetKeyboardLayout(thread_id)
    virtual_key = windll.user32.VkKeyScanExW(qtkeys, keyboard_layout)
    if virtual_key == -1:
        keyboard_layout = user32.GetKeyboardLayout(0x409)
        virtual_key = windll.user32.VkKeyScanExW(qtkeys, keyboard_layout)
    # Key code is the low order byte
    keys = virtual_key & 0xFF

    return keys
