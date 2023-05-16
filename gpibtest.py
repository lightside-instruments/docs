import gpib

con=gpib.dev(0,1)

gpib.write(con,'A1B23456')

