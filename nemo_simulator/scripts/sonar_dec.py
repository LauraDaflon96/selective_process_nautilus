#!/usr/bin/env python 
import rospy
from geometry_msgs.msg import PointStamped
from math import sqrt

class Sonardec(object):

    def __init__(self):
        self.sonar_sub = rospy.Subscriber("/sonar_data", PointStamped, self.sonar_callback)
        self.pub_rate = rospy.Rate(10)

    def sonar_callback(self, data):

        self.sonar_x = data.point.x 
        self.sonar_y = data.point.y
        self.r = sqrt(data.point.x**2 + data.point.y**2)
        print("esse eh o r:{}".format(self.r))
def main():     
    rate = rospy.Rate(5)
    while not rospy.is_shutdown():
        rospy.init_node("swiming", anonymous=True)
        sonardec_object = Sonardec()
    rate.sleep()

if __name__ == '__main__':
    main()

