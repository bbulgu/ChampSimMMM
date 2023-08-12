import os
import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def plotMyCSV(csv_file, changingValue, IPCValue):
    df = pd.read_csv(csv_file)
    df_pivot = pd.pivot_table(
    df,
    values=IPCValue,
    index="TraceName",
    columns=changingValue,
    aggfunc=np.mean
    )

    # Plot a bar chart using the DF
    ax = df_pivot.plot(kind="bar")
    # Get a Matplotlib figure from the axes object for formatting purposes
    fig = ax.get_figure()
    # Change the plot dimensions (width, height)
    fig.set_size_inches(7, 6)
    # Change the axes labels
    ax.set_xlabel("Trace Name")
    ax.set_ylabel(IPCValue)

    fig.savefig(f"{csv_file}_{changingValue}_{IPCValue}barplot.png")


def get_results(RESULTS_DIR, LATENCY, CHANGING_VALUE):
    csv_file_name = f'{RESULTS_DIR}/results_{LATENCY}latency.csv'
    with open(csv_file_name, 'w+', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["TraceName", "DRAM", "Cpus", "BlockSize", "MSHR", "Partitioning", "Latency", "ROB", "Weight", "IPC"])
        files = os.listdir(RESULTS_DIR)
        files.sort()
        
        for filename in files:
            f = os.path.join(RESULTS_DIR, filename)
            # checking if it is a file
            if os.path.isfile(f) and f.endswith(".txt"):
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
                        ipc = float(whole_text.partition("Finished")[2].partition("cumulative IPC: ")[2].partition(" (")[0]) ## if heartbeat need finished
                        ipc *= weight
                        if latency == LATENCY:
                            writer.writerow([trace_name, dram, cpus, block, mshr, partitioning, latency, rob, weight, ipc]) 
    
    df = pd.read_csv(csv_file_name)
    df = df.groupby(["TraceName", "DRAM", "Cpus", "BlockSize", "MSHR", "Partitioning", "Latency", "ROB"]).agg({"IPC": "sum", "Weight": "sum"})
    df["final IPC"] = df["IPC"] / df["Weight"]
    fin_csv_name = f'{RESULTS_DIR}/pandas_results_{LATENCY}latency.csv'

    mins = df.groupby("TraceName").min("final IPC").rename(columns={'final IPC':'min IPC'})
    mins = mins[["min IPC"]]
    df_new = df.join(mins, on="TraceName")
    df_new["normalized IPC"] = df_new["final IPC"] / df_new["min IPC"]

    df_new.to_csv(fin_csv_name)

    plotMyCSV(fin_csv_name, CHANGING_VALUE, "normalized IPC")
    plotMyCSV(fin_csv_name, CHANGING_VALUE, "final IPC")


def get_all_results():
    get_results("BlockSizeResults", 0, "BlockSize")
    get_results("BlockSizeResults", 30, "BlockSize")
    get_results("DramResults", 0, "DRAM")
    get_results("DramResults", 30, "DRAM")
    get_results("PartitioningResults", 0, "Partitioning")
    get_results("PartitioningResults", 30, "Partitioning")
    get_results("RobResults", 30, "ROB")
    get_results("RobResults", 0, "ROB")
    get_results("MSHRResults", 0, "MSHR")
    get_results("MSHRResults", 30, "MSHR")

    # manually do latency
    """
    df0 = pd.read_csv("LatencyResults/pandas_results_0latency.csv")
    df1 = pd.read_csv("LatencyResults/pandas_results_30latency.csv")
    df2 = pd.read_csv("LatencyResults/pandas_results_120latency.csv")
    df3 = pd.read_csv("LatencyResults/pandas_results_480latency.csv")
    frames = [df0, df1, df2, df3]
    df = pd.concat(frames)
    mins = df.groupby("TraceName").min("final IPC").rename(columns={'final IPC':'min IPC'})
    mins = mins[["min IPC"]]
    df_new = df.join(mins, on="TraceName")
    df_new["normalized IPC"] = df_new["final IPC"] / df_new["min IPC"]
    df_new.to_csv("pandas_normalized_combined_results.csv")
    plotMyCSV("LatencyResults/pandas_normalized_combined_results.csv", "Latency", "normalized IPC")
    """
    # add cpus