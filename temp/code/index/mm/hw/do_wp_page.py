#!/usr/bin/env python
# coding=utf-8

from __future__ import print_function
from bcc import BPF

b = BPF(text = '''
        #include <uapi/linux/ptrace.h>
        #include <linux/ktime.h>
        
        BPF_HASH(timer, u32, ktime_t);
      
        int kprobe__do_wp_page(struct pt_regs *ctx)
        {
               
                u32 pid = bpf_get_current_pid_tgid();
             
                ktime_t start = bpf_ktime_get_ns();
                timer.update(&pid, &start);

                return 0;
        }
   
        int kretprobe__do_wp_page(struct pt_regs *ctx)
        {
             
                ktime_t end = bpf_ktime_get_ns();
                int ret = PT_REGS_RC(ctx);
                
                u32 pid = bpf_get_current_pid_tgid();
                
                ktime_t delta;
                
                ktime_t *tsp = timer.lookup(&pid);
                if ((ret >= 0) && (tsp != NULL))
                        delta = end - *tsp;
         
                //if (delta >= 10000000) {
                //        bpf_trace_printk("%lld\\n", delta);
                //}

                bpf_trace_printk("%lld\\n", delta);

                return 0;
        }
        ''')


print("%-19s %-16s %-6s %18s" % ("Time-Delay", "COMM", "PID","TIME(s)"))

while True:
    try:
        (task, pid, cpu, flags, ts, us) = b.trace_fields()#内核时间以纳秒(ns)为单位
        #1s = 1000毫秒(ms)        
        #1ms = 1000微妙(us)
        #1us = 1000纳秒(ns)
        #1ns = 1000皮秒(ps)
        ms = float(us) / 1000000    
	
	#print("%-19.4fms %-16s %-6d %19.9f" % (ms, task, pid, ts))
	print("%-8.4fms %16s %13d %19.9f" % (ms, task, pid, ts))
    except KeyboardInterrupt:
        exit()
        


