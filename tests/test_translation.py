from tests.test_monitor import *
from frontend.parser import parse


class TestTranslation:
    def test1(self):
        specification = parse("""exist A, B . A("Data1") & B("Data2")""")
        dejavu = specification.translate()
        print(dejavu)


test = TestTranslation()

test.test1()



