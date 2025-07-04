主cmakelist分析

```cmake
cmake_minimum_required(VERSION 3.6)

#CMAKE_CURRENT_SOURCE_DIR 表示当前 CMakeLists.txt 目录  ..代表上一级目录
# prj_root directory realtek_amebapro2_v0_example
set (prj_root "${CMAKE_CURRENT_SOURCE_DIR}/..")
# sdk_root  directory sdk-ameba-v9.6b
set (sdk_root "${CMAKE_CURRENT_SOURCE_DIR}/../../..")
#当前同级目录下包含config.cmake文件
include(./config.cmake)


[[
file(GLOB ...) 是用于获取符合特定模式的文件列表的命令。它会将符合给定路径模式的所有文件列出，并存储在变量中。
NETWORK_BINARY 是用来存储找到的文件列表的变量。
"${NN_MODEL_PATH}/*.nb" 是路径模式，用来查找在 ${NN_MODEL_PATH} 目录下扩展名为 .nb 的所有文件。

set(NN_MODEL_PATH		${prj_root}/src/test_model/model_nb)    ---config.cmake
]]

file(GLOB NETWORK_BINARY
  "${NN_MODEL_PATH}/*.nb"
)

[[
file(COPY ...) 用于将文件或目录从源位置复制到目标位置。 • ${NETWORK_BINARY} 是文件列表变量，表示要复制的文件。 • DESTINATION . 指定了目标位置为当前目录（. 代表当前目录）
]]

file(COPY ${NETWORK_BINARY}
     DESTINATION .)
 [[
    这段CMake脚本的功能是：
    1. 检查引导加载器是否需要构建：如果CMakeLists.txt文件存在，则构建引导加载器并设置相关的变量；否则，直接使用已经发布的            boot.bin文件。 
    2. 设置相关的二进制文件和依赖：根据构建过程或使用已发布的文件，设置boot_image、fcs_param和boot_dep变量。  
    • 如果CMakeLists.txt存在，CMake会构建引导加载器并设置路径； 
    • 如果CMakeLists.txt不存在，则直接使用预构建的boot.bin文件。
 ]]    

if (EXISTS "${prj_root}/GCC-RELEASE/bootloader/CMakeLists.txt")
	message(STATUS "build bootloader")
	#将bootloader子目录添加到CMake构建中
	add_subdirectory (bootloader)
	set(boot_image bootloader/boot.bin)
	set(fcs_param bootloader/boot_fcs.bin)
	set(boot_dep bootloader)
else()
	message(STATUS "use released boot.bin")
	set(boot_image ${prj_root}/GCC-RELEASE/bootloader/boot.bin)
	set(fcs_param ${prj_root}/GCC-RELEASE/bootloader/boot_fcs.bin)
	set(boot_dep ${ELF2BIN})
endif()

[[


]]

#判断BUILD_TZ是否为真   “TZ”（通常是“Trusted Zone”或“安全区域”）构建）。如果为真，CMake将进入该分支。
if(BUILD_TZ)
#如果BUILD_WLANMP为真，设置目标名称为flash_tz_mp；如果BUILD_WLANMP为假，设置目标名称为flash_tz
	if(BUILD_WLANMP)
		set(target flash_tz_mp)
	else()
		set(target flash_tz)
	endif()
	[[
	设置一些构建所需的文件路径： 
	• fw: 设置为application/firmware_tz.bin，即固件文件的路径，这个文件是用于“Trusted Zone”构建的固件。 
	• isp_iq: 设置为application/firmware_isp_iq.bin，可能是ISP（Image Signal Processor）相关的固件。 
	• app_dep: 设置为application.s和application.ns，这些可能是应用程序的源文件或者配置文件。 
	• symbols: 设置为application/application.ns.symbols，可能是符号文件，用于调试或者构建过程。  
	]]
	set(fw application/firmware_tz.bin)
	set(isp_iq application/firmware_isp_iq.bin)
	set(app_dep application.s application.ns)
	set(symbols application/application.ns.symbols)
	#bttrace: 设置为application/APP.trace，可能是蓝牙跟踪数据文件。
	set(bttrace application/APP.trace)
	#将application目录添加为一个子目录，这样CMake会查找该目录下的CMakeLists.txt文件，并构建其中定义的目标
	add_subdirectory (application)
else()
    
	if(BUILD_WLANMP)
		set(target flash_ntz_mp)
	else()
		set(target flash_ntz)
	endif()
	set(fw application/firmware_ntz.bin)
	set(isp_iq application/firmware_isp_iq.bin)
	set(app_dep application.ntz)
	set(symbols application/application.ntz.symbols)
	
	set(bttrace application/APP.trace)
	add_subdirectory (application)
endif()




     
     



```







config.cmake

```

```



prj_root :   realtek_amebapro2_v0_example

sdk_root:   sdk-ameba-v9.6b













