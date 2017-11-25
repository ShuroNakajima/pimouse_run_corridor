#!/usr/bin/env python
import sys, rospy, copy
from geometry_msgs.msg import Twist
from std_srvs.srv import Trigger, TriggerResponse
from pimouse_ros.msg import LightSensorValues

class WallStop():
    def __init__(self):
        self.cmd_vel = rospy.Publisher('cmd_vel', Twist, queue_size=1)

        self.sensor_values = LightSensorValues()
        rospy.Subscriber('/lightsensors', LightSensorValues, self.callback)

    def callback(self, messages):
        self.sensor_values = messages
        rospy.logerr("ccccccccccccc")

    def run(self):
        rate = rospy.Rate(10)
        data = Twist()
        rospy.logerr("aaaaaaaaaa")

        while not rospy.is_shutdown():
            data.linear.x = 0.2 if self.sensor_values.sum_all < 500 else 0.0
            self.cmd_vel.publish(data)
            rospy.logerr("bbbbbbbbbb")
            rate.sleep()

if __name__=='__main__':
    rospy.init_node('wall_stop',log_level=rospy.INFO)
    w=WallStop()
    rospy.wait_for_service('/motor_on')
    rospy.wait_for_service('/morot_off')
    rospy.on_shutdown(rospy.ServiceProxy('/motor_off',Trigger).call)
    on=rospy.ServiceProxy('/motor_on',Trigger)
    on()
    w.run()
