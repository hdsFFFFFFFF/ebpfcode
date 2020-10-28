#!/usr/bin/env python
# coding=utf-8

from bcc import BPF

b= BPF(text = '''
       #include <uapi/linux/ptrace.h>
       
       //int kprobe_wakeup_all_kswapd(struct pt_regs *ctx)
       int kprobe_sys_clone(struct pt_regs *ctx)
       {
                //bpf_trace_printk("WARNING:A zone is low on free memory!\\n");
                bpf_trace_printk("hello, world\\n");

                return 0;
       }
       ''')

#print("Tracing for function of wakeup_kswapd...")

b.trace_print()
