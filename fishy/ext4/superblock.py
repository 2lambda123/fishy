import pprint

from .parser import Parser

pp = pprint.PrettyPrinter(indent=4)

BOOT_SECTOR_SIZE = 1024
BLOCK_SIZE = 1024
BYTEORDER = 'little'


class Superblock:

    # Structure of Superblock:
    # name: {offset: hex, size: in bytes, [format: python builtin function (e.g. hex, bin, etc...] }
    structure = {
        "inode_count":        {"offset": 0x0, "size": 4},
        "total_block_count":  {"offset": 0x4, "size": 4},
        "sr_block_count":     {"offset": 0x8, "size": 4},
        "free_block_count":   {"offset": 0xC, "size": 4},
        "free_inode_count":   {"offset": 0x10, "size": 4},
        "first_data_block":   {"offset": 0x14, "size": 4},
        "log_block_size":     {"offset": 0x18, "size": 4},
        "log_cluster_size":   {"offset": 0x1C, "size": 4},
        "blocks_per_group":   {"offset": 0x20, "size": 4},
        "clusters_per_group": {"offset": 0x24, "size": 4},
        "inodes_per_group":   {"offset": 0x28, "size": 4},
        "mount_time":         {"offset": 0x2C, "size": 4},
        "write_time":         {"offset": 0x30, "size": 4},
        "mount_count":        {"offset": 0x34, "size": 2},
        "max_mount_count":    {"offset": 0x36, "size": 2},
        "magic_number":       {"offset": 0x38, "size": 2, "format": "hex"},
        "fs_state":           {"offset": 0x3A, "size": 2},
        "fs_errors":          {"offset": 0x3C, "size": 2},
        "minor_rev_level":    {"offset": 0x3E, "size": 2},
        "last_check":         {"offset": 0x40, "size": 4},
        "check_interval":     {"offset": 0x44, "size": 4},
        "creator_os":         {"offset": 0x48, "size": 4},
        "rev_level":          {"offset": 0x4C, "size": 4},
        "def_res_uid":        {"offset": 0x50, "size": 2},
        "def_res_gid":        {"offset": 0x52, "size": 2},
        "first_nonres_inode": {"offset": 0x54, "size": 4},
        "inode_size":         {"offset": 0x58, "size": 2},
        "block_group_nr":     {"offset": 0x5A, "size": 2},
        "feature_compat":     {"offset": 0x5C, "size": 4, "format": "hex"},
        "feature_incompat":   {"offset": 0x60, "size": 4, "format": "hex"},
        "feature_ro_compat":  {"offset": 0x64, "size": 4, "format": "hex"},
        "volume_uuid":        {"offset": 0x68, "size": 16},
        "volume_name":        {"offset": 0x78, "size": 16, "format": "ascii"},
        "last_mounted_dir":   {"offset": 0x88, "size": 64, "format": "ascii"},
        "algo_usage_bitmap":  {"offset": 0xC8, "size": 4},
        "prealloc_blocks":    {"offset": 0xCC, "size": 1},
        "prealloc_dir_blocks":{"offset": 0xCD, "size": 1},
        "res_gdt_blocks":     {"offset": 0xCE, "size": 2},
        "journal_uuid":       {"offset": 0xD0, "size": 16},
        "journal_inode_nr":   {"offset": 0xE0, "size": 4},
        "journal_dev":        {"offset": 0xE4, "size": 4},
        "last_orphan":        {"offset": 0xE8, "size": 4},
        "hash_seed":          {"offset": 0xEC, "size": 16},
        "def_hash_version":   {"offset": 0xFC, "size": 1, "format": "hex"},
        "jnl_backup_type":    {"offset": 0xFD, "size": 1},
        "group_desc_size":    {"offset": 0xFE, "size": 2},
        "default_mount_opts": {"offset": 0x100, "size": 4, "format": "hex"},
        "first_meta_bg":      {"offset": 0x104, "size": 4},
        "mkfs_time":          {"offset": 0x108, "size": 4},
        "jnl_blocks[17]":     {"offset": 0x10C, "size": 4},
        "blocks_count_hi":    {"offset": 0x150, "size": 4},
        "r_blocks_count_hi":  {"offset": 0x154, "size": 4},
        "free_blocks_count_hi":{"offset": 0x158, "size": 4},
        "min_extra_isize":    {"offset": 0x15C, "size": 2},
        "want_extra_isize":   {"offset": 0x15E, "size": 2},
        "flags":              {"offset": 0x160, "size": 4, "format": "hex"},
        "raid_stride":        {"offset": 0x164, "size": 2},
        "mmp_interval":       {"offset": 0x166, "size": 2},
        "mmp_block":          {"offset": 0x168, "size": 8},
        "raid_stripe_width":  {"offset": 0x170, "size": 4},
        "log_groups_per_flex":{"offset": 0x174, "size": 1},
        "checksum_type":      {"offset": 0x175, "size": 1},
        "reserved_pad":       {"offset": 0x176, "size": 2},
        "kbytes_written":     {"offset": 0x178, "size": 8},
        "snapshot_inum":      {"offset": 0x180, "size": 4},
        "snapshot_id":        {"offset": 0x184, "size": 4},
        "snapshot_r_blocks_count":{"offset": 0x188, "size": 8},
        "snapshot_list":      {"offset": 0x190, "size": 4},
        "error_count":        {"offset": 0x194, "size": 4},
        "first_error_time":   {"offset": 0x198, "size": 4},
        "first_error_ino":    {"offset": 0x19C, "size": 4},
        "first_error_block":  {"offset": 0x1A0, "size": 8},
        "first_error_func[32]":{"offset": 0x1A8, "size": 32},
        "first_error_line":   {"offset": 0x1C8, "size": 4},
        "last_error_time":    {"offset": 0x1CC, "size": 4},
        "last_error_ino":     {"offset": 0x1D0, "size": 4},
        "last_error_line":    {"offset": 0x1D4, "size": 4},
        "last_error_block":   {"offset": 0x1D8, "size": 8},
        "last_error_func[32]":{"offset": 0x1E0, "size": 32},
        "mount_opts[64]":     {"offset": 0x200, "size": 64},
        "usr_quota_inum":     {"offset": 0x240, "size": 4},
        "grp_quota_inum":     {"offset": 0x244, "size": 4},
        "overhead_blocks":    {"offset": 0x248, "size": 4},
        "backup_bgs[2]":      {"offset": 0x24C, "size": 8},
        "encrypt_algos[4]":   {"offset": 0x254, "size": 4},
        "encrypt_pw_salt[16]":{"offset": 0x258, "size": 16},
        "lpf_ino":            {"offset": 0x268, "size": 4},
        "prj_quota_inum":     {"offset": 0x26C, "size": 4},
        "checksum_seed":      {"offset": 0x270, "size": 4},
        "reserved[98]":       {"offset": 0x274, "size": 392},
        "checksum":           {"offset": 0x3FC, "size": 4}
    }

    def __init__(self, filename):
        self.data = self.parse_superblock(filename)

    def parse_superblock(self, filename):
        d = Parser.parse(filename, BOOT_SECTOR_SIZE, BLOCK_SIZE, structure=self.structure)
        return d