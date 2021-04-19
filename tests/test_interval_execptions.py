from tests.test_helper import *
from execptions.execptions import *


class TestIntervalExceptions:
    def test_multiple_begin_error_1(self):
        sequence = [["begin", 1, "Data1"], ["begin", 1, "Data1"],
                    ["begin", 3, "Data1"], ["end", 1], ["end", 3]]

        try:
            bdds = update_bdds_without_specification(sequence, i_num_of_variables=1, i_expansion_length=2)
        except MultipleBeginError:
            assert True

    def test_multiple_begin_error_2(self):
        sequence = [["begin", 1, "Data1"], ["begin", 2, "Data2"], ["begin", 3, "Data3"],
                    ["end", 1], ["end", 2], ["end", 3], ["begin", 1, "Data2"]]

        try:
            bdds = update_bdds_without_specification(sequence, i_num_of_variables=1, i_expansion_length=2)
        except MultipleBeginError:
            assert True

    def test_multiple_end_error_1(self):
        sequence = [["begin", 1, "Data1"], ["begin", 3, "Data1"], ["end", 1], ["end", 1]]
        try:
            bdds = update_bdds_without_specification(sequence, i_num_of_variables=1, i_expansion_length=2)
        except MultipleEndError:
            assert True

    def test_multiple_end_error_2(self):
        sequence = [["begin", 1, "Data1"], ["begin", 2, "Data1"], ["begin", 3, "Data1"],
                    ["end", 1], ["end", 2], ["end", 3], ["end", 1]]
        try:
            bdds = update_bdds_without_specification(sequence, i_num_of_variables=1, i_expansion_length=2)
        except MultipleEndError:
            assert True

    def test_ends_before_start_error_1(self):
        sequence = [["end", 1], ["begin", 3, "Data1"]]
        try:
            bdds = update_bdds_without_specification(sequence, i_num_of_variables=1, i_expansion_length=2)
        except EndsBeforeBeginError:
            assert True

    def test_ends_before_start_error_2(self):
        sequence = [["begin", 1, "Data1"], ["begin", 2, "Data1"], ["begin", 3, "Data1"],
                    ["end", 4], ["end", 2], ["end", 3], ["end", 1]]
        try:
            bdds = update_bdds_without_specification(sequence, i_num_of_variables=1, i_expansion_length=2)
        except EndsBeforeBeginError:
            assert True

    def test_bad_event_value_error_1(self):
        sequence = [["begin", 1, "Data1"], ["boooo", 3, "Data1"]]
        try:
            bdds = update_bdds_without_specification(sequence, i_num_of_variables=1, i_expansion_length=2)
        except BadEventValueError:
            assert True

    def test_bad_event_value_error_2(self):
        sequence = [["begin", 1, "Data1"], ["begin", 2, "Data1"], ["begin", 3, "Data1"],
                    ["boooo", 4], ["end", 2], ["end", 3], ["end", 1]]
        try:
            bdds = update_bdds_without_specification(sequence, i_num_of_variables=1, i_expansion_length=2)
        except BadEventValueError:
            assert True

    def test_interval_data_error_1(self):
        sequence = [["begin", 1], ["begin", 1, "Data1"],
                    ["begin", 3, "Data1"], ["end", 1], ["end", 3]]

        try:
            bdds = update_bdds_without_specification(sequence, i_num_of_variables=1, i_expansion_length=2)
        except IntervalDataError:
            assert True

    def test_interval_data_error_2(self):
        sequence = [["begin", 1, "Data1"], ["begin", 2, "Data2"], ["begin", 3, "Data3"],
                    ["end", 1], ["end", 2], ["end", 3], ["begin", 4]]

        try:
            bdds = update_bdds_without_specification(sequence, i_num_of_variables=1, i_expansion_length=2)
        except IntervalDataError:
            assert True
