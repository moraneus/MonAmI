import timeit


def set_method():
    SETUP_CODE = f'import json\n' \
                 f'from logic.list_atl import ListAtl\n' \
                 f'from os import sep\n' \
                 f'from execptions.execptions import IntervalDataError, BadEventValueError, EndsBeforeBeginError\n' \
                 f'from frontend.parser import parse\n'

    TEST_CODE = '''def read_json(i_json_file):
    with open(i_json_file, "r") as json_file:
        data = json.load(json_file)
    return data
    
    def main():

        # Read input files
        configuration = read_json(f"input{sep}configuration")
        execution = read_json(f"input{sep}trace")["execution"]
        property = parse(read_json(f"input{sep}property")["property"].replace("'", '"'))
    
        # Print input to console
        if configuration["DEBUG"]:
            IO.seperator("START")
            IO.execution(execution)
            IO.property(property)
    
        # BDD constructor object
        list_atl = ListAtl(i_debug=configuration["DEBUG"])
    
        # Define an empty dictionary which map interval into data
        interval_data_dict = {}
    
        for event in execution:
            try:
                event_type = event[0]
                interval_id = event[1]
    
                # Add the interval: data into the interval_data_dict
                if event_type == "begin":
                    # In a case when "begin" event doesn't contain a data.
                    try:
                        interval_data_dict[interval_id] = {"data": event[2]}
    
                    except IndexError:
                        raise IntervalDataError(interval_id)
    
                # because data at the 'end' event is not mandatory, several exceptions are catches here
                if interval_id not in interval_data_dict.keys():
                    if event_type == 'end':
                        raise EndsBeforeBeginError(interval_id)
                    else:
                        raise BadEventValueError(interval_id)
    
                # Call the main BDD update function
                list_atl.event_update(event_type, interval_id, interval_data_dict[interval_id])
    
                if configuration["DEBUG"]:
                    IO.ast_header()
    
            except Exception as err:
                IO.error(err)
                break

if __name__ == '__main__':
    main()'''

    times = timeit.repeat(setup=SETUP_CODE,
                          stmt=TEST_CODE,
                          repeat=3,
                          number=100)
    print(f'SET implementation time: {(min(times))}')


def bdd_method():
    SETUP_CODE = f'from logic.bitstring_table import BitstringTable\n' \
                 f'from logic.bdd_atl import BddAtl\n' \
                 f'from os import sep\n' \
                 f'from execptions.execptions import IntervalDataError, BadEventValueError, EndsBeforeBeginError\n'

    TEST_CODE = '''def read_json(i_json_file):
    with open(i_json_file, "r") as json_file:
        data = json.load(json_file)
    return data
    
    def main():

        # Read input files
        configuration = read_json(f"input{sep}configuration")
        execution = read_json(f"input{sep}trace")["execution"]
        property = parse(read_json(f"input{sep}property")["property"].replace("'", '"'))
    
        # BDD constructor object
        bdd_atl = BddAtl(property.intervals,
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
                event_type = event[0]
                interval_id = event[1]
                interval_bitstring = interval_hash_table.lookup(event_type, interval_id)
    
                # Add the interval: data into the interval_data_dict
                if event_type == "begin":
                    # In a case when "begin" event doesn't contain a data.
                    try:
                        data = event[2]
                        data_bitstring = data_hash_table.lookup(event_type, data)
                        interval_data_dict[interval_id] = {"data": data, "data_bitstring": data_bitstring}
    
                    except IndexError:
                        raise IntervalDataError(interval_id)
    
                # because data at the 'end' event is not mandatory, several exceptions are catches here
                if interval_id not in interval_data_dict.keys():
                    if event_type == 'end':
                        raise EndsBeforeBeginError(interval_id)
                    else:
                        raise BadEventValueError(interval_id)
    
                # Call the main BDD update function
                bdd_atl.event_update(event_type, interval_id, interval_bitstring, interval_data_dict[interval_id])
    
    
            except Exception as err:
                break


if __name__ == '__main__':
    main()'''

    times = timeit.repeat(setup=SETUP_CODE,
                          stmt=TEST_CODE,
                          repeat=3,
                          number=100)

    print(f'BDD implementation time: {(min(times))}')


if __name__ == "__main__":
    set_method()
    bdd_method()
