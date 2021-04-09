from logic.bdd_atl import BddAtl
from logic.bitstring_table import BitstringTable
from execptions.interval_execptions import IntervalDataError


def update_bdds(i_sequence_of_events, i_num_of_variables):
    a = BddAtl(i_num_of_variables=i_num_of_variables, i_debug=False)
    interval_hash_table = BitstringTable(i_bit_string_length=i_num_of_variables)
    data_hash_table = BitstringTable(i_bit_string_length=i_num_of_variables)

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
            a.event_update(event_type, interval_id, interval_bitstring, data_bitstring)
        else:
            a.event_update(event_type, interval_id, interval_bitstring)

    return a.bdds
