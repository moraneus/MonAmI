import json
from logic.bitstring_table import BitstringTable
from logic.bdd_atl import BddAtl
from graphics.io import IO
from os import sep
from execptions.execptions import IntervalDataError
from frontend.parser import parse


def read_json(i_json_file):
    with open(i_json_file, "r") as json_file:
        data = json.load(json_file)
    return data


def main():
    IO.banner()
    configuration = read_json(f"input{sep}configuration")
    execution = read_json(f"input{sep}trace")["execution"]
    property = parse(read_json(f"input{sep}property")["property"].replace("'", '"'))


    if configuration["DEBUG"]:
        IO.seperator("START")
        IO.execution(execution)
        IO.property(property)

    # BDD constructor object
    bdd_atl = BddAtl(property.intervals,
                     i_interval_size=configuration["INTERVAL_SIZE"],
                     i_debug=configuration["DEBUG"])
    # Interval bitstring DB object
    interval_hash_table = BitstringTable(configuration["INTERVAL_SIZE"],
                                         configuration["EXPANSION_LENGTH"],
                                         i_debug=configuration["DEBUG"])
    # Data bitstring DB object
    data_hash_table = BitstringTable(configuration["DATA_SIZE"],
                                     configuration["EXPANSION_LENGTH"],
                                     i_debug=configuration["DEBUG"])

    for event in execution:
        try:
            event_type = event[0]
            interval = event[1]
            interval_bitstring = interval_hash_table.lookup(event_type, interval)

            if event_type == "begin":
                # In a case when "begin" event doesn't contain a data.
                try:
                    data = event[2]
                except IndexError:
                    raise IntervalDataError(interval)

                data_bitstring = data_hash_table.lookup(event_type, data)
                bdd_atl.event_update(event_type, interval, interval_bitstring, data, data_bitstring)
            else:
                bdd_atl.event_update(event_type, interval, interval_bitstring)

            if configuration["DEBUG"]:
                IO.ast_header()

            result = property.eval(bdd_manager = bdd_atl,
                                   data_manager = data_hash_table,
                                   debug_mode = configuration["DEBUG"]) == bdd_atl.bdd_manager.true

            if configuration["DEBUG"]:
                if result:
                    IO.true()
                else:
                    IO.false()

            if result:
                IO.seperator('FINAL STATE')
                IO.execution(execution)
                IO.property(property)
                for bdd_name, bdd_data in bdd_atl.bdds.items():
                    IO.bdd_state(bdd_name, bdd_data)
                IO.true()
                IO.seperator('THE END')
                break

        except Exception as err:
            IO.error(err)
            break


if __name__ == '__main__':
    main()
