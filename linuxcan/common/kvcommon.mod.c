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

KSYMTAB_FUNC(vCanTime, "", "");
KSYMTAB_FUNC(kv_do_gettimeofday, "", "");
KSYMTAB_FUNC(vCanCalc_dt, "", "");
KSYMTAB_FUNC(vCanSupportsBusParamsTq, "", "");
KSYMTAB_FUNC(vCanFlushSendBuffer, "", "");
KSYMTAB_FUNC(vCanGetCardInfo, "", "");
KSYMTAB_FUNC(vCanGetCardInfo2, "", "");
KSYMTAB_FUNC(vCanAddCardChannel, "", "");
KSYMTAB_FUNC(vCanRemoveCardChannel, "", "");
KSYMTAB_FUNC(vCanDispatchEvent, "", "");
KSYMTAB_FUNC(vCanDispatchPrintfEvent, "", "");
KSYMTAB_FUNC(vCanInitData, "", "");
KSYMTAB_FUNC(vCanInit, "", "");
KSYMTAB_FUNC(vCanCleanup, "", "");
KSYMTAB_FUNC(queue_reinit, "", "");
KSYMTAB_FUNC(queue_init, "", "");
KSYMTAB_FUNC(queue_irq_lock, "", "");
KSYMTAB_FUNC(queue_length, "", "");
KSYMTAB_FUNC(queue_empty, "", "");
KSYMTAB_FUNC(queue_back, "", "");
KSYMTAB_FUNC(queue_push, "", "");
KSYMTAB_FUNC(queue_front, "", "");
KSYMTAB_FUNC(queue_pop, "", "");
KSYMTAB_FUNC(queue_release, "", "");
KSYMTAB_FUNC(queue_add_wait_for_space, "", "");
KSYMTAB_FUNC(queue_remove_wait_for_space, "", "");
KSYMTAB_FUNC(queue_wakeup_on_space, "", "");
KSYMTAB_FUNC(calculateCRC32, "", "");
KSYMTAB_FUNC(packed_EAN_to_BCD_with_csum, "", "");
KSYMTAB_FUNC(get_usb_root_hub_id, "", "");
KSYMTAB_FUNC(softSyncLoc2Glob, "", "");
KSYMTAB_FUNC(softSyncHandleTRef, "", "");
KSYMTAB_FUNC(softSyncAddMember, "", "");
KSYMTAB_FUNC(softSyncRemoveMember, "", "");
KSYMTAB_FUNC(softSyncGetTRefList, "", "");
KSYMTAB_FUNC(set_capability_value, "", "");
KSYMTAB_FUNC(set_capability_mask, "", "");
KSYMTAB_FUNC(convert_vcan_to_hydra_cmd, "", "");
KSYMTAB_FUNC(card_has_capability, "", "");
KSYMTAB_FUNC(card_has_capability_ex, "", "");
KSYMTAB_FUNC(set_capability_ex_value, "", "");
KSYMTAB_FUNC(set_capability_ex_mask, "", "");
KSYMTAB_FUNC(convert_vcan_ex_to_hydra_cmd, "", "");
KSYMTAB_FUNC(dlc_bytes_to_dlc_fd, "", "");
KSYMTAB_FUNC(dlc_dlc_to_bytes_fd, "", "");
KSYMTAB_FUNC(dlc_is_dlc_ok, "", "");
KSYMTAB_FUNC(dlc_dlc_to_bytes_classic, "", "");
KSYMTAB_FUNC(ticks_init, "", "");
KSYMTAB_FUNC(ticks_to_64bit_ns, "", "");

SYMBOL_CRC(vCanTime, 0x390a3705, "");
SYMBOL_CRC(kv_do_gettimeofday, 0x88c2dbba, "");
SYMBOL_CRC(vCanCalc_dt, 0x118238a0, "");
SYMBOL_CRC(vCanSupportsBusParamsTq, 0x27c98135, "");
SYMBOL_CRC(vCanFlushSendBuffer, 0xc31dd9f6, "");
SYMBOL_CRC(vCanGetCardInfo, 0x1ad8797b, "");
SYMBOL_CRC(vCanGetCardInfo2, 0x52497ba5, "");
SYMBOL_CRC(vCanAddCardChannel, 0x487aa866, "");
SYMBOL_CRC(vCanRemoveCardChannel, 0x57858536, "");
SYMBOL_CRC(vCanDispatchEvent, 0xb5f7c829, "");
SYMBOL_CRC(vCanDispatchPrintfEvent, 0x27ed581d, "");
SYMBOL_CRC(vCanInitData, 0x7094968f, "");
SYMBOL_CRC(vCanInit, 0x4d368c95, "");
SYMBOL_CRC(vCanCleanup, 0x02798d1c, "");
SYMBOL_CRC(queue_reinit, 0x55555880, "");
SYMBOL_CRC(queue_init, 0xfe2fd6f8, "");
SYMBOL_CRC(queue_irq_lock, 0x206ebad6, "");
SYMBOL_CRC(queue_length, 0xa02aea3a, "");
SYMBOL_CRC(queue_empty, 0x679e43d1, "");
SYMBOL_CRC(queue_back, 0x244ab863, "");
SYMBOL_CRC(queue_push, 0x6782eeca, "");
SYMBOL_CRC(queue_front, 0xfaa20ff6, "");
SYMBOL_CRC(queue_pop, 0x220f6eb0, "");
SYMBOL_CRC(queue_release, 0x30372d96, "");
SYMBOL_CRC(queue_add_wait_for_space, 0x87d7787f, "");
SYMBOL_CRC(queue_remove_wait_for_space, 0x10fa71db, "");
SYMBOL_CRC(queue_wakeup_on_space, 0xe6cf5658, "");
SYMBOL_CRC(calculateCRC32, 0x235ea4c1, "");
SYMBOL_CRC(packed_EAN_to_BCD_with_csum, 0xfd06f019, "");
SYMBOL_CRC(get_usb_root_hub_id, 0x5facbfa9, "");
SYMBOL_CRC(softSyncLoc2Glob, 0xfd3aeb40, "");
SYMBOL_CRC(softSyncHandleTRef, 0x1b8169ab, "");
SYMBOL_CRC(softSyncAddMember, 0x601e6580, "");
SYMBOL_CRC(softSyncRemoveMember, 0xe480c8fe, "");
SYMBOL_CRC(softSyncGetTRefList, 0xc4b8281f, "");
SYMBOL_CRC(set_capability_value, 0xb26930f6, "");
SYMBOL_CRC(set_capability_mask, 0x96824440, "");
SYMBOL_CRC(convert_vcan_to_hydra_cmd, 0x15388bbc, "");
SYMBOL_CRC(card_has_capability, 0x7800868a, "");
SYMBOL_CRC(card_has_capability_ex, 0x5f312a97, "");
SYMBOL_CRC(set_capability_ex_value, 0x2b262ebe, "");
SYMBOL_CRC(set_capability_ex_mask, 0xe7437bee, "");
SYMBOL_CRC(convert_vcan_ex_to_hydra_cmd, 0x752b9cc1, "");
SYMBOL_CRC(dlc_bytes_to_dlc_fd, 0xbfaf25a3, "");
SYMBOL_CRC(dlc_dlc_to_bytes_fd, 0x63fbdd18, "");
SYMBOL_CRC(dlc_is_dlc_ok, 0xab1ad228, "");
SYMBOL_CRC(dlc_dlc_to_bytes_classic, 0xede295c6, "");
SYMBOL_CRC(ticks_init, 0x2289f050, "");
SYMBOL_CRC(ticks_to_64bit_ns, 0x6adf812a, "");

static const struct modversion_info ____versions[]
__used __section("__versions") = {
	{ 0xe3ec2f2b, "alloc_chrdev_region" },
	{ 0x49cd25ed, "alloc_workqueue" },
	{ 0x7f02188f, "__msecs_to_jiffies" },
	{ 0x52c5c991, "__kmalloc_noprof" },
	{ 0xa6257a2f, "complete" },
	{ 0xc5b6f236, "queue_work_on" },
	{ 0x608741b5, "__init_swait_queue_head" },
	{ 0x92540fbf, "finish_wait" },
	{ 0x6775d5d3, "class_destroy" },
	{ 0x4829a47e, "memcpy" },
	{ 0x37a0cba, "kfree" },
	{ 0x4afb2238, "add_wait_queue" },
	{ 0x8c26d495, "prepare_to_wait_event" },
	{ 0xe2964344, "__wake_up" },
	{ 0x34db050b, "_raw_spin_lock_irqsave" },
	{ 0xba8fbd64, "_raw_spin_lock" },
	{ 0x92997ed8, "_printk" },
	{ 0x1000e51, "schedule" },
	{ 0x8ddd8aad, "schedule_timeout" },
	{ 0xf0fdf6cb, "__stack_chk_fail" },
	{ 0xe46021ca, "_raw_spin_unlock_bh" },
	{ 0x6cbbfc54, "__arch_copy_to_user" },
	{ 0x441d0de9, "__kmalloc_large_noprof" },
	{ 0x7682ba4e, "__copy_overflow" },
	{ 0x3a6d85d3, "cdev_add" },
	{ 0xfe487975, "init_wait_entry" },
	{ 0x2c9a4c10, "device_create" },
	{ 0x59c02473, "class_create" },
	{ 0x8c03d20c, "destroy_workqueue" },
	{ 0x4dfa8d4b, "mutex_lock" },
	{ 0x9166fada, "strncpy" },
	{ 0x9ec6ca96, "ktime_get_real_ts64" },
	{ 0xcefb0c9f, "__mutex_init" },
	{ 0xd35cce70, "_raw_spin_unlock_irqrestore" },
	{ 0xdcb764ad, "memset" },
	{ 0x25974000, "wait_for_completion" },
	{ 0xd9a5ea54, "__init_waitqueue_head" },
	{ 0xfb384d37, "kasprintf" },
	{ 0x6091b333, "unregister_chrdev_region" },
	{ 0x3213f038, "mutex_unlock" },
	{ 0x8b970f46, "device_destroy" },
	{ 0x5443de3e, "__kmalloc_cache_noprof" },
	{ 0xc3690fc, "_raw_spin_lock_bh" },
	{ 0x12a4e128, "__arch_copy_from_user" },
	{ 0x37110088, "remove_wait_queue" },
	{ 0xa65c6def, "alt_cb_patch_nops" },
	{ 0xb5b54b34, "_raw_spin_unlock" },
	{ 0xa01f13a6, "cdev_init" },
	{ 0x4fc61f86, "kmalloc_caches" },
	{ 0x27271c6b, "cdev_del" },
	{ 0x474e54d2, "module_layout" },
};

MODULE_INFO(depends, "");


MODULE_INFO(srcversion, "59F9BB295A19C30C5247EE6");
