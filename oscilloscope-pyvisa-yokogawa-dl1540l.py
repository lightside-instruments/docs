# Communication interface User's Manual https://cdn.tmi.yokogawa.com/IM701530-11E.pdf

import sys
import time
import os
import datetime

#import vxi11

##con=gpib.dev(0,3)
#instr = vxi11.vxi11.Instrument("TCPIP::10.13.37.28::gpib,1::INSTR")
#con=instr
samples=20000

import pyvisa

addr = "TCPIP::10.13.37.28::gpib,1::INSTR"

rm = pyvisa.ResourceManager()
print(rm.list_resources())

instr=rm.open_resource(addr)
reply=instr.query('*IDN?')
print(reply)

instr.timeout=100000
con=instr

def cmd_binary(instr, cmd):
        instr.write(cmd)
#        c = instr.read_bytes(instr.bytes_in_buffer)
        c = instr.read_raw()
        return c

def cmd(instr, cmd):
        result = ""
        instr.write(cmd)
#        c = instr.read_bytes(instr.bytes_in_buffer)
        c = instr.read_raw()
        result=c
        result=c.decode("utf-8")
        return result

def setup_channel(channel, voltage_range):
        reply=cmd(con, ':CHANnel'+str(channel)+'?')
        print (reply)
        con.write(':CHAN'+str(channel)+':MODE ON')
        con.write(':CHAN'+str(channel)+':POS 0')
        con.write(':CHAN'+str(channel)+':PROBE 1')
        con.write('CHAN'+str(channel)+':VDIV:VALue %f V'%(voltage_range/8))
        print('CHAN'+str(channel)+':VDIV:VALue %f V'%(voltage_range/8))

def disable_channel(channel):
        reply=cmd(con, ':CHANnel'+str(channel)+'?')
        print (reply)
        con.write(':CHAN'+str(channel)+':MODE OFF')

def read_waveform(trace, type="ASCII", vdiv=1) :
        con.write('WAVeform:TRACE '+ str(trace) + '')

        con.write('WAVeform:FORMAT %s'%(type))

        reply=cmd(con, "WAVeform:START?")
        print(reply)
        reply=cmd(con, "WAVeform:END?")
        print(reply)

        reply=cmd(con, "WAVeform:BITS?")
        print(reply)

        reply=cmd(con, "WAVeform:TYPE?")
        print(reply)

        reply=cmd(con, "WAVeform:SIGN?")
        print(reply)

        float_array = []
        block_size_max=1000

        for offset in range(0,samples,block_size_max):
            con.write('WAVeform:START ' + str(offset) + '')
            if((offset+block_size_max) > samples):
                block_size=samples-offset
            else:
                block_size=block_size_max
            con.write('WAVeform:END '+ str(offset+block_size-1) + '')

            reply=cmd(con, "WAVeform:START?")
            print(reply)
            reply=cmd(con, "WAVeform:END?")
            print(reply)


            reply=cmd(con, 'WAVeform?')
            print(reply)

            start = time.time()


            if(type=="ASCII"):
                reply=cmd(con, "WAVeform:SEND?")
            else:
                c=cmd_binary(con, "WAVeform:SEND?")

            end = time.time()

            if(type=="BYTE"):
                reply=""
                for byte in c[10:-1]:
                    #val = float(byte)
                    val = float(byte)-127
                    #val = float(vdiv)*(float(byte)-127)*1.0/25; 
                    if(reply==""):
                        reply = str(val)
                    else:
                        reply = reply + "," + str(val)
            elif(type=="WORD"):
                reply=""
                for i in range(10,(len(c)-1),2):
                    num=int.from_bytes(c[i:i+2], byteorder='big', signed=True)

                    val = float(vdiv)*(num)*1.0/3200
                    if(reply==""):
                        reply = str(val);
                    else:
                        reply = reply + "," + str(val)

            if(type=="ASCII"):
                print("Read %d bytes in %lf seconds" %(len(reply), (end - start)))
                #print(reply)
            else:
                print("Read %d bytes in %lf seconds" %(len(c), (end - start)))
                #print(c)

            float_array.extend( [float(i) for i in reply.split(',')])

        print("signal%d=%s"%(trace,str(float_array)))
        return(float_array)


instr.write('*RST')
reply=cmd(instr,'*IDN?')
print (reply)


# datetime object containing current date and time
now = datetime.datetime.now()
date_string = now.strftime("%Y/%m/%d")
time_string = now.strftime("%H:%M:%S")

print(date_string)
print(time_string)
instr.write('SYSTem:CLOCk:DATE "%s"'%(date_string[2:]))
instr.write('SYSTem:CLOCk:TIME "%s"'%(time_string))

instr.write(':TIM:TDIV 10us')

reply2=cmd(instr, "WAVeform:LENGth?")
print(reply2)

setup_channel(1,8.00)
setup_channel(2,8.00)
reply=cmd(instr, "TIMebase:SRATe?")
print(reply)
disable_channel(3)
disable_channel(4)
reply=cmd(instr, "TIMebase:SRATe?")
print(reply)

reply=cmd(instr, 'ACQuire:RECordlength?')
print (reply)


reply=cmd(instr, 'TRIGger?')
print (reply)

instr.write('TRIGger:MODE SINGLE')
instr.write('TRIGger:POSITION -3')
instr.write('TRIGGER:SIMPLE:EDGE:SLOPE FALL')
instr.write('TRIGger:SOURce:CHANnel1:LEVel +0.5V')
instr.write('TRIGger:SOURce:COUPling AC')

reply=cmd(instr, 'TRIGger?')
print (reply)

reply=cmd(instr, 'ACQuire:RECordlength?')
print (reply)

instr.write('ACQuire:RECordlength 400000')


#instr.write(instr,'*WAI')
#print (reply)
#time.sleep(4)

reply=cmd(instr, 'ACQuire:RECordlength?')
print (reply)

reply=cmd(instr, "TIMebase:SRATe?")
print(reply)

reply=cmd(instr, "ACQuire?")
print(reply)

#instr.write(instr, 'WAVEFORM:DATASELECT ACQDATA')
#instr.write(instr, 'TRIGger:ACTion:STARt')

instr.write('START')

print("Waiting for trigger ...")

while (1):
    reply=cmd(instr, 'STATus:CONDition?')
    print(reply)
    if(reply.strip()=="0"):
        break
    time.sleep(1)

instr.write(':STOP')
#instr.write('TRIGger:ACTion:STOP')


reply=cmd(instr, "ACQuire?")
print(reply)


reply=cmd(instr, "WAVeform:LENGth?")
print(reply)

reply=cmd(instr, "WAVeform:TRIGger?")
print(reply)


os.system("cat /proc/interrupts > interrupts-before.txt")
read_waveform(1, type="ASCII")
os.system("cat /proc/interrupts > interrupts-after.txt")
os.system("diff interrups-before.txt interrupts-after.txt")
#read_waveform(1, type="ASCII")
read_waveform(1, type="BYTE")
#read_waveform(2, type="ASCII")
#read_waveform(2, type="BYTE")
#read_waveform(2, type="WORD")
#read_waveform(3)
#read_waveform(4)
