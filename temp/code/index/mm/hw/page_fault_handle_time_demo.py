#!/usr/bin/env python
# coding=utf-8

from bcc import BPF

b = BPF(text = '''
        #include <uapi/linux/ptrace.h>
        /*
         * 如果使用高精度定时器，为了防止溢出，需要使用一个更大的变量类型来存储
         * ktime_t是一个以nanosecond精度来表示的墙上时间
         */
        #include <linux/ktime.h>

        BPF_HASH(timer, ktime_t *);//用hash table来存储时间戳
        
        int kprobe__handle_mm_fault(struct pt_regs *ctx)
        {
                ktime_t *key = 0;
                ktime_t start1 = bpf_ktime_get_ns();
                u64 start2 = bpf_ktime_get_ns();

                timer.update(&key, &start1);

                bpf_trace_printk("start1:%lld start2:%d\\n", start1, start2 / 1000000);
        
                return 0;
        }

        int kretprobe__handle_mm_fault(struct pt_regs *ctx)
        {
                int ret = PT_REGS_RC(ctx);
                bpf_trace_printk("ret value:%d\\n", ret);

                ktime_t end;
                //ktime_t delta, *tsp;
            
                end = bpf_ktime_get_ns();
                //tsp = timer.lookup(&key);
                //delta = end - *tsp;
                bpf_trace_printk("end time:%lld\\n", end);

                return 0;
        }
        ''')

b.trace_print()
