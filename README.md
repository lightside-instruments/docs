# The ice4pi - ice40 Raspberry Pi hat
Use yosys to develop functionality with iCE40HX-1K FPGA for your Pi... on your Pi.
![Title](title.gif)

# Story

The ice4pi board is open-source hardware hat for Raspberry Pi in the Pi Zero form factor and can be used with Raspberry Pi 2-4 and Zero - (OSHWA UID: NO000002).

All Raspberry Pi GPIOs + 8 PMOD IOs + 5 LEDs are connected to the iCE40HX-1K FPGA.

Here is a link to the schematics.

You can use the yosys toolchain to synthesize logic from Verilog and reload the board with image stored in a SPI flash while the Raspberry Pi is running. Simple projects like the examples take 10 seconds to synthesize and reload the FPGA on Raspberry Pi 4B, 50 seconds to synthesize and reload on a Raspberry Pi Zero.

You can buy the board on Amazon https://www.amazon.com/dp/B0BY32HH4G

Despite its brevity this article is complete and you will be able to synthesize and load the 4 basic examples:

    Example 1: Blinking LEDs (the default rot.v example part of iCEstick)
    Example 2: I2C slave (toggle LEDs and read PMOD pins over I2C)
    Example 3: SPI slave (Send data back and forth with spi-pipe)
    Example 4: Using the PLL (12 MHz to 120 MHz clock conversion)

Make sure the SPI interface is enabled since it will be used to program the device.

Use:

```
sudo raspi-config
```

"Interface options -> SPI"

Example 2 will need the I2C interface so you can enable it as well.

"Interface options -> I2C"

You need to restart after that.

Getting Started

Assuming you have Raspberry Pi up and running with a connected shield. Clone the ice4pi repository:

git clone https://github.com/lightside-instruments/ice4pi.git

The repository contains the KiCAD project of the board and a simple example in Verilog that toggles the LEDs.

# Example 1 - Blinking LEDs

Lets start with building and loading the rot.v Verilog example part of the ice4pi project:

```
cd ice4pi/example
```

1. Install all necessary packages to synthesize rot.v and build bit image (rot.bin) for the ice4pi:

```
sudo apt-get -y install yosys fpga-icestorm arachne-pnr flashrom
```

2. Synthesize (rot.bin) :

```
make
```

3. Load the rot.bin file to the shield:
```
sudo make load
```

LEDs are blinking! You can modify the rot.v code and rebuild/reload - make ; sudo make load

# Example 2 - I2C slave

Build your own I2C slave that you can access from the Raspberry Pi command line and... toggle the LEDs and read the PMOD connector signals.

Before you begin make sure I2C interface is enabled:
```
sudo raspi-config
```

"Interface options -> I2C"

You need to restart after that.

```
git clone https://github.com/lightside-instruments/ice4pi-example-i2cslave.git
cd ice4pi-example-i2cslave
make
sudo make load
```

Validate new i2c device is accessible:
```
sudo apt-get install i2c-tools
pi@raspberrypi:~ $ i2cdetect -r -y 1
0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
00:          -- -- -- -- -- -- -- -- -- -- -- -- --
10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
30: -- -- -- -- -- -- -- -- -- -- -- -- 3c -- -- --
40: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
70: -- -- -- -- -- UU -- --
```
Writing 0x03 to address 0x00 of the device:
```
pi@raspberrypi:~ $ i2cset -y 1 0x3c 0x00 0x03 b
```
Two diodes light up!

Reading the level on the PMOD pins:

# Pin IO4 (indexation 1-8) connected to logical zero (0V)
```
pi@raspberrypi:~/ice4pi-i2cslave$ i2cget -y 1 0x3c 0x04 b
0x00
```
# Connected to logical one (e.g. 3.3V)

pi@raspberrypi:~/ice4pi-i2cslave$ i2cget -y 1 0x3c 0x04 b
0x20

Example 3 - SPI slave

This example will build Verilog SPI slave device that will receive and send back all SPI data sent by the Raspberry Pi host back to it.

Here is the code: top.v
```
git clone https://github.com/lightside-instruments/ice4pi-example-i2cslave.git -b ice4pi-example-spi-slave ice4pi-example-spi-slave
cd ice4pi-example-spi-slave
make
sudo make load
```
In order to demonstrate the functionality first install the spi-pipe tool if you have not done that yet:
```
sudo apt-get install spi-tools
```
Validate the spi loopback:
```
echo -n 0123456789ABCDEF | spi-pipe -d /dev/spidev0.1 -s 10000000
```
You should get back
```
F0123456789ABCDE
```
(F may be NUL if this is your first call)

# Example 4 - Using the PLL

The ICE40 FPGA has a single PLL that can be used to synthesize clock with frequency that is different then the 12MHz input clock or any other external clock available.

This example instantiates the PLL so that it generate 120MHz. It instantiates rot.v LED toggle example with this clock and you should see the same result only 10x faster.

Here is the code: top.v
```
git clone https://github.com/lightside-instruments/ice4pi-example-i2cslave.git -b ice4pi-example-pll ice4pi-example-pll
cd ice4pi-example-pll
make
sudo make load
```
This example has pre-configured instantiation of the PLL to generate 120 MHz clock from the 12MHz input clock. If you want to change that you can use the icepll tool and edit the Verilog in top.v accordingly:

```
pi@raspberrypi:~ $ icepll -i 12 -o 120 -f pll.v -m
F_PLLIN:    12.000 MHz (given)
F_PLLOUT:  120.000 MHz (requested)
F_PLLOUT:  120.000 MHz (achieved)
FEEDBACK: SIMPLE
F_PFD:   12.000 MHz
F_VCO:  960.000 MHz
DIVR:  0 (4'b0000)
DIVF: 79 (7'b1001111)
DIVQ:  3 (3'b011)
FILTER_RANGE: 1 (3'b001)
PLL configuration written to: pll.v
```

# The END
