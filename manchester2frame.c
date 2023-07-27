#include <stdio.h>
#include <stdint.h>


void dump_binary(uint32_t samples, int width)
{
    unsigned int i;
    for(i=(32-width);i<32;i++) {
    	printf("%c",((samples<<i)&0x80000000)?'1':'0');
    }
}

void dump_frame(unsigned int len, uint8_t* frame)
{
    unsigned int i;
    for(i=0;i<len;i++){
        printf("%02X",frame[i]);
    }
    printf("\n");
}


#define IDLE 0
#define LOW  1
#define HIGH 2
#define START_OF_IDLE 3

int bit(unsigned int i, uint64_t fifo)
{
    if((fifo<<i)&0x8000000000000000) {
    	return 1;
    } else {
        return 0;
    }
}

int is_idle_to_start_of_idle(unsigned int offset, uint64_t fifo)
{
    if(((fifo<<offset) & 0xFFFFF00000000000)==0xFFFFF00000000000) {
    	/* 20 1s */
        return 1;
    } else {
        return 0;
    }
}

int is_idle_to_high(unsigned int offset, uint64_t fifo)
{
    if(((fifo<<offset) & 0xFFE0000000000000)==0xFFE0000000000000) {
    	/* >11 1s */
        return 1;
    } else {
        return 0;
    }
    
    return 0;
}

#define DELTA 5

int is_high_to_low(unsigned int offset, uint64_t fifo)
{
    if(bit(offset-DELTA, fifo) && !bit(offset+DELTA, fifo)) {
    	return 1;
    } else {
        return 0;
    }
}
int is_high_to_high(unsigned int offset, uint64_t fifo)
{
    if(!bit(offset-DELTA, fifo) && bit(offset+DELTA, fifo)) {
    	return 1;
    } else {
        return 0;
    }

}
int is_high_to_start_of_idle(unsigned int offset, uint64_t fifo)
{
    if(bit(offset-DELTA, fifo) && bit(offset+DELTA, fifo)) {
    	return 1;
    } else {
        return 0;
    }

}

int is_low_to_low(unsigned int offset, uint64_t fifo)
{
    if(bit(offset-DELTA, fifo) && !bit(offset+DELTA, fifo)) {
    	return 1;
    } else {
        return 0;
    }
}
int is_low_to_high(unsigned int offset, uint64_t fifo)
{
    if(!bit(offset-DELTA, fifo) && bit(offset+DELTA, fifo)) {
    	return 1;
    } else {
        return 0;
    }
}
int is_low_to_start_of_idle(unsigned int offset, uint64_t fifo)
{
    if(((fifo<<(offset+DELTA)) & 0xFFFFF00000000000)==0xFFFFF00000000000) {
        return 1;
    } else {
        return 0;
    }
}

int is_start_of_idle_to_idle(unsigned int offset, uint64_t fifo)
{
    if(((fifo<<offset) & 0xFFFFF00000000000)!=0xFFFFF00000000000) {
    	/* 20 1s */
        return 1;
    } else {
        return 0;
    }
}

unsigned int state_machine(uint32_t samples)
{
    unsigned int i;
    static uint64_t fifo=0;
    static unsigned int state = IDLE;
    static int start_bit_count=0;
    static int origin=20;
    static int offset; /* here is where the edge of the manchester transition is expected - adjusted upon first transition from IDLE to HIGH */

    fifo=(fifo<<20) | (samples&0x000FFFFF);
    dump_binary(samples,20);
    printf("\n");
    dump_binary(fifo>>32,32);
    dump_binary(fifo&0x00000000FFFFFFFF,32);
    printf("\n");
    printf("offset=%d\n", offset);
        
    if(state==IDLE) {
    	for(i=0;i<20;i++) {
            if(is_idle_to_start_of_idle(i+origin,fifo)) {
                state=START_OF_IDLE;
                offset=origin+i;
            } else if(is_idle_to_high(i+origin,fifo)) {
                state=HIGH;
                offset=origin+i;
            }
            if(state!=IDLE) {
                break;
            }
        }
    } else if(state==START_OF_IDLE) {
        if(is_start_of_idle_to_idle(offset,fifo)) {
            state=IDLE;
        }
    } else if(state==HIGH) {
        if(is_high_to_start_of_idle(offset,fifo)) {
            state=START_OF_IDLE;
        } else if(is_high_to_low(offset,fifo)) {
            state=LOW;
        } else if(is_high_to_high(offset,fifo)) {
            state=HIGH;
        } else {
            state=IDLE;
        }
    } else if(state==LOW) {
        if(is_low_to_start_of_idle(offset,fifo)) {
            state=START_OF_IDLE;
        } else if(is_low_to_low(offset,fifo)) {
            state=LOW;
        } else if(is_low_to_high(offset,fifo)) {
            state=HIGH;
        } else {
            state=IDLE;
        }
    }

    return state;
}

int main(int argc, char** argv)
{
    int ret;
    unsigned int i=0;
    uint32_t samples;
    uint32_t fifo;
    unsigned int state;
    unsigned int prev = IDLE;
    unsigned int bits_count;
    uint8_t octet;
    uint8_t frame[1530];
    int sfd_delimeter = 0;
    FILE* f;

    if(argc==1) {
        f = stdin;
    } else {
        f = fopen(argv[1], "r");
        if(f==NULL) {
            perror("Error opening file.\n");
            return -1;
        }
    }
    do{
        ret = fread(&samples, sizeof(uint32_t), 1, f);
        if(ret==1) {
            state = state_machine(samples);
            printf("[%d] state=%d\n", i, state);
            if(prev==IDLE) {
                sfd_delimeter = 0;
                if(state==HIGH) {
#if 0
                    /* Raspberry Pi 4B hack - it sends 2 bits short of the complete preamble sequence 0x555555555555 */
                    bits_count=3;
                    octet=0xA8;
#else
                    bits_count=1;
                    octet=0x80;
#endif
                }
            } else if(prev==HIGH || prev==LOW) {
                if(state==HIGH || state==LOW) {
#if 1
//lost initial preamble bits hack
                    if(bits_count>24 && bits_count<63 && !sfd_delimeter) {
                        if(prev==HIGH && state==HIGH) {
                            sfd_delimeter = 1;
                            frame[0]=0x55;
                            frame[1]=0x55;
                            frame[2]=0x55;
                            frame[3]=0x55;
                            frame[4]=0x55;
                            frame[5]=0x55;
                            frame[6]=0x55;
                            octet = 0xD5;
                            octet = octet<<1;
                            printf("Warning: the preamble+sfd bit sequence was %u bits long instead of 64\n",bits_count+1);
                            bits_count=64-1;
                        }
                    }
#endif
                    octet=octet>>1;
                    if(state==HIGH) {
                        octet|=0x80;
                    }
                    bits_count++;
                    if((bits_count%8)==0) {
                        frame[bits_count/8-1]=octet;
                        printf("octet[%u] <- %02X\n",(bits_count/8-1),octet);
                        octet=0;
                    }
                } else if(state==START_OF_IDLE) {
                    dump_frame(bits_count/8, frame);
                }
            } 

            prev = state;
        }
        i++;
    } while(ret==1);
}
