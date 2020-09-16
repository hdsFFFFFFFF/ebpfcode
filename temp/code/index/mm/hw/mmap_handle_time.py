#!/usr/bin/env python
# coding=utf-8

from __future__ import print_function
from bcc import BPF

b = BPF(text = '''
        #include <uapi/linux/ptrace.h>
        #include <linux/ktime.h>

        BPF_HASH(timer, u32, ktime_t);

        int kprobe__ksys_mmap_pgoff(struct pt_regs *ctx)
        {
                u32 pid = bpf_get_current_pid_tgid();
                ktime_t start = bpf_ktime_get_ns();
                
                timer.update(&pid, &start);

                return 0;
        }

        int kretprobe__ksys_mmap_pgoff(struct pt_regs *ctx)
        {
                ktime_t end = bpf_ktime_get_ns();
                int ret = PT_REGS_RC(ctx);
                
                u32 pid = bpf_get_current_pid_tgid();
                
                ktime_t delta;
                ktime_t *tsp = timer.lookup(&pid);
                if ((ret >= 0) && (tsp != NULL))
                        delta = end - *tsp;

                bpf_trace_printk("%lld\\n", delta);

                return 0;
        }
        ''')

print("Tracing for mmap handling time...Ctrl-C to end")

while True:
    try:
        (tsk, pid, cpu, flags, ts, us) = b.trace_fields()#内核时间以纳秒(ns)为单位
        #1s = 1000毫秒(ms)        
        #1ms = 1000微妙(us)
        #1us = 1000纳秒(ns)
        #1ns = 1000皮秒(ps)
        ms = float(us) / 1000000    
        print('mmap handling time:%8.4fms\n' % (ms))
    except KeyboardInterrupt:
        exit()
        

