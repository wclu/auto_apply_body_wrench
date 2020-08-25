#!/usr/bin/env python


import rospy
import std_msgs
import geometry_msgs.msg
import rosgraph_msgs
import gazebo_msgs.srv
import math


sim_time = 0

def apply_body_wrench_client(body_name, reference_frame, reference_point, wrench, start_time, duration):
    rospy.wait_for_service('/gazebo/apply_body_wrench')
    try:
        apply_body_wrench = rospy.ServiceProxy('/gazebo/apply_body_wrench', gazebo_msgs.srv.ApplyBodyWrench)
        k = apply_body_wrench(body_name, reference_frame, reference_point, wrench, start_time, duration)
        # rospy.loginfo(k)
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e


def clear_body_wrench_client(body_name):
    rospy.wait_for_service('gazebo/clear_body_wrenches')
    try:
        clear_body_wrench = rospy.ServiceProxy('gazebo/clear_body_wrenches', gazebo_msgs.srv.BodyRequest)
        clear_body_wrench(body_name)
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e


def read_clock(msg):
    global sim_time
    sim_time = msg.clock.secs
    # rospy.loginfo(sim_time)


def node():
    # Set Paramters for Subscriber
    global sim_time
    rospy.init_node("clock_subs_node", anonymous=True)
    rospy.Subscriber("/clock", rosgraph_msgs.msg.Clock, read_clock)
    node_update_rate = 0.1
    rate = rospy.Rate(1/node_update_rate)

    # Set Paramters for service
    test_start_time = 25 # sec for sim time
    test_period = 5 # sec for sim time
    body_name = 'alma::base'
    reference_frame = 'world'
    start_time = rospy.Time(secs = 0, nsecs = 0) # start as soon as possible if start_time is not specified, or start_time < current time
    duration = rospy.Duration(secs = node_update_rate, nsecs = 0)
    reference_point = geometry_msgs.msg.Point(x = 0, y = 0, z = 0)
    force = [[50, 0, 0],[0, 24, 0],[0, 0, 50]] # [Fx, Fy, Fz] for each test period. Length can be added.


    rospy.loginfo("Initiling...")
    while not rospy.is_shutdown():
        i = (sim_time-test_start_time)/test_period
        if (i>=0) & (i<len(force)):
            wrench = geometry_msgs.msg.Wrench( \
                force = geometry_msgs.msg.Vector3( x = force[i][0], y = force[i][1], z = force[i][2]), \
                torque = geometry_msgs.msg.Vector3(x = 0, y = 0, z = 0))
            clear_body_wrench_client(body_name)
            apply_body_wrench_client(body_name, reference_frame, reference_point, wrench, start_time, duration)
            rospy.loginfo("period %d" % (i+1))
        else:
            rospy.loginfo(sim_time)
        rate.sleep()


if __name__ == "__main__":
    try:
        node()
    except rospy.ROSInterruptException:
        pass
