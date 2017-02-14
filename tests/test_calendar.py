import unittest
import time
from jarpis import event

class BasicTestSuite(unittest.TestCase):

    def test_event_create(self):
        object = event.Event(1,"Party", time.time(), time.time(), True, 1, 1, None);

        print(object.create())

        if object.create().__eq__("Event created!"):
            assert True
        else:
            assert False

if __name__ == '__main__':
    unittest.main()