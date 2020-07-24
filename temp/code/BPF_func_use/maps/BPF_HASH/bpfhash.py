#!/usr/bin/env python
# coding=utf-8


#analyze disksnoop.py

from __future__ import print_function
from bcc import BPF
from bcc.utils import printb

REQ_WRITE = 1

b = BPF(text = '''
        /*
         *定义寄存器组的结构体：struct pt_regs
         * 内核路径：/arch/x86/include/uapi/asm/ptrace.h
         */
        #include <uapi/linux/ptrace.h>  

        //定义了内核数据结构：struct request
        // 内核路径：/include/linux/blkdev.h
        #include <blkdev.h>

        //define hash table name:start
        //define key pointer type:struct request *
        BPF_HASH(start, struct request *);

        /* define probe_1 */
        /*
         *two arguments:ctx point to registers context
         *              req is key pointer,point to 'struct request'
         */
        void trace_start(struct pt_regs *ctx, struct request *req) {
                //stroed start timestamp 
                u64 ts = bpf_ktime_get_ns();

                //update timestamp 
                start.update(&req, &ts);//用后面的覆写以前的值
        }

        /* define probe_2 */
        void trace_completion(struct pt_regs *ctx, struct request *req) {
                u64 *tsp, delta;

                //return a pointer to its value if it exists,else NULL
                tsp start.loopup(&req);
                if (tsp) {
                        //u64 bpf_ktime_get_ns(void)
                        delta = bpf_ktime_get_ns() - *tsp;

                        /* struct request {
                         *          ...
                         *          unsigned int cmd_flags;
                         *          ...
                         *          unsigned int __data_len;
                         *          ...
                         * };
                         */
                        bpf_trace_printk("%d %x %d\\n", 
                                            req->__data_len, 
                                            req->cmd_flags, 
                                            delta / 1000);
                        start.delete(&req); //delete key
                }
        }
        ''')

#call class BPF's method:get_kprobe_functions
if BPF.get_kprobe_functions(b'blk_start_request'):
    b.attach_kprobe(event = 'blk_start_request', 
                              fn_name = 'trace_start')

b.attach_kprobe(event = 'blk_start_request', fn_name = 'trace_start')
b.attach_kprobe(event = 'blk_account_io_completion', 
                              fn_name = 'trace_completion')

#header
#-号左对齐，+号右对齐(默认不用写出+号)
print('%-18s %-2s %-7s %8s' % ('TIME(s)', 'T', 'BYTES', 'LAT(ms)'))

#format output
while True:
    try:
        (task, pid, cpu, flags, ts, msg) = b.trace_fields()
        (bytes_s, bflags_s, us_s) = msg.split()

        if int(bflags_s, 16) & REQ_WRITE:
            type_s = b'w'
