#!/usr/bin/env python

import rospy

from test_task import TestTask
from task_states import TaskRunning, TaskDone

from std_msgs.msg import String

from motions_server.abstract_command_handler import (TaskHandledState,
                                                     AbstractCommandHandler)
from motions_server.abstract_safety_handler import AbstractSafetyResponder


class CommandHandler(AbstractCommandHandler):
    def __init__(self):
        self._task_running_pub = rospy.Publisher('task_running', String, queue_size=10)

    def check_request(self, request):
        if request == 'test_task':
            return TestTask()
        else:
            return None

    def wait_until_ready(self, timeout):
        return

    def handle(self, command, state):
        if isinstance(state, TaskRunning):
            self._handle_task_running(command)
            return TaskHandledState.OKAY
        elif isinstance(state, TaskDone):
            self._handle_task_done(command)
            return TaskHandledState.DONE
        else:
            rospy.logerr('CommandHandler: Task provided invalid state')
            return TaskHandledState.ABORTED

    def _handle_task_running(self, command):
        msg = String()
        msg.data = command.data
        self._task_running_pub.publish(msg)

    def _handle_task_done(self, command):
        self._handle_task_running(command)


class SafetyResponder(AbstractSafetyResponder):
    def __init__(self):
        pass

    def activate_safety_response(self):
        return

    def wait_until_ready(self):
        return
