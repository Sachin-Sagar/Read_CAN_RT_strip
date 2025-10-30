#include <linux/module.h>
#include <linux/export-internal.h>
#include <linux/compiler.h>

MODULE_INFO(name, KBUILD_MODNAME);

__visible struct module __this_module
__section(".gnu.linkonce.this_module") = {
	.name = KBUILD_MODNAME,
	.init = init_module,
#ifdef CONFIG_MODULE_UNLOAD
	.exit = cleanup_module,
#endif
	.arch = MODULE_ARCH_INIT,
};



static const struct modversion_info ____versions[]
__used __section("__versions") = {
	{ 0x487aa866, "vCanAddCardChannel" },
	{ 0x30372d96, "queue_release" },
	{ 0xc31dd9f6, "vCanFlushSendBuffer" },
	{ 0x4d368c95, "vCanInit" },
	{ 0x4829a47e, "memcpy" },
	{ 0x37a0cba, "kfree" },
	{ 0x1ad8797b, "vCanGetCardInfo" },
	{ 0xe2964344, "__wake_up" },
	{ 0xba8fbd64, "_raw_spin_lock" },
	{ 0x92997ed8, "_printk" },
	{ 0x8ddd8aad, "schedule_timeout" },
	{ 0xf0fdf6cb, "__stack_chk_fail" },
	{ 0x52497ba5, "vCanGetCardInfo2" },
	{ 0x441d0de9, "__kmalloc_large_noprof" },
	{ 0x7094968f, "vCanInitData" },
	{ 0x220f6eb0, "queue_pop" },
	{ 0xe6cf5658, "queue_wakeup_on_space" },
	{ 0xb26930f6, "set_capability_value" },
	{ 0xb5f7c829, "vCanDispatchEvent" },
	{ 0xfaa20ff6, "queue_front" },
	{ 0xdcb764ad, "memset" },
	{ 0x679e43d1, "queue_empty" },
	{ 0x57858536, "vCanRemoveCardChannel" },
	{ 0x390a3705, "vCanTime" },
	{ 0x5443de3e, "__kmalloc_cache_noprof" },
	{ 0xa65c6def, "alt_cb_patch_nops" },
	{ 0xb5b54b34, "_raw_spin_unlock" },
	{ 0x2798d1c, "vCanCleanup" },
	{ 0x4fc61f86, "kmalloc_caches" },
	{ 0x474e54d2, "module_layout" },
};

MODULE_INFO(depends, "kvcommon");


MODULE_INFO(srcversion, "F7FA974643FF34FEB47B347");
