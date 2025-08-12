# Softcore 64MHz single core OpenPOWER ppc64le with 6.xx linux kernel and minimalistic rootfs
Working walk-through: https://codeconstruct.com.au/docs/microwatt-orangecrab/

At this point you have a 6.xx linux kernel booting serial login/terminal and you can mount micro SD cards and read/write files.

Next step to chroot into Debian with rootfs on a microSD card. 
# Debian chroot

Generating a debootstrap rootfs (the qemu part did not work): https://wiki.debian.org/ppc64el/Installation

Running the second stage on the orange crab does no work either since the linux kernels the chrooted filesystem is built with different kernel headers/API. 

Work in progress ...
