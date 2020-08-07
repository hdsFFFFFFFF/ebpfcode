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

        int kprobe__handle_mm_fault(struct pt_regs *ctx)
        {
                ktime_t start = bpf_ktime_get_ns();

                bpf_trace_printk("start:%lld\\n", start);
        
                return 0;
        }

        int kretprobe__handle_mm_fault(struct pt_regs *ctx, ktime_t *k)
        {
                int ret = PT_REGS_RC(ctx);

                ktime_t end = bpf_ktime_get_ns();

                bpf_trace_printk("end time:%lld\\n", end);

                return 0;
        }
        ''')

b.trace_print(fmt = '{5, 6}')
