import json
from logic.bitstring_table import BitstringTable
from logic.bdd_atl import BddAtl
from graphics.io import IO
from os import sep
from execptions.interval_execptions import IntervalDataError


def main():
    IO.banner()
    with open(f'input{sep}input.json') as json_file:
        data = json.load(json_file)
    for key, value in data.items():
        IO.seperator(key)
        IO.execution_details(value['run'])

        a = BddAtl(i_num_of_variables=1, i_debug=True)
        interval_hash_table = BitstringTable(i_bit_string_length=1)
        data_hash_table = BitstringTable(i_bit_string_length=1)

        for event in value['run']:
            try:
                event_type = event[0]
                interval_id = event[1]
                interval_bitstring = interval_hash_table.lookup(event_type, interval_id)
                if event_type == "begin":
                    try:
                        data = event[2]
                    except IndexError:
                        raise IntervalDataError(interval_id)

                    data_bitstring = data_hash_table.lookup(event_type, data)
                    a.event_update(event_type, interval_id, interval_bitstring, data_bitstring)
                else:
                    a.event_update(event_type, interval_id, interval_bitstring)
            except Exception as err:
                IO.error(err)
                break
        IO.seperator('FINAL STATE')
        print(a)
        IO.seperator('THE END')



if __name__ == '__main__':
    main()