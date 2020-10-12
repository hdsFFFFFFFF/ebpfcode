#!/usr/bin/env python
# coding=utf-8

import os, sys

path = "/proc/zoneinfo"

f = open (path)
line = f.readline()

while line:
    print(line.rstrip())
    line = f.readline()

f.close()
