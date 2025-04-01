#!/usr/bin/env python3
import rospy
from std_msgs.msg import Float64

class EncoderFromCommand:
    def __init__(self):
        rospy.init_node('encoder_from_command', anonymous=True)

        # Subscriber để nhận dữ liệu vận tốc từ các topic điều khiển
        rospy.Subscriber('/front_wheel_joint_velocity_controller/command', Float64, self.front_wheel_callback)
        rospy.Subscriber('/left_wheel_joint_velocity_controller/command', Float64, self.left_wheel_callback)
        rospy.Subscriber('/right_wheel_joint_velocity_controller/command', Float64, self.right_wheel_callback)

        self.left_wheel_speed = 0.0
        self.right_wheel_speed = 0.0
        self.front_wheel_speed=0.0

        rospy.loginfo("Node encoder_from_command đang chạy...")

        rospy.spin()

    def front_wheel_callback(self, msg):
        self.front_wheel_speed = msg.data
        rospy.loginfo(f"ENCODER | Left Wheel Speed: {self.front_wheel_speed:.3f} rad/s")

    def left_wheel_callback(self, msg):
        self.left_wheel_speed = msg.data
        rospy.loginfo(f"ENCODER | Left Wheel Speed: {self.left_wheel_speed:.3f} rad/s")

    def right_wheel_callback(self, msg):
        self.right_wheel_speed = msg.data
        rospy.loginfo(f"ENCODER | Right Wheel Speed: {self.right_wheel_speed:.3f} rad/s")

if __name__ == '__main__':
    try:
        EncoderFromCommand()
    except rospy.ROSInterruptException:
        pass
