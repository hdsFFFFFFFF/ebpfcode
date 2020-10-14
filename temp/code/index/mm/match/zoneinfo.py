#!/usr/bin/env python
# coding=utf-8

import os, sys
import time

file_path = "/proc/zoneinfo"

fd = open (file_path)

while True:
    try:
        time.sleep(1)
        with fd as file_object:
            contents = file_object.read()
            print(contents.rstrip())
    except IOError:
        msg = "Sorry, the file does not exist."
        print(msg)
    except KeyboardInterrupt:
        exit()

