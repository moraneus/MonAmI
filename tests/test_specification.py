from tests.test_helper import *
import unittest
from frontend.parser import parse

# Test cases created by Klaus

def monitor(sequence, specification):
    return update_bdds_with_specification(sequence, specification, i_num_of_variables=3)


class TestSpecification(unittest.TestCase):
    sequence = [["begin", 1, 'A'],
                ["end", 1],
                ["begin", 2, 'B'],
                ["end", 2],
                ["begin", 3, 'B'],
                ["begin", 4, 'C'],
                ["end", 4],
                ["end", 3]]

    def test1(self):
        specification = parse(
            """
            exist A, B, C . 
              A("A") & B("B") & C("C") &
              A < B &
              B i C
            """)
        result = monitor(TestSpecification.sequence, specification)
        assert result