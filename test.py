import unittest
import time
import threading

from pylog4all import Log4allClient




# hostname="http://localhost/log4all"
hostname = "http://localhost:6543"


class MassiveTest(unittest.TestCase):
    def setUp(self):
        self.log4ll = Log4allClient(hostname)

    def test_add_log(self):
        self.assertTrue(self.log4ll.add_log('log4all-client-python', 'ERROR', "test_unittest"))

    def test_multi_thread(self):
        for t in range(0, 5):
            print "starting thread"
            th = ThAddLog("th" + str(t))
            th.start()


class ThAddLog(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name
        self.log4allcl = Log4allClient(hostname)

    def run(self):
        print("running thread:" + self.name)
        for i in range(0, 10):
            msg = "#thread:" + self.name + "." + str(i) + " time " + str(time.time())
            try:
                success, msg = self.log4allcl.add_log('log4all-client-python', 'INFO', msg)
                if not success:
                    print("ERROR:" + msg)
            except Exception as e:
                print "Error:" + str(e)


if __name__ == '__main__':
    unittest.main()