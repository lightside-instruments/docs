import sys
import gpib
import time
import os

def cmd(con, cmd):
        result = ""
        gpib.write(con,cmd)

        c = gpib.read(con,2048)
        result=c.decode("utf-8")

        return result

def setup_channel(channel):
        reply=cmd(con, ':CHANnel'+str(channel)+'?\n')
        print (reply)
        gpib.write(con,':CHAN'+str(channel)+':MODE ON\n')
#       gpib.write(con,':CHAN'+str(channel)+':POS 0\n')
        gpib.write(con, 'CHAN'+str(channel)+':VDIV:VALue 50V\n')


def read_waveform(trace) :
        gpib.write(con, 'WAVeform:TRACE '+ str(trace) + '\n')

        gpib.write(con, 'WAVeform:FORMAT ASCII\n')

        gpib.write(con, 'WAVeform:START ' + str(0) + '\n')
        gpib.write(con, 'WAVeform:END '+ str(110-1) + '\n')

        reply=cmd(con, "WAVeform:BITS?\n")
        print(reply)

        reply=cmd(con, "WAVeform:TYPE?\n")
        print(reply)

        reply=cmd(con, 'WAVeform?\n')
        print(reply)
        reply=cmd(con, "WAVeform:SEND?\n")
        print(reply)

con=gpib.dev(0,3)

#gpib.write(con, '*RST\n')
reply=cmd(con, '*IDN?\n')
print (reply)
reply=cmd(con, ':CHANnel'+str(1)+'?\n')
print (reply)


gpib.write(con,':TIM:TDIV 100ns\n')

setup_channel(1)
setup_channel(2)
setup_channel(3)
setup_channel(4)

gpib.write(con, 'START\n')

time.sleep(2)

gpib.write(con,':STOP\n')

read_waveform(1)
read_waveform(2)
read_waveform(3)
read_waveform(4)

