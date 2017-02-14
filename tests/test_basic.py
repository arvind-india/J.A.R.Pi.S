
from .context import jarpis

import unittest


class BasicTestSuite(unittest.TestCase):

    def test_absolute_truth_and_meaning(self):
        assert True

    def test_say_hmm(self):
        if jarpis.test().__eq__("hmm"):
            assert True
        else:
            assert False


if __name__ == '__main__':
    unittest.main()