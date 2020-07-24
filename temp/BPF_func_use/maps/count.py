#!/usr/bin/env python
# coding=utf-8

from bcc import BPF

b = BPF(text = '''
        #include <uapi/linux/ptrace.h>

        BPF_HASH(event)
        ''')
