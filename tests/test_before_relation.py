from tests.test_helper import *
import unittest


class TestBeforeRelation(unittest.TestCase):
    def test_before_1_pass(self):
        sequence = [["begin", 'Boo', 'Data1'], ["end", 'Boo'], ["begin", 3, 'Data2'], ["end", 3]]
        results = {
            'XXYY': [{'X0': False, 'Y0': True}],
            'XYXY': [],
            'XYYX': []
        }
        bdds = update_bdds(sequence, i_num_of_variables=1)

        for key in results.keys():
            self.assertCountEqual(results[key], list(bdds[key]))


    def test_before_2_pass(self):
        sequence =  [["begin", 7, "Data1"], ["end", 7], ["begin", 2, "Data1"], ["end", 2],
                     ["begin", 3, "Data2"], ["end", 3]]
        results = {
            'XXYY': [{'X0': False, 'X1': False, 'X2': False, 'Y0': False, 'Y1': False, 'Y2': True},
                     {'X0': False, 'X1': False, 'X2': False, 'Y0': False, 'Y1': True, 'Y2': False},
                     {'X0': False, 'X1': False, 'X2': True, 'Y0': False, 'Y1': True, 'Y2': False}],
            'XYXY': [],
            'XYYX': []
        }
        bdds = update_bdds(sequence, i_num_of_variables=1)

        for key in results.keys():
            self.assertCountEqual(results[key], list(bdds[key]))

    def test_before_3_pass(self):
        sequence =  [["begin", 7, "Data1"], ["end", 7], ["begin", 2, "Data1"], ["end", 2],
                     ["begin", 3, "Data2"], ["end", 3], ["begin", 1, "Data1"], ["end", 1]]
        results = {
            'XXYY': [{'X0': False, 'X1': False, 'X2': False, 'Y0': False, 'Y1': False, 'Y2': True},
                     {'X0': False, 'X1': False, 'X2': False, 'Y0': False, 'Y1': True, 'Y2': False},
                     {'X0': False, 'X1': False, 'X2': True, 'Y0': False, 'Y1': True, 'Y2': False},
                     {'X0': False, 'X1': False, 'X2': False, 'Y0': False, 'Y1': True, 'Y2': True},
                     {'X0': False, 'X1': False, 'X2': True, 'Y0': False, 'Y1': True, 'Y2': True},
                     {'X0': False, 'X1': True, 'X2': False, 'Y0': False, 'Y1': True, 'Y2': True}],
            'XYXY': [],
            'XYYX': []
        }
        bdds = update_bdds(sequence, i_num_of_variables=1)

        for key in results.keys():
            self.assertCountEqual(results[key], list(bdds[key]))

