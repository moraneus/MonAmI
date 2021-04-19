from tests.test_helper import *
import unittest


class TestBeforeRelation(unittest.TestCase):
    def test_mixed_1_pass(self):
        sequence = [["begin", 'Dog', "Data1"], ["begin", 'Cat', "Data2"], ["end", 'Cat'],
                    ["end", 'Dog'], ["begin", 'Bird', "Data3"], ["end", 'Bird']]
        results = {
            # In 'XXYY' we merging bot results (dog before bird and cat before bird) into one.
            'XXYY': [{'X0': False, 'X1': False, 'Y0': False, 'Y1': True, 'Y2': False}],
            'XYXY': [],
            'XYYX': [{'X0': False, 'X1': False, 'X2': False, 'Y0': False, 'Y1': False, 'Y2': True}]
        }

        bdds = update_bdds_without_specification(sequence, i_num_of_variables=1, i_expansion_length=2)

        for key in results.keys():
            self.assertCountEqual(results[key], list(bdds[key]))

    def test_mixed_2_pass(self):
        sequence =  [["begin", 1, "Data1"], ["begin", 4, "Data1"], ["end", 1],
                     ["begin", 2, "Data2"], ["end", 2], ["end", 4], ["begin", 3, "Data3"], ["end", 3]]
        results = {
            'XXYY': [{'X0': False, 'X1': False, 'X2': False, 'Y0': False, 'Y1': True, 'Y2': False},
                     {'X0': False, 'X1': False, 'X2': False, 'Y0': False, 'Y1': True, 'Y2': True},
                     {'X0': False, 'X1': False, 'X2': True, 'Y0': False, 'Y1': True, 'Y2': True},
                     {'X0': False, 'X1': True, 'X2': False, 'Y0': False, 'Y1': True, 'Y2': True}],
            'XYXY': [{'X0': False, 'X1': False, 'X2': False, 'Y0': False, 'Y1': False, 'Y2': True}],
            'XYYX': [{'X0': False, 'X1': False, 'X2': True, 'Y0': False, 'Y1': True, 'Y2': False}]
        }

        bdds = update_bdds_without_specification(sequence, i_num_of_variables=1, i_expansion_length=2)

        for key in results.keys():
            self.assertCountEqual(results[key], list(bdds[key]))

    def test_mixed_3_pass(self):
        sequence =  [["begin", 1, "Data1"], ["begin", 'F', "Data2"], ["end", 1], ["begin", 2, "Data3"],
                     ["end", 2], ["end", 'F'], ["begin", 3, "Data4"], ["end", 3], ["begin", 'Five', "Data1"],
                     ["begin", 7, "Data10"], ["end", 7], ["begin", 6, "Data1"], ["end", 'Five'], ["end", 6]]
        results = {
            'XXYY': [{'X0': False, 'X1': False, 'X2': False, 'Y0': False, 'Y1': True, 'Y2': False}, # 1 Before 2
                     {'X0': False, 'X1': False, 'X2': False, 'Y0': False, 'Y1': True, 'Y2': True}, # 1 Before 3
                     {'X0': False, 'X1': False, 'X2': False, 'Y0': True, 'Y1': False, 'Y2': False}, # 1 Before Five
                     {'X0': False, 'X1': False, 'X2': False, 'Y0': True, 'Y1': True, 'Y2': False}, # 1 Before 6
                     {'X0': False, 'X1': False, 'X2': False, 'Y0': True, 'Y1': False, 'Y2': True}, # 1 Before 7
                     {'X0': False, 'X1': False, 'X2': True, 'Y0': False, 'Y1': True, 'Y2': True}, # F Before 3
                     {'X0': False, 'X1': False, 'X2': True, 'Y0': True, 'Y1': False, 'Y2': False}, # F Before Five
                     {'X0': False, 'X1': False, 'X2': True, 'Y0': True, 'Y1': True, 'Y2': False}, # F Before 6
                     {'X0': False, 'X1': False, 'X2': True, 'Y0': True, 'Y1': False, 'Y2': True}, # F Before 7
                     {'X0': False, 'X1': True, 'X2': False, 'Y0': False, 'Y1': True, 'Y2': True}, # 2 Before 3
                     {'X0': False, 'X1': True, 'X2': False, 'Y0': True, 'Y1': False, 'Y2': False}, # 2 Before Five
                     {'X0': False, 'X1': True, 'X2': False, 'Y0': True, 'Y1': True, 'Y2': False}, # 2 Before 6
                     {'X0': False, 'X1': True, 'X2': False, 'Y0': True, 'Y1': False, 'Y2': True}, # 2 Before 7
                     {'X0': False, 'X1': True, 'X2': True, 'Y0': True, 'Y1': False, 'Y2': False}, # 3 Before Five
                     {'X0': False, 'X1': True, 'X2': True, 'Y0': True, 'Y1': True, 'Y2': False}, # 3 Before 6
                     {'X0': False, 'X1': True, 'X2': True, 'Y0': True, 'Y1': False, 'Y2': True}, # 3 Before 7
                     {'X0': True, 'X1': False, 'X2': True, 'Y0': True, 'Y1': True, 'Y2': False}], # 7 Before 6
            'XYXY': [{'X0': False, 'X1': False, 'X2': False, 'Y0': False, 'Y1': False, 'Y2': True}, # 1 Overlaps F
                     {'X0': True, 'X1': False, 'X2': False, 'Y0': True, 'Y1': True, 'Y2': False}], # Five Overlaps 6
            'XYYX': [{'X0': False, 'X1': False, 'X2': True, 'Y0': False, 'Y1': True, 'Y2': False}, # F Contains 2
                     {'X0': True, 'X1': False, 'X2': False, 'Y0': True, 'Y1': False, 'Y2': True}] # Five Contains 7
        }

        bdds = update_bdds_without_specification(sequence, i_num_of_variables=1, i_expansion_length=2)

        for key in results.keys():
            self.assertCountEqual(results[key], list(bdds[key]))
