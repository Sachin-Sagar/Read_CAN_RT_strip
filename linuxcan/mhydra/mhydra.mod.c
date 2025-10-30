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
	{ 0x49cd25ed, "alloc_workqueue" },
	{ 0x9dcb80d8, "usb_free_urb" },
	{ 0x5facbfa9, "get_usb_root_hub_id" },
	{ 0x4a3ad70e, "wait_for_completion_timeout" },
	{ 0xede295c6, "dlc_dlc_to_bytes_classic" },
	{ 0x27ed581d, "vCanDispatchPrintfEvent" },
	{ 0x487aa866, "vCanAddCardChannel" },
	{ 0x7f02188f, "__msecs_to_jiffies" },
	{ 0x52c5c991, "__kmalloc_noprof" },
	{ 0x63fbdd18, "dlc_dlc_to_bytes_fd" },
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
	{ 0x222dc810, "__put_task_struct" },
	{ 0x4d368c95, "vCanInit" },
	{ 0x4829a47e, "memcpy" },
	{ 0x37a0cba, "kfree" },
	{ 0xb3f7646e, "kthread_should_stop" },
	{ 0xe480c8fe, "softSyncRemoveMember" },
	{ 0xe2964344, "__wake_up" },
	{ 0x96824440, "set_capability_mask" },
	{ 0x34db050b, "_raw_spin_lock_irqsave" },
	{ 0xba8fbd64, "_raw_spin_lock" },
	{ 0xbfaf25a3, "dlc_bytes_to_dlc_fd" },
	{ 0x20bc8744, "wake_up_process" },
	{ 0x92997ed8, "_printk" },
	{ 0x8ddd8aad, "schedule_timeout" },
	{ 0x6fbe60ba, "usb_bulk_msg" },
	{ 0xf0fdf6cb, "__stack_chk_fail" },
	{ 0x296695f, "refcount_warn_saturate" },
	{ 0x2b262ebe, "set_capability_ex_value" },
	{ 0x441d0de9, "__kmalloc_large_noprof" },
	{ 0x4ca11597, "usb_submit_urb" },
	{ 0x7094968f, "vCanInitData" },
	{ 0x1b8169ab, "softSyncHandleTRef" },
	{ 0x118238a0, "vCanCalc_dt" },
	{ 0xbd9f15bf, "usb_free_coherent" },
	{ 0x8c03d20c, "destroy_workqueue" },
	{ 0x220f6eb0, "queue_pop" },
	{ 0xe6cf5658, "queue_wakeup_on_space" },
	{ 0xf74654c, "usb_poison_urb" },
	{ 0x9166fada, "strncpy" },
	{ 0xe7437bee, "set_capability_ex_mask" },
	{ 0xb26930f6, "set_capability_value" },
	{ 0x6adf812a, "ticks_to_64bit_ns" },
	{ 0xd45b3bc6, "kthread_stop" },
	{ 0x1e5b8225, "usb_deregister" },
	{ 0xd35cce70, "_raw_spin_unlock_irqrestore" },
	{ 0xb5f7c829, "vCanDispatchEvent" },
	{ 0x87d7787f, "queue_add_wait_for_space" },
	{ 0xfaa20ff6, "queue_front" },
	{ 0xdcb764ad, "memset" },
	{ 0x2289f050, "ticks_init" },
	{ 0x25974000, "wait_for_completion" },
	{ 0x6782eeca, "queue_push" },
	{ 0x679e43d1, "queue_empty" },
	{ 0xaad8c7d6, "default_wake_function" },
	{ 0x57858536, "vCanRemoveCardChannel" },
	{ 0xcb661d89, "kthread_create_on_node" },
	{ 0x601e6580, "softSyncAddMember" },
	{ 0x3cf8929c, "usb_unlink_urb" },
	{ 0xfd3aeb40, "softSyncLoc2Glob" },
	{ 0x15388bbc, "convert_vcan_to_hydra_cmd" },
	{ 0x5443de3e, "__kmalloc_cache_noprof" },
	{ 0x3c12dfe, "cancel_work_sync" },
	{ 0xa65c6def, "alt_cb_patch_nops" },
	{ 0xa02aea3a, "queue_length" },
	{ 0x88c2dbba, "kv_do_gettimeofday" },
	{ 0xb5b54b34, "_raw_spin_unlock" },
	{ 0x2798d1c, "vCanCleanup" },
	{ 0xfe2fd6f8, "queue_init" },
	{ 0x4fc61f86, "kmalloc_caches" },
	{ 0x752b9cc1, "convert_vcan_ex_to_hydra_cmd" },
	{ 0x2d3385d3, "system_wq" },
	{ 0x474e54d2, "module_layout" },
};

MODULE_INFO(depends, "kvcommon");

MODULE_ALIAS("usb:v0BFDp0100d*dc*dsc*dp*ic*isc*ip*in*");
MODULE_ALIAS("usb:v0BFDp0102d*dc*dsc*dp*ic*isc*ip*in*");
MODULE_ALIAS("usb:v0BFDp0104d*dc*dsc*dp*ic*isc*ip*in*");
MODULE_ALIAS("usb:v0BFDp0105d*dc*dsc*dp*ic*isc*ip*in*");
MODULE_ALIAS("usb:v0BFDp0106d*dc*dsc*dp*ic*isc*ip*in*");
MODULE_ALIAS("usb:v0BFDp0107d*dc*dsc*dp*ic*isc*ip*in*");
MODULE_ALIAS("usb:v0BFDp0108d*dc*dsc*dp*ic*isc*ip*in*");
MODULE_ALIAS("usb:v0BFDp0109d*dc*dsc*dp*ic*isc*ip*in*");
MODULE_ALIAS("usb:v0BFDp010Ad*dc*dsc*dp*ic*isc*ip*in*");
MODULE_ALIAS("usb:v0BFDp010Bd*dc*dsc*dp*ic*isc*ip*in*");
MODULE_ALIAS("usb:v0BFDp010Cd*dc*dsc*dp*ic*isc*ip*in*");
MODULE_ALIAS("usb:v0BFDp010Dd*dc*dsc*dp*ic*isc*ip*in*");
MODULE_ALIAS("usb:v0BFDp010Ed*dc*dsc*dp*ic*isc*ip*in*");
MODULE_ALIAS("usb:v0BFDp010Fd*dc*dsc*dp*ic*isc*ip*in*");
MODULE_ALIAS("usb:v0BFDp0110d*dc*dsc*dp*ic*isc*ip*in*");
MODULE_ALIAS("usb:v0BFDp0111d*dc*dsc*dp*ic*isc*ip*in*");
MODULE_ALIAS("usb:v0BFDp0112d*dc*dsc*dp*ic*isc*ip*in*");
MODULE_ALIAS("usb:v0BFDp0113d*dc*dsc*dp*ic*isc*ip*in*");
MODULE_ALIAS("usb:v0BFDp0114d*dc*dsc*dp*ic*isc*ip*in*");
MODULE_ALIAS("usb:v0BFDp0115d*dc*dsc*dp*ic*isc*ip*in*");
MODULE_ALIAS("usb:v0BFDp0116d*dc*dsc*dp*ic*isc*ip*in*");
MODULE_ALIAS("usb:v0BFDp0117d*dc*dsc*dp*ic*isc*ip*in*");
MODULE_ALIAS("usb:v0BFDp0118d*dc*dsc*dp*ic*isc*ip*in*");
MODULE_ALIAS("usb:v0BFDp0119d*dc*dsc*dp*ic*isc*ip*in*");
MODULE_ALIAS("usb:v0BFDp011Ad*dc*dsc*dp*ic*isc*ip*in*");
MODULE_ALIAS("usb:v0BFDp011Bd*dc*dsc*dp*ic*isc*ip*in*");
MODULE_ALIAS("usb:v0BFDp011Cd*dc*dsc*dp*ic*isc*ip*in*");
MODULE_ALIAS("usb:v0BFDp011Dd*dc*dsc*dp*ic*isc*ip*in*");

MODULE_INFO(srcversion, "2617E9C9553DD53B75640F0");
