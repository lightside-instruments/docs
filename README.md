# Capturing Ethernet Frame with Scope
![Title](title.png)

# Introduction
This document describes method for capturing Ethernet (10BASE-T) frame with oscilloscope. The process described has these steps:

* connect two channels with probes latched to the Ethernet cable - TX pair 2 - orange
* setting a scope trigger for the start of frame condition
* reading the discrete samples representing the analog voltage from each of the twisted pair wires
* subtracting the second from the first channels to get a differential signal
* lowpass filtering the oversampled signal (optional)
* generating a binary 0s and 1s pulsetrain representation of the filtered oversampled signal
* detection of frame beginning
* decoding of the manchester encoded frame data
* printing frame data upon end of frame detection to standard output

The following command line tool (sources provided) calls do the specified steps:

```
sudo apt-get install python3 gcc octave-cli
python3 oscilloscope.py | tee out.txt | grep ch | tee channels.m
octave-cli ethfilter.m # uses channels.m and generates signal.bin (sequence of 32 bit little endian integers each 32 bit integer contains 20 binary values (LSB) of the oversampled 200 MS/s aquisition data)
gcc manchester2frame.c -o manchester2frame
cat signal.bin | ./manchester2frame  | grep 55555555555555D5
```

This is the end output - in this case ARP request packet:
55555555555555D5FFFFFFFFFFFFE45F01E3FE7208060001080006040001E45F01E3FE720A0000030000000000000A00000200000000000000000000000000000000000084919005

[oscilloscope.py](oscilloscope.py)
[manchester2frame.c](manchester2frame.c)
