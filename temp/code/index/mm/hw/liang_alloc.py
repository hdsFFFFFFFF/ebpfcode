#!/usr/bin/env python
# coding=utf-8

from bcc import BPF
# define BPF program
b = BPF(text="""
#include <uapi/linux/ptrace.h>
#include <linux/ktime.h>

BPF_HASH(timer, u32, ktime_t);
int kprobe____alloc_pages_nodemask(struct pt_regs *ctx) {
 	
    	u32 pid = bpf_get_current_pid_tgid(); //获取执行该命令的进程ID
        ktime_t start = bpf_ktime_get_ns();
	timer.update(&pid, &start);
    
    return 0;
}

int kretprobe____alloc_pages_nodemask(struct pt_regs *ctx){
    		int ret = PT_REGS_RC(ctx);
		ktime_t end = bpf_ktime_get_ns();
             
                //获取pid
                u32 pid = bpf_get_current_pid_tgid();
                
                ktime_t delta;
                //在hash中查找pid，如果存在，则返回对应的值，否则返回NULL。
                ktime_t *tsp = timer.lookup(&pid);
                if ((ret >= 0) && (tsp != NULL))
                        delta = end - *tsp;
                        //delta保存时间差
                bpf_trace_printk("%lld\\n", delta);
    return 0;
        }
""")




# header
print("%-19s %-16s %-6s %18s" % ("Time-Delay", "COMM", "PID","TIME(s)"))


# format output
while True:
    try:
        (task, pid, cpu, flags, ts, us) = b.trace_fields()#内核时间以纳秒(ns)为单位
        #1s = 1000毫秒(ms)        
        #1ms = 1000微妙(us)
        #1us = 1000纳秒(ns)
        #1ns = 1000皮秒(ps)
        ms = float(us) / 1000000    
	
	print("%-19.9f %-16s %-6d %19.9f" % (ms, task, pid, ts))
    except KeyboardInterrupt:
        exit()
        
