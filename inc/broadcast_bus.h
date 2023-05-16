#ifndef BROADCAST_BUS_H
#define BROADCAST_BUS_H

#include <list>
#include <atomic>
#include "block.h"

class BroadcastBus
{
    public:
    std::list<PACKET> buffer;
    std::list<PACKET> prev_buffer;
    int clear_array[NUM_CPUS];

    int items_written;

    std::list<PACKET>::iterator read();           // returns an iterator that points to the beginning of the buffer

    void write(PACKET packet);                    // (over)writes the packet
    void printBus(); 
    void clear(int cpuid);                        // remove everything at the end of the cycle

};

#endif
