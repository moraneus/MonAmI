from tests.test_monitor import *
import unittest


class TestDuringRelation(unittest.TestCase):
    def test_during_1_pass(self):
        sequence = [["begin", 1, 'Data1'], ["begin", 'M', 'Data1'], ["end", 'M'], ["end", 1]]
        results = {
            'XXYY': [],
            'XYXY': [],
            'XYYX': [{'_X0': False, '_Y0': True}]
        }

        bdds = update_bdds_only(sequence, i_num_of_variables=1, i_expansion_length=2)

        for key in results.keys():
            self.assertCountEqual(results[key], list(bdds[key]))


    def test_during_2_pass(self):
        sequence =  [["begin", 'One', 'Data1'], ["begin", 'TWO', 'Data2'], ["begin", 3, 'Data1'], ["end", 3], ["end", 'TWO'], ["end", 'One']]
        results = {
            'XXYY': [],
            'XYXY': [],
            'XYYX': [{'_X0': False, '_X1': False, '_X2': False, '_Y0': False, '_Y1': False, '_Y2': True},
                     {'_X0': False, '_X1': False, '_X2': False, '_Y0': False, '_Y1': True, '_Y2': False},
                     {'_X0': False, '_X1': False, '_X2': True, '_Y0': False, '_Y1': True, '_Y2': False}]
        }

        bdds = update_bdds_only(sequence, i_num_of_variables=1, i_expansion_length=2)

        for key in results.keys():
            self.assertCountEqual(results[key], list(bdds[key]))


    def test_during_3_pass(self):
        sequence =  [["begin", 'One', 'Data1'], ["begin", 'TWO', 'Data2'], ["begin", 3, 'Data1'],
                     ["begin", 4, "Data4"], ["end", 4], ["end", 3], ["end", 'TWO'], ["end", 'One']]
        results = {
            'XXYY': [],
            'XYXY': [],
            'XYYX': [{'_X0': False, '_X1': False, '_X2': False, '_Y0': False, '_Y1': False, '_Y2': True},
                     {'_X0': False, '_X1': False, '_X2': False, '_Y0': False, '_Y1': True, '_Y2': False},
                     {'_X0': False, '_X1': False, '_X2': False, '_Y0': False, '_Y1': True, '_Y2': True},
                     {'_X0': False, '_X1': False, '_X2': True, '_Y0': False, '_Y1': True, '_Y2': False},
                     {'_X0': False, '_X1': False, '_X2': True, '_Y0': False, '_Y1': True, '_Y2': True},
                     {'_X0': False, '_X1': True, '_X2': False, '_Y0': False, '_Y1': True, '_Y2': True}]
        }

        bdds = update_bdds_only(sequence, i_num_of_variables=1, i_expansion_length=2)

        for key in results.keys():
            self.assertCountEqual(results[key], list(bdds[key]))

