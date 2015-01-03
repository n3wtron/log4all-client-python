import random
import time

from datetime import datetime


__author__ = 'igor'

import unittest

from pylog4all.client import Log4allClient

hostname = "http://localhost:6543"


class MyTestCase(unittest.TestCase):
    def test_add_search(self):
        dt_since = datetime.now()
        rnd = int(time.mktime(dt_since.timetuple()))+int(random.uniform(0,999))
        message = 'testAddMessage #rand:' + str(rnd)
        stack = 'testStackMessage'
        level = 'ERROR'
        cl = Log4allClient(hostname)
        self.assertTrue(cl.add_log('l4a', level, message, stack)[0])
        time.sleep(1)
        search_result = cl.search_log(query='#rand=' + str(rnd), since=dt_since, to=datetime.now(),full=True)
        self.assertEqual(len(search_result), 1)
        self.assertEqual(rnd,int(search_result[0]['tags']['rand']))
        print(str(search_result[0]))


if __name__ == '__main__':
    unittest.main()
