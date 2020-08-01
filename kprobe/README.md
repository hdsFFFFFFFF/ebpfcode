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