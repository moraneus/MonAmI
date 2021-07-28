
import sys
import _nfer
import csv

spec = sys.argv[1]
trace = sys.argv[2]
minimal = sys.argv[3]
doprint = sys.argv[4]

if minimal == "true":
    _nfer.minimal(True)
else:
    _nfer.minimal(False)

_nfer.load(spec)

results = []
with open(trace) as eventfile:
    reader = csv.reader(eventfile, delimiter='|')
    for row in reader:
        name = row[0]
        time = int(row[1])
        fields = row[2].split(";")
        data = row[3].split(";")
        map = dict(zip(fields,data))
        intervals = _nfer.add(name,time, time,map)
        if intervals is not None:
            results.extend(intervals)
print(len(results))
if doprint == "true":
    for interval in results:
        print(interval)
