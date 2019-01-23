#!/usr/bin/env python

import rospy
import actionlib

from robot_motions_server_ros.msg import TaskRequestAction, TaskRequestGoal

def run(server_name):
    client = actionlib.SimpleActionClient(server_name, TaskRequestAction)

    rospy.loginfo('TaskActionClient: Waiting for server')
    client.wait_for_server()
    rospy.loginfo('TaskActionClient: server ready')

    request = TaskRequestGoal(action_type='test_task')
    client.send_goal_and_wait(request)

    rospy.logwarn('Success: {}'.format(client.get_result().success))

    # test cancel
    request = TaskRequestGoal(action_type='test_task')
    client.send_goal(request)
    client.cancel_goal()
    rospy.logwarn('Goal Canceled')

    # test preempt
    request = TaskRequestGoal(action_type='test_task')
    client.send_goal(request)

    rospy.sleep(.25)

    request = TaskRequestGoal(action_type='test_task', preempt=True)
    client.send_goal_and_wait(request)

if __name__ == '__main__':
    rospy.init_node('test_action_client')
    rospy.loginfo('Test Action Client starting up')
    name = rospy.get_param('/task_manager/action_server_name')
    run(name)
