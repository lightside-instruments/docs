import gpib
import time

def cmd(con, cmd):
        result = ""
        gpib.write(con,cmd)

        c = gpib.read(con,2048)
        result=c.decode("utf-8")

        return result


con=gpib.dev(0,2)


reply=cmd(con,'*IDN?\n')
print("Instrument identification string:")
print("    " + reply)

gpib.write(con,'*RST\n')        # Set power-on condition
gpib.write(con,'Current 0.5\n') # Set current limit to 0.5A
gpib.write(con,'Output on\n')   # Turn output on

print("Voltage Current\n\n")

# Step from 0.6 to 0.8 volt in 0.02 step
voltage = 0.6
while(voltage<0.8001):
    voltage = voltage + 0.02
    # Set output voltage
    gpib.write(con,'Volt %f\n'%(voltage))
    time.sleep(0.5)
    # Measure output current
    reply = cmd(con,"Measure:Current?\n")
    current=float(reply)
    print("%.3f %6.4f\n"%(voltage, current))

gpib.write(con,'Output off\n') # Turn output off

