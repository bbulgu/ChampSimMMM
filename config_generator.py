import json
import os
import subprocess

def execute_command(command):
    try:
        result = subprocess.run(command, stderr=subprocess.PIPE, stdout=subprocess.DEVNULL, check=True, shell=True)
        # Print the error output if there were any errors
        if result.stderr:
            print(result.stderr.decode().strip())
            return -1
        return 0
    except subprocess.CalledProcessError as e:
        print(f"Command '{command}' failed with error code {e.returncode}")
        print(e.stderr.decode().strip())
        return -1
    
def try_execute_exit(command):
    if execute_command(command) == 0:
        print(f"Successfully ran {command}")
    else:
        print(f"{command} failed, exiting program!")
        exit()

def execute_nowait(command):
    proc = subprocess.Popen([command], shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)


# configurable stuff, change here

# cache size calculation: Number of sets × Number of ways × Block size
# sets: 64, ways: 8
# cache sizes we want: 4, 16, 64, 256, 1024 KBs 
# block sizes:         8, 32, 128, 512, 2048

# change partitioning methods
trace_path = "traces/"

os.system("module load gcc/13.1.0")
simulation_instructions = 5000000


for block_size in [128, 512, 2048]:
    for num_cpus in [4, 16, 64]:
         for mshr_l1d_size in [4, 16, 64]:
            for memory_partitioning_method in ["zero", "basic", "shift", "shift6"]:
                for trace_name in ["649.fotonik3d_s-1B.champsimtrace.xz", "648.exchange2_s-72B.champsimtrace.xz", "605.mcf_s-484B.champsimtrace.xz"]:
                    for broadcast_latency in [0, 30]:
                        for rob_size in [100, 200, 400, 800, 1600]:
                            trace_name_short = trace_name[0:3]
                            make_file_name = f"DRAM_{num_cpus}cpus_{block_size}block_{mshr_l1d_size}mshr_{memory_partitioning_method}partitioning_{broadcast_latency}latency_rob_{rob_size}"
                            file_name = f"QUICKresults/{trace_name_short}_{simulation_instructions}_{make_file_name}.txt"
                            if (os.path.isfile(file_name)):
                                print(f"{file_name} exists, skipping")
                                continue                        

                            print(f"creating config file for {trace_name_short}_{simulation_instructions}_{num_cpus}cpus_{block_size}block_{mshr_l1d_size}mshr_{memory_partitioning_method}partitioning_{broadcast_latency}latency!")
                            # for the simulation
                            
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
                                "block_size": block_size,
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
                                    "mshr_size": mshr_l1d_size,
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

                            print(f"Successfully wrote to the config file {config_file_name}")

                            # run the og config script on that file
                    
                            try_execute_exit("./config.sh config_autogenerated.json")
                                
                            # make
                            if (os.path.isfile(f"bin/{make_file_name}")):
                                print(f"{make_file_name} exists, skipping make")
                            else:
                                subprocess.run(f"make -e OUTPUT_BASENAME=\"{make_file_name}\"", stderr=subprocess.PIPE, stdout=subprocess.DEVNULL, check=True, shell=True)

                            # simulate
                            print("trying to simulate")
                            traces_str = ""
                            for trace in range(num_cpus):
                                traces_str += f"{trace_path}{trace_name} "

                            execute_nowait(f"bin/{make_file_name} --warmup_instructions 0 --simulation_instructions {simulation_instructions} {traces_str} >> {file_name}")
                            print(f"finished running {trace_name_short}_{simulation_instructions}_{num_cpus}cpus_{block_size}block_{mshr_l1d_size}mshr_{memory_partitioning_method}partitioning_{broadcast_latency}latency")

                            # TODO: Change main champsim file to only output the necessary stuff
                            # TODO: Pipe the output to a file
                            # TODO: Create a script to get times from files
                            # TODO: Add different interleaving options
                            # TODO: Add some error handling
                            # TODO: Make this script run the simulator as well
                            # TODO: Make another script to run this script many times with different stuff