# -*- coding: utf-8 -*-

import sys

keybinder = None
if sys.platform.startswith("win"):
    from .win import WinKeyBinder

    keybinder = WinKeyBinder()
else:
    from .x11 import X11KeyBinder

    keybinder = X11KeyBinder()
