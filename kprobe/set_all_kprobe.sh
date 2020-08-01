#!/bin/bash

TRACE_DIR=/sys/kernel/debug/tracing/
echo > $TRACE_DIR/kprobe_events
grep -iw t /proc/kallsyms | tr -d . | \
	awk 'BEGIN{i=0};{print("p:"$3"_"i, "0x"$1); i++}' | \
    	while read l; do echo $l >> $TRACE_DIR/kprobe_events ; done
