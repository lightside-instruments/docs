# Introduction
One way to control a stepper motor driving the hands of a clock is with a Raspberry Pi running LinuxCNC.

On http://linuxcnc.org/downloads/ there is a link `LinuxCNC 2.9.2 Raspberry Pi 5 OS based on Debian Bookworm Raspberry Pi 5 Uspace compatible with Mesa Ethernet boards. Note that SPI is not currently supported with the Pi5.`

So we downloaded https://www.linuxcnc.org/iso/rpi-5-debian-bookworm-6.1.61-rt15-arm64-ext4-2023-11-17-1520.img.xz extracted and copied to a micro SD card. Booted and with DHCP allocated IP on the Ethernet connection SSH-ed with the user:cnc pass:cnc credentials.

`ssh -X cnc@10.13.37.104`

If you are new to LinuxCNC you should probably read some documentation or find someone with experience to kick start you.

You can run `linuxcnc` from the command line select a suitable example with the GUI and then edit the *.ini configuration copied to ~/linuxcnc

However since the goal is to make headless installation that just moves the hand of the clock we will use a single command line that starts the server and uses a crontab script executed every minute and advances the clock hand with a gcode command e.g. "G0 X100".

Only one configuration file had to be changed to specify Raspberry Pi GPIOs instead of parallel port pins - check out linuxcnc/configs/by_interface.parport.stepper/standard_pinout.hal the original version of this file is kept in linuxcnc/before.

The example file named stepper_mm.ini  was copied to stepper_mm_sh.ini in order to start linuxcnc without GUI.

We made some changes so that GPIOs named PIN11 and PIN36 (check your gpiod pin names with gpioinfo) (edit the files in ./linuxcnc)

To do this we decided to start the linuxcnc command from /etc/rc.local . And yes there are some special parameters that specify that no GUI is needed and instead a linucncrsh tool with telnet/netcat port interface will be used as cli:

```
...
su cnc -c "linuxcnc /home/cnc/linuxcnc/configs/by_interface.parport.stepper/stepper_mm_sh.ini"
...
```



Create a command file /home/cnc/cmd.txt:


```
hello EMC batch-command-script 1.0
set enable EMCTOO
set verbose on
set estop off
set machine on
set home 0
set home 1
set home 2
set mode mdi
set mdi g91
set mdi g0x100
quit
```


And added a crontab entry:

```
...
* * * * * nc  -N -q 20 localhost 5007 < cmd.txt > /tmp/log.txt
...
```


The ./linuxcnc contains a copy of the working /home/cnc/linuxcnc directory. Copy this without changes and your clock will work after a restart.
