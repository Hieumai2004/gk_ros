# chaỵ mô phỏng trên gazebo
roslaunch gk_ros control.launch
#chay mo phong tren rviz 
roslaunch gk_ros display.launch
#điều khiển xe bằng bàn phím 
B1:gắn plugin vào file urdf
 <gazebo>
  <plugin name="gazebo_ros_control" filename="libgazebo_ros_control.so"/>
</gazebo>
B2: chạy node để điều khiển xe va khop tay bằng bàn phím
 rosrun gk_ros omni_control.py
 w: Tiến, s: Lùi, a: Trái, d: Phải, q: Xoay trái, e: Xoay phải, c: Khop1, v: Khop2
# điều khiển xe theo toc do mong muon
B1: xóa plugin trene va gắn plugin vào file urdf
<gazebo>
    <plugin name="object_controller" filename="libgazebo_ros_planar_move.so">
      <commandTopic>cmd_vel</commandTopic>
      <odometryTopic>odom</odometryTopic>
      <odometryFrame>odom</odometryFrame>
      <odometryRate>30.0</odometryRate>
      <robotBaseFrame>base_footprint</robotBaseFrame>
    </plugin>
  </gazebo> 
  B2 chạy node 
  rosrun gk_ros kinematic_omni.py
  
  B3 : sau đó publish vận tốc mong muốn 
  vd: rostopic pub /cmd_vel geometry_msgs/Twist "linear:
  x: 1.0
  y: 0.0
  z: 0.0
angular:
  x: 0.0
  y: 0.0
# chạy node encoder
rosrun gk_ros encoder.py
# xem thông tin từ imu
rostopic echo /imu
