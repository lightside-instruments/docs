#include <stdio.h>
#include <stdint.h>
#include <assert.h>

int get_bit(unsigned int i, uint32_t fifo)
{
    if((fifo>>i)&1) {
    	return 1;
    } else {
        return 0;
    }
}

void set_bit(unsigned int i, uint8_t* octet)
{
    *octet = (1<<i)|(*octet);
}


int main(int argc, char** argv)
{
    int ret;
    unsigned int i=0;
    uint8_t in;
    uint8_t in_sw;
    uint8_t out1;
    uint8_t out2;
    unsigned int bit;
    FILE* outf;
    FILE* inf;

    if(argc==1) {
        inf = stdin;
        outf = stdout;
    } else {
        inf = fopen(argv[1], "r");
        if(inf==NULL) {
            perror("Error opening file.\n");
            return -1;
        }
        outf = fopen(argv[2], "w");
        if(outf==NULL) {
            perror("Error opening file.\n");
            return -1;
        }
    }
    do {
        ret = fread(&in, sizeof(uint8_t), 1, inf);
        //printf("%02X\n",in);

        //swap to LSB first
        in_sw = 0;
        for(bit=0;bit<8;bit++) {
            in_sw = in_sw<<1;
            in_sw = in_sw | get_bit(bit, in);
        }

        in = in_sw;

        out1=0;
        out2=0;
        if(ret==1) {
            if(get_bit(7, in)) {
                set_bit(6,&out1);
            } else {
                set_bit(7,&out1);
            }
            if(get_bit(6, in)) {
                set_bit(4,&out1);
            } else {
                set_bit(5,&out1);
            }
            if(get_bit(5, in)) {
                set_bit(2,&out1);
            } else {
                set_bit(3,&out1);
            }
            if(get_bit(4, in)) {
                set_bit(0,&out1);
            } else {
                set_bit(1,&out1);
            }
            if(get_bit(3, in)) {
                set_bit(6,&out2);
            } else {
                set_bit(7,&out2);
            }
            if(get_bit(2, in)) {
                set_bit(4,&out2);
            } else {
                set_bit(5,&out2);
            }
            if(get_bit(1, in)) {
                set_bit(2,&out2);
            } else {
                set_bit(3,&out2);
            }
            if(get_bit(0, in)) {
                set_bit(0,&out2);
            } else {
                set_bit(1,&out2);
            }
            //printf("%02X\n",out1);
            //printf("%02X\n",out2);

            ret = fwrite(&out1, sizeof(uint8_t), 1, outf);
            assert(ret==1);
            ret = fwrite(&out2, sizeof(uint8_t), 1, outf);
            assert(ret==1);            
        }
        i++;
    } while(ret==1);
    return 0;
}
 
