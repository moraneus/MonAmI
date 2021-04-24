from logic.bdd_atl import BddAtl
from logic.bitstring_table import BitstringTable
from execptions.execptions import IntervalDataError


def update_bdds_without_specification(i_sequence_of_events, i_num_of_variables, i_expansion_length):
    bdd_atl = BddAtl([], i_interval_size=i_num_of_variables, i_debug=False)
    interval_hash_table = BitstringTable(i_num_of_variables, i_expansion_length, i_debug=False)
    data_hash_table = BitstringTable(i_num_of_variables, i_expansion_length, i_debug=False)

    for event in i_sequence_of_events:
        event_type = event[0]
        interval_id = event[1]
        interval_bitstring = interval_hash_table.lookup(event_type, interval_id)
        if event_type == "begin":
            try:
                data = event[2]
            except IndexError:
                raise IntervalDataError(interval_id)

            data_bitstring = data_hash_table.lookup(event_type, data)
            bdd_atl.event_update(event_type, interval_id, interval_bitstring, data, data_bitstring)
        else:
            bdd_atl.event_update(event_type, interval_id, interval_bitstring)

    return bdd_atl.bdds


def update_bdds_with_specification(i_sequence_of_events, i_specification, i_num_of_variables):
    bdd_atl = BddAtl(i_specification.intervals, i_interval_size=i_num_of_variables, i_debug=False)
    interval_hash_table = BitstringTable(i_num_of_variables, i_debug=False)
    data_hash_table = BitstringTable(i_num_of_variables, i_debug=False)

    for event in i_sequence_of_events:
        event_type = event[0]
        interval_id = event[1]
        interval_bitstring = interval_hash_table.lookup(event_type, interval_id)
        if event_type == "begin":
            try:
                data = event[2]
            except IndexError:
                raise IntervalDataError(interval_id)

            data_bitstring = data_hash_table.lookup(event_type, data)
            bdd_atl.event_update(event_type, interval_id, interval_bitstring, data, data_bitstring)
        else:
            bdd_atl.event_update(event_type, interval_id, interval_bitstring)

        result = i_specification.eval(bdd_manager=bdd_atl,
                                      data_manager=data_hash_table,
                                      debug_mode=True) == bdd_atl.bdd_manager.true

        if result:
            break

    return result
