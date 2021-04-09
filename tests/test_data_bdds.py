from tests.test_helper import *
import unittest


class TestDataBdds(unittest.TestCase):
    def test_data_1_all_data_is_the_same_interval_and_data_not_extended(self):
        sequence = [["begin", 'Boo', 'Data1'], ["end", 'Boo'], ["begin", 3, 'Data1'], ["end", 3]]
        results = {
            'XD': [{'D0': False}]
        }

        bdds = update_bdds(sequence, i_num_of_variables=1)

        for key in results.keys():
            self.assertCountEqual(results[key], list(bdds[key]))

    def test_data_2_all_data_is_the_same_interval_is_extended_data_is_not(self):
        sequence = [["begin", 1, 'Data1'], ["end", 1], ["begin", 2, 'Data1'], ["end", 2],
                    ["begin", 3, 'Data1'], ["end", 3]]
        results = {
            'XD': [{'X0': False, 'X1':False, 'X2': False, 'D0': False},
                   {'X0': False, 'X1': False, 'X2': True, 'D0': False},
                   {'X0': False, 'X1': True, 'X2': False, 'D0': False}]
        }

        bdds = update_bdds(sequence, i_num_of_variables=1)

        for key in results.keys():
            self.assertCountEqual(results[key], list(bdds[key]))

    def test_data_3_all_data_is_the_same_interval_is_extended_data_is_not(self):
        sequence = [["begin", 'Boo', 'Data1'], ["end", 'Boo'], ["begin", 3, 'Data1'], ["end", 3],
                    ["begin", 2, "Data1"], ["end", 2], ["begin", 4, "Data1"], ["end", 4]]
        results = {
            'XD': [{'X0': False, 'D0': False}]
        }

        bdds = update_bdds(sequence, i_num_of_variables=1)

        for key in results.keys():
            self.assertCountEqual(results[key], list(bdds[key]))


    def test_data_4_all_data_is_not_the_same_interval_and_data_is_not_extended(self):
        sequence = [["begin", 1, 'Data1'], ["end", 1], ["begin", 2, 'Data2'], ["end", 2]]
        results = {
            'XD': [{'X0': False, 'D0': False},
                   {'X0': True, 'D0': True}]
        }

        bdds = update_bdds(sequence, i_num_of_variables=1)

        for key in results.keys():
            self.assertCountEqual(results[key], list(bdds[key]))

    def test_data_5_data_is_not_the_same_interval_and_data_is_extended(self):
        sequence = [["begin", 1, 'Data1'], ["end", 1], ["begin", 2, 'Data2'], ["end", 2],
                    ["begin", 3, "Data3"], ["end", 3]]
        results = {
            'XD': [{'X0': False, 'X1': False, 'X2': False, 'D0': False, 'D1': False, 'D2': False},
                   {'X0': False, 'X1': False, 'X2': True,'D0': False, 'D1': False, 'D2': True},
                   {'X0': False, 'X1': True, 'X2': False, 'D0': False, 'D1': True, 'D2': False}]
        }

        bdds = update_bdds(sequence, i_num_of_variables=1)

        for key in results.keys():
            self.assertCountEqual(results[key], list(bdds[key]))

    def test_data_6_all_data_is_not_the_same_interval_and_data_is_extended(self):
        sequence = [["begin", 1, 'Data1'], ["end", 1], ["begin", 2, 'Data2'], ["end", 2],
                    ["begin", 3, "Data3"], ["end", 3]]
        results = {
            'XD': [{'X0': False, 'X1': False, 'X2': False, 'D0': False, 'D1': False, 'D2': False},
                   {'X0': False, 'X1': False, 'X2': True,'D0': False, 'D1': False, 'D2': True},
                   {'X0': False, 'X1': True, 'X2': False, 'D0': False, 'D1': True, 'D2': False}]
        }

        bdds = update_bdds(sequence, i_num_of_variables=1)

        for key in results.keys():
            self.assertCountEqual(results[key], list(bdds[key]))

    def test_data_7_all_data_is_not_the_same_interval_and_data_is_extended(self):
        sequence = [["begin", 1, 'Data1'], ["end", 1], ["begin", 2, 'Data2'], ["end", 2],
                    ["begin", 3, "Data3"], ["end", 3], ["begin", 4, "Data4"], ["end", 4],
                    ["begin", 5, "Data5"], ["end", 5], ["begin", 6, "Data6"], ["end", 6],
                    ["begin", 7, "Data7"], ["end", 7], ["begin", 8, "Data8"], ["end", 8],
                    ["begin", 9, "Data9"], ["end", 9], ["begin", 10, "Data10"], ["end", 10]]
        results = {
            'XD': [{'X0': False, 'X1': False, 'X2': False, 'X3': False, 'X4': False,
                    'D0': False, 'D1': False, 'D2': False, 'D3': False, 'D4': False},
                   {'X0': False, 'X1': False, 'X2': False, 'X3': False, 'X4': True,
                    'D0': False, 'D1': False, 'D2': False, 'D3': False, 'D4': True},
                   {'X0': False, 'X1': False, 'X2': False, 'X3': True, 'X4': False,
                    'D0': False, 'D1': False, 'D2': False, 'D3': True, 'D4': False},
                   {'X0': False, 'X1': False, 'X2': False, 'X3': True, 'X4': True,
                    'D0': False, 'D1': False, 'D2': False, 'D3': True, 'D4': True},
                   {'X0': False, 'X1': False, 'X2': True, 'X3': False, 'X4': False,
                    'D0': False, 'D1': False, 'D2': True, 'D3': False, 'D4': False},
                   {'X0': False, 'X1': False, 'X2': True, 'X3': False, 'X4': True,
                    'D0': False, 'D1': False, 'D2': True, 'D3': False, 'D4': True},
                   {'X0': False, 'X1': False, 'X2': True, 'X3': True, 'X4': False,
                    'D0': False, 'D1': False, 'D2': True, 'D3': True, 'D4': False},
                   {'X0': False, 'X1': False, 'X2': True, 'X3': True, 'X4': True,
                    'D0': False, 'D1': False, 'D2': True, 'D3': True, 'D4': True},
                   {'X0': False, 'X1': True, 'X2': False, 'X3': False, 'X4': False,
                    'D0': False, 'D1': True, 'D2': False, 'D3': False, 'D4': False},
                   {'X0': False, 'X1': True, 'X2': False, 'X3': False, 'X4': True,
                    'D0': False, 'D1': True, 'D2': False, 'D3': False, 'D4': True}
                   ]
        }

        bdds = update_bdds(sequence, i_num_of_variables=1)

        for key in results.keys():
            self.assertCountEqual(results[key], list(bdds[key]))



