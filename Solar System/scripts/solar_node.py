#!/usr/bin/env python
import rospy
import math
import sys
import tf
import tf2_ros
import geometry_msgs.msg
'''Para o calculo do x e y, estimou-se a orbita como uma circuferencia perfeita.
Entao, a partir do MCU, tem-se que 2*pi/periodo = variacao angular/tempo.A variacao angular foi usada
com seno e cosseno, a partir do raio da circuferencia de orbita ao redor do sol. Os raios foram colocados
de modo referencial, a fim de diminuir discrepancias enormes, mas mantendo a proporcao. Para o Periodo, manteve-se
como encontrando no site https://nssdc.gsfc.nasa.gov/planetary/factsheet/ (apenas passou de horas para segundos, 
a fim de manter-se sincronizado com a conversao do rospy.Time'''
def sistema(planeta,oradius,period):
    broadcaster = tf2_ros.StaticTransformBroadcaster()
    num = (2*math.pi*rospy.Time.now().to_sec())/(period*3600)
    static_transformStamped = geometry_msgs.msg.TransformStamped()
    static_transformStamped.header.stamp = rospy.Time.now()
    static_transformStamped.header.frame_id = "Sun"
    static_transformStamped.child_frame_id = planeta

    static_transformStamped.transform.translation.x = oradius * math.sin(num) 
    static_transformStamped.transform.translation.y = oradius * math.cos(num)
    static_transformStamped.transform.translation.z = 0

    static_transformStamped.transform.rotation.x = 0 
    static_transformStamped.transform.rotation.y = 0
    static_transformStamped.transform.rotation.z = 0
    static_transformStamped.transform.rotation.w = 1

    broadcaster.sendTransform(static_transformStamped)

planets = rospy.get_param('list of planets')
radius = rospy.get_param('list of radius')
period = rospy.get_param('list of periods')

if __name__ == "__main__":
    rospy.init_node("solar", anonymous = True)
    while not rospy.is_shutdown():
        for i in range(len(planets)):
            rospy.Subscriber('listener',geometry_msgs.msg.Pose,sistema(planets[i],radius[i],period[i]))
    rospy.spin()