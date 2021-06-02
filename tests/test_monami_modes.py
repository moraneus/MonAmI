from tests.test_monitor import *
from frontend.parser import parse


class TestSpecificationSatisfaction():
    sequence = [["begin", 1, 'Data1'], ["end", 1], ["begin", 2, 'Data2'], ["end", 2],
                ["begin", 3, 'Data3'], ["begin", 4, 'Data4'], ["end", 4], ["end", 3],
                ["begin", 5, 'Data1'], ["begin", 6, 'Data6'], ["end", 5], ["end", 6]]

    def test_specification_satisfaction_1(self):
        specification = parse("""exist A, B . A("Data1") & B("Data2")""")
        expected_result = True
        current_result = monitor(TestSpecificationSatisfaction.sequence, specification,
                                 1, "SATISFACTION")

        assert expected_result == current_result[0]

    def test_specification_satisfaction_2(self):
        specification = parse("""!exist A, B . A("Data8") & B("Data2")""")
        expected_result = True
        current_result = monitor(TestSpecificationSatisfaction.sequence, specification,
                                 1, "VIOLATION")

        assert expected_result == current_result[0]

    def test_specification_satisfaction_3(self):
        specification = parse("""!exist A, B . A("Data8") & B("Data2")""")
        expected_result = True
        current_result = monitor(TestSpecificationSatisfaction.sequence, specification,
                                 1, "SATISFACTION")

        assert expected_result == current_result[0]

    def test_specification_satisfaction_4(self):
        specification = parse("""exist A, B . A("Data8") & B("Data2")""")
        expected_result = False
        current_result = monitor(TestSpecificationSatisfaction.sequence, specification,
                                 1, "VIOLATION")

        assert expected_result == current_result[0]

    def test_specification_satisfaction_5(self):
        specification = parse("""exist A, B . A("Data1") & B("Data2") & A < B""")
        expected_result = True
        current_result = monitor(TestSpecificationSatisfaction.sequence, specification,
                                 1, "SATISFACTION")

        assert expected_result == current_result[0]

    def test_specification_satisfaction_6(self):
        specification = parse("""!exist A, B . A("Data1") & B("Data2") & A < B""")
        expected_result = False
        current_result = monitor(TestSpecificationSatisfaction.sequence, specification,
                                 1, "VIOLATION")

        assert expected_result == current_result[0]

    def test_specification_satisfaction_7(self):
        specification = parse("""!exist A, B . A("Data1") & B("Data2") & A < B""")
        expected_result = False
        current_result = monitor(TestSpecificationSatisfaction.sequence, specification,
                                 1, "CONTINUE-SMALL")

        assert expected_result == current_result[0]

    def test_specification_satisfaction_8(self):
        specification = parse("""!exist A, B . A("Data1") & B("Data2") & A < B""")
        expected_result = False
        current_result = monitor(TestSpecificationSatisfaction.sequence, specification,
                                 1, "CONTINUE-BIG")

        assert expected_result == current_result[0]


    def test_specification_satisfaction_9(self):
        specification = parse("""exist A, B, C, D, E . A("Data1") & B("Data2") & C("Data3")
         & A < B & A < C & A < D & A < E""")
        expected_result = True
        current_result = monitor(TestSpecificationSatisfaction.sequence, specification,
                                 1, "CONTINUE-BIG")

        assert expected_result == current_result[0]

    def test_specification_satisfaction_10(self):
        specification = parse("""exist A, B, C, D, E . A("Data1") & B("Data2") & C("Data3")
         & A < B & A < C & A < D & A < E""")
        expected_result = True
        current_result = monitor(TestSpecificationSatisfaction.sequence, specification,
                                 1, "CONTINUE-SMALL")
        assert expected_result == current_result[0]

    def test_specification_satisfaction_11(self):
        specification = parse("""!exist A, B, C, D, E . A("Data1") & B("Data2") & C("Data3")
         & A < B & A < C & A < D & A < E""")
        expected_result = False
        current_result = monitor(TestSpecificationSatisfaction.sequence, specification,
                                 1, "CONTINUE-BIG")

        assert expected_result == current_result[0]

    def test_specification_satisfaction_12(self):
        specification = parse("""!exist A, B, C, D, E . A("Data1") & B("Data2") & C("Data3")
         & A < B & A < C & A < D & A < E""")
        expected_result = False
        current_result = monitor(TestSpecificationSatisfaction.sequence, specification,
                                 1, "CONTINUE-SMALL")

        assert expected_result == current_result[0]

    def test_specification_satisfaction_13(self):
        specification = parse("""forall A, B . A("Data2") & B("Data4") -> A < B""")
        expected_result = True

        current_result = monitor(TestSpecificationSatisfaction.sequence, specification,
                                 1, "CONTINUE-BIG")
        assert expected_result == current_result[0]

    def test_specification_satisfaction_14(self):
        specification = parse("""forall A, B . A("Data1") & B("Data2") -> A < B""")
        expected_result = False

        current_result = monitor(TestSpecificationSatisfaction.sequence, specification,
                                 1, "CONTINUE-SMALL")
        assert expected_result == current_result[0]

    def test_specification_satisfaction_15(self):
        specification = parse("""!forall A, B . A("Data1") & B("Data2") -> A < B""")
        expected_result = True

        current_result = monitor(TestSpecificationSatisfaction.sequence, specification,
                                 1, "CONTINUE-BIG")
        assert expected_result == current_result[0]

    def test_specification_satisfaction_16(self):
        specification = parse("""!forall A, B . A("Data1") & B("Data2") -> A < B""")
        expected_result = True

        current_result = monitor(TestSpecificationSatisfaction.sequence, specification,
                                 1, "CONTINUE-SMALL")
        assert expected_result == current_result[0]



