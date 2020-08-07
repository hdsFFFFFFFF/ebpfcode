#!/usr/bin/env python
# coding=utf-8

from bcc import BPF

BPF(text="""
#include <uapi/linux/ptrace.h>
BPF_HASH(rvalues, u64, unsigned long);
int kretprobe__randomize_stack_top(struct pt_regs *ctx) {
    u64 zero = 0;
    unsigned long rvalue = PT_REGS_RC(ctx);
    rvalues.lookup(&zero);
    return 0;
}

int kretprobe__load_elf_binary(struct pt_regs *ctx) {
    u64 zero = 0;
    unsigned long *rvalue_ptr = rvalues.lookup(&zero);
    if (rvalue_ptr) {
        unsigned long rvalue = *rvalue_ptr;
        bpf_trace_printk("value returned by randomize_stack_top: %d", rvalue);
    }
    return 0;
}
""").trace_print()
#randomize_stack_top的返回值rvalues用键0 保存在哈希映射中（也可以使用BPF_ARRAY，因为键已在此处固定）。
#load_elf_binary通过在哈希图上进行简单查找即可检索到该值。

#注意：如果有多个进程调用这些函数，则可以将它们的PID用作哈希映射的键，以区分不同的返回值。

#bcc提供了更高级别的Python API，可在内核中加载eBPF程序并与之交互。可以使用eBPF程序代替内核模块来检测kprobes。

