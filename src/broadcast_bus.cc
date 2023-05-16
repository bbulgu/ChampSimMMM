#include <list>
#include <atomic>

#include "block.h"
#include "broadcast_bus.h"


int address_to_cpu2(unsigned long long address) {
  return address % NUM_CPUS;
}

// reads a packet from the bus buffer
std::list<PACKET>::iterator BroadcastBus::read(){
    //  std::cout << "The read method of the broadcast bus has been invoked." << std::endl;
     return buffer.begin();
}                          

// adds a packet to the bus buffer 
void BroadcastBus::write(PACKET packet)            // (over)writes the packet
{
    items_written++;
    // std::cout << "Writing to the bus" << std::endl;
    // packet.printPacket();
    if (items_written % 1000 == 0)
        std::cout << "Now there are " << items_written << " elements written in the bus in total." << std::endl;
    if ( packet.v_address == 140732575011232 && packet.instr_id == 97141)
        std::cout << "Writing the troublemaker on the bus" << std::endl;
    //std::cout << "Writing to the bus" << std::endl;
    //packet.printPacket();
    buffer.push_back(packet);
    // printBus();
}

void BroadcastBus::printBus(){
    std::cout<<"printing the contents of the broadcast bus"<<std::endl;
    for (std::list<PACKET>::iterator it = buffer.begin(); it != buffer.end(); ++it)
    {
        PACKET current = *it;
        int cpu = address_to_cpu2(current.v_address);
        current.printPacket();
    }

} 
/**/
void BroadcastBus::clear(int cpuid)
{
    for (std::list<PACKET>::iterator it = buffer.begin(); it != buffer.end(); ++it)
    {
        PACKET current = *it;
        int written_counter = 0;
        for (int i=0; i<NUM_CPUS; i++) {
            if (current.written_on_inbox[i])
                written_counter++;
        }
        //std::cout << written_counter << std::endl;
        // N-1 cpus must write it to their inbox, 1 cpu already "owns" the packet
        if (written_counter == (NUM_CPUS-1)) {
            //std::cout << "Deleting packet from broadcast bus" << std::endl;
            //current.printPacket();
            it = buffer.erase(it);
        }
    }
}


// OBSOLETE VERSION
/*
// clears the bus buffer, should be called at the begining of every cycle before the filling of the buffer with the new packets
void BroadcastBus::clear(int cpuid)
{
    std::cout << "Clearing is called from cpuid =" << cpuid << std::endl;
    clear_array[cpuid] = 1;
    int clear_counter = 0;
    for (int i = 0; i<NUM_CPUS; i++) {
        if (clear_array[i] == 1){
            clear_counter++;
        }
    }
    if (clear_counter == NUM_CPUS)
    {
        //if (buffer.size() > 0)
        //{
            std::cout << "Clearing the broadcast bus from cpuid =" << cpuid << std::endl;
            std::cout << "its size is " << buffer.size() << std::endl;
        //}
        
        prev_buffer.clear();
        for (std::list<PACKET>::iterator it = buffer.begin(); it != buffer.end(); ++it)
        {
            PACKET current = *it;
            prev_buffer.push_back(current);
            //int cpu = address_to_cpu2(current.v_address);
            //std::cout << " Bus contents: virtual addr = " << current.v_address << " belongs to cpu = "<< cpu << ", ip: " << current.ip << ", instr id: " << current.instr_id << std::endl;

        }
        
        buffer.clear();
        for (int i = 0; i<NUM_CPUS; i++) {
            clear_array[i] = 0;
        }
    }    
}
*/
