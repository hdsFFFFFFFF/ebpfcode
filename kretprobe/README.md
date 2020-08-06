### kretprobes

#### 可以用来做什么?

- 探测函数的`返回值`和`执行时间`

#### 用法

Syntax：`kretprobe_kernel_function_name`

kretprobe__是一个特殊的前缀，它为内核函数创建一个kretprobe(内核函数返回的动态跟踪)。

也可以通过声明一个普通的C函数来使用kretprobes，然后使用Python的`BPF.attach_kretprobe()`将其与内核函数关联。

PT_REGS_RC(ctx)用作声明函数的返回值，声明如下：

```c
kretprobe_kernel_function_name(struct pt_regs *ctx)
```

例如：

```c
int kretprobe__tcp_v4_connect(struct pt_regs *ctx)
{
				int ret = PT_REGS_RC(ctx);
				[...]
}
```

