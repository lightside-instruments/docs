#Debian XPS-15 hybrid
apt install nvidia-detect
nvidia-detect
apt-install nvidia-driver
apt install linux-headers-$(uname -r)
update-initramfs -u
reboot
