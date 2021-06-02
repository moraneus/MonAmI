from tests.test_monitor import *
import unittest


class TestBeforeRelation(unittest.TestCase):
    def test_overlaps_1_pass(self):
        sequence = [["begin", 1, "Data1"], ["begin", 3, "Data1"], ["end", 1], ["end", 3]]
        results = {
            'XXYY': [],
            'XYXY': [{'_X0': False, '_Y0': True}],
            'XYYX': []
        }

        bdds = update_bdds_only(sequence, i_num_of_variables=1, i_expansion_length=2)

        for key in results.keys():
            self.assertCountEqual(results[key], list(bdds[key]))

    def test_overlaps_2_pass(self):
        sequence =  [["begin", 1, "Data1"], ["begin", 2, "Data1"], ["begin", 3, "Data2"], ["end", 1], ["end", 2], ["end", 3]]
        results = {
            'XXYY': [],
            'XYXY': [{'_X0': False, '_X1': False, '_X2': False, '_Y0': False, '_Y1': True, '_Y2': False},
                     {'_X0': False, '_X1': False, '_X2': False, '_Y0': False, '_Y1': False, '_Y2': True},
                     {'_X0': False, '_X1': False, '_X2': True, '_Y0': False, '_Y1': True, '_Y2': False}],
            'XYYX': []
        }

        bdds = update_bdds_only(sequence, i_num_of_variables=1, i_expansion_length=2)

        for key in results.keys():
            self.assertCountEqual(results[key], list(bdds[key]))
