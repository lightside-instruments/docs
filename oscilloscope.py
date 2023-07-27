# Communication interface User's Manual https://cdn.tmi.yokogawa.com/IM701530-11E.pdf

import sys
import gpib
import time
import os
import datetime

def cmd_binary(con, cmd):
        gpib.write(con,cmd)
        c = gpib.read(con,1024*1024)
        return c

def cmd(con, cmd):
        result = ""
        gpib.write(con,cmd)
        c = gpib.read(con,1024*1024)
        result=c.decode("utf-8")
        return result

def setup_channel(channel):
        reply=cmd(con, ':CHANnel'+str(channel)+'?\n')
        print (reply)
        gpib.write(con,':CHAN'+str(channel)+':MODE ON\n')
        gpib.write(con,':CHAN'+str(channel)+':POS 0\n')
        gpib.write(con,':CHAN'+str(channel)+':PROBE 1\n')
        gpib.write(con, 'CHAN'+str(channel)+':VDIV:VALue 1V\n')

def disable_channel(channel):
        reply=cmd(con, ':CHANnel'+str(channel)+'?\n')
        print (reply)
        gpib.write(con,':CHAN'+str(channel)+':MODE OFF\n')

def read_waveform(trace, type="ASCII") :
        gpib.write(con, 'WAVeform:TRACE '+ str(trace) + '\n')

        gpib.write(con, 'WAVeform:FORMAT %s\n'%(type))

        reply=cmd(con, "WAVeform:START?\n")
        print(reply)
        reply=cmd(con, "WAVeform:END?\n")
        print(reply)

        gpib.write(con, 'WAVeform:START ' + str(0) + '\n')
        gpib.write(con, 'WAVeform:END '+ str(40000-1) + '\n')

        reply=cmd(con, "WAVeform:BITS?\n")
        print(reply)

        reply=cmd(con, "WAVeform:TYPE?\n")
        print(reply)

        reply=cmd(con, 'WAVeform?\n')
        print(reply)

        start = time.time()


        if(type=="ASCII"):
            reply=cmd(con, "WAVeform:SEND?\n")
        else:
            c=cmd_binary(con, "WAVeform:SEND?\n")

        end = time.time()

        if(type=="BYTE"):
            reply=""
            for byte in c:
                val = byte*1.0/25;
                if(reply==""):
                    reply = str(val)
                else:
                    reply = reply + "," + str(val)
        elif(type=="WORD"):
            reply=""
            for i in range(0,int(len(c)/2)):
                val = (c[2*i]*256+c[2*i+1])*1.0/3200
                if(reply==""):
                    reply = str(val);
                else:
                    reply = reply + "," + str(val)

        if(type=="ASCII"):
            print("Read %d bytes in %lf seconds" %(len(reply), (end - start)))
            print(reply)
        else:
            print("Read %d bytes in %lf seconds" %(len(c), (end - start)))
            print(c)

        
        float_array = [float(i) for i in reply.split(',')]
        print("ch%d=%s"%(trace,str(float_array)))

con=gpib.dev(0,3)

gpib.write(con, '*RST\n')
reply=cmd(con, '*IDN?\n')
print (reply)


# datetime object containing current date and time
now = datetime.datetime.now()
date_string = now.strftime("%Y/%m/%d")
time_string = now.strftime("%H:%M:%S")

print(date_string)
print(time_string)
gpib.write(con,'SYSTem:CLOCk:DATE "%s"\n'%(date_string[2:]))
gpib.write(con,'SYSTem:CLOCk:TIME "%s"\n'%(time_string))

gpib.write(con,':TIM:TDIV 10us\n')

reply2=cmd(con, "WAVeform:LENGth?\n")
print(reply2)

setup_channel(1)
setup_channel(2)
reply=cmd(con, "TIMebase:SRATe?\n")
print(reply)
disable_channel(3)
disable_channel(4)
reply=cmd(con, "TIMebase:SRATe?\n")
print(reply)

reply=cmd(con, 'ACQuire:RECordlength?\n')
print (reply)


reply=cmd(con, 'TRIGger?\n')
print (reply)

gpib.write(con,'TRIGger:MODE SINGLE\n')
gpib.write(con,'TRIGger:POSITION -3\n')
gpib.write(con,'TRIGGER:SIMPLE:EDGE:SLOPE FALL\n')
gpib.write(con,'TRIGger:SOURce:CHANnel1:LEVel -0.5V\n')
gpib.write(con,'TRIGger:SOURce:COUPling AC\n')

reply=cmd(con, 'TRIGger?\n')
print (reply)

reply=cmd(con, 'ACQuire:RECordlength?\n')
print (reply)

gpib.write(con,'ACQuire:RECordlength 2000000\n')


#gpib.write(con,'*WAI\n')
#print (reply)
#time.sleep(4)

reply=cmd(con, 'ACQuire:RECordlength?\n')
print (reply)

reply=cmd(con, "TIMebase:SRATe?\n")
print(reply)

reply=cmd(con, "ACQuire?\n")
print(reply)

#gpib.write(con, 'WAVEFORM:DATASELECT ACQDATA\n')
#gpib.write(con, 'TRIGger:ACTion:STARt\n')

gpib.write(con, 'START\n')

print("Waiting for trigger ...")

while (1):
    reply=cmd(con, 'STATus:CONDition?')
    print(reply)
    if(reply.strip()=="0"):
        break
    time.sleep(1)

gpib.write(con,':STOP\n')
#gpib.write(con, 'TRIGger:ACTion:STOP\n')


reply=cmd(con, "ACQuire?\n")
print(reply)


reply=cmd(con, "WAVeform:LENGth?\n")
print(reply)

reply=cmd(con, "WAVeform:TRIGger?\n")
print(reply)


os.system("cat /proc/interrupts > interrupts-before.txt")
read_waveform(1, type="ASCII")
os.system("cat /proc/interrupts > interrupts-after.txt")
os.system("diff interrups-before.txt interrupts-after.txt")
read_waveform(1, type="BYTE")
read_waveform(1, type="WORD")
read_waveform(2, type="ASCII")
read_waveform(2, type="BYTE")
read_waveform(2, type="WORD")
#read_waveform(3)
#read_waveform(4)
