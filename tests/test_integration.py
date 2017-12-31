#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Integration tests for pyqtkeybind."""

import os
import time
from subprocess import Popen, PIPE


def test_hotkey_integration(xvfb):
    xdocmd = "xdotool key Control+Shift+A"
    xdoexit = "xdotool key Control+Shift+E"
    cmd = ["python", "sample/hotkey.py"]

    proc = Popen(cmd, stdout=PIPE)
    time.sleep(3)
    os.system(xdocmd)
    os.system(xdoexit)

    assert "hello world" in proc.communicate()[0].decode("ascii")
