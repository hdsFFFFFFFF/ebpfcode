#!/usr/bin/env python
# coding=utf-8

from bcc import BPF

b = BPF(text = '''
     #include <linux/ptrace.h>

     int kprobe__alloc_page(struct pt_regs *ctx) {
            bpf_trace_printk("hello world\\n");

            return 0;
    }
     ''')

b.trace_print()
