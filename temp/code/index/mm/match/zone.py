#!/usr/bin/python

from __future__ import print_function
from bcc import BPF
from time import sleep, strftime
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("interval", nargs="?", default=99999999,
        help="output interval, in seconds")
parser.add_argument("counts", nargs="?", default=99999999,
        help="number of inputs")

args = parser.parse_args()
countdown = int(args.counts)

bpf_text = """
#include <uapi/linux/ptrace.h>
#include <linux/mmzone.h>
#include <asm-generic/atomic-long.h>

struct key_t {
    char name[32];
};

BPF_HASH(dist, struct key_t, s64);

int put_zone(struct pt_regs *ctx, struct zone *zone, gfp_t gfp_flags, int order, enum zone_type claazone_idex)
{
    struct key_t key;
    s64 pt = (zone->vm_stat[NR_VM_ZONE_STAT_ITEMS]).counter;
    char *name = (char *)zone->name;
    bpf_probe_read_kernel(&key.name, sizeof(key.name), name);
    dist.update(&key, &pt);
    return 0;
}
"""

b = BPF(text=bpf_text)
b.attach_kprobe(event="handle_mm_fault", fn_name="put_zone")

exiting = 0 if args.interval else 1
dist = b.get_table("dist")

while (1):
    try:
        sleep(int(args.interval))
    except KeyboardInterrupt:
        exiting = 1

    for k, v in dist.items():
        print("%-26s %11d" % (k.name.decode('utf-8', 'replace'), v.value))

    dist.clear()

    print("--" * 20)

    countdown -= 1

    if exiting or countdown <= 0:
        exit()

