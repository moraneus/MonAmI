from tests.test_helper import *
import unittest


class TestDuringRelation(unittest.TestCase):
    def test_during_1_pass(self):
        sequence = [["begin", 1, 'Data1'], ["begin", 'M', 'Data1'], ["end", 'M'], ["end", 1]]
        results = {
            'XXYY': [],
            'XYXY': [],
            'XYYX': [{'X0': False, 'Y0': True}]
        }

        bdds = update_bdds_without_specification(sequence, i_num_of_variables=1, i_expansion_length=2)

        for key in results.keys():
            self.assertCountEqual(results[key], list(bdds[key]))


    def test_during_2_pass(self):
        sequence =  [["begin", 'One', 'Data1'], ["begin", 'TWO', 'Data2'], ["begin", 3, 'Data1'], ["end", 3], ["end", 'TWO'], ["end", 'One']]
        results = {
            'XXYY': [],
            'XYXY': [],
            'XYYX': [{'X0': False, 'X1': False, 'X2': False, 'Y0': False, 'Y1': False, 'Y2': True},
                     {'X0': False, 'X1': False, 'X2': False, 'Y0': False, 'Y1': True, 'Y2': False},
                     {'X0': False, 'X1': False, 'X2': True, 'Y0': False, 'Y1': True, 'Y2': False}]
        }

        bdds = update_bdds_without_specification(sequence, i_num_of_variables=1, i_expansion_length=2)

        for key in results.keys():
            self.assertCountEqual(results[key], list(bdds[key]))


    def test_during_3_pass(self):
        sequence =  [["begin", 'One', 'Data1'], ["begin", 'TWO', 'Data2'], ["begin", 3, 'Data1'],
                     ["begin", 4, "Data4"], ["end", 4], ["end", 3], ["end", 'TWO'], ["end", 'One']]
        results = {
            'XXYY': [],
            'XYXY': [],
            'XYYX': [{'X0': False, 'X1': False, 'X2': False, 'Y0': False, 'Y1': False, 'Y2': True},
                     {'X0': False, 'X1': False, 'X2': False, 'Y0': False, 'Y1': True, 'Y2': False},
                     {'X0': False, 'X1': False, 'X2': False, 'Y0': False, 'Y1': True, 'Y2': True},
                     {'X0': False, 'X1': False, 'X2': True, 'Y0': False, 'Y1': True, 'Y2': False},
                     {'X0': False, 'X1': False, 'X2': True, 'Y0': False, 'Y1': True, 'Y2': True},
                     {'X0': False, 'X1': True, 'X2': False, 'Y0': False, 'Y1': True, 'Y2': True}]
        }

        bdds = update_bdds_without_specification(sequence, i_num_of_variables=1, i_expansion_length=2)

        for key in results.keys():
            self.assertCountEqual(results[key], list(bdds[key]))

