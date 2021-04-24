from tests.test_helper import *
import unittest


class TestDataBdds(unittest.TestCase):
    def test_data_1_all_data_is_the_same_interval_and_data_not_extended(self):
        sequence = [["begin", 'Boo', 'Data1'], ["end", 'Boo'], ["begin", 3, 'Data1'], ["end", 3]]
        results = {
            'XD': [{'_D0': False}]
        }

        bdds = update_bdds_without_specification(sequence, i_num_of_variables=1, i_expansion_length=2)

        for key in results.keys():
            self.assertCountEqual(results[key], list(bdds[key]))

    def test_data_2_all_data_is_the_same_interval_is_extended_data_is_not(self):
        sequence = [["begin", 1, 'Data1'], ["end", 1], ["begin", 2, 'Data1'], ["end", 2],
                    ["begin", 3, 'Data1'], ["end", 3]]
        results = {
            'XD': [{'_X0': False, '_X1':False, '_X2': False, '_D0': False},
                   {'_X0': False, '_X1': False, '_X2': True, '_D0': False},
                   {'_X0': False, '_X1': True, '_X2': False, '_D0': False}]
        }

        bdds = update_bdds_without_specification(sequence, i_num_of_variables=1, i_expansion_length=2)

        for key in results.keys():
            self.assertCountEqual(results[key], list(bdds[key]))

    def test_data_3_all_data_is_the_same_interval_is_extended_data_is_not(self):
        sequence = [["begin", 'Boo', 'Data1'], ["end", 'Boo'], ["begin", 3, 'Data1'], ["end", 3],
                    ["begin", 2, "Data1"], ["end", 2], ["begin", 4, "Data1"], ["end", 4]]
        results = {
            'XD': [{'_X0': False, '_D0': False}]
        }

        bdds = update_bdds_without_specification(sequence, i_num_of_variables=1, i_expansion_length=2)

        for key in results.keys():
            self.assertCountEqual(results[key], list(bdds[key]))


    def test_data_4_all_data_is_not_the_same_interval_and_data_is_not_extended(self):
        sequence = [["begin", 1, 'Data1'], ["end", 1], ["begin", 2, 'Data2'], ["end", 2]]
        results = {
            'XD': [{'_X0': False, '_D0': False},
                   {'_X0': True, '_D0': True}]
        }

        bdds = update_bdds_without_specification(sequence, i_num_of_variables=1, i_expansion_length=2)

        for key in results.keys():
            self.assertCountEqual(results[key], list(bdds[key]))

    def test_data_5_data_is_not_the_same_interval_and_data_is_extended(self):
        sequence = [["begin", 1, 'Data1'], ["end", 1], ["begin", 2, 'Data2'], ["end", 2],
                    ["begin", 3, "Data3"], ["end", 3]]
        results = {
            'XD': [{'_X0': False, '_X1': False, '_X2': False, '_D0': False, '_D1': False, '_D2': False},
                   {'_X0': False, '_X1': False, '_X2': True,'_D0': False, '_D1': False, '_D2': True},
                   {'_X0': False, '_X1': True, '_X2': False, '_D0': False, '_D1': True, '_D2': False}]
        }

        bdds = update_bdds_without_specification(sequence, i_num_of_variables=1, i_expansion_length=2)

        for key in results.keys():
            self.assertCountEqual(results[key], list(bdds[key]))

    def test_data_6_all_data_is_not_the_same_interval_and_data_is_extended(self):
        sequence = [["begin", 1, 'Data1'], ["end", 1], ["begin", 2, 'Data2'], ["end", 2],
                    ["begin", 3, "Data3"], ["end", 3]]
        results = {
            'XD': [{'_X0': False, '_X1': False, '_X2': False, '_D0': False, '_D1': False, '_D2': False},
                   {'_X0': False, '_X1': False, '_X2': True,'_D0': False, '_D1': False, '_D2': True},
                   {'_X0': False, '_X1': True, '_X2': False, '_D0': False, '_D1': True, '_D2': False}]
        }

        bdds = update_bdds_without_specification(sequence, i_num_of_variables=1, i_expansion_length=2)

        for key in results.keys():
            self.assertCountEqual(results[key], list(bdds[key]))

    def test_data_7_all_data_is_not_the_same_interval_and_data_is_extended(self):
        sequence = [["begin", 1, 'Data1'], ["end", 1], ["begin", 2, 'Data2'], ["end", 2],
                    ["begin", 3, "Data3"], ["end", 3], ["begin", 4, "Data4"], ["end", 4],
                    ["begin", 5, "Data5"], ["end", 5], ["begin", 6, "Data6"], ["end", 6],
                    ["begin", 7, "Data7"], ["end", 7], ["begin", 8, "Data8"], ["end", 8],
                    ["begin", 9, "Data9"], ["end", 9], ["begin", 10, "Data10"], ["end", 10]]
        results = {
            'XD': [{'_X0': False, '_X1': False, '_X2': False, '_X3': False, '_X4': False,
                    '_D0': False, '_D1': False, '_D2': False, '_D3': False, '_D4': False},
                   {'_X0': False, '_X1': False, '_X2': False, '_X3': False, '_X4': True,
                    '_D0': False, '_D1': False, '_D2': False, '_D3': False, '_D4': True},
                   {'_X0': False, '_X1': False, '_X2': False, '_X3': True, '_X4': False,
                    '_D0': False, '_D1': False, '_D2': False, '_D3': True, '_D4': False},
                   {'_X0': False, '_X1': False, '_X2': False, '_X3': True, '_X4': True,
                    '_D0': False, '_D1': False, '_D2': False, '_D3': True, '_D4': True},
                   {'_X0': False, '_X1': False, '_X2': True, '_X3': False, '_X4': False,
                    '_D0': False, '_D1': False, '_D2': True, '_D3': False, '_D4': False},
                   {'_X0': False, '_X1': False, '_X2': True, '_X3': False, '_X4': True,
                    '_D0': False, '_D1': False, '_D2': True, '_D3': False, '_D4': True},
                   {'_X0': False, '_X1': False, '_X2': True, '_X3': True, '_X4': False,
                    '_D0': False, '_D1': False, '_D2': True, '_D3': True, '_D4': False},
                   {'_X0': False, '_X1': False, '_X2': True, '_X3': True, '_X4': True,
                    '_D0': False, '_D1': False, '_D2': True, '_D3': True, '_D4': True},
                   {'_X0': False, '_X1': True, '_X2': False, '_X3': False, '_X4': False,
                    '_D0': False, '_D1': True, '_D2': False, '_D3': False, '_D4': False},
                   {'_X0': False, '_X1': True, '_X2': False, '_X3': False, '_X4': True,
                    '_D0': False, '_D1': True, '_D2': False, '_D3': False, '_D4': True}
                   ]
        }

        bdds = update_bdds_without_specification(sequence, i_num_of_variables=1, i_expansion_length=2)

        for key in results.keys():
            self.assertCountEqual(results[key], list(bdds[key]))



