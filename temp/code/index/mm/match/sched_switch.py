#!/usr/bin/env python
# coding=utf-8

from bcc import BPF 

b = BPF(text = '''
        #include <uapi/linux/ptrace.h>
        #include <linux/vmstat.h>

        int kprobe_sys_clone(struct pt_regs *ctx)
        {
                unsigned long stat;

                stat = zone_numa_state_snapshot
                bpf_trace_printk("hello...\\n");

                return 0;
        }
        ''')

print("Begin to trace...")

b.trace_print()
