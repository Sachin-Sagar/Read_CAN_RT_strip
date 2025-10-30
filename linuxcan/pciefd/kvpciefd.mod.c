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
	{ 0xc1514a3b, "free_irq" },
	{ 0xc31db0ce, "is_vmalloc_addr" },
	{ 0x4a3ad70e, "wait_for_completion_timeout" },
	{ 0x95b9dbf9, "pci_enable_device" },
	{ 0x487aa866, "vCanAddCardChannel" },
	{ 0x52c5c991, "__kmalloc_noprof" },
	{ 0x3fd7c8cf, "pci_iomap" },
	{ 0x9af41181, "pci_alloc_irq_vectors" },
	{ 0xa6257a2f, "complete" },
	{ 0xc5b6f236, "queue_work_on" },
	{ 0x30372d96, "queue_release" },
	{ 0x55555880, "queue_reinit" },
	{ 0x608741b5, "__init_swait_queue_head" },
	{ 0x505a3642, "dma_unmap_page_attrs" },
	{ 0x1967e59c, "__pci_register_driver" },
	{ 0x4d368c95, "vCanInit" },
	{ 0x4b6bbff7, "pci_request_regions" },
	{ 0x4829a47e, "memcpy" },
	{ 0x37a0cba, "kfree" },
	{ 0x1ad8797b, "vCanGetCardInfo" },
	{ 0x206ebad6, "queue_irq_lock" },
	{ 0xc3055d20, "usleep_range_state" },
	{ 0xe2964344, "__wake_up" },
	{ 0xd56fa8f1, "pci_irq_vector" },
	{ 0x96824440, "set_capability_mask" },
	{ 0x34db050b, "_raw_spin_lock_irqsave" },
	{ 0xba8fbd64, "_raw_spin_lock" },
	{ 0x7792cd56, "pci_unregister_driver" },
	{ 0xf4348bfa, "dev_driver_string" },
	{ 0xdf2ebb87, "_raw_read_unlock_irqrestore" },
	{ 0x708c6123, "dma_map_page_attrs" },
	{ 0x6b2dc060, "dump_stack" },
	{ 0x92997ed8, "_printk" },
	{ 0x8427cc7b, "_raw_spin_lock_irq" },
	{ 0x8ddd8aad, "schedule_timeout" },
	{ 0xf0fdf6cb, "__stack_chk_fail" },
	{ 0x52497ba5, "vCanGetCardInfo2" },
	{ 0x2b262ebe, "set_capability_ex_value" },
	{ 0x441d0de9, "__kmalloc_large_noprof" },
	{ 0xa916b694, "strnlen" },
	{ 0xb1342cdb, "_raw_read_lock_irqsave" },
	{ 0x7094968f, "vCanInitData" },
	{ 0x70b38102, "pci_clear_master" },
	{ 0x4d7a00d5, "__dma_sync_single_for_cpu" },
	{ 0x92d5838e, "request_threaded_irq" },
	{ 0x24d273d1, "add_timer" },
	{ 0x235ea4c1, "calculateCRC32" },
	{ 0x69dd3b5b, "crc32_le" },
	{ 0x220f6eb0, "queue_pop" },
	{ 0x4b750f53, "_raw_spin_unlock_irq" },
	{ 0xe6cf5658, "queue_wakeup_on_space" },
	{ 0x9166fada, "strncpy" },
	{ 0xe7437bee, "set_capability_ex_mask" },
	{ 0xb26930f6, "set_capability_value" },
	{ 0x449ad0a7, "memcmp" },
	{ 0xd35cce70, "_raw_spin_unlock_irqrestore" },
	{ 0x70796a17, "pci_iounmap" },
	{ 0xb5f7c829, "vCanDispatchEvent" },
	{ 0xfaa20ff6, "queue_front" },
	{ 0xdcb764ad, "memset" },
	{ 0x7cf55e07, "pci_set_master" },
	{ 0x25974000, "wait_for_completion" },
	{ 0x679e43d1, "queue_empty" },
	{ 0x57858536, "vCanRemoveCardChannel" },
	{ 0xeb078aee, "_raw_write_unlock_irqrestore" },
	{ 0x15ba50a6, "jiffies" },
	{ 0x3c3ff9fd, "sprintf" },
	{ 0xc6f46339, "init_timer_key" },
	{ 0xe1bb96dd, "pci_release_regions" },
	{ 0xa77117cf, "__dma_sync_single_for_device" },
	{ 0x5443de3e, "__kmalloc_cache_noprof" },
	{ 0x56470118, "__warn_printk" },
	{ 0xc43d6f7b, "pci_disable_device" },
	{ 0xa65c6def, "alt_cb_patch_nops" },
	{ 0xf1d15c7b, "dma_set_mask" },
	{ 0x5021bd81, "_raw_write_lock_irqsave" },
	{ 0xb5b54b34, "_raw_spin_unlock" },
	{ 0x3b1b010f, "pci_free_irq_vectors" },
	{ 0x2798d1c, "vCanCleanup" },
	{ 0xf9a482f9, "msleep" },
	{ 0x4fc61f86, "kmalloc_caches" },
	{ 0x2d3385d3, "system_wq" },
	{ 0x188ea314, "jiffies_to_timespec64" },
	{ 0x474e54d2, "module_layout" },
};

MODULE_INFO(depends, "kvcommon");

MODULE_ALIAS("pci:v00001A07d0000000Dsv*sd*bc*sc*i*");
MODULE_ALIAS("pci:v00001A07d0000000Esv*sd*bc*sc*i*");
MODULE_ALIAS("pci:v00001A07d0000000Fsv*sd*bc*sc*i*");
MODULE_ALIAS("pci:v00001A07d00000010sv*sd*bc*sc*i*");
MODULE_ALIAS("pci:v00001A07d00000011sv*sd*bc*sc*i*");
MODULE_ALIAS("pci:v00001A07d00000012sv*sd*bc*sc*i*");
MODULE_ALIAS("pci:v00001A07d00000013sv*sd*bc*sc*i*");
MODULE_ALIAS("pci:v00001A07d00000014sv*sd*bc*sc*i*");
MODULE_ALIAS("pci:v00001A07d00000015sv*sd*bc*sc*i*");
MODULE_ALIAS("pci:v00001A07d00000016sv*sd*bc*sc*i*");
MODULE_ALIAS("pci:v00001A07d00000017sv*sd*bc*sc*i*");
MODULE_ALIAS("pci:v00001A07d00000018sv*sd*bc*sc*i*");
MODULE_ALIAS("pci:v00001A07d00000019sv*sd*bc*sc*i*");

MODULE_INFO(srcversion, "415630F54B0046A462C3147");
