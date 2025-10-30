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
	{ 0x95b9dbf9, "pci_enable_device" },
	{ 0x487aa866, "vCanAddCardChannel" },
	{ 0x52c5c991, "__kmalloc_noprof" },
	{ 0x3fd7c8cf, "pci_iomap" },
	{ 0xc5b6f236, "queue_work_on" },
	{ 0x30372d96, "queue_release" },
	{ 0xc31dd9f6, "vCanFlushSendBuffer" },
	{ 0x1967e59c, "__pci_register_driver" },
	{ 0x4d368c95, "vCanInit" },
	{ 0x4b6bbff7, "pci_request_regions" },
	{ 0x4829a47e, "memcpy" },
	{ 0x37a0cba, "kfree" },
	{ 0x1ad8797b, "vCanGetCardInfo" },
	{ 0xe2964344, "__wake_up" },
	{ 0x34db050b, "_raw_spin_lock_irqsave" },
	{ 0xba8fbd64, "_raw_spin_lock" },
	{ 0x7792cd56, "pci_unregister_driver" },
	{ 0x92997ed8, "_printk" },
	{ 0xfd06f019, "packed_EAN_to_BCD_with_csum" },
	{ 0x8ddd8aad, "schedule_timeout" },
	{ 0xf0fdf6cb, "__stack_chk_fail" },
	{ 0x52497ba5, "vCanGetCardInfo2" },
	{ 0x441d0de9, "__kmalloc_large_noprof" },
	{ 0x7094968f, "vCanInitData" },
	{ 0x92d5838e, "request_threaded_irq" },
	{ 0x220f6eb0, "queue_pop" },
	{ 0xe6cf5658, "queue_wakeup_on_space" },
	{ 0xb26930f6, "set_capability_value" },
	{ 0x449ad0a7, "memcmp" },
	{ 0xd35cce70, "_raw_spin_unlock_irqrestore" },
	{ 0x70796a17, "pci_iounmap" },
	{ 0xb5f7c829, "vCanDispatchEvent" },
	{ 0xfaa20ff6, "queue_front" },
	{ 0xdcb764ad, "memset" },
	{ 0x57858536, "vCanRemoveCardChannel" },
	{ 0x3c3ff9fd, "sprintf" },
	{ 0x390a3705, "vCanTime" },
	{ 0xe1bb96dd, "pci_release_regions" },
	{ 0xeae3dfd6, "__const_udelay" },
	{ 0x5443de3e, "__kmalloc_cache_noprof" },
	{ 0xc43d6f7b, "pci_disable_device" },
	{ 0xa65c6def, "alt_cb_patch_nops" },
	{ 0xb5b54b34, "_raw_spin_unlock" },
	{ 0x2798d1c, "vCanCleanup" },
	{ 0x4fc61f86, "kmalloc_caches" },
	{ 0x2d3385d3, "system_wq" },
	{ 0x474e54d2, "module_layout" },
};

MODULE_INFO(depends, "kvcommon");

MODULE_ALIAS("pci:v000010E8d00008406sv*sd*bc*sc*i*");
MODULE_ALIAS("pci:v00001A07d00000008sv*sd*bc*sc*i*");

MODULE_INFO(srcversion, "8E07C8A78210140911253ED");
