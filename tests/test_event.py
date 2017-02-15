import unittest
import time
from jarpis import event

class BasicTestSuite(unittest.TestCase):

    def test_event_create(self):
        object = event.Event(1,"Party", time.time(), time.time(), True, 1, 1, None);

        if object.create()._id.__eq__("1") and object.create()._private.__eq__(True):
            assert True
        else:
            assert False

if __name__ == '__main__':
    unittest.main()