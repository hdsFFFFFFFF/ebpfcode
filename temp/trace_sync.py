#!/usr/bin/env python
# coding=utf-8

from bcc import BPF

b = BPF(text = '''
        int kprobe__sys_sync(void *ctx) {
                bpf_trace_printk("sys_sync() called");

                return 0;
        }
        ''')

print 'Tracing sys_sync()...Ctrl-C to end'
while True:
    try:
        b.trace_print()
    except KeyboardInterrupt:
        exit()

