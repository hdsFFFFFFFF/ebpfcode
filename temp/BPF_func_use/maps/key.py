#!/usr/bin/env python
# coding=utf-8

from bcc import BPF 

b = BPF(text = '''
        #include <uapi/linux/ptrace.h>

        BPF_HASH(event);

        int kprobe__sys_clone(void *ctx) {
                u64 key = 0;
                u64 count = 0;
                u64 *val_ptr;
                
        bpf_trace_printk("first key value:%llu\\n", key);

                val_ptr = event.lookup(&key);
                if (val_ptr) {
                        count++;
                        event.delete(&key);
        bpf_trace_printk("after delete key value:%llu\\n", key);
                }

        event.update(&key, &count);
        bpf_trace_printk("after update key value:%llu\\n", key);

        return 0;
        }
        ''')

b.trace_print(fmt = '{5}')
