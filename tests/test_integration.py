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

    proc = Popen(cmd, stdout=PIPE, stderr=PIPE)
    time.sleep(6)
    os.system(xdocmd)
    os.system(xdoexit)

    stdout, stderr = proc.communicate()
    print("stderr = {0}".format(stderr.decode("ascii")))
    assert proc.returncode == 0
    assert "hello world" in stdout.decode("ascii")
