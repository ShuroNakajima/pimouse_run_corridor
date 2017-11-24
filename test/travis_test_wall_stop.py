#!/usr/bin/env python
import unittest, rostest
import rosnode, rospy
import time
from geometry_msgs.msg import Twist
from pimouse_ros.msg import LightSensorValues

class WallStopTest(unittest.TestCase):
    def setUp(self):
	rospy.Subscriber('/cmd_vel', Twist, self.callback)
	self.values=Twist()

    def callback(self,messages):
	self.values=messages
        print(values)

    def test_node_exist(self):
        nodes=rosnode.get_node_names()
	self.assertIn('/cmd_vel',nodes,"node does not exist")

    def set_and_get(self, lf, ls, rs, rf):
        with open("/dev/rtlightsensor0","w") as f:
            f.write("%d %d %d %d\n" % (rf, rs, ls, lf))

        with open("/dev/rtlightsensor0","r") as f1:            
            pppp = f1.readline()

        print(pppp)

        time.sleep(3)

        with open("/dev/rtmotor_raw_l0","r") as lf,\
             open("/dev/rtmotor_raw_r0","r") as rf:
#            left = int(lf.readline().rstrip())
#            right = int(rf.readline().rstrip())
            left = 100
            right = 200
            
        return left, right

    def test_io(self):
        left, right = self.set_and_get(400, 100, 100, 0) #total:600
        self.assertTrue(left == 0 and right == 0, "can't stop")

        left, right = self.set_and_get(400, 0, 0, 99) #total:499
        self.assertTrue(left != 0 and right != 0, "cant't move again")

        left, right = self.set_and_get(150, 0, 200, 150) #total:500
        self.assertTrue(left == 0 and right == 0, "can't stop")

if __name__=='__main__':
    time.sleep(3)
    rospy.init_node('travis_test_wall_stop')
    rostest.rosrun('pimouse_run_corridor','travis_test_wall_stop',WallStopTest)
