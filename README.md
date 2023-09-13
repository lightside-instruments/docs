# Wireless LAN/GPIB gateway with open-source hardware

![Title](title.png)

This walk-through will install linux-gpib, python-vxi11-server and tcpip2instr on a Raspberry Pi with gpib4pi shield.


# Introduction

GPIB (IEEE-488) is the most common interface for communication with test and measurement equipment. If you own oscilloscope, power supply, signal generator, spectrum analyzer or any other test and measurement device from a decent manufacturer produced in the last 40 years it probably has a GPIB interface.

National Instruments and Keysight (former HP) produce the most common GPIB adapters. They are using proprietary hardware.

There are standard protocols for accessing GPIB devices over network. The devices that implement them are called LAN/GPIB gateways.

Here we describe a solution based on open-source hardware and software components. A solution we (Lightside Instruments AS) use and maintain as a tool used in our professional test and verification tasks.

The proprietary LAN/GPIB gateway E5810B is one of the popular proprietary alternatives.

If you do not have one of those or you just want to use open-source hardware and software in your project we wrote this article. You can build your own using:

* open-source hardware - gpib4pi adapter (OSHWA approved design: NO000003 can be purchased from Amazon link)
* Raspberry Pi (Zero, 2-4)
* open-source software - linux-gpib, python-vxi11-server, tcpip2instr

#Installation
You should start by connecting and powering the board and installing the linux-gpib driver and user space libraries. We maintain a dedicated walk-through here

At this point your GPIB adapter and linux-gpib stack should be operational and what is left is installing the server side protocol specific software:

```
sudo apt-get install rpcbind
sudo systemctl start rpcbind
sudo systemctl enable rpcbind
git clone https://github.com/coburnw/python-vxi11-server.git
git clone https://git.loetlabor-jena.de/thasti/tcpip2instr.git
cd tcpip2instr
```
Running the server:
```
root@raspberrypi:~/tcpip2instr# python tcpip2instr.py
Press Ctrl+C to exit
INFO:__main__:starting time_device
INFO:vxi11_server.instrument_server:abortServer started...
INFO:vxi11_server.rpc:registering (395183, 1, 6, 41681) on ('0.0.0.0', 41681)
INFO:vxi11_server.instrument_server:coreServer started...
```

At this point your server is listening for incoming connections from clients (test programs or controllers like LabView):

#Testing

Python client script example based on python-vxi11 is added.

You need to install the python3-pyvisa package:

```
user@pc:~$ sudo apt-get install python3-pyvisa
```
Listing of vxi11-test.py (make sure you replace the resource name with the correct IP and correct GPIB address):

```
import vxi11
instr = vxi11.vxi11.Instrument("TCPIP::192.168.14.20::gpib,2::INSTR")
instr.write("*IDN?")
print(instr.read())
```

Running:
```
user@pc:~/vxi11-test$ sudo apt-get install python3-pyvisa
user@pc:~/vxi11-test$ python3 vxi11-test.py
Agilent Technologies,E3647A,0,1.7-5.0-1.0
```

You can also use the gateway from popular instrument controllers like LabView.

In order to start the server at every reboot you need to edit your /etc/rc.local file:

```
#!/bin/sh -e
modprobe gpib_bitbang
gpib_config
sleep 1
cd /root/tcpip2instr
python3 tcpip2instr.py 1>/var/log/tcpip2instr.stdout 2>/var/log/tcpip2instr.stderr &
```

Now you can reboot the device and get a persistent connectivity to your GPIB devices.
