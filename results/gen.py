import csv
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

with open('results.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    data = [dict(row) for row in reader]
    for d in data:
        del d['']

print(data)

def duration_to_sec(dur):
    mins_as_sec = int(f"{dur[0]}{dur[1]}") * 60
    secs = float("".join(dur[3:]))
    return mins_as_sec + secs

def dur_fmt(secs, _):
    return "{:02}:{:02}".format(int(secs/60), int(secs % 60))

task_keys = [f"Task {i}" for i in range(1,5)]
rank_keys = [f"Rank {i}" for i in range(1,5)]
# Assign ranks
for i, t in enumerate(task_keys):
    for rank, row in enumerate(sorted(data, key=lambda row: row[t])):
        row[rank_keys[i]] = rank + 1

example_ranks = [row[r] for r in rank_keys for row in data if row["Variant"] == "Examples"]
baseline_ranks = [row[r] for r in rank_keys for row in data if row["Variant"] == "No Examples"]

print(example_ranks, len(example_ranks), sum(example_ranks))
print(baseline_ranks, len(baseline_ranks), sum(baseline_ranks))


example_tasks = [[duration_to_sec(row[t]) for row in data if row["Variant"] == "Examples"] for t in task_keys]
baseline_tasks = [[duration_to_sec(row[t]) for row in data if row["Variant"] == "No Examples"] for t in task_keys]

print(example_tasks)

import numpy as np
import matplotlib.pyplot as plt

# Fixing random state for reproducibility
np.random.seed(19680801)

# fake up some data
spread = np.random.rand(50) * 100
center = np.ones(25) * 50
flier_high = np.random.rand(10) * 100 + 100
flier_low = np.random.rand(10) * -100


fig1, axs = plt.subplots(ncols=len(example_tasks))
axs[0].set_ylabel("Time (mm:ss)")
for task_i in range(len(task_keys)):
    example_tasks = [duration_to_sec(row[task_keys[task_i]]) for row in data if row["Variant"] == "Examples"]
    baseline_tasks = [duration_to_sec(row[task_keys[task_i]]) for row in data if row["Variant"] == "No Examples"]
    axs[task_i].set_xlim(-.5, 1.5)
    axs[task_i].set_ylim(0, 750)
    axs[task_i].set_title(f'Task {task_i + 1}')
    axs[task_i].scatter(["Examples" for _ in example_tasks] + ["No Examples" for _ in baseline_tasks], example_tasks + baseline_tasks, marker="o", edgecolors=[(0, 0, 0, 1)])

    if task_i == 0:
        axs[task_i].yaxis.set_major_formatter(ticker.FuncFormatter(dur_fmt))
    else:
        axs[task_i].yaxis.set_major_formatter(ticker.NullFormatter())


plt.show()
