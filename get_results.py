import os
import csv
import pandas as pd

# parse variables
# sort based on latencies
def get_results(LATENCY):
    RESULTS_DIR = "toy"
    csv_file_name = f'{RESULTS_DIR}results_{LATENCY}latency.csv'
    with open(csv_file_name, 'w+', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["TraceName", "DRAM", "Cpus", "BlockSize", "MSHR", "Partitioning", "Latency", "ROB", "IPC"])
        files = os.listdir(RESULTS_DIR)
        files.sort()
        
        for filename in files:
            f = os.path.join(RESULTS_DIR, filename)
            # checking if it is a file
            if os.path.isfile(f):
                #print(f)
                with open(f, "r") as file:
                    whole_text = file.read()
                    if ("Finished CPU" in whole_text):
                        lst = filename.split("_")
                        trace_name = lst[0]
                        weight = float(lst[1])
                        dram = lst[2] == "DRAM"
                        cpus = int(lst[3].partition("cpus")[0])
                        block = int(lst[4].partition("block")[0])
                        mshr = int(lst[5].partition("mshr")[0])
                        partitioning = lst[6].partition("partitioning")[0]
                        latency = int(lst[7].partition("latency")[0])
                        rob = int(lst[9].partition(".txt")[0])
                        ipc = float(whole_text.partition("cumulative IPC: ")[2].partition(" (")[0])
                        ipc *= weight
                        if latency == LATENCY:
                            writer.writerow([trace_name, dram, cpus, block, mshr, partitioning, latency, rob, ipc])


    df = pd.read_csv(csv_file_name)
    print(df)
    df = df.groupby(["TraceName", "DRAM", "Cpus", "BlockSize", "MSHR", "Partitioning", "Latency", "ROB"]).agg({"IPC": "sum"})
    print(df)
    df.to_csv(f'pandas_{csv_file_name}')
    

get_results(0)
get_results(30)