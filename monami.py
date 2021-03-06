import json
from logic.bitstring_table import BitstringTable
from logic.bdd_atl import BddAtl
from graphics.io import IO
from os import sep
import math
from execptions.execptions import IntervalDataError
from frontend.parser import parse


def read_json(i_json_file):
    with open(i_json_file, "r") as json_file:
        data = json.load(json_file)
    return data


def main():
    IO.banner()

    # Read input files
    configuration = read_json(f"input{sep}configuration")
    execution = read_json(configuration["TRACE"])["execution"]
    property = parse(read_json(configuration["PROPERTY"])["property"].replace("'", '"'))

    # Print input to console
    if configuration["DEBUG"]:
        IO.seperator("START")
        IO.execution(execution)
        IO.property(property)

    # Set the initial size of interval bitstring
    if configuration['INTERVAL_SIZE'] == "AUTO":
        interval_bitstring_length = math.ceil(math.log(len(execution) / 2, 2))
    else:
        interval_bitstring_length = configuration["INTERVAL_SIZE"]

    # Set the initial size of data bitstring
    if configuration['DATA_SIZE'] == "AUTO":
        data_bitstring_length = math.ceil(math.log(len(execution) / 2, 2))
    else:
        data_bitstring_length = configuration["DATA_SIZE"]

    # BDD constructor object
    bdd_atl = BddAtl(property.get_intervals(),
                     i_interval_size=interval_bitstring_length,
                     i_data_size=data_bitstring_length,
                     i_debug=configuration["DEBUG"])

    # Interval bitstring DB object
    interval_hash_table = BitstringTable(interval_bitstring_length,
                                         configuration["EXPANSION_LENGTH"],
                                         i_debug=configuration["DEBUG"])

    # Data bitstring DB object
    data_hash_table = BitstringTable(data_bitstring_length,
                                     configuration["EXPANSION_LENGTH"],
                                     i_debug=configuration["DEBUG"])

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

            if configuration["DEBUG"]:
                IO.ast_header()

            # Check if the property is satisfied in the MODE ["VIOLATION", "SATISFACTION" or "CONTINUE-SMALL"]
            if configuration["MODE"] != "CONTINUE-BIG":
                result = property.eval(bdd_manager=bdd_atl,
                                       data_manager=data_hash_table,
                                       debug_mode=configuration["DEBUG"]) == bdd_atl.bdd_manager.true

                # Print the result for the current event
                if configuration["DEBUG"]:
                    if result:
                        IO.true()
                    else:
                        IO.false()

                # In a case of MODE == VIOLATION the tool stop when property eval results is False.
                # In a case of MODE == SATISFACTION the tool stop when property eval results is True.
                # In a case of MODE == CONTINUE-SMALL the tool evaluate the property after every event until the
                # end of the trace.
                # In a case of MODE == CONTINUE-BIG the tool evaluate the property once at the end of the trace.
                # Any other case the tool will act the same as CONTINUE-BIG.
                if configuration["MODE"] == "VIOLATION":
                    if not result:
                        break
                elif configuration["MODE"] == "SATISFACTION":
                    if result:
                        break

        except Exception as err:
            IO.error(err)
            break

    # Check if the property is satisfied in the MODE "CONTINUE-BIG"
    if configuration["MODE"] not in ["VIOLATION", "SATISFACTION", "CONTINUE-SMALL"]:
        result = property.eval(bdd_manager=bdd_atl,
                               data_manager=data_hash_table,
                               debug_mode=configuration["DEBUG"]) == bdd_atl.bdd_manager.true

    # Print the final BDDs state
    if configuration["DEBUG"]:
        IO.final(execution, property, bdd_atl.bdds.items())

    if result:
        IO.true()
    else:
        IO.false()


if __name__ == '__main__':
    main()
