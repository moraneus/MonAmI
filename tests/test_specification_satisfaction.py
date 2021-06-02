from tests.test_monitor import *
from frontend.parser import parse


class TestSpecificationSatisfaction():
    sequence = [["begin", 1, 'Data1'], ["end", 1], ["begin", 2, 'Data2'], ["end", 2],
                ["begin", 3, 'Data3'], ["begin", 4, 'Data4'], ["end", 4], ["end", 3],
                ["begin", 5, 'Data1'], ["begin", 6, 'Data6'], ["end", 5], ["end", 6]]

    def test_specification_satisfaction_1_pass(self):
        specification = parse("""exist A, B . A("Data1") & B("Data2")""")
        expected_result = True
        current_result = monitor(TestSpecificationSatisfaction.sequence, specification,
                                 i_num_of_variables=1)

        assert expected_result == current_result[0]

    def test_specification_satisfaction_2_fail(self):
        specification = parse("""exist A, B . A("Data8") & B("Data2")""")
        expected_result = False
        current_result = monitor(TestSpecificationSatisfaction.sequence, specification,
                                 i_num_of_variables=1)

        assert expected_result == current_result[0]

    def test_specification_satisfaction_3_pass(self):
        specification = parse("""exist A, B . A("Data1") & B("Data2") & A < B""")
        expected_result = True
        current_result = monitor(TestSpecificationSatisfaction.sequence, specification,
                                 i_num_of_variables=1)

        assert expected_result == current_result[0]

    def test_specification_satisfaction_4_fail(self):
        specification = parse("""exist A, B . A("Data2") & B("Data3") &  B < A""")
        expected_result = False
        current_result = monitor(TestSpecificationSatisfaction.sequence, specification,
                                 i_num_of_variables=1)

        assert expected_result == current_result[0]

    def test_specification_satisfaction_5_pass(self):
        specification = parse("""exist A, B, C, D, E . A("Data1") & B("Data2") & C("Data3")
         & A < B & A < C & A < D & A < E""")
        expected_result = True
        current_result = monitor(TestSpecificationSatisfaction.sequence, specification,
                                 i_num_of_variables=1)

        assert expected_result == current_result[0]

    def test_specification_satisfaction_6_fail(self):
        specification = parse("""exist A, B, C, D, E . A("Data1") & B("Data2") & C("Data3")
         & A o B & A < C & A < D & A < E""")
        expected_result = False
        current_result = monitor(TestSpecificationSatisfaction.sequence, specification,
                                 i_num_of_variables=1)

        assert expected_result == current_result[0]

    def test_specification_satisfaction_7_pass(self):
        specification = parse("""exist A, B . A o B & A("Data1") & B("Data6")""")
        expected_result = True
        current_result = monitor(TestSpecificationSatisfaction.sequence, specification,
                                 i_num_of_variables=1)

        assert expected_result == current_result[0]

    def test_specification_satisfaction_8_fail(self):
        specification = parse("""exist A, B . A o B & A("Data6") & B("Data1")""")
        expected_result = False
        current_result = monitor(TestSpecificationSatisfaction.sequence, specification,
                                 i_num_of_variables=1)

        assert expected_result == current_result[0]

    def test_specification_satisfaction_9_pass(self):
        specification = parse("""exist A, B, C, D, E . A("Data1") & B("Data2") & C("Data4") & A < B & A < C & D o E""")
        expected_result = True
        current_result = monitor(TestSpecificationSatisfaction.sequence, specification,
                                 i_num_of_variables=1)

        assert expected_result == current_result[0]

    def test_specification_satisfaction_10_fail(self):
        specification = parse("""exist A, B, C, D, E . A("Data1") & B("Data2") & C("Data4") & A < B & A < C & D i E""")
        expected_result = True
        current_result = monitor(TestSpecificationSatisfaction.sequence, specification,
                                 i_num_of_variables=1)

        assert expected_result == current_result[0]

    def test_specification_satisfaction_11_pass(self):
        specification = parse("""exist A, B, C, D, E . A("Data1") & B("Data2") & C("Data4")
         & A < B & A < C & D o E & E("Data6")""")
        expected_result = True
        current_result = monitor(TestSpecificationSatisfaction.sequence, specification,
                                 i_num_of_variables=1)

        assert expected_result == current_result[0]

    def test_specification_satisfaction_12_fail(self):
        specification = parse("""exist A, B, C, D, E . A("Data1") & B("Data2") & C("Data4")
         & A < B & A < C & D o E & E("Data5")""")
        expected_result = False
        current_result = monitor(TestSpecificationSatisfaction.sequence, specification,
                                 i_num_of_variables=1)

        assert expected_result == current_result[0]

    def test_specification_satisfaction_13_pass(self):
        specification = parse("""exist A, B, C, D, E . A("Data1") & B("Data2") & C("Data4")
         & A < B & A < C & D o E & E("Data6") & D("Data1")""")
        expected_result = True
        current_result = monitor(TestSpecificationSatisfaction.sequence, specification,
                                 i_num_of_variables=1)

        assert expected_result == current_result[0]

    def test_specification_satisfaction_14_fail(self):
        specification = parse("""exist A, B, C, D, E . A("Data1") & B("Data2") & C("Data4")
         & A < B & A < C & D o E & E("Data6") & D("Data5")""")
        expected_result = False
        current_result = monitor(TestSpecificationSatisfaction.sequence, specification,
                                 i_num_of_variables=1)

        assert expected_result == current_result[0]

    def test_specification_satisfaction_15_pass(self):
        specification = parse("""exist A, B . A i B & A("Data3") & B("Data4")""")
        expected_result = True
        current_result = monitor(TestSpecificationSatisfaction.sequence, specification,
                                 i_num_of_variables=1)

        assert expected_result == current_result[0]

    def test_specification_satisfaction_16_fail(self):
        specification = parse("""exist A, B . A i B & A("Data4") & B("Data3")""")
        expected_result = False
        current_result = monitor(TestSpecificationSatisfaction.sequence, specification,
                                 i_num_of_variables=1)

        assert expected_result == current_result[0]

    def test_specification_satisfaction_17_pass(self):
        specification = parse("""exist A, B . same(A, B) & A("Data1")""")
        expected_result = True
        current_result = monitor(TestSpecificationSatisfaction.sequence, specification,
                                 i_num_of_variables=1)

        assert expected_result == current_result[0]

    def test_specification_satisfaction_18_pass(self):
        specification = parse("""exist A, B . same(A, B) & A("Data2")""")
        expected_result = True
        current_result = monitor(TestSpecificationSatisfaction.sequence, specification,
                                 i_num_of_variables=1)

        assert expected_result == current_result[0]

    def test_specification_satisfaction_19_pass(self):
        specification = parse("""exist A, B . same(A, B) & A("Data1") & A < B""")
        expected_result = True
        current_result = monitor(TestSpecificationSatisfaction.sequence, specification,
                                 i_num_of_variables=1)

        assert expected_result == current_result[0]

    def test_specification_satisfaction_20_fail(self):
        specification = parse("""exist A, B . same(A, B) & A("Data2") & A < B""")
        expected_result = False
        current_result = monitor(TestSpecificationSatisfaction.sequence, specification,
                                 i_num_of_variables=1)

        assert expected_result == current_result[0]

    def test_specification_satisfaction_21_pass(self):
        specification = parse("""exist A, B . A("Data1") & A < B | A("Data6") & A < B""")
        expected_result = True
        current_result = monitor(TestSpecificationSatisfaction.sequence, specification,
                                 i_num_of_variables=1)
        assert expected_result == current_result[0]

    def test_specification_satisfaction_22_fail(self):
        specification = parse("""exist A, B . A("Data5") & A < B | A("Data6") & A < B""")
        expected_result = False
        current_result = monitor(TestSpecificationSatisfaction.sequence, specification,
                                 i_num_of_variables=1)
        assert expected_result == current_result[0]

    def test_specification_satisfaction_23_pass(self):
        specification = parse("""exist A, B . !(A("Data6") & A < B)""")
        expected_result = True
        current_result = monitor(TestSpecificationSatisfaction.sequence, specification,
                                 i_num_of_variables=1)
        assert expected_result == current_result[0]

    def test_specification_satisfaction_24_pass(self):
        specification = parse("""exist A, B . A("Data6") & !A < B""")
        expected_result = True
        current_result = monitor(TestSpecificationSatisfaction.sequence, specification,
                                 i_num_of_variables=1)
        assert expected_result == current_result[0]

    def test_specification_satisfaction_25_fail(self):
        specification = parse("""exist A, B . (A("Data6") & !!A < B)""")
        expected_result = False
        current_result = monitor(TestSpecificationSatisfaction.sequence, specification,
                                 i_num_of_variables=1)
        assert expected_result == current_result[0]

    def test_specification_satisfaction_26_pass(self):
        specification = parse("""exist A, B, C . !(A o B & B o C)""")
        expected_result = True
        current_result = monitor(TestSpecificationSatisfaction.sequence, specification,
                                 i_num_of_variables=1)
        assert expected_result == current_result[0]

    def test_specification_satisfaction_27_fail(self):
        specification = parse("""exist A, B, C . A o B & B o C""")
        expected_result = False
        current_result = monitor(TestSpecificationSatisfaction.sequence, specification,
                                 i_num_of_variables=1)
        assert expected_result == current_result[0]

    def test_specification_satisfaction_28_pass(self):
         specification = parse("""exist A, B, C, D, E, F . A < B -> (C i D & E o F)""")

         expected_result = True
         current_result = monitor(TestSpecificationSatisfaction.sequence, specification,
                                  i_num_of_variables=1)
         assert expected_result == current_result[0]

    def test_specification_satisfaction_29_pass(self):
         specification = parse("""exist A, B, C, D . (A < B) -> (C i D & C("Data2"))""")

         expected_result = True
         current_result = monitor(TestSpecificationSatisfaction.sequence, specification,
                                  i_num_of_variables=1)
         assert expected_result == current_result[0]

    def test_specification_satisfaction_30_pass(self):
        sequence = [["begin", 1, 'Data1'], ["end", 1], ["begin", 2, 'Data2'], ["end", 2]]

        specification = parse("""forall A, B . A("Data1") & B("Data2") -> A < B""")
        expected_result = True

        current_result = monitor(sequence, specification,
                                 i_num_of_variables=1)
        assert expected_result == current_result[0]

    def test_specification_satisfaction_31_pass(self):
         specification = parse("""!exist A, B, C, D . (A < B) -> (C i D & C("Data2"))""")

         expected_result = False
         current_result = monitor(TestSpecificationSatisfaction.sequence, specification,
                                  i_num_of_variables=1)
         assert expected_result == current_result[0]


