#!/usr/bin/env python
# coding=utf-8

from bcc import BPF

b = BPF(text = '''
        #include <uapi/linux/ptrace.h>
        #include <linux/ktime.h>

        BPF_HASH(timer, ktime_t *, ktime_t);
        ktime_t key;
        
        int kprobe__handle_mm_fault(struct pt_regs *ctx)
        {
                //ktime_t *key = 0;
                ktime_t start = bpf_ktime_get_ns();
                timer.update(&key, &start);

                return 0;
        }

        int kretprobe__handle_mm_fault(struct pt_regs *ctx)
        {
                int ret = PT_REGS_RC(ctx);
                //bpf_trace_printk("ret value:%d\\n", ret);

                ktime_t end;
                ktime_t delta, *tsp;
            
                if (ret >= 0) {
                        end = bpf_ktime_get_ns();
                        tsp = timer.lookup(&key);
                        delta = end - *tsp;
                        bpf_trace_printk("delta:%d\\n", delta / 1000000);
                }

                return 0;
        }
        ''')

b.trace_print()
