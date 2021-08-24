#!/usr/bin/env python
# coding: utf-8
import numpy as np 
import cv2
import rospy
from sensor_msgs.msg import Image
from move_marlin import MoveMarlin
from cv_bridge import CvBridge, CvBridgeError
from geometry_msgs.msg import Twist, Point, PointStamped
from sonar_dec import Sonardec

class Fisher(object):
    def __init__ (self):
        self.bridge_object = CvBridge()
        self.image_sub = rospy.Subscriber("/camera/image_raw", Image, self.camera_callback)
        self.movemarlin_object = MoveMarlin()
        self.sonar_object = Sonardec()

    def camera_callback(self,data):
        try:
            cv_image = self.bridge_object.imgmsg_to_cv2(data,desired_encoding='bgr8')
        except CvBridgeError as e:
            print(e)

        height, width, channels = cv_image.shape
        descentre = 200
        rows_to_watch = 20

        hsv_nemo = cv2.cvtColor(cv_image,cv2.COLOR_BGR2HSV)
        darker_red = np.array([0, 250, 0])
        lighter_red = np.array([255, 255, 255])
        
        mask = cv2.inRange(hsv_nemo, darker_red,lighter_red)
        m = cv2.moments(mask,False)


        crop_img = cv_image[(height)/2+descentre:(height)/2+(descentre+rows_to_watch)][1:width]

        try:
            cx, cy = m['m10']/m['m00'], m['m01']/m['m00']
        except ZeroDivisionError:
            cx,cy = height/2,width/2
        res = cv2.bitwise_and(cv_image,cv_image, mask=mask)
        cv2.circle(res,(int(cx),int(cy)),10,(255,0,255),-1)
        cv2.imshow("RES", res)

        cv2.waitKey(3)
        error_x = cx - width/2
        print(cx)
        print(cy)
        print(error_x)
        print(width)
        if cy > 298 and error_x == -280:
            twist_object = Twist()
            twist_object.angular.z = -error_x/120
            self.movemarlin_object.moving(twist_object)
        else:
            if self.sonar_object.r < 4:
                twist_object = Twist()
                twist_object.linear.y = 0
                twist_object.angular.z = 0
                self.movemarlin_object.moving(twist_object)
            else:
                twist_object = Twist()
                twist_object.linear.y = 2.5
                twist_object.angular.z = -error_x/200
                self.movemarlin_object.moving(twist_object)
        
    
    def cleanUp(self):
        self.movemarlin_object.stop()
        cv2.destroyAllWindows()


def main():
    rospy.init_node('marlin_swiming', anonymous = True)
    marlin = Fisher()
    rate = rospy.Rate(5)
    ctrl_c=False
    def shutdownhook():
        marlin_object.cleanUp()
        ctrl_c = True
    rospy.on_shutdown(shutdownhook)
    while not ctrl_c:
        rate.sleep()

if __name__ == "__main__":
    main()