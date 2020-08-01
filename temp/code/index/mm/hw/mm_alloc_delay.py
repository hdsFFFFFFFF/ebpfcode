#!/usr/bin/env python
# coding=utf-8


from bcc import BPF

b = BPF(text = '''
        #include <uapi/linux/ptrace.h>

        int kprobe____alloc_pages_nodemask(struct pt_regs *ctx) {
                bpf_trace_printk("hello\\n");

                return 0;
        }
        ''')

b.trace_print()
