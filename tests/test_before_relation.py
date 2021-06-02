from tests.test_monitor import *
import unittest


class TestBeforeRelation(unittest.TestCase):
    def test_before_1_pass(self):
        sequence = [["begin", 'Boo', 'Data1'], ["end", 'Boo'], ["begin", 3, 'Data2'], ["end", 3]]
        results = {
            'XXYY': [{'_X0': False, '_Y0': True}],
            'XYXY': [],
            'XYYX': []
        }
        bdds = update_bdds_only(sequence, i_num_of_variables=1, i_expansion_length=2)

        for key in results.keys():
            self.assertCountEqual(results[key], list(bdds[key]))


    def test_before_2_pass(self):
        sequence =  [["begin", 7, "Data1"], ["end", 7], ["begin", 2, "Data1"], ["end", 2],
                     ["begin", 3, "Data2"], ["end", 3]]
        results = {
            'XXYY': [{'_X0': False, '_X1': False, '_X2': False, '_Y0': False, '_Y1': False, '_Y2': True},
                     {'_X0': False, '_X1': False, '_X2': False, '_Y0': False, '_Y1': True, '_Y2': False},
                     {'_X0': False, '_X1': False, '_X2': True, '_Y0': False, '_Y1': True, '_Y2': False}],
            'XYXY': [],
            'XYYX': []
        }
        bdds = update_bdds_only(sequence, i_num_of_variables=1, i_expansion_length=2)

        for key in results.keys():
            self.assertCountEqual(results[key], list(bdds[key]))

    def test_before_3_pass(self):
        sequence =  [["begin", 7, "Data1"], ["end", 7], ["begin", 2, "Data1"], ["end", 2],
                     ["begin", 3, "Data2"], ["end", 3], ["begin", 1, "Data1"], ["end", 1]]
        results = {
            'XXYY': [{'_X0': False, '_X1': False, '_X2': False, '_Y0': False, '_Y1': False, '_Y2': True},
                     {'_X0': False, '_X1': False, '_X2': False, '_Y0': False, '_Y1': True, '_Y2': False},
                     {'_X0': False, '_X1': False, '_X2': True, '_Y0': False, '_Y1': True, '_Y2': False},
                     {'_X0': False, '_X1': False, '_X2': False, '_Y0': False, '_Y1': True, '_Y2': True},
                     {'_X0': False, '_X1': False, '_X2': True, '_Y0': False, '_Y1': True, '_Y2': True},
                     {'_X0': False, '_X1': True, '_X2': False, '_Y0': False, '_Y1': True, '_Y2': True}],
            'XYXY': [],
            'XYYX': []
        }
        bdds = update_bdds_only(sequence, i_num_of_variables=1, i_expansion_length=2)

        for key in results.keys():
            self.assertCountEqual(results[key], list(bdds[key]))


a = TestBeforeRelation()
a.test_before_1_pass()
print("dsfsdfsdf")