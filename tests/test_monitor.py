from logic.bdd_atl import BddAtl
from logic.bitstring_table import BitstringTable
from execptions.execptions import IntervalDataError
from frontend.ast import Forall, Not


def update_bdds_only(i_sequence_of_events, i_num_of_variables, i_expansion_length):
    bdd_atl = BddAtl([], i_interval_size=i_num_of_variables, i_data_size=i_num_of_variables, i_debug=False)
    interval_hash_table = BitstringTable(i_num_of_variables, i_expansion_length, i_debug=False)
    data_hash_table = BitstringTable(i_num_of_variables, i_expansion_length, i_debug=False)
    interval_data_dict = {}

    for event in i_sequence_of_events:
        event_type = event[0]
        interval_id = event[1]
        interval_bitstring = interval_hash_table.lookup(event_type, interval_id)

        # Save the data which relate to an interval in a dict
        if event_type == "begin":
            try:
                data = event[2]
                data_bitstring = data_hash_table.lookup(event_type, data)
                interval_data_dict[interval_id] = {"data": data, "data_bitstring": data_bitstring}
            except IndexError:
                raise IntervalDataError(interval_id)

        else:
            if interval_id not in interval_data_dict.keys():
                interval_data_dict[interval_id] = {"data": None, "data_bitstring": ""}


        bdd_atl.event_update(event_type, interval_id, interval_bitstring, interval_data_dict[interval_id])

    return bdd_atl.bdds


def monitor(i_sequence_of_events, i_specification, i_num_of_variables=1, i_mode="CONTINUE-SMALL"):
    bdd_atl = BddAtl(i_specification.get_intervals(), i_interval_size=i_num_of_variables,
                     i_data_size=i_num_of_variables, i_debug=False)
    interval_hash_table = BitstringTable(i_num_of_variables, i_debug=False)
    data_hash_table = BitstringTable(i_num_of_variables, i_debug=False)
    interval_data_dict = {}
    verdicts = []

    for event in i_sequence_of_events:
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

        # Check if the property is satisfied in the MODE ["VIOLATION", "SATISFACTION" or "CONTINUE-SMALL"]
        if i_mode != "CONTINUE-BIG":
            result = i_specification.eval(bdd_manager=bdd_atl,
                                   data_manager=data_hash_table,
                                   debug_mode=False) == bdd_atl.bdd_manager.true
            verdicts.append(result)

            if i_mode == "VIOLATION":
                if not result:
                    break
            elif i_mode == "SATISFACTION":
                if result:
                    break

    # Check if the property is satisfied in the MODE "CONTINUE-BIG"
    if i_mode not in ["VIOLATION", "SATISFACTION", "CONTINUE-SMALL"]:
        result = i_specification.eval(bdd_manager=bdd_atl,
                               data_manager=data_hash_table,
                               debug_mode=False) == bdd_atl.bdd_manager.true
        verdicts.append(result)

    return result, verdicts
