import os
import csv

RESULTS_DIR = "VaryingCache"
with open(f'{RESULTS_DIR}results.csv', 'w', newline='') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(["TraceName", "IPC", "Number of Cycles"])
    for filename in os.listdir(RESULTS_DIR):
        f = os.path.join(RESULTS_DIR, filename)
        # checking if it is a file
        if os.path.isfile(f):
            print(f)
            with open(f, "r") as file:
                whole_text = file.read()
                if ("Finished CPU" in whole_text):
                    trace_name = filename
                    ipc = float(whole_text.partition("cumulative IPC: ")[2].partition("(")[0])
                    cycles = int(whole_text.partition("Finished")[2].partition("cycles: ")[2].partition(" c")[0])

                    writer.writerow([trace_name, ipc, cycles])


