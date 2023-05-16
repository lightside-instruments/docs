#include <gpib/ib.h>

int main() {
	    int dev;
	    
	       dev=ibdev(0,1,0,T3s,0,0);
	           ibwrt(dev,"A1B23456",8);
}

