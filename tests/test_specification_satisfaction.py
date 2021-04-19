from tests.test_helper import *
from frontend.parser import parse


class TestSpecificationSatisfaction():
    sequence = [["begin", 1, 'Data1'], ["end", 1], ["begin", 2, 'Data2'], ["end", 2],
                ["begin", 3, 'Data3'], ["begin", 4, 'Data4'], ["end", 4], ["end", 3],
                ["begin", 5, 'Data1'], ["begin", 6, 'Data6'], ["end", 5], ["end", 6]]

    def test_specification_satisfaction_1_pass(self):
        specification = parse("""exist A, B . A("Data1") & B("Data2")""")
        expected_result = True
        current_result = update_bdds_with_specification(TestSpecificationSatisfaction.sequence, specification,
                                                        i_num_of_variables=1)

        assert expected_result == current_result

    def test_specification_satisfaction_1_fail(self):
        specification = parse("""exist A, B . A("Data8") & B("Data2")""")
        expected_result = False
        current_result = update_bdds_with_specification(TestSpecificationSatisfaction.sequence, specification,
                                                        i_num_of_variables=1)

        assert expected_result == current_result

    def test_specification_satisfaction_2_pass(self):
        specification = parse("""exist A, B . A("Data1") & B("Data2") & A < B""")
        expected_result = True
        current_result = update_bdds_with_specification(TestSpecificationSatisfaction.sequence, specification,
                                                        i_num_of_variables=1)

        assert expected_result == current_result

    def test_specification_satisfaction_2_fail(self):
        specification = parse("""exist A, B . A("Data2") & B("Data3") &  B < A""")
        expected_result = False
        current_result = update_bdds_with_specification(TestSpecificationSatisfaction.sequence, specification,
                                                        i_num_of_variables=1)

        assert expected_result == current_result


    def test_specification_satisfaction_3_pass(self):
        specification = parse("""exist A, B, C, G, E . A("Data1") & B("Data2") & C("Data3")
         & A < B & A < C & A < G & A < E""")
        expected_result = True
        current_result = update_bdds_with_specification(TestSpecificationSatisfaction.sequence, specification,
                                                        i_num_of_variables=1)

        assert expected_result == current_result

    def test_specification_satisfaction_3_fail(self):
        specification = parse("""exist A, B, C, G, E . A("Data1") & B("Data2") & C("Data3")
         & A o B & A < C & A < G & A < E""")
        expected_result = False
        current_result = update_bdds_with_specification(TestSpecificationSatisfaction.sequence, specification,
                                                        i_num_of_variables=1)

        assert expected_result == current_result

    def test_specification_satisfaction_4_pass(self):
        specification = parse("""exist A, B . A o B & A("Data1") & B("Data6")""")
        expected_result = True
        current_result = update_bdds_with_specification(TestSpecificationSatisfaction.sequence, specification,
                                                        i_num_of_variables=1)

        assert expected_result == current_result

    def test_specification_satisfaction_4_fail(self):
        specification = parse("""exist A, B . A o B & A("Data6") & B("Data1")""")
        expected_result = False
        current_result = update_bdds_with_specification(TestSpecificationSatisfaction.sequence, specification,
                                                        i_num_of_variables=1)

        assert expected_result == current_result

    def test_specification_satisfaction_5_pass(self):
        specification = parse("""exist A, B, C, G, E . A("Data1") & B("Data2") & C("Data4") & A < B & A < C & G o E""")
        expected_result = True
        current_result = update_bdds_with_specification(TestSpecificationSatisfaction.sequence, specification,
                                                        i_num_of_variables=1)

        assert expected_result == current_result

    def test_specification_satisfaction_5_fail(self):
        specification = parse("""exist A, B, C, G, E . A("Data1") & B("Data2") & C("Data4") & A < B & A < C & G i E""")
        expected_result = True
        current_result = update_bdds_with_specification(TestSpecificationSatisfaction.sequence, specification,
                                                        i_num_of_variables=1)

        assert expected_result == current_result

    def test_specification_satisfaction_6_pass(self):
        specification = parse("""exist A, B, C, G, E . A("Data1") & B("Data2") & C("Data4")
         & A < B & A < C & G o E & E("Data6")""")
        expected_result = True
        current_result = update_bdds_with_specification(TestSpecificationSatisfaction.sequence, specification,
                                                        i_num_of_variables=1)

        assert expected_result == current_result

    def test_specification_satisfaction_6_fail(self):
        specification = parse("""exist A, B, C, G, E . A("Data1") & B("Data2") & C("Data4")
         & A < B & A < C & G o E & E("Data5")""")
        expected_result = False
        current_result = update_bdds_with_specification(TestSpecificationSatisfaction.sequence, specification,
                                                        i_num_of_variables=1)

        assert expected_result == current_result

    def test_specification_satisfaction_7_pass(self):
        specification = parse("""exist A, B, C, G, E . A("Data1") & B("Data2") & C("Data4")
         & A < B & A < C & G o E & E("Data6") & G("Data1")""")
        expected_result = True
        current_result = update_bdds_with_specification(TestSpecificationSatisfaction.sequence, specification,
                                                        i_num_of_variables=1)

        assert expected_result == current_result

    def test_specification_satisfaction_7_fail(self):
        specification = parse("""exist A, B, C, G, E . A("Data1") & B("Data2") & C("Data4")
         & A < B & A < C & G o E & E("Data6") & G("Data5")""")
        expected_result = False
        current_result = update_bdds_with_specification(TestSpecificationSatisfaction.sequence, specification,
                                                        i_num_of_variables=1)

        assert expected_result == current_result

    def test_specification_satisfaction_8_pass(self):
        specification = parse("""exist A, B . A i B & A("Data3") & B("Data4")""")
        expected_result = True
        current_result = update_bdds_with_specification(TestSpecificationSatisfaction.sequence, specification,
                                                        i_num_of_variables=1)

        assert expected_result == current_result

    def test_specification_satisfaction_8_fail(self):
        specification = parse("""exist A, B . A i B & A("Data4") & B("Data3")""")
        expected_result = False
        current_result = update_bdds_with_specification(TestSpecificationSatisfaction.sequence, specification,
                                                        i_num_of_variables=1)

        assert expected_result == current_result

    def test_specification_satisfaction_9_pass(self):
        specification = parse("""exist A, B . same(A, B) & A("Data1")""")
        expected_result = True
        current_result = update_bdds_with_specification(TestSpecificationSatisfaction.sequence, specification,
                                                        i_num_of_variables=1)

        assert expected_result == current_result

    def test_specification_satisfaction_10_pass(self):
        specification = parse("""exist A, B . same(A, B) & A("Data2")""")
        expected_result = True
        current_result = update_bdds_with_specification(TestSpecificationSatisfaction.sequence, specification,
                                                        i_num_of_variables=1)

        assert expected_result == current_result

    def test_specification_satisfaction_11_pass(self):
        specification = parse("""exist A, B . same(A, B) & A("Data1") & A < B""")
        expected_result = True
        current_result = update_bdds_with_specification(TestSpecificationSatisfaction.sequence, specification,
                                                        i_num_of_variables=1)

        assert expected_result == current_result

    def test_specification_satisfaction_11_fail(self):
        specification = parse("""exist A, B . same(A, B) & A("Data2") & A < B""")
        expected_result = False
        current_result = update_bdds_with_specification(TestSpecificationSatisfaction.sequence, specification,
                                                        i_num_of_variables=1)

        assert expected_result == current_result

    def test_specification_satisfaction_12_pass(self):
        specification = parse("""exist A, B . A("Data1") & A < B | A("Data6") & A < B""")
        expected_result = True
        current_result = update_bdds_with_specification(TestSpecificationSatisfaction.sequence, specification,
                                                        i_num_of_variables=1)
        assert expected_result == current_result

    def test_specification_satisfaction_12_fail(self):
        specification = parse("""exist A, B . A("Data5") & A < B | A("Data6") & A < B""")
        expected_result = False
        current_result = update_bdds_with_specification(TestSpecificationSatisfaction.sequence, specification,
                                                        i_num_of_variables=1)
        assert expected_result == current_result

    def test_specification_satisfaction_13_pass(self):
        specification = parse("""exist A, B . !(A("Data6") & A < B)""")
        expected_result = True
        current_result = update_bdds_with_specification(TestSpecificationSatisfaction.sequence, specification,
                                                        i_num_of_variables=1)
        assert expected_result == current_result

    def test_specification_satisfaction_14_pass(self):
        specification = parse("""exist A, B . A("Data6") & !A < B""")
        expected_result = True
        current_result = update_bdds_with_specification(TestSpecificationSatisfaction.sequence, specification,
                                                        i_num_of_variables=1)
        assert expected_result == current_result

    def test_specification_satisfaction_14_fail(self):
        specification = parse("""exist A, B . (A("Data6") & !!A < B)""")
        expected_result = False
        current_result = update_bdds_with_specification(TestSpecificationSatisfaction.sequence, specification,
                                                        i_num_of_variables=1)
        assert expected_result == current_result

    def test_specification_satisfaction_15_pass(self):
        specification = parse("""exist A, B, C . !(A o B & B o C)""")
        expected_result = True
        current_result = update_bdds_with_specification(TestSpecificationSatisfaction.sequence, specification,
                                                        i_num_of_variables=1)
        assert expected_result == current_result

    def test_specification_satisfaction_15_fail(self):
        specification = parse("""exist A, B, C . A o B & B o C""")
        expected_result = False
        current_result = update_bdds_with_specification(TestSpecificationSatisfaction.sequence, specification,
                                                        i_num_of_variables=1)
        assert expected_result == current_result
