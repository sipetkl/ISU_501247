import math
import time
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from std_msgs.msg import Float64

class Lab1Controller(Node):
    def __init__(self):
        super().__init__('lab1_controller')
        self.ns = self.get_namespace().strip('/')
        self.get_logger().info(f'Запущен узел контроллера в пространстве: {self.ns}')
        self.cmd_pub = self.create_publisher(Twist, 'turtle1/cmd_vel', 10)
        self.pose_sub = self.create_subscription(
            Pose, 'turtle1/pose', self.own_pose_callback, 10
        )
        self.current_pose = None

        if 'ns1' in self.ns:
            self.role = 'leader'
            self.target_points = [(2.0, 3.0), (5.0, 4.0), (4.0, 2.0), (5.0, 4.0)]
            self.target_idx = 0
            self.start_time = None
            self.finished = False
            self.result_pub = self.create_publisher(Float64, '/result_501247', 10)
        else:
            self.role = 'follower'
            self.target_pose = None
            self.leader_sub = self.create_subscription(
                Pose, '/ns1_501247/turtle1/pose', self.leader_pose_callback, 10
            )
        self.timer = self.create_timer(0.05, self.control_loop)

    def own_pose_callback(self, msg):
        self.current_pose = msg
        if self.role == 'leader' and self.start_time is None:
            self.start_time = time.time()

    def leader_pose_callback(self, msg):
        self.target_pose = msg

    def control_loop(self):
        if self.current_pose is None:
            return

        cmd = Twist()

        if self.role == 'leader':
            if self.finished:
                self.cmd_pub.publish(cmd)
                return

            tx, ty = self.target_points[self.target_idx]
            dx = tx - self.current_pose.x
            dy = ty - self.current_pose.y
            dist = math.hypot(dx, dy)
            if dist < 0.15:
                self.target_idx += 1
                if self.target_idx >= len(self.target_points):
                    self.finished = True
                    elapsed = time.time() - self.start_time
                    self.get_logger().info(f'Ведущая черепаха завершила путь за {elapsed:.2f} сек!')

                    res = Float64()
                    res.data = float(elapsed)
                    self.result_pub.publish(res)
                    return
            target_angle = math.atan2(dy, dx)
            angle_err = math.atan2(
                math.sin(target_angle - self.current_pose.theta),
                math.cos(target_angle - self.current_pose.theta)
            )
            if abs(angle_err) > 0.15:
                cmd.angular.z = 2.5 * angle_err
                cmd.linear.x = 0.4 * math.cos(angle_err)
            else:
                cmd.linear.x = min(2.0, 1.5 * dist)
                cmd.angular.z = 1.2 * angle_err

            self.cmd_pub.publish(cmd)

        elif self.role == 'follower':
            if self.target_pose is None:
                return

            dx = self.target_pose.x - self.current_pose.x
            dy = self.target_pose.y - self.current_pose.y
            dist = math.hypot(dx, dy)

            target_angle = math.atan2(dy, dx)
            angle_err = math.atan2(
                math.sin(target_angle - self.current_pose.theta),
                math.cos(target_angle - self.current_pose.theta)
            )
            if dist > 0.08:
                if abs(angle_err) > 0.2:
                    cmd.angular.z = 3.0 * angle_err
                    cmd.linear.x = 0.4 * math.cos(angle_err)
                else:
                    cmd.linear.x = min(2.5, 2.0 * dist)
                    cmd.angular.z = 2.0 * angle_err

            self.cmd_pub.publish(cmd)

def main(args=None):
    rclpy.init(args=args)
    node = Lab1Controller()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
