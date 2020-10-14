#!/usr/bin/env python
# coding=utf-8

from bcc import BPF
import os
import sys
import time
import thread

def load_BPF(thread_name, delay):
    b = BPF(text = '''
            #include <uapi/linux/ptrace.h>

            int kprobe_wakeup_kswapd(struct pt_regs *ctx)
            {
                    bpf_trace_printk("WARNING:A zone is low on free memory!\\n");

                    return 0;
            }
            ''')


    b.trace_print()

def zone_info(thread_name, delay):
    while True:
        try:
            print("----------------------------------------------------------------------------------------------------------------------------")
            file_path = "/proc/zoneinfo"
            fd = open(file_path)
            contents = fd.read()
            print(contents.rstrip())
            time.sleep(delay)
        except IOError:
            msg = "Sorry, the file does not exist."
        except KeyboardInterrupt:
            fd.close()
            exit()

try:
    thread.start_new_thread(load_BPF, ("BPF progream", 0))
    thread.start_new_thread(zone_info, ("zoneinfo", 10))
except:
    print"Error:unable to start thread"

while 1:
    pass
