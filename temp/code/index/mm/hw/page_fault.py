#!/usr/bin/env python
# coding=utf-8

from bcc import BPF

global count

b = BPF(text = '''
        #include <uapi/linux/ptrace.h>

        BPF_HASH(cnt, u32);

        static u32 count = 0;

        int kprobe__handle_mm_fault (struct pt_regs *ctx) {
                count++;
                bpf_trace_printk("call count:%d\\n", count);

                return 0;
        }
        ''')

b.trace_print()
