Evaluation
==========

This section summarizes some evaluations we made for the different implemented
hiding techniques.

FileSlack
---------

* **Gained capacity**: Depending on the configured block and cluster size as
  well as the size of the original file, that is used to hide data, this hiding
  technique can store *(cluster_size - block_size) x stored_files*. Though the
  gained capacity is very high.
* **Detection probability**: A check with fsck.fat neither detected the hidden files,
  nor showed any other suspicious output.  Same for chkdsk on NTFS.
* **Stability**: Low. If the original file changes in size, the hidden data
  might be overwritten by further writes. So, this technique should be used
  preferably with non-changing filesystems or files that don't change.

MFTSlack
--------

* **Gained capacity**: Depending on the allocated MFT entry size as well as the
  actual size of data in each entry, that is used to hide data, this hiding
  technique can store *(allocated_size - actual_size) - 2 bytes per fixup value
  in slack*.  Though the gained capacity is high (~300B per MFT entry using our
  testfs-ntfs-stable2.dd image with a MFT entry size of 1024B).
* **Detection probability**: With the --domirr option a check with chkdsk neither
  detected the hidden files, nor showed any other suspicious output. Without
  chkdsk detects an error in the $MFTMirr.
* **Stability**: Low. If attributes in the original mft entry change, the
  hidden data might be overwritten. So, this technique should preferably used
  with non-changing filesystems.

Bad Cluster Allocation
----------------------

* **Gained capacity**: As bad cluster allocation uses whole clusters to store
  files, there is no limit in storing data, except the *count of clusters* that
  are available on the filesystem.
* **Detection probability**: fsck.fat detects all clusters that are marked as bad, as
  nowadays filesystems don't use this flag anymore.
* **Stability**: High. This technique uses legit filesystem capabilities to
  mark a cluster as unusable. So, data stored in bad clusters will stay there
  without complications.

Additional Cluster Allocation
-----------------------------

* **Gained capacity**: As additional cluster allocation uses whole clusters to
  store files, there is no limit in storing data, except the *count of
  clusters* that are available on the filesystem.
* **Detection probability**: fsck.fat detects cluster chains, that are longer than the
  size value of directory entries. So this check would show, that something
  suspicious is going on there.
* **Stability**: Low. If the original file changes in size, the hidden data
  will be overwritten or partially truncated. So, this technique should be used
  preferably with non-changing filesystems or files that don't change.

* **Gained capacity**: 
* **Detection probability**: 
* **Stability**: High Medium Low
  
Reserved Group Descriptor Tables
--------------------------------

* **Gained capacity**: This hiding technique can hide up to `reseved_gdt_blocks * block_groups * block_size` bytes.
* **Detection probability**: High. Detection tools as well as the bare eye will detect written data here.
* **Stability**: Medium. As long as the filesystem is not expanded, your files are save.

File Slack
----------

* **Gained capacity**: WIP
* **Detection probability**: WIP
* **Stability**: High Medium Low WIP

Superblock Slack
----------------

* **Gained capacity**: `block_size - 2048 bytes + superblock_copies * (block_size - 1024 bytes)`
* **Detection probability**: High. Detection tools as well as the bare eye will detect written data here.
* **Stability**: High. This will not get overwritten.

Inode
-----
osd2
****

* **Gained capacity**: `number of inodes * 2 bytes`
* **Detection probability**: fsck notices wrong checksums, therefore it is quite easy to detect.
* **Stability**: High. These fields are unused.

obso_faddr
**********

* **Gained capacity**: `number of inodes * 4 bytes`
* **Detection probability**: fsck notices wrong checksums, therefore it is quite easy to detect.
* **Stability**: High. These fields are obsolete, therefore unused.