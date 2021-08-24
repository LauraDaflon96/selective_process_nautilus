#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist

class MoveMarlin(object):

    def __init__(self):

        self.cmd_vel_pub = rospy.Publisher('/cmd_vel',Twist,queue_size=10)
        self.cmd_vel_subs = rospy.Subscriber('/cmd_vel',Twist,self.cmdvel_callback)
        self.last_cmdvel_command = Twist()
        self._cmdvel_pub_rate = rospy.Rate(10)
        self.shutdown_detected = False

    def cmdvel_callback(self,msg):
        self.last_cmdvel_command = msg
    
    def compare_twist_commands(self,twist1,twist2):
        LX = twist1.linear.x  == twist2.linear.x 
        LY = twist1.linear.y  == twist2.linear.y
        LZ = twist1.linear.z  == twist2.linear.z
        AX = twist1.angular.x  == twist2.angular.x
        AY = twist1.angular.y  == twist2.angular.y
        AZ = twist1.angular.z  == twist2.angular.z
        equal = LX and LY and LZ and AX and AY and AZ
        return equal

    def moving(self, twist_object):
        current_equal_to_new = False
        while (not (current_equal_to_new) and not (self.shutdown_detected)):
            self.cmd_vel_pub.publish(twist_object)
            self._cmdvel_pub_rate.sleep()
            current_equal_to_new = self.compare_twist_commands(twist1 = self.last_cmdvel_command, twist2=twist_object)
            
    def stop(self):
        twist_object = Twist()
        twist_object.angular.x = 0.0
        self.move_robot(twist_object)
        self.shutdown_detected = True

def main():
     while not rospy.is_shutdown():
        rospy.init_node("marlin", anonymous=True)

        movemarlin_object = MoveMarlin()
        twist_object = Twist
        rate = rospy.Rate(5)
        movemarlin_object.moving(twist_object)
     rate.sleep()

if __name__ == '__main__':
    main()