import datetime
import subprocess
import matplotlib as mpl
import matplotlib.pyplot as plt
import sys

changes = dict()
output = subprocess.check_output('git log --all --reverse --pretty --cc --date=raw', cwd=sys.argv[1]).decode(errors='ignore')
hits = 0
timestamp = 0
for line in output.split('\n'):
    if line.startswith("Date"):
        line_parts = line.split()
        timestamp_str = line_parts[-2]
        timestamp = int(timestamp_str)
        changes[timestamp] = 0
    elif line.startswith("@@"):
        line_parts = line.split()
        deleted_str = line_parts[1]
        deleted = int(deleted_str.split(',')[1]) if ',' in deleted_str else abs(int(deleted_str))
        added_str = line_parts[2]
        added = int(added_str.split(',')[1]) if ',' in added_str else int(added_str)
        hits += (deleted + added)
        changes[timestamp] = hits

dpi = 80
fig = plt.figure(dpi=dpi, figsize=(512 / dpi, 384 / dpi))
mpl.rcParams.update({'font.size': 10})

xs = []
ys = []

for key, value in changes.items():
    if value:
        xs += [datetime.datetime.fromtimestamp(key)]
        ys += [value]

plt.axis([min(xs), max(xs), 0, max(ys)])

plt.title('Rate Of Hits')
plt.xlabel('timestamp')
plt.ylabel('hits')

plt.plot(xs, ys, color='red', linestyle='solid', label='roh')

plt.show()
