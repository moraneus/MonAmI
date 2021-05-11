import json
from logic.bitstring_table import BitstringTable
from logic.bdd_atl import BddAtl
from os import sep
from execptions.execptions import IntervalDataError
from frontend.parser import parse
from frontend.ast import Forall, Not
import linecache
import os
import tracemalloc
import timeit

def display_top(snapshot, key_type='lineno', limit=3):
    snapshot = snapshot.filter_traces((
        tracemalloc.Filter(False, "<frozen importlib._bootstrap>"),
        tracemalloc.Filter(False, "<unknown>"),
    ))
    top_stats = snapshot.statistics(key_type)

    print("Top %s lines" % limit)
    for index, stat in enumerate(top_stats[:limit], 1):
        frame = stat.traceback[0]
        # replace "/path/to/module/file.py" with "module/file.py"
        filename = os.sep.join(frame.filename.split(os.sep)[-2:])
        print("#%s: %s:%s: %.1f KiB"
              % (index, filename, frame.lineno, stat.size / 1024))
        line = linecache.getline(frame.filename, frame.lineno).strip()
        if line:
            print('    %s' % line)

    other = top_stats[limit:]
    if other:
        size = sum(stat.size for stat in other)
        print("%s other: %.1f KiB" % (len(other), size / 1024))
    total = sum(stat.size for stat in top_stats)
    print("Total allocated size: %.1f KiB" % (total / 1024))


def read_json(i_json_file):
    with open(i_json_file, "r") as json_file:
        data = json.load(json_file)
    return data

def main():

    ###################################################################################################################
    # You need to create your own initial configuration file and input (trace and a property).
    # Once it is done, set the *_file variable to those files and execute this script.
    # You can see the progress through the console prints, depends on the size of the trace you create.
    # At violation, satisfaction or at the end of the trace you will get an output which summerize the allocated memory
    # and the time it takes.
    ###################################################################################################################

    configuration_file = f"..{sep}input{sep}configuration"
    trace_file = f"..{sep}input{sep}trace2000"
    property_file = f"..{sep}input{sep}property"

    # Read input files
    configuration = read_json(configuration_file)
    execution = read_json(trace_file)["execution"]
    property = parse(read_json(property_file)["property"].replace("'", '"'))

    counter = 1

    # BDD constructor object
    bdd_atl = BddAtl(property.get_intervals(),
                     i_interval_size=configuration["INTERVAL_SIZE"],
                     i_debug=False)

    # Interval bitstring DB object
    interval_hash_table = BitstringTable(configuration["INTERVAL_SIZE"],
                                         configuration["EXPANSION_LENGTH"],
                                         i_debug=False)

    # Data bitstring DB object
    data_hash_table = BitstringTable(configuration["DATA_SIZE"],
                                     configuration["EXPANSION_LENGTH"],
                                     i_debug=False)

    # Define an empty dictionary which map interval into data
    interval_data_dict = {}

    for event in execution:
        try:
            print(f'[MAIN LOOP]: {counter}')
            event_type = event[0]
            interval_id = event[1]
            interval_bitstring = interval_hash_table.lookup(event_type, interval_id)

            # Add the interval: data into the interval_data_dict
            if event_type == "begin":
                try:
                    data = event[2]
                    data_bitstring = data_hash_table.lookup(event_type, data)
                    interval_data_dict[interval_id] = {"data": data, "data_bitstring": data_bitstring}

                # In a case when "begin" event doesn't contain a data.
                except IndexError:
                    raise IntervalDataError(interval_id)

            # In a case when the event is not in type of 'begin'.
            else:
                if interval_id not in interval_data_dict.keys():
                    interval_data_dict[interval_id] = {"data": None, "data_bitstring": ""}

            # Call the main BDD update function
            bdd_atl.event_update(event_type, interval_id, interval_bitstring, interval_data_dict[interval_id])

            # Check if the property is satisfied
            result = property.eval(bdd_manager=bdd_atl,
                                   data_manager=data_hash_table,
                                   debug_mode=False) == bdd_atl.bdd_manager.true

            # Print the final state of the BDDs when the property is satisfied or violated.
            # It depends on the property type and the expected result.
            if isinstance(property, Forall) or isinstance(property, Not):
                if not result:
                    break
            else:
                if result:
                    break
            counter += 1

        except Exception as err:
            break


if __name__ == '__main__':
    tracemalloc.start()
    start = timeit.default_timer()
    main()
    stop = timeit.default_timer()
    print('Time: ', stop - start)
    snapshot = tracemalloc.take_snapshot()
    display_top(snapshot)



