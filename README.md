# Presentation slides
## Slide: The current solution

 Talks about Ultra96, Network Programmability Kit

## Slide: The required SBC for remote management of network tester

 Talks about importance of:

 0. Open-source toolchain
 1. C Toolchain
 2. SerDes
 3. Linux
 4. Management protocols and model based management NETCONF/YANG (netconfd)
 5. Debian

## Slide: Result

## Slide: Yosys, RiscV, OpenPOWER, LiteX


## Slide: Simplest softcore CPU that can run C programs

 Talks about ice40 with femtoRV


## Step 2. Simplest softcore CPU platform with SerDes

 Talks about Gatemate

## Step 3. Simplest softcore CPU that can run Linux
 Talks about Lattice Versa (ECP5UM-45F)
## Step 4. Simplest softcore CPU that can run Debian
 Talks about ROCKET RiscV architecture on OrangeCrab ECP5UM-85F
 Talks about OpenPOWER on orangecrab

## Step 5. Performance evaluation


# Installing liteX
mkdir litex
cd litex
sudo apt install python3-venv
python3 -m venv my_project_env
source my_project_env/bin/activate
./litex_setup.py --init --install


# TODO
## [x] Produce a orangecrab from the designfiles to validate DDR RAM signal integrity with the selected PCB stackup.
## [ ] Produce Ultra96 board replacement based on ECP5UM-85F (4x SFP+ instead of 6x SFP+)
## [ ] Produce Ultra96 board replacement based on Gatemate (1x SFP+ instead of 6x SFP+)
## [ ] Produce ice4pi board replacement based on ECP5UM-85F (1x SFP+ instead of 1x Ethernet 1Gb)
## [ ] Produce ice4pi board replacement based on Gatemate (1x SFP+ instead of 1x Ethernet 1Gb)
## [ ] Integrate existing AXI-lite cores in the liteX design


