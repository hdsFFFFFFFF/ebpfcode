#!/usr/bin/env python
# coding=utf-8

import os, sys
import time


while True:
    try:
        print("################################################################")
        #with fd as file_object:
        file_path = "/proc/zoneinfo"

        fd = open (file_path)
        contents = fd.read()
        print(contents.rstrip())
        time.sleep(3)
    except IOError:
        msg = "Sorry, the file does not exist."
        print(msg)
    except KeyboardInterrupt:
        fd.close()
        exit()

