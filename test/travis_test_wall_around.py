#!/usr/bin/env python
import unittest, rostest
import rosnode, rospy
import time

class WallAroundTest(unittest.TestCase):
    def set_and_get(self, lf, ls, rs, rf):
        with open("/dev/rtlightsensor0","w") as f:
            f.write("%d %d %d %d\n" % (rf, rs, ls, lf))

        time.sleep(0.3)

        with open("/dev/rtmotor_raw_l0","r") as lf,\
             open("/dev/rtmotor_raw_r0","r") as rf:
            left = int(lf.readline().rstrip())
            right = int(rf.readline().rstrip())

        return left, right

    def test_io(self):
        left, right = self.set_and_get(400, 0, 0, 0) #wall_front
        self.assertTrue(left > right, "wall_front logic FAIL")

        left, right = self.set_and_get(0, 0, 1000, 0) #too_right
        self.assertTrue( left < right, "too_right logic FAIL")

        left, right = self.set_and_get(0, 1000, 0, 0) #too_left
        self.assertTrue( left > right, "too_left logic FAIL")

        left, right = self.set_and_get(0, 5, 0, 0) #don't control when far from a wall
        self.assertTrue( 0 < left and 0 < right, "normal situation logic FAIL")

        left, right = self.set_and_get(0, 50, 0, 0) #curve to right
        self.assertTrue( 0 < left == right, "straight logit FAIL")        

if __name__=='__main__':
    time.sleep(3)
    rospy.init_node('travis_test_wall_around')
    rostest.rosrun('pimouse_run_corridor','travis_test_wall_around',WallAroundTest)
