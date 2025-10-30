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
	{ 0xaabb1e65, "usb_alloc_urb" },
	{ 0x5416eb0, "try_module_get" },
	{ 0x49cd25ed, "alloc_workqueue" },
	{ 0x9dcb80d8, "usb_free_urb" },
	{ 0x4a3ad70e, "wait_for_completion_timeout" },
	{ 0x487aa866, "vCanAddCardChannel" },
	{ 0x7f02188f, "__msecs_to_jiffies" },
	{ 0x52c5c991, "__kmalloc_noprof" },
	{ 0x8dfc0fe6, "usb_alloc_coherent" },
	{ 0xa6257a2f, "complete" },
	{ 0xc5b6f236, "queue_work_on" },
	{ 0x30372d96, "queue_release" },
	{ 0x55555880, "queue_reinit" },
	{ 0x244ab863, "queue_back" },
	{ 0x608741b5, "__init_swait_queue_head" },
	{ 0x10fa71db, "queue_remove_wait_for_space" },
	{ 0xa728742c, "usb_register_driver" },
	{ 0xc31dd9f6, "vCanFlushSendBuffer" },
	{ 0x4d368c95, "vCanInit" },
	{ 0x4829a47e, "memcpy" },
	{ 0x37a0cba, "kfree" },
	{ 0x1ad8797b, "vCanGetCardInfo" },
	{ 0xe2964344, "__wake_up" },
	{ 0x34db050b, "_raw_spin_lock_irqsave" },
	{ 0xba8fbd64, "_raw_spin_lock" },
	{ 0x20bc8744, "wake_up_process" },
	{ 0x92997ed8, "_printk" },
	{ 0x8ddd8aad, "schedule_timeout" },
	{ 0x6fbe60ba, "usb_bulk_msg" },
	{ 0xf0fdf6cb, "__stack_chk_fail" },
	{ 0x52497ba5, "vCanGetCardInfo2" },
	{ 0x441d0de9, "__kmalloc_large_noprof" },
	{ 0x4ca11597, "usb_submit_urb" },
	{ 0x7094968f, "vCanInitData" },
	{ 0xbd9f15bf, "usb_free_coherent" },
	{ 0xcf03f87f, "__module_put_and_kthread_exit" },
	{ 0x8c03d20c, "destroy_workqueue" },
	{ 0x220f6eb0, "queue_pop" },
	{ 0xe6cf5658, "queue_wakeup_on_space" },
	{ 0xb26930f6, "set_capability_value" },
	{ 0x1e5b8225, "usb_deregister" },
	{ 0xd35cce70, "_raw_spin_unlock_irqrestore" },
	{ 0xb5f7c829, "vCanDispatchEvent" },
	{ 0x87d7787f, "queue_add_wait_for_space" },
	{ 0xfaa20ff6, "queue_front" },
	{ 0xdcb764ad, "memset" },
	{ 0x25974000, "wait_for_completion" },
	{ 0x6782eeca, "queue_push" },
	{ 0x679e43d1, "queue_empty" },
	{ 0xaad8c7d6, "default_wake_function" },
	{ 0x57858536, "vCanRemoveCardChannel" },
	{ 0xcb661d89, "kthread_create_on_node" },
	{ 0x5443de3e, "__kmalloc_cache_noprof" },
	{ 0x473aa263, "usb_kill_urb" },
	{ 0xa65c6def, "alt_cb_patch_nops" },
	{ 0xa02aea3a, "queue_length" },
	{ 0xb5b54b34, "_raw_spin_unlock" },
	{ 0x2798d1c, "vCanCleanup" },
	{ 0xfe2fd6f8, "queue_init" },
	{ 0x4fc61f86, "kmalloc_caches" },
	{ 0x474e54d2, "module_layout" },
};

MODULE_INFO(depends, "kvcommon");

MODULE_ALIAS("usb:v0BFDp0004d*dc*dsc*dp*ic*isc*ip*in*");
MODULE_ALIAS("usb:v0BFDp0002d*dc*dsc*dp*ic*isc*ip*in*");
MODULE_ALIAS("usb:v0BFDp0005d*dc*dsc*dp*ic*isc*ip*in*");
MODULE_ALIAS("usb:v0BFDp0003d*dc*dsc*dp*ic*isc*ip*in*");

MODULE_INFO(srcversion, "B192DE3F023267E5B0714D2");
