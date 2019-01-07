#!/usr/bin/env python

import rospy
import actionlib

from robot_motions_server_ros.msg import TaskRequestAction, TaskRequestGoal

def run(server_name):
    client = actionlib.SimpleActionClient(server_name, TaskRequestAction)
    client.wait_for_server()

    request = TaskRequestGoal(action_type='test_task')
    client.send_goal_and_wait(request)

    rospy.logwarn('Success: {}'.format(client.get_result().success))

if __name__ == '__main__':
    rospy.init_node('test_action_client')
    name = rospy.get_param('/task_manager/action_server_name')
    run(name)
