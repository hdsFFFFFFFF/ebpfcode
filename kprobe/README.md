### `kprobes`

语法：`kprobe_ _kernel_function_name`

`kprobe`是一个特殊的前缀，它为其余部分提供的内核函数名称创建`kprobe`(内核函数调用的动态跟踪)。

还可以通过声明一个普通的C函数来使用`kprobes`，然后使用Python的`BPF.attach_kprobe()`将其与内核函数关联。

参数在声明中指定：

```c
kprobe__kernel_function_name(struct pt_regs *ctx [, argument1])
```

For example:

```c
int kprobe__tcp_v4_connect(struct pt_regs *ctx, struct sock *sk) {
				[...]
}
```

`kprobe`需要以下参数来检测内核函数`tcp_v4_connect()`

- `struct pt_regs *ctx`：寄存器和`BPF`上下文
- `struct sock *sk`：`tcp_v4_connect()`的第一个参数

第一个参数始终为`struct pt_regs *`，其余为内核函数的参数(如果你不打算使用它们，则无需指定它们)。



#### `kprobes`黑名单：`kprobe blacklist`

`NOKPROBES_SYMBOL`宏用来将一个内核函数加入黑名单列表`kprobe_blacklist_entry`。

`kprobes`可以捕获几乎任何内核代码的地址，但无法捕获内核代码的某些部分，比如黑名单中的内容。

`Kprobes`使用黑名单检查给定的探测地址，如果给定的地址在黑名单中，则拒绝注册。

参考资料

- [kprobes: Introduce NOKPROBE_SYMBOL() macro for blacklist](https://lore.kernel.org/patchwork/patch/424335/)
- [kprobes: introduce NOKPROBE_SYMBOL, bugfixes and scalbility efforts](https://lwn.net/Articles/588619/)

#### 如果绕过黑名单

如果想让所有的内核函数都可以设置`kprobes`，执行以下脚本：

```shell
  #!/bin/sh
  TRACE_DIR=/sys/kernel/debug/tracing/
  echo > $TRACE_DIR/kprobe_events
  grep -iw t /proc/kallsyms | tr -d . | \
    awk 'BEGIN{i=0};{print("p:"$3"_"i, "0x"$1); i++}' | \
    while read l; do echo $l >> $TRACE_DIR/kprobe_events ; done
```

由于它根本不会检查黑名单，因此会看到许多写入错误，但没有问题。

