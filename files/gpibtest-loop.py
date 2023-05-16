import gpib
import time

con=gpib.dev(0,1)

gpib.write(con,'B123456')
i=0
while(i<10):
        gpib.write(con,'A1B3')
        time.sleep(0.1)
        gpib.write(con,'A2B1')
        time.sleep(0.1)
        gpib.write(con,'A3B2')
        time.sleep(0.1)
        i=i+1
