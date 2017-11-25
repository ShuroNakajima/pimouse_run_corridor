#!/usr/bin/env python
import unittest, rostest
import rosnode, rospy
import time
from geometry_msgs.msg import Twist
from pimouse_ros.msg import LightSensorValues

class WallStopTest(unittest.TestCase):
    def setUp(self):
	self.values=Twist()        
	rospy.Subscriber('cmd_vel', Twist, self.callback)        
#        self.sensor_values = LightSensorValues()
#        rospy.Subscriber('/lightsensors', LightSensorValues, self.callback)

    def callback(self,messages):
	self.values=messages
#        self.sensor_values = messages
#        print(messages)

    def set_and_get(self, lf, ls, rs, rf):
        with open("/dev/rtlightsensor0","w") as f:
            f.write("%d %d %d %d\n" % (rf, rs, ls, lf))

        time.sleep(1)

        with open("/dev/rtmotor_raw_l0","r") as lf,\
             open("/dev/rtmotor_raw_r0","r") as rf:
            left = int(lf.readline().rstrip())
            right = int(rf.readline().rstrip())
#            left = 100
#            right = 200
            
        return left, right

    def test_on_off(self):
        off = rospy.ServiceProxy('/motor_off', Trigger)
        ret = off()
        self.assertEqual(ret.success, True, "motor off does not succeeded")
        self.assertEqual(ret.message, "OFF", "motor off wrong message")
        with open("/dev/rtmotoren0","r") as f:
            data = f.readline()
            self.assertEqual(data, "0\n", "wrong value in rtmotor0 at motor off")

        on = rospy.ServiceProxy('/motor_on', Trigger)
        ret = on()
        self.assertEqual(ret.success, True, "motor on does not succeeded")
        self.assertEqual(ret.message, "ON", "motor on wrong message")
        with open("/dev/rtmotoren0","r") as f:
            data = f.readline()
            self.assertEqual(data,"1\n","wrong value in rtmotor0 at motor on")

    def test_node_exist(self):
        nodes = rosnode.get_node_names()
        self.assertIn('/wall_stop', nodes, "node does not exist")

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
