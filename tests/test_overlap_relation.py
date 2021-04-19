from tests.test_helper import *
import unittest


class TestBeforeRelation(unittest.TestCase):
    def test_overlaps_1_pass(self):
        sequence = [["begin", 1, "Data1"], ["begin", 3, "Data1"], ["end", 1], ["end", 3]]
        results = {
            'XXYY': [],
            'XYXY': [{'X0': False, 'Y0': True}],
            'XYYX': []
        }

        bdds = update_bdds_without_specification(sequence, i_num_of_variables=1, i_expansion_length=2)

        for key in results.keys():
            self.assertCountEqual(results[key], list(bdds[key]))

    def test_overlaps_2_pass(self):
        sequence =  [["begin", 1, "Data1"], ["begin", 2, "Data1"], ["begin", 3, "Data2"], ["end", 1], ["end", 2], ["end", 3]]
        results = {
            'XXYY': [],
            'XYXY': [{'X0': False, 'X1': False, 'X2': False, 'Y0': False, 'Y1': True, 'Y2': False},
                     {'X0': False, 'X1': False, 'X2': False, 'Y0': False, 'Y1': False, 'Y2': True},
                     {'X0': False, 'X1': False, 'X2': True, 'Y0': False, 'Y1': True, 'Y2': False}],
            'XYYX': []
        }

        bdds = update_bdds_without_specification(sequence, i_num_of_variables=1, i_expansion_length=2)

        for key in results.keys():
            self.assertCountEqual(results[key], list(bdds[key]))
