# Create Random Trace File 
1. You can create a random execution in the `trace` file using the script `trace_generator.py`, located in the`input` folder.
2. The trace_generator.py gets as input a `data` and `rules` files which are a JSON type.
3. It also needs to get as arguments num of intervals, output filename, the percentage of rules cover in the trace, and the maximum depth of the intervals.
4. Examples of how to call the trace generator script:

```python
# "rules" - rules filename.
# "data" - data filename.
# 500 - trace with 500 intervals (or 1000 events).
# "output.json" - output filename.
# 30 - Percentage cover of rules in the trace.
# 3 - The maximum depth on intervals.

trace_generator = TraceGenerator("rules", "data", 500, 'output.json', 30, 3)
trace_generator.convert()
```