from tests.test_monitor import *
import unittest


class TestBeforeRelation(unittest.TestCase):
    def test_mixed_1_pass(self):
        sequence = [["begin", 'Dog', "Data1"], ["begin", 'Cat', "Data2"], ["end", 'Cat'],
                    ["end", 'Dog'], ["begin", 'Bird', "Data3"], ["end", 'Bird']]
        results = {
            # In 'XXYY' we merging bot results (dog before bird and cat before bird) into one.
            'XXYY': [{'_X0': False, '_X1': False, '_Y0': False, '_Y1': True, '_Y2': False}],
            'XYXY': [],
            'XYYX': [{'_X0': False, '_X1': False, '_X2': False, '_Y0': False, '_Y1': False, '_Y2': True}]
        }

        bdds = update_bdds_only(sequence, i_num_of_variables=1, i_expansion_length=2)

        for key in results.keys():
            self.assertCountEqual(results[key], list(bdds[key]))

    def test_mixed_2_pass(self):
        sequence =  [["begin", 1, "Data1"], ["begin", 4, "Data1"], ["end", 1],
                     ["begin", 2, "Data2"], ["end", 2], ["end", 4], ["begin", 3, "Data3"], ["end", 3]]
        results = {
            'XXYY': [{'_X0': False, '_X1': False, '_X2': False, '_Y0': False, '_Y1': True, '_Y2': False},
                     {'_X0': False, '_X1': False, '_X2': False, '_Y0': False, '_Y1': True, '_Y2': True},
                     {'_X0': False, '_X1': False, '_X2': True, '_Y0': False, '_Y1': True, '_Y2': True},
                     {'_X0': False, '_X1': True, '_X2': False, '_Y0': False, '_Y1': True, '_Y2': True}],
            'XYXY': [{'_X0': False, '_X1': False, '_X2': False, '_Y0': False, '_Y1': False, '_Y2': True}],
            'XYYX': [{'_X0': False, '_X1': False, '_X2': True, '_Y0': False, '_Y1': True, '_Y2': False}]
        }

        bdds = update_bdds_only(sequence, i_num_of_variables=1, i_expansion_length=2)

        for key in results.keys():
            self.assertCountEqual(results[key], list(bdds[key]))

    def test_mixed_3_pass(self):
        sequence =  [["begin", 1, "Data1"], ["begin", 'F', "Data2"], ["end", 1], ["begin", 2, "Data3"],
                     ["end", 2], ["end", 'F'], ["begin", 3, "Data4"], ["end", 3], ["begin", 'Five', "Data1"],
                     ["begin", 7, "Data10"], ["end", 7], ["begin", 6, "Data1"], ["end", 'Five'], ["end", 6]]
        results = {
            'XXYY': [{'_X0': False, '_X1': False, '_X2': False, '_Y0': False, '_Y1': True, '_Y2': False}, # 1 Before 2
                     {'_X0': False, '_X1': False, '_X2': False, '_Y0': False, '_Y1': True, '_Y2': True}, # 1 Before 3
                     {'_X0': False, '_X1': False, '_X2': False, '_Y0': True, '_Y1': False, '_Y2': False}, # 1 Before Five
                     {'_X0': False, '_X1': False, '_X2': False, '_Y0': True, '_Y1': True, '_Y2': False}, # 1 Before 6
                     {'_X0': False, '_X1': False, '_X2': False, '_Y0': True, '_Y1': False, '_Y2': True}, # 1 Before 7
                     {'_X0': False, '_X1': False, '_X2': True, '_Y0': False, '_Y1': True, '_Y2': True}, # F Before 3
                     {'_X0': False, '_X1': False, '_X2': True, '_Y0': True, '_Y1': False, '_Y2': False}, # F Before Five
                     {'_X0': False, '_X1': False, '_X2': True, '_Y0': True, '_Y1': True, '_Y2': False}, # F Before 6
                     {'_X0': False, '_X1': False, '_X2': True, '_Y0': True, '_Y1': False, '_Y2': True}, # F Before 7
                     {'_X0': False, '_X1': True, '_X2': False, '_Y0': False, '_Y1': True, '_Y2': True}, # 2 Before 3
                     {'_X0': False, '_X1': True, '_X2': False, '_Y0': True, '_Y1': False, '_Y2': False}, # 2 Before Five
                     {'_X0': False, '_X1': True, '_X2': False, '_Y0': True, '_Y1': True, '_Y2': False}, # 2 Before 6
                     {'_X0': False, '_X1': True, '_X2': False, '_Y0': True, '_Y1': False, '_Y2': True}, # 2 Before 7
                     {'_X0': False, '_X1': True, '_X2': True, '_Y0': True, '_Y1': False, '_Y2': False}, # 3 Before Five
                     {'_X0': False, '_X1': True, '_X2': True, '_Y0': True, '_Y1': True, '_Y2': False}, # 3 Before 6
                     {'_X0': False, '_X1': True, '_X2': True, '_Y0': True, '_Y1': False, '_Y2': True}, # 3 Before 7
                     {'_X0': True, '_X1': False, '_X2': True, '_Y0': True, '_Y1': True, '_Y2': False}], # 7 Before 6
            'XYXY': [{'_X0': False, '_X1': False, '_X2': False, '_Y0': False, '_Y1': False, '_Y2': True}, # 1 Overlaps F
                     {'_X0': True, '_X1': False, '_X2': False, '_Y0': True, '_Y1': True, '_Y2': False}], # Five Overlaps 6
            'XYYX': [{'_X0': False, '_X1': False, '_X2': True, '_Y0': False, '_Y1': True, '_Y2': False}, # F Contains 2
                     {'_X0': True, '_X1': False, '_X2': False, '_Y0': True, '_Y1': False, '_Y2': True}] # Five Contains 7
        }

        bdds = update_bdds_only(sequence, i_num_of_variables=1, i_expansion_length=2)

        for key in results.keys():
            self.assertCountEqual(results[key], list(bdds[key]))
