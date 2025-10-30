savedcmd_/home/sachin/Downloads/linuxcan/pciefd/drivers/xilinx/spi/src/xspi_options.o :=  aarch64-linux-gnu-gcc-14 -Wp,-MMD,/home/sachin/Downloads/linuxcan/pciefd/drivers/xilinx/spi/src/.xspi_options.o.d -nostdinc -I/usr/src/linux-headers-6.12.47+rpt-common-rpi/arch/arm64/include -I./arch/arm64/include/generated -I/usr/src/linux-headers-6.12.47+rpt-common-rpi/include -I./include -I/usr/src/linux-headers-6.12.47+rpt-common-rpi/arch/arm64/include/uapi -I./arch/arm64/include/generated/uapi -I/usr/src/linux-headers-6.12.47+rpt-common-rpi/include/uapi -I./include/generated/uapi -include /usr/src/linux-headers-6.12.47+rpt-common-rpi/include/linux/compiler-version.h -include /usr/src/linux-headers-6.12.47+rpt-common-rpi/include/linux/kconfig.h -include /usr/src/linux-headers-6.12.47+rpt-common-rpi/include/linux/compiler_types.h -D__KERNEL__ -mlittle-endian -DCC_USING_PATCHABLE_FUNCTION_ENTRY -DKASAN_SHADOW_SCALE_SHIFT= -fmacro-prefix-map=/usr/src/linux-headers-6.12.47+rpt-common-rpi/= -std=gnu11 -fshort-wchar -funsigned-char -fno-common -fno-PIE -fno-strict-aliasing -mgeneral-regs-only -DCONFIG_CC_HAS_K_CONSTRAINT=1 -Wno-psabi -mabi=lp64 -fno-asynchronous-unwind-tables -fno-unwind-tables -mbranch-protection=pac-ret -Wa,-march=armv8.5-a -DARM64_ASM_ARCH='"armv8.5-a"' -DKASAN_SHADOW_SCALE_SHIFT= -fno-delete-null-pointer-checks -O2 -fno-allow-store-data-races -fstack-protector-strong -fno-omit-frame-pointer -fno-optimize-sibling-calls -ftrivial-auto-var-init=zero -fno-stack-clash-protection -fpatchable-function-entry=4,2 -fmin-function-alignment=8 -fstrict-flex-arrays=3 -fno-strict-overflow -fno-stack-check -fconserve-stack -fno-builtin-wcslen -fno-builtin-wcslen -Wall -Wextra -Wundef -Werror=implicit-function-declaration -Werror=implicit-int -Werror=return-type -Werror=strict-prototypes -Wno-format-security -Wno-trigraphs -Wno-frame-address -Wno-address-of-packed-member -Wmissing-declarations -Wmissing-prototypes -Wframe-larger-than=2048 -Wno-main -Wno-dangling-pointer -Wvla -Wno-pointer-sign -Wcast-function-type -Wno-array-bounds -Wno-stringop-overflow -Wno-alloc-size-larger-than -Wimplicit-fallthrough=5 -Werror=date-time -Werror=incompatible-pointer-types -Werror=designated-init -Wenum-conversion -Wunused -Wno-unused-but-set-variable -Wno-unused-const-variable -Wno-packed-not-aligned -Wno-format-overflow -Wno-format-truncation -Wno-stringop-truncation -Wno-override-init -Wno-missing-field-initializers -Wno-type-limits -Wno-shift-negative-value -Wno-maybe-uninitialized -Wno-sign-compare -Wno-unused-parameter -mstack-protector-guard=sysreg -mstack-protector-guard-reg=sp_el0 -mstack-protector-guard-offset=1424 -DLINUX=1 -I/home/sachin/Downloads/linuxcan/pciefd -I/home/sachin/Downloads/linuxcan/pciefd/../include -I/home/sachin/Downloads/linuxcan/pciefd/hw -I/home/sachin/Downloads/linuxcan/pciefd/util -I/home/sachin/Downloads/linuxcan/pciefd/drivers/kvaser -I/home/sachin/Downloads/linuxcan/pciefd/drivers/kvaser/pwm -I/home/sachin/Downloads/linuxcan/pciefd/drivers/kvaser/pciefd -I/home/sachin/Downloads/linuxcan/pciefd/drivers/kvaser/spi_flash -I/home/sachin/Downloads/linuxcan/pciefd/drivers/kvaser/hydra_flash -I/home/sachin/Downloads/linuxcan/pciefd/drivers/altera/inc -I/home/sachin/Downloads/linuxcan/pciefd/drivers/altera/inc/sys -I/home/sachin/Downloads/linuxcan/pciefd/drivers/altera/HAL/inc -I/home/sachin/Downloads/linuxcan/pciefd/drivers/kvaser/spi/sf2_spi -I/home/sachin/Downloads/linuxcan/pciefd/drivers/xilinx/common/src -I/home/sachin/Downloads/linuxcan/pciefd/drivers/xilinx/spi/src -Wall -Wno-date-time -D_DEBUG=0 -DDEBUG=0 -DWIN32=0  -DMODULE  -DKBUILD_BASENAME='"xspi_options"' -DKBUILD_MODNAME='"kvpciefd"' -D__KBUILD_MODNAME=kmod_kvpciefd -c -o /home/sachin/Downloads/linuxcan/pciefd/drivers/xilinx/spi/src/xspi_options.o /home/sachin/Downloads/linuxcan/pciefd/drivers/xilinx/spi/src/xspi_options.c  

source_/home/sachin/Downloads/linuxcan/pciefd/drivers/xilinx/spi/src/xspi_options.o := /home/sachin/Downloads/linuxcan/pciefd/drivers/xilinx/spi/src/xspi_options.c

deps_/home/sachin/Downloads/linuxcan/pciefd/drivers/xilinx/spi/src/xspi_options.o := \
  /usr/src/linux-headers-6.12.47+rpt-common-rpi/include/linux/compiler-version.h \
    $(wildcard include/config/CC_VERSION_TEXT) \
  /usr/src/linux-headers-6.12.47+rpt-common-rpi/include/linux/kconfig.h \
    $(wildcard include/config/CPU_BIG_ENDIAN) \
    $(wildcard include/config/BOOGER) \
    $(wildcard include/config/FOO) \
  /usr/src/linux-headers-6.12.47+rpt-common-rpi/include/linux/compiler_types.h \
    $(wildcard include/config/DEBUG_INFO_BTF) \
    $(wildcard include/config/PAHOLE_HAS_BTF_TAG) \
    $(wildcard include/config/FUNCTION_ALIGNMENT) \
    $(wildcard include/config/CC_HAS_SANE_FUNCTION_ALIGNMENT) \
    $(wildcard include/config/X86_64) \
    $(wildcard include/config/ARM64) \
    $(wildcard include/config/LD_DEAD_CODE_DATA_ELIMINATION) \
    $(wildcard include/config/LTO_CLANG) \
    $(wildcard include/config/HAVE_ARCH_COMPILER_H) \
    $(wildcard include/config/CC_HAS_COUNTED_BY) \
    $(wildcard include/config/UBSAN_SIGNED_WRAP) \
    $(wildcard include/config/CC_HAS_ASM_INLINE) \
  /usr/src/linux-headers-6.12.47+rpt-common-rpi/include/linux/compiler_attributes.h \
  /usr/src/linux-headers-6.12.47+rpt-common-rpi/include/linux/compiler-gcc.h \
    $(wildcard include/config/MITIGATION_RETPOLINE) \
    $(wildcard include/config/ARCH_USE_BUILTIN_BSWAP) \
    $(wildcard include/config/SHADOW_CALL_STACK) \
    $(wildcard include/config/KCOV) \
  /usr/src/linux-headers-6.12.47+rpt-common-rpi/arch/arm64/include/asm/compiler.h \
    $(wildcard include/config/ARM64_PTR_AUTH_KERNEL) \
    $(wildcard include/config/ARM64_PTR_AUTH) \
    $(wildcard include/config/BUILTIN_RETURN_ADDRESS_STRIPS_PAC) \
  /home/sachin/Downloads/linuxcan/pciefd/drivers/xilinx/spi/src/xspi.h \
  /home/sachin/Downloads/linuxcan/pciefd/drivers/xilinx/common/src/xil_types.h \
  /usr/src/linux-headers-6.12.47+rpt-common-rpi/include/linux/types.h \
    $(wildcard include/config/HAVE_UID16) \
    $(wildcard include/config/UID16) \
    $(wildcard include/config/ARCH_DMA_ADDR_T_64BIT) \
    $(wildcard include/config/PHYS_ADDR_T_64BIT) \
    $(wildcard include/config/64BIT) \
    $(wildcard include/config/ARCH_32BIT_USTAT_F_TINODE) \
  /usr/src/linux-headers-6.12.47+rpt-common-rpi/include/uapi/linux/types.h \
  arch/arm64/include/generated/uapi/asm/types.h \
  /usr/src/linux-headers-6.12.47+rpt-common-rpi/include/uapi/asm-generic/types.h \
  /usr/src/linux-headers-6.12.47+rpt-common-rpi/include/asm-generic/int-ll64.h \
  /usr/src/linux-headers-6.12.47+rpt-common-rpi/include/uapi/asm-generic/int-ll64.h \
  /usr/src/linux-headers-6.12.47+rpt-common-rpi/arch/arm64/include/uapi/asm/bitsperlong.h \
  /usr/src/linux-headers-6.12.47+rpt-common-rpi/include/asm-generic/bitsperlong.h \
  /usr/src/linux-headers-6.12.47+rpt-common-rpi/include/uapi/asm-generic/bitsperlong.h \
  /usr/src/linux-headers-6.12.47+rpt-common-rpi/include/uapi/linux/posix_types.h \
  /usr/src/linux-headers-6.12.47+rpt-common-rpi/include/linux/stddef.h \
  /usr/src/linux-headers-6.12.47+rpt-common-rpi/include/uapi/linux/stddef.h \
  /usr/src/linux-headers-6.12.47+rpt-common-rpi/arch/arm64/include/uapi/asm/posix_types.h \
  /usr/src/linux-headers-6.12.47+rpt-common-rpi/include/uapi/asm-generic/posix_types.h \
  /home/sachin/Downloads/linuxcan/pciefd/drivers/xilinx/common/src/xil_assert.h \
  /usr/src/linux-headers-6.12.47+rpt-common-rpi/include/linux/bug.h \
    $(wildcard include/config/GENERIC_BUG) \
    $(wildcard include/config/BUG_ON_DATA_CORRUPTION) \
  /usr/src/linux-headers-6.12.47+rpt-common-rpi/arch/arm64/include/asm/bug.h \
  /usr/src/linux-headers-6.12.47+rpt-common-rpi/include/linux/stringify.h \
  /usr/src/linux-headers-6.12.47+rpt-common-rpi/arch/arm64/include/asm/asm-bug.h \
    $(wildcard include/config/DEBUG_BUGVERBOSE) \
  /usr/src/linux-headers-6.12.47+rpt-common-rpi/arch/arm64/include/asm/brk-imm.h \
  /usr/src/linux-headers-6.12.47+rpt-common-rpi/include/asm-generic/bug.h \
    $(wildcard include/config/BUG) \
    $(wildcard include/config/GENERIC_BUG_RELATIVE_POINTERS) \
    $(wildcard include/config/SMP) \
  /usr/src/linux-headers-6.12.47+rpt-common-rpi/include/linux/compiler.h \
    $(wildcard include/config/TRACE_BRANCH_PROFILING) \
    $(wildcard include/config/PROFILE_ALL_BRANCHES) \
    $(wildcard include/config/OBJTOOL) \
  /usr/src/linux-headers-6.12.47+rpt-common-rpi/arch/arm64/include/asm/rwonce.h \
    $(wildcard include/config/LTO) \
    $(wildcard include/config/AS_HAS_LDAPR) \
  /usr/src/linux-headers-6.12.47+rpt-common-rpi/include/asm-generic/rwonce.h \
  /usr/src/linux-headers-6.12.47+rpt-common-rpi/include/linux/kasan-checks.h \
    $(wildcard include/config/KASAN_GENERIC) \
    $(wildcard include/config/KASAN_SW_TAGS) \
  /usr/src/linux-headers-6.12.47+rpt-common-rpi/include/linux/kcsan-checks.h \
    $(wildcard include/config/KCSAN) \
    $(wildcard include/config/KCSAN_WEAK_MEMORY) \
    $(wildcard include/config/KCSAN_IGNORE_ATOMICS) \
  /usr/src/linux-headers-6.12.47+rpt-common-rpi/include/linux/instrumentation.h \
    $(wildcard include/config/NOINSTR_VALIDATION) \
  /usr/src/linux-headers-6.12.47+rpt-common-rpi/include/linux/once_lite.h \
  /usr/src/linux-headers-6.12.47+rpt-common-rpi/include/linux/panic.h \
    $(wildcard include/config/PANIC_TIMEOUT) \
  /usr/src/linux-headers-6.12.47+rpt-common-rpi/include/linux/printk.h \
    $(wildcard include/config/MESSAGE_LOGLEVEL_DEFAULT) \
    $(wildcard include/config/CONSOLE_LOGLEVEL_DEFAULT) \
    $(wildcard include/config/CONSOLE_LOGLEVEL_QUIET) \
    $(wildcard include/config/EARLY_PRINTK) \
    $(wildcard include/config/PRINTK) \
    $(wildcard include/config/PRINTK_INDEX) \
    $(wildcard include/config/DYNAMIC_DEBUG) \
    $(wildcard include/config/DYNAMIC_DEBUG_CORE) \
  /usr/src/linux-headers-6.12.47+rpt-common-rpi/include/linux/stdarg.h \
  /usr/src/linux-headers-6.12.47+rpt-common-rpi/include/linux/init.h \
    $(wildcard include/config/MEMORY_HOTPLUG) \
    $(wildcard include/config/HAVE_ARCH_PREL32_RELOCATIONS) \
  /usr/src/linux-headers-6.12.47+rpt-common-rpi/include/linux/build_bug.h \
  /usr/src/linux-headers-6.12.47+rpt-common-rpi/include/linux/kern_levels.h \
  /usr/src/linux-headers-6.12.47+rpt-common-rpi/include/linux/linkage.h \
    $(wildcard include/config/ARCH_USE_SYM_ANNOTATIONS) \
  /usr/src/linux-headers-6.12.47+rpt-common-rpi/include/linux/export.h \
    $(wildcard include/config/MODVERSIONS) \
  /usr/src/linux-headers-6.12.47+rpt-common-rpi/arch/arm64/include/asm/linkage.h \
  /usr/src/linux-headers-6.12.47+rpt-common-rpi/include/linux/ratelimit_types.h \
  /usr/src/linux-headers-6.12.47+rpt-common-rpi/include/linux/bits.h \
  /usr/src/linux-headers-6.12.47+rpt-common-rpi/include/linux/const.h \
  /usr/src/linux-headers-6.12.47+rpt-common-rpi/include/vdso/const.h \
  /usr/src/linux-headers-6.12.47+rpt-common-rpi/include/uapi/linux/const.h \
  /usr/src/linux-headers-6.12.47+rpt-common-rpi/include/vdso/bits.h \
  /usr/src/linux-headers-6.12.47+rpt-common-rpi/include/uapi/linux/bits.h \
  /usr/src/linux-headers-6.12.47+rpt-common-rpi/include/uapi/linux/param.h \
  /usr/src/linux-headers-6.12.47+rpt-common-rpi/arch/arm64/include/uapi/asm/param.h \
  /usr/src/linux-headers-6.12.47+rpt-common-rpi/include/asm-generic/param.h \
    $(wildcard include/config/HZ) \
  /usr/src/linux-headers-6.12.47+rpt-common-rpi/include/uapi/asm-generic/param.h \
  /usr/src/linux-headers-6.12.47+rpt-common-rpi/include/linux/spinlock_types_raw.h \
    $(wildcard include/config/DEBUG_SPINLOCK) \
    $(wildcard include/config/DEBUG_LOCK_ALLOC) \
  /usr/src/linux-headers-6.12.47+rpt-common-rpi/arch/arm64/include/asm/spinlock_types.h \
  /usr/src/linux-headers-6.12.47+rpt-common-rpi/include/asm-generic/qspinlock_types.h \
    $(wildcard include/config/NR_CPUS) \
  /usr/src/linux-headers-6.12.47+rpt-common-rpi/include/asm-generic/qrwlock_types.h \
  /usr/src/linux-headers-6.12.47+rpt-common-rpi/arch/arm64/include/uapi/asm/byteorder.h \
  /usr/src/linux-headers-6.12.47+rpt-common-rpi/include/linux/byteorder/little_endian.h \
  /usr/src/linux-headers-6.12.47+rpt-common-rpi/include/uapi/linux/byteorder/little_endian.h \
  /usr/src/linux-headers-6.12.47+rpt-common-rpi/include/linux/swab.h \
  /usr/src/linux-headers-6.12.47+rpt-common-rpi/include/uapi/linux/swab.h \
  arch/arm64/include/generated/uapi/asm/swab.h \
  /usr/src/linux-headers-6.12.47+rpt-common-rpi/include/uapi/asm-generic/swab.h \
  /usr/src/linux-headers-6.12.47+rpt-common-rpi/include/linux/byteorder/generic.h \
  /usr/src/linux-headers-6.12.47+rpt-common-rpi/include/linux/lockdep_types.h \
    $(wildcard include/config/PROVE_RAW_LOCK_NESTING) \
    $(wildcard include/config/LOCKDEP) \
    $(wildcard include/config/LOCK_STAT) \
  /home/sachin/Downloads/linuxcan/pciefd/drivers/xilinx/common/src/xstatus.h \
  /home/sachin/Downloads/linuxcan/pciefd/drivers/xilinx/common/src/xbasic_types.h \
  /home/sachin/Downloads/linuxcan/pciefd/drivers/xilinx/spi/src/xspi_l.h \
  /home/sachin/Downloads/linuxcan/pciefd/drivers/xilinx/common/src/xil_io.h \
  /home/sachin/Downloads/linuxcan/pciefd/drivers/xilinx/spi/src/xspi_i.h \

/home/sachin/Downloads/linuxcan/pciefd/drivers/xilinx/spi/src/xspi_options.o: $(deps_/home/sachin/Downloads/linuxcan/pciefd/drivers/xilinx/spi/src/xspi_options.o)

$(deps_/home/sachin/Downloads/linuxcan/pciefd/drivers/xilinx/spi/src/xspi_options.o):
