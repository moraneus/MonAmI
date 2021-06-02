###################################################################################################################
# You need to create your own initial input files (trace and a property).
# Once it is done, you can give them as input while running the script.
# i.e. python3 run_monami_experiments.py <path/to/property> <path/to/trace>
# You can see the structure of those file in the input folder.
###################################################################################################################

import json
import math
import sys
import tracemalloc
import timeit
from logic.bitstring_table import BitstringTable
from logic.bdd_atl import BddAtl
from execptions.execptions import IntervalDataError
from frontend.parser import parse


def display_allocated_memory(snapshot, key_type='lineno'):
    snapshot = snapshot.filter_traces((
        tracemalloc.Filter(False, "<frozen importlib._bootstrap>"),
        tracemalloc.Filter(False, "<unknown>"),
    ))
    top_stats = snapshot.statistics(key_type)
    total = sum(stat.size for stat in top_stats)
    print(f"Allocated Memory: {'%.2f' % (total / 1024)}KB")


def read_json(i_json_file):
    with open(i_json_file, "r") as json_file:
        data = json.load(json_file)
    return data


def main():
    property_file = sys.argv[1]
    trace_file = sys.argv[2]
    cb = int(sys.argv[3])

    # Read input files
    execution = read_json(trace_file)["execution"]
    property = parse(read_json(property_file)["property"].replace("'", '"'))

    bitstring_size = math.ceil(math.log(len(execution)/2, 2))
    counter = 1

    # BDD constructor object
    bdd_atl = BddAtl(property.get_intervals(), i_interval_size=bitstring_size, i_debug=False)

    # Interval bitstring DB object
    interval_hash_table = BitstringTable(bitstring_size, 1, i_debug=False)

    # Data bitstring DB object
    data_hash_table = BitstringTable(bitstring_size, 1, i_debug=False)

    # Define an empty dictionary which map interval into data
    interval_data_dict = {}

    for event in execution:
        try:
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

            # Check property in CS mode
            if not cb:
                property.eval(bdd_manager=bdd_atl, data_manager=data_hash_table, debug_mode=False)
            # print(f'[MAIN LOOP]: {counter, result}')
            # counter += 1

        except Exception as err:
            print(err)
            break

    # Check property in CB mode
    if cb:
        property.eval(bdd_manager=bdd_atl, data_manager=data_hash_table, debug_mode=False)


if __name__ == '__main__':
    tracemalloc.start()
    start = timeit.default_timer()
    main()
    stop = timeit.default_timer()
    print(f"Time: {'%.2f' % (stop - start)}")
    snapshot = tracemalloc.take_snapshot()
    display_allocated_memory(snapshot)



