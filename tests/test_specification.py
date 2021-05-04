from tests.test_helper import *
import unittest
from frontend.parser import parse

# Test cases created by Klaus

def monitor(sequence, specification):
    return update_bdds_with_specification(sequence, specification, i_num_of_variables=3)


class TestSpecification(unittest.TestCase):
    sequence = [["begin", 1, 'Data1'], ["end", 1], ["begin", 2, 'Data2'], ["end", 2],
                ["begin", 3, 'Data3'], ["begin", 4, 'Data4'], ["end", 4], ["end", 3],
                ["begin", 5, 'Data1'], ["begin", 6, 'Data6'], ["end", 5], ["end", 6]]

    def test1(self):
        specification = parse("""exist A, B . A("Data1") & B("Data2")""")
        assert monitor(TestSpecification.sequence, specification)
