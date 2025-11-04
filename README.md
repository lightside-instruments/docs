# Eye Diagram acquisition for SFP+ ports and transceiver characterization of 1Gb and 10Gb Ethernet devices
We will share our experience with the process of design and production of networking device with SFP+ ports and validating the signal integrity performance of its tranceivers.
Both the DUT (OSHWA NO000005) and the SFP to SMA coaxial breakout module (OSHWA NO000009) used are opensource-hardware KiCAD designs published by us with the intent to serve as request for comment and reference designs that can be modified and improved by the SI community.

## Getting started
* https://github.com/ngscopeclient/scopehal-testdata
* https://www.youtube.com/watch?v=SysecTECvBI
* https://www.youtube.com/watch?v=UQKZS4z8P-w&t=1852s - Beyond Scope. What else can R&S MXO4 do with Open Source Hard- & Software? 

# Setup

 yangcli user@192.168.4.139> create /interfaces/interface[name='eth1']/traffic-generator -- interframe-gap=96 frame-data=6CA96F0000026CA96F00000108004500002ED4A500000A115816C0000201C0000202C0200007001A00000102030405060708090A0B0C0D0E0F1011126EECF305 frame-size=64
 yangcli user@192.168.4.139> merge /interfaces/interface[name='eth1'] -- type=ethernetCsmacd
 yangcli user@192.168.4.139> commit
 
# Acquisition
* https://github.com/lightside-instruments/yuma123-netconfd-module/tree/lsi-ivi-scope-test-measurements-spark/measurements/spark-sfp-acquisition
to capture 64 octets frame and 20 octets interframe gap (includes 7+1 preamble octets)
84*8=672 ns of capture time
## Storage scope
## Sampling scope
# Visualization and analysis
## ngscopeclient
## Matlab/Octave




# Terminology
LVDS
1000Base-X
VCM
VOD

# References
* LVDS Owner's Manual, 4th Edition, Texas Instruments, 2008. https://www.ti.com/lit/ug/snla187/snla187.pdf
