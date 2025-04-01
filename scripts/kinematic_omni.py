#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import Float64

# Thông số robot
WHEEL_RADIUS = 0.055  # Bán kính bánh xe (m)
L = 0.2  # Khoảng cách từ tâm robot đến bánh xe

class OmniWheelController:
    def __init__(self):
        rospy.init_node('cmd_vel_to_omni')

        # Publisher cho 3 bánh xe
        self.pub_left = rospy.Publisher('/left_wheel_joint_velocity_controller/command', Float64, queue_size=10)
        self.pub_right = rospy.Publisher('/right_wheel_joint_velocity_controller/command', Float64, queue_size=10)
        self.pub_front = rospy.Publisher('/front_wheel_joint_velocity_controller/command', Float64, queue_size=10)

        # Subscriber nhận lệnh /cmd_vel
        rospy.Subscriber('/cmd_vel', Twist, self.cmd_vel_callback)

    def cmd_vel_callback(self, msg):
        Vx = msg.linear.x
        Vy = msg.linear.y
        omega = msg.angular.z

        # Tính vận tốc cho từng bánh xe
        v_left = (Vx - Vy - omega * L) / WHEEL_RADIUS
        v_right = (Vx + Vy + omega * L) / WHEEL_RADIUS
        v_front = (-Vx + Vy - omega * L) / WHEEL_RADIUS

        # Xuất lệnh điều khiển
        self.pub_left.publish(-v_left)
        self.pub_right.publish(v_right)
        self.pub_front.publish(v_front)

        rospy.loginfo(f"Left: {v_left:.2f}, Right: {v_right:.2f}, Front: {v_front:.2f}")

if __name__ == '__main__':
    controller = OmniWheelController()
    rospy.spin()
