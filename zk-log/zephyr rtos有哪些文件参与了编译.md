build目录会有一个json文件，compile_commands.json  该文件中描述出了参与编译的文件

![image-20250603152404912](https://newbie-typora.oss-cn-shenzhen.aliyuncs.com/zhongke/image-20250603152404912.png)

```
{
"directory": xxxxxxxxxxxxxxxxxx
"command":xxxxxxxxxxxx
"file":xxxxxxxxxxxx
"output":xxxxxxxxxxxx
}  
```

## 字段解释

| 字段名        | 含义                                                         | 示例/说明                                                    |
| ------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| `"directory"` | 编译命令运行时的工作目录（即 `gcc`/`clang` 等执行时的 `cwd`） | 比如：`"/home/you/project/build"`                            |
| `"command"`   | 实际完整的编译命令行（含编译器路径、所有参数和文件名）       | 比如：`"arm-none-eabi-gcc -I... -D... -c ../src/main.c -o main.o"` |
| `"file"`      | 被编译的源代码文件路径（通常为相对或绝对路径）               | 比如：`"../src/main.c"`                                      |
| `"output"`    | 此源文件编译后生成的目标文件路径                             | 比如：`"CMakeFiles/app.dir/src/main.c.obj"` 或 `"main.o"`    |



写一个脚本只获取  file 字段 来看实际参与编译的文件，当前的compile_commands.json文件太多了不好观察

- 运行后会生成 `files.txt`

```python
import json

with open('compile_commands.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

with open('files.txt', 'w', encoding='utf-8') as f:
    for entry in data:
        f.write(entry['file'] + '\n')
```



![image-20250603153124180](https://newbie-typora.oss-cn-shenzhen.aliyuncs.com/zhongke/image-20250603153124180.png)



查看files.txt

- 依照目录来分析参与编译的文件这样就好分析的多了

```
C:\Users\29955\zephyrproject\art_pi_app\src\main.c
C:\Users\29955\zephyrproject\zephyr\lib\heap\heap.c
C:\Users\29955\zephyrproject\zephyr\lib\os\cbprintf_packaged.c
C:\Users\29955\zephyrproject\zephyr\lib\os\printk.c
C:\Users\29955\zephyrproject\zephyr\lib\os\sem.c
C:\Users\29955\zephyrproject\zephyr\lib\os\thread_entry.c
C:\Users\29955\zephyrproject\zephyr\lib\os\cbprintf_complete.c
C:\Users\29955\zephyrproject\zephyr\lib\os\assert.c
C:\Users\29955\zephyrproject\zephyr\lib\os\reboot.c
C:\Users\29955\zephyrproject\zephyr\lib\utils\dec.c
C:\Users\29955\zephyrproject\zephyr\lib\utils\hex.c
C:\Users\29955\zephyrproject\zephyr\lib\utils\rb.c
C:\Users\29955\zephyrproject\zephyr\lib\utils\timeutil.c
C:\Users\29955\zephyrproject\zephyr\lib\utils\bitarray.c
C:\Users\29955\zephyrproject\zephyr\lib\utils\ring_buffer.c
C:\Users\29955\zephyrproject\zephyr\build\zephyr\misc\generated\configs.c
C:\Users\29955\zephyrproject\zephyr\soc\st\stm32\common\stm32cube_hal.c
C:\Users\29955\zephyrproject\zephyr\soc\st\stm32\common\soc_config.c
C:\Users\29955\zephyrproject\zephyr\soc\st\stm32\stm32h7x\soc_m7.c
C:\Users\29955\zephyrproject\zephyr\soc\st\stm32\stm32h7x\mpu_regions.c
C:\Users\29955\zephyrproject\zephyr\subsys\mem_mgmt\mem_attr.c
C:\Users\29955\zephyrproject\zephyr\subsys\tracing\tracing_none.c
C:\Users\29955\zephyrproject\zephyr\arch\arm\core\offsets\offsets.c
C:\Users\29955\zephyrproject\zephyr\misc\empty_file.c
C:\Users\29955\zephyrproject\zephyr\misc\empty_file.c
C:\Users\29955\zephyrproject\zephyr\build\zephyr\isr_tables.c
C:\Users\29955\zephyrproject\zephyr\arch\common\sw_isr_common.c
C:\Users\29955\zephyrproject\zephyr\arch\common\isr_tables.c
C:\Users\29955\zephyrproject\zephyr\arch\arm\core\fatal.c
C:\Users\29955\zephyrproject\zephyr\arch\arm\core\nmi.c
C:\Users\29955\zephyrproject\zephyr\arch\arm\core\nmi_on_reset.S
C:\Users\29955\zephyrproject\zephyr\arch\arm\core\tls.c
C:\Users\29955\zephyrproject\zephyr\arch\arm\core\cortex_m\exc_exit.c
C:\Users\29955\zephyrproject\zephyr\arch\arm\core\cortex_m\fault.c
C:\Users\29955\zephyrproject\zephyr\arch\arm\core\cortex_m\fault_s.S
C:\Users\29955\zephyrproject\zephyr\arch\arm\core\cortex_m\fpu.c
C:\Users\29955\zephyrproject\zephyr\arch\arm\core\cortex_m\reset.S
C:\Users\29955\zephyrproject\zephyr\arch\arm\core\cortex_m\scb.c
C:\Users\29955\zephyrproject\zephyr\arch\arm\core\cortex_m\thread_abort.c
C:\Users\29955\zephyrproject\zephyr\arch\arm\core\cortex_m\vector_table.S
C:\Users\29955\zephyrproject\zephyr\arch\arm\core\cortex_m\swap_helper.S
C:\Users\29955\zephyrproject\zephyr\arch\arm\core\cortex_m\irq_manage.c
C:\Users\29955\zephyrproject\zephyr\arch\arm\core\cortex_m\prep_c.c
C:\Users\29955\zephyrproject\zephyr\arch\arm\core\cortex_m\thread.c
C:\Users\29955\zephyrproject\zephyr\arch\arm\core\cortex_m\cpu_idle.c
C:\Users\29955\zephyrproject\zephyr\arch\arm\core\cortex_m\irq_init.c
C:\Users\29955\zephyrproject\zephyr\arch\arm\core\cortex_m\isr_wrapper.c
C:\Users\29955\zephyrproject\zephyr\arch\arm\core\cortex_m\__aeabi_read_tp.S
C:\Users\29955\zephyrproject\zephyr\arch\arm\core\mpu\arm_core_mpu.c
C:\Users\29955\zephyrproject\zephyr\arch\arm\core\mpu\arm_mpu.c
C:\Users\29955\zephyrproject\zephyr\lib\libc\picolibc\assert.c
C:\Users\29955\zephyrproject\zephyr\lib\libc\picolibc\cbprintf.c
C:\Users\29955\zephyrproject\zephyr\lib\libc\picolibc\chk_fail.c
C:\Users\29955\zephyrproject\zephyr\lib\libc\picolibc\errno_wrap.c
C:\Users\29955\zephyrproject\zephyr\lib\libc\picolibc\exit.c
C:\Users\29955\zephyrproject\zephyr\lib\libc\picolibc\locks.c
C:\Users\29955\zephyrproject\zephyr\lib\libc\picolibc\stdio.c
C:\Users\29955\zephyrproject\zephyr\lib\libc\common\source\stdlib\abort.c
C:\Users\29955\zephyrproject\zephyr\lib\libc\common\source\stdlib\malloc.c
C:\Users\29955\zephyrproject\zephyr\misc\empty_file.c
C:\Users\29955\zephyrproject\zephyr\drivers\interrupt_controller\intc_exti_stm32.c
C:\Users\29955\zephyrproject\zephyr\drivers\clock_control\clock_stm32_ll_h7.c
C:\Users\29955\zephyrproject\zephyr\drivers\console\uart_console.c
C:\Users\29955\zephyrproject\zephyr\drivers\gpio\gpio_stm32.c
C:\Users\29955\zephyrproject\zephyr\drivers\pinctrl\common.c
C:\Users\29955\zephyrproject\zephyr\drivers\pinctrl\pinctrl_stm32.c
C:\Users\29955\zephyrproject\zephyr\drivers\reset\reset_stm32.c
C:\Users\29955\zephyrproject\zephyr\drivers\serial\uart_stm32.c
C:\Users\29955\zephyrproject\zephyr\drivers\timer\sys_clock_init.c
C:\Users\29955\zephyrproject\zephyr\drivers\timer\cortex_m_systick.c
C:\Users\29955\zephyrproject\modules\hal\stm32\stm32cube\stm32h7xx\soc\system_stm32h7xx.c
C:\Users\29955\zephyrproject\modules\hal\stm32\stm32cube\stm32h7xx\drivers\src\stm32h7xx_hal.c
C:\Users\29955\zephyrproject\modules\hal\stm32\stm32cube\stm32h7xx\drivers\src\stm32h7xx_hal_rcc.c
C:\Users\29955\zephyrproject\modules\hal\stm32\stm32cube\stm32h7xx\drivers\src\stm32h7xx_hal_rcc_ex.c
C:\Users\29955\zephyrproject\modules\hal\stm32\stm32cube\stm32h7xx\drivers\src\stm32h7xx_hal_cortex.c
C:\Users\29955\zephyrproject\modules\hal\stm32\stm32cube\stm32h7xx\drivers\src\stm32h7xx_ll_rcc.c
C:\Users\29955\zephyrproject\modules\hal\stm32\stm32cube\stm32h7xx\drivers\src\stm32h7xx_ll_utils.c
C:\Users\29955\zephyrproject\zephyr\kernel\main_weak.c
C:\Users\29955\zephyrproject\zephyr\kernel\banner.c
C:\Users\29955\zephyrproject\zephyr\kernel\busy_wait.c
C:\Users\29955\zephyrproject\zephyr\kernel\device.c
C:\Users\29955\zephyrproject\zephyr\kernel\errno.c
C:\Users\29955\zephyrproject\zephyr\kernel\fatal.c
C:\Users\29955\zephyrproject\zephyr\kernel\init.c
C:\Users\29955\zephyrproject\zephyr\kernel\init_static.c
C:\Users\29955\zephyrproject\zephyr\kernel\kheap.c
C:\Users\29955\zephyrproject\zephyr\kernel\mem_slab.c
C:\Users\29955\zephyrproject\zephyr\kernel\float.c
C:\Users\29955\zephyrproject\zephyr\kernel\version.c
C:\Users\29955\zephyrproject\zephyr\kernel\idle.c
C:\Users\29955\zephyrproject\zephyr\kernel\mailbox.c
C:\Users\29955\zephyrproject\zephyr\kernel\msg_q.c
C:\Users\29955\zephyrproject\zephyr\kernel\mutex.c
C:\Users\29955\zephyrproject\zephyr\kernel\queue.c
C:\Users\29955\zephyrproject\zephyr\kernel\sem.c
C:\Users\29955\zephyrproject\zephyr\kernel\stack.c
C:\Users\29955\zephyrproject\zephyr\kernel\system_work_q.c
C:\Users\29955\zephyrproject\zephyr\kernel\work.c
C:\Users\29955\zephyrproject\zephyr\kernel\condvar.c
C:\Users\29955\zephyrproject\zephyr\kernel\thread.c
C:\Users\29955\zephyrproject\zephyr\kernel\sched.c
C:\Users\29955\zephyrproject\zephyr\kernel\pipe.c
C:\Users\29955\zephyrproject\zephyr\kernel\timeslicing.c
C:\Users\29955\zephyrproject\zephyr\kernel\xip.c
C:\Users\29955\zephyrproject\zephyr\kernel\timeout.c
C:\Users\29955\zephyrproject\zephyr\kernel\timer.c
C:\Users\29955\zephyrproject\zephyr\kernel\mempool.c
C:\Users\29955\zephyrproject\zephyr\kernel\dynamic_disabled.c
```

按照参与目录大致分析

## 1. `art_pi_app/src/`

- **你的应用程序代码**（如 `main.c`）。
- 通常是用户业务逻辑、入口、main loop 等。

------

## 2. `zephyr/lib/`

- **通用库函数与操作系统基础功能**。
- 如 `heap.c`、`cbprintf_*`、`printk.c`、`assert.c` 等，涉及动态内存、打印、断言、信号量、线程入口等。
- `utils/`：常用工具类（如 hex/dec/rb/bitarray/ring_buffer 等循环缓冲、数组处理工具）。

------

## 3. `zephyr/build/zephyr/` & `zephyr/misc/`

- **自动生成文件、配置文件等辅助代码**。
- 如 `configs.c`、`isr_tables.c`、`empty_file.c` 等，可能为构建生成的初始化配置或中断表。

------

## 4. `zephyr/soc/st/stm32/`

- **目标 SoC（如 STM32）相关的适配和底层代码**。
- `common/`、`stm32h7x/`等：包含HAL适配、SoC配置、特定处理器功能（如 `soc_config.c`、`mpu_regions.c`）。

------

## 5. `zephyr/subsys/`

- **Zephyr子系统代码**。
- 如 `mem_mgmt/`（内存管理）、`tracing/`（追踪日志/调试子系统等）。

------

## 6. `zephyr/arch/`

- **架构相关代码**（此处是 ARM 架构）。
- `arm/core/`、`core/cortex_m/`、`core/mpu/` 等：涉及CPU异常、上下文切换、MPU、ISR、fault/中断/向量表、空闲、线程管理、架构适配等。
- `.S` 文件为 ARM 汇编实现的底层启动或关键性能函数。

------

## 7. `zephyr/kernel/`

- **Zephyr内核核心代码**。
- 涉及任务调度（`sched.c`）、线程（`thread.c`）、信号量（`sem.c`）、队列、互斥锁、定时器、工作队列（`work.c`）、主入口（`main_weak.c`）、错误处理（`fatal.c`）、时钟（`timer.c`）、内存池、浮点支持等。
- 这是RTOS最关键的部分。

------

## 8. `zephyr/drivers/`

- **设备驱动层**。
- `interrupt_controller/`：中断控制器
- `clock_control/`：时钟驱动
- `console/`：串口/控制台
- `gpio/`：通用IO
- `pinctrl/`：引脚复用/配置
- `reset/`：芯片复位
- `serial/`：串口通信
- `timer/`：定时器

------

## 9. `modules/hal/stm32/stm32cube/`

- **STM32官方HAL库**（硬件抽象层，Zephyr通过它操作底层硬件）。
- `drivers/src/`、`soc/`：与具体芯片型号和片上外设相关的底层实现，如时钟、外设驱动、系统启动等。

------

## 10. `zephyr/lib/libc/`

- **C库实现（如 picolibc）**。
- 基础的标准C库功能实现，如assert、errno、exit、malloc、stdio等。

------

## 11. 其他

- 还有如 `zephyr/arch/common/`、`subsys/`、`kernel/`、`misc/`、`utils/`、`drivers/`，基本对应Zephyr各功能模块/系统组件。
- `empty_file.c` 一般为占位符，部分自动生成文件为配置或占位。