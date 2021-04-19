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
    config = read_json(f"input{sep}configuration")
    input_data = read_json(f"input{sep}input")
    execution = input_data["execution"]
    specification = parse(input_data["specification"].replace("'", '"'))

    if config["DEBUG"]:
        IO.seperator("START")
        IO.execution(execution)
        IO.property(specification)

    bdd_atl = BddAtl(specification.intervals, i_interval_size=config["INTERVAL_SIZE"], i_debug=config["DEBUG"])
    interval_hash_table = BitstringTable(config["INTERVAL_SIZE"], config["EXPANSION_LENGTH"])
    data_hash_table = BitstringTable(config["DATA_SIZE"], config["EXPANSION_LENGTH"])

    for event in execution:
        try:
            event_type = event[0]
            interval_id = event[1]
            interval_bitstring = interval_hash_table.lookup(event_type, interval_id)
            if event_type == "begin":
                # In a case when "begin" event doesn't contain a data.
                try:
                    data = event[2]
                except IndexError:
                    raise IntervalDataError(interval_id)

                data_bitstring = data_hash_table.lookup(event_type, data)
                bdd_atl.event_update(event_type, interval_id, interval_bitstring, data_bitstring)
            else:
                bdd_atl.event_update(event_type, interval_id, interval_bitstring)

            if config["DEBUG"]:
                IO.ast_header(f'{event_type} -> {interval_id}')

            result = specification.eval(bdd_atl, data_hash_table, config["DEBUG"]) == bdd_atl.bdd_manager.true

            if config["DEBUG"]:
                if result:
                    IO.true()
                else:
                    IO.false()

            if result:
                IO.seperator('FINAL STATE')
                IO.execution(execution)
                IO.property(specification)
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
