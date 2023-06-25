import json
import os

block_size_default = 64
page_size_default = 4096
heartbeat_frequency_default = 10000000

# configurable stuff, change here

# for the config file
num_cpus = 3
broadcast_latency = 120  # TODO: Make this configurable in the script
rob_size = 400
memory_partitioning_method = "zero"

print(f"Creating a config file with {num_cpus} cpus, a broadcast latency of {broadcast_latency}, memory partitioning method {memory_partitioning_method} and rob size of {rob_size}!")

# for the simulation
simulation_instructions = 5000
trace_path = "traces/"
trace_name = "649.fotonik3d_s-1B.champsimtrace.xz"

# can add other variables to config but this might be a good place to start

sample_ooo_cpu = {
    "frequency": 4000,
    "ifetch_buffer_size":64,
    "decode_buffer_size":32,
    "dispatch_buffer_size":32,
    "rob_size": 352,
    "lq_size": 128,
    "sq_size": 72,
    "fetch_width": 6,
    "decode_width": 6,
    "dispatch_width": 6,
    "execute_width": 4,
    "lq_width": 2,
    "sq_width": 2,
    "retire_width": 5,
    "mispredict_penalty": 1,
    "scheduler_size": 128,
    "decode_latency": 1,
    "dispatch_latency": 1,
    "schedule_latency": 0,
    "execute_latency": 0,
    "broadcast_latency": 50,
    "memory_partitioning_method": "basic",
    "branch_predictor": "bimodal",
    "btb": "basic_btb"
} 

outDict = {
    "executable_name": "bin/champsim",
    "block_size": 64,
    "page_size": 4096,
    "heartbeat_frequency": 10000000,
    "num_cores": num_cpus,

    "ooo_cpu": [
    ],

    "DIB": {
        "window_size": 16,
        "sets": 32,
        "ways": 8
    },

    "L1I": {
        "sets": 64,
        "ways": 8,
        "rq_size": 64,
        "wq_size": 64,
        "pq_size": 32,
        "mshr_size": 8,
        "latency": 4,
        "max_read": 2,
        "max_write": 2,
        "prefetch_as_load": False,
        "virtual_prefetch": True,
        "prefetch_activate": "LOAD,PREFETCH",
        "prefetcher": "no_instr"
    },

    "L1D": {
        "sets": 64,
        "ways": 12,
        "rq_size": 64,
        "wq_size": 64,
        "pq_size": 8,
        "mshr_size": 16,
        "latency": 5,
        "max_read": 2,
        "max_write": 2,
        "prefetch_as_load": False,
        "virtual_prefetch": False,
        "prefetch_activate": "LOAD,PREFETCH",
        "prefetcher": "no"
    },

    "L2C": {
        "sets": 1024,
        "ways": 8,
        "rq_size": 32,
        "wq_size": 32,
        "pq_size": 16,
        "mshr_size": 32,
        "latency": 10,
        "max_read": 1,
        "max_write": 1,
        "prefetch_as_load": False,
        "virtual_prefetch": False,
        "prefetch_activate": "LOAD,PREFETCH",
        "prefetcher": "no"
    },

    "ITLB": {
        "sets": 16,
        "ways": 4,
        "rq_size": 16,
        "wq_size": 16,
        "pq_size": 0,
        "mshr_size": 8,
        "latency": 1,
        "max_read": 2,
        "max_write": 2,
        "prefetch_as_load": False
    },

    "DTLB": {
        "sets": 16,
        "ways": 4,
        "rq_size": 16,
        "wq_size": 16,
        "pq_size": 0,
        "mshr_size": 8,
        "latency": 1,
        "max_read": 2,
        "max_write": 2,
        "prefetch_as_load": False
    },

    "STLB": {
        "sets": 128,
        "ways": 12,
        "rq_size": 32,
        "wq_size": 32,
        "pq_size": 0,
        "mshr_size": 16,
        "latency": 8,
        "max_read": 1,
        "max_write": 1,
        "prefetch_as_load": False
    },

	"PTW": {
		"pscl5_set": 1,
		"pscl5_way": 2,
		"pscl4_set": 1,
		"pscl4_way": 4,
		"pscl3_set": 2,
		"pscl3_way": 4,
		"pscl2_set": 4,
		"pscl2_way": 8,
		"ptw_rq_size": 16,
		"ptw_mshr_size": 5,
		"ptw_max_read": 2,
		"ptw_max_write": 2
	},

    "LLC": {
        "frequency": 4000,
        "sets": 2048,
        "ways": 16,
        "rq_size": 32,
        "wq_size": 32,
        "pq_size": 32,
        "mshr_size": 64,
        "latency": 20,
        "max_read": 1,
        "max_write": 1,
        "prefetch_as_load": False,
        "virtual_prefetch": False,
        "prefetch_activate": "LOAD,PREFETCH",
        "prefetcher": "no",
        "replacement": "lru"
    },

    "physical_memory": {
        "frequency": 3200,
        "channels": 1,
        "ranks": 1,
        "banks": 8,
        "rows": 65536,
        "columns": 128,
        "channel_width": 8,
        "wq_size": 64,
        "rq_size": 64,
        "tRP": 12.5,
        "tRCD": 12.5,
        "tCAS": 12.5,
        "turn_around_time": 7.5
    },

    "virtual_memory": {
        "size": 8589934592,
        "num_levels": 5,
        "minor_fault_penalty": 200
    }
}

sample_ooo_cpu["broadcast_latency"] = broadcast_latency
sample_ooo_cpu["rob_size"] = rob_size
sample_ooo_cpu["memory_partitioning_method"] = memory_partitioning_method
outDict["num_cores"] = num_cpus

for cpu in range(num_cpus):
    outDict["ooo_cpu"].append(sample_ooo_cpu)

config_file_name = "config_autogenerated.json"

# write the new config to a json file
with open(config_file_name, 'w') as outfile:
    json.dump(outDict, outfile, indent=4)

print("Successfully wrote to the config file {config_file_name}")

# run the og config script on that file
os.system("./config.sh config_autogenerated.json")
print("Successfully ran the config script!")

# make
os.system("make")
print("Ran make!")

# simulate
print("trying to simulate")
traces_str = ""
for trace in range(num_cpus):
    traces_str += f"{trace_path}{trace_name} "
os.system(f"bin/champsim --warmup_instructions 0 --simulation_instructions {simulation_instructions} {traces_str} >> results/{trace_name}_{simulation_instructions}.txt")
print("finished everything.")

# TODO: Change main champsim file to only output the necessary stuff
# TODO: Pipe the output to a file
# TODO: Create a script to get times from files
# TODO: Add different interleaving options
# TODO: Add some error handling
# TODO: Make this script run the simulator as well
# TODO: Make another script to run this script many times with different stuff
