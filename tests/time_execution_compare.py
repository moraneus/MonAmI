import timeit


def set_method():
    SETUP_CODE = f'from logic.list_atl import ListAtl\n' \
                 f'from execptions.interval_execptions import IntervalDataError\n' \
                 f'from graphics.io import IO\n' \
                 f'from os import sep\n' \
                 f'import json\n'

    TEST_CODE = '''with open(f'..{sep}input{sep}input.json') as json_file:
        data = json.load(json_file)
        for key, value in data.items():
            b = ListAtl(i_debug=False)
        for event in value['run']:
            try:
                event_type = event[0]
                interval_id = event[1]
                if event_type == "begin":
                    try:
                        data = event[2]
                    except IndexError:
                        raise IntervalDataError(interval_id)
                    b.event_update(event_type, interval_id, data)
                else:
                    b.event_update(event_type, interval_id)
            except Exception as err:
                IO.error(err)
                break'''

    times = timeit.repeat(setup=SETUP_CODE,
                          stmt=TEST_CODE,
                          repeat=3,
                          number=100)
    print(f'SET implementation time: {(min(times))}')


def bdd_method():
    SETUP_CODE = f'from logic.bdd_atl import BddAtl\n' \
                 f'from logic.bitstring_table import BitstringTable\n' \
                 f'from execptions.interval_execptions import IntervalDataError\n' \
                 f'from graphics.io import IO\n' \
                 f'from os import sep\n' \
                 f'import json\n'

    TEST_CODE = '''with open(f'..{sep}input{sep}input.json') as json_file:
        data = json.load(json_file)
        for key, value in data.items():
            a = BddAtl(i_num_of_variables=1, i_debug=False)
            interval_hash_table = BitstringTable(i_bit_string_length=3)
            data_hash_table = BitstringTable(i_bit_string_length=3)

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
                break'''

    times = timeit.repeat(setup=SETUP_CODE,
                          stmt=TEST_CODE,
                          repeat=3,
                          number=100)

    print(f'BDD implementation time: {(min(times))}')


if __name__ == "__main__":
    set_method()
    bdd_method()