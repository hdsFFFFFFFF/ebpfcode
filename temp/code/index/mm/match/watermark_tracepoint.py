#!/usr/bin/env python
# coding=utf-8

from bcc import BPF

b = BPF(text = """
        TRACEPOINT_PROBE(vmscan, mm_vmscan_wakeup_kswapd)
        {
                bpf_trace_printk("WARNING:A zone is low on free memory!\\n");

                return 0;
        }
        """)

print("Tracing for function of wakeup_kswapd..")

b.trace_print()
