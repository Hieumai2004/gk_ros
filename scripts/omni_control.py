#!/usr/bin/env python3
import rospy
from std_msgs.msg import Float64
import sys
import tty
import termios

class OmniKeyboardControl:
   def __init__(self):
       # Khởi tạo node ROS
       rospy.init_node('omni_keyboard_control', anonymous=True)


       # Publisher cho các lệnh vận tốc bánh xe
       self.pub_left = rospy.Publisher('/left_wheel_joint_velocity_controller/command', Float64, queue_size=10)
       self.pub_right = rospy.Publisher('/right_wheel_joint_velocity_controller/command', Float64, queue_size=10)
       self.pub_front = rospy.Publisher('/front_wheel_joint_velocity_controller/command', Float64, queue_size=10)
        
       # Publisher cho cac lenh dieu khien khop tay
       self.pub_prismatic = rospy.Publisher('/arm_1_joint_controller/command', Float64, queue_size=10)
       self.pub_revolute = rospy.Publisher('/arm_2_joint_controller/command', Float64, queue_size=10)

       #vi tri cua khop tay may
       self.prismatic_position = 0.0  # Khớp tịnh tiến
       self.revolute_position = 0.0  # Khớp quay

       # Tốc độ tối đa (radian/s)
       self.max_speed = 10.0  # Giới hạn từ URDF: velocity="10"
       self.max_prismatic=0.1
       self.prismatic_direction = 1  # 1: tiến, -1: lùi
       self.revolute_min = -1.57  # -90 độ (rad)
       self.revolute_max = 0   # 90 độ (rad)
       self.revolute_direction = 1  # 1: quay tới, -1: quay lùi
  
     

       # Vận tốc hiện tại của từng bánh
       self.left_speed = 0.0
       self.right_speed = 0.0
       self.front_speed = 0.0
       

   def get_key(self):
       # Đọc phím từ bàn phím mà không cần nhấn Enter
       fd = sys.stdin.fileno()
       old_settings = termios.tcgetattr(fd)
       try:
           tty.setraw(fd)
           key = sys.stdin.read(1)
       finally:
           termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
       return key


   def run(self):
       rospy.loginfo("Điều khiển robot omni 3 bánh bằng bàn phím:")
       rospy.loginfo("w: Tiến, s: Lùi, a: Trái, d: Phải, q: Xoay trái, e: Xoay phải, c: Khop1, v: Khop2")
       rospy.loginfo("x: Dừng và thoát")


       while not rospy.is_shutdown():
           key = self.get_key()


           # Đặt lại vận tốc về 0 trước khi tính toán
           self.left_speed = 0.0
           self.right_speed = 0.0
           self.front_speed = 0.0
           self.prismatic_speed = 0.0
           self.revolute_speed = 0.0

           # Điều khiển chuyển động
           if key == 's':  # lui
               self.left_speed = self.max_speed
               self.right_speed = -self.max_speed
               self.front_speed = 0.0
           elif key == 'w':  # Tien
               self.left_speed = -self.max_speed
               self.right_speed = self.max_speed
               self.front_speed = 0.0
           elif key == 'd':  # Sang phai
               self.left_speed = -self.max_speed
               self.right_speed = self.max_speed
               self.front_speed = -self.max_speed
           elif key == 'a':  # Sang trai
               self.left_speed = self.max_speed
               self.right_speed = -self.max_speed
               self.front_speed = self.max_speed
           elif key == 'q':  # Xoay trái
               self.left_speed = -self.max_speed
               self.right_speed  = self.max_speed
               self.front_speed = self.max_speed
           elif key == 'e':  # Xoay phải
               self.left_speed = self.max_speed
               self.right_speed = -self.max_speed
               self.front_speed = -self.max_speed
           elif key == 'z':  # Dừng và thoát
               self.left_speed = 0.0
               self.right_speed = 0.0
               self.front_speed = 0.0
           elif key =='c': #khop1
                if self.prismatic_position + (self.prismatic_direction * 0.01) > self.max_prismatic:
                   self.prismatic_direction = -1  # Đảo hướng lùi
                elif self.prismatic_position + (self.prismatic_direction * 0.01) < 0.0:
                     self.prismatic_direction = 1  # Đảo hướng tiến

                self.prismatic_position += self.prismatic_direction * 0.01
                rospy.loginfo(f"Khớp 1 (Tịnh tiến): {self.prismatic_position:.2f}")

           elif key =='v': #khop2
               if self.revolute_position + (self.revolute_direction * 0.1) > self.revolute_max:
                  self.revolute_direction = -1  # Đảo hướng quay lùi
               elif self.revolute_position + (self.revolute_direction * 0.1) < self.revolute_min:
                    self.revolute_direction = 1  # Đảo hướng quay tới

               self.revolute_position += self.revolute_direction * 0.1
               rospy.loginfo(f"Khớp 2 (Quay): {self.revolute_position:.2f}")

           elif key == 'x':  # Dừng và thoát
               self.left_speed = 0.0
               self.right_speed = 0.0
               self.front_speed = 0.0
               self.pub_left.publish(self.left_speed)
               self.pub_right.publish(self.right_speed)
               self.pub_front.publish(self.front_speed)
               

               rospy.loginfo("Dừng robot và thoát")
               break


           # Gửi lệnh vận tốc
           self.pub_left.publish(self.left_speed)
           self.pub_right.publish(self.right_speed)
           self.pub_front.publish(self.front_speed)
           self.pub_prismatic.publish(self.prismatic_position)
           self.pub_revolute.publish(self.revolute_position)

           # Hiển thị trạng thái
           rospy.loginfo(f"Left: {self.left_speed:.2f}, Right: {self.right_speed:.2f}, Front: {self.front_speed:.2f}")


           rospy.sleep(0.1)  # Tránh đọc phím quá nhanh


if __name__ == '__main__':
   try:
       controller = OmniKeyboardControl()
       controller.run()
   except rospy.ROSInterruptException:
       pass
