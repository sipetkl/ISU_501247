import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
from std_msgs.msg import Float64

import math


class TurtleController(Node):

    def __init__(self):
        super().__init__('turtle_controller')
            
        self.pub = self.create_publisher(
            Twist,
            'turtle1/cmd_vel',
            10
        )

        if self.get_namespace() == '/ns1_501247':

            self.sub = self.create_subscription(
                Pose,
                'turtle1/pose',
                self.pose_cb_1,
                10
            )

            self.res_pub = self.create_publisher(
                Float64,
                '/result_501247',
                10
            )

        else:

            self.sub_leader = self.create_subscription(
                Pose,
                '/ns1_501247/turtle1/pose',
                self.leader_pose_save,
                10
            )

            self.sub_follower = self.create_subscription(
                Pose,
                'turtle1/pose',
                self.pose_cb_2,
                10
            )

        self.start_time = self.get_clock().now()

        self.target_index = 0

        self.points = [
            [2.0, 3.0],
            [5.0, 4.0],
            [4.0, 2.0],
            [5.0, 4.0]
        ]

        self.tolerance = 0.05

        self.leader_pose = None

        self.is_done = False


    def pose_cb_1(self, msg: Pose):

        cmd = Twist()

        if self.target_index >= len(self.points):

            if not self.is_done:

                time_diff = self.get_clock().now() - self.start_time
                seconds = time_diff.nanoseconds / 1e9

                res_msg = Float64()
                res_msg.data = float(seconds)

                self.res_pub.publish(res_msg)

                self.get_logger().info(f'Done in {seconds:.2f} seconds')

                self.is_done = True

            cmd.linear.x = 0.0
            cmd.angular.z = 0.0
            self.pub.publish(cmd)
            
            if self.is_done:
                res_msg = Float64()
                time_diff = self.get_clock().now() - self.start_time
                res_msg.data = float(time_diff.nanoseconds / 1e9)
                self.res_pub.publish(res_msg)

            return

        curr_x = msg.x
        curr_y = msg.y
        curr_theta = msg.theta

        target_x, target_y = self.points[self.target_index]

        diff_x = target_x - curr_x
        diff_y = target_y - curr_y

        desired_angle = math.atan2(diff_y, diff_x)
        angle_diff = desired_angle - curr_theta

        normalized_angle = math.atan2(
            math.sin(angle_diff),
            math.cos(angle_diff)
        )

        if abs(normalized_angle) > self.tolerance:

            if normalized_angle > 0:
                cmd.angular.z = 1.5 * min(abs(normalized_angle), 2.0)
            else:
                cmd.angular.z = -1.5 * min(abs(normalized_angle), 2.0)

            self.pub.publish(cmd)
            return

        dist = (diff_x**2 + diff_y**2)**0.5

        if dist > self.tolerance:

            cmd.linear.x = 1.5 * min(dist, 1.5)

        else:
            self.get_logger().info(f'Reached target ({target_x}, {target_y})')
            self.target_index += 1

        self.pub.publish(cmd)
    

    def pose_cb_2(self, msg: Pose):

        if self.leader_pose is None:
            return
        
        cmd = Twist()

        lead_x = self.leader_pose.x
        lead_y = self.leader_pose.y

        follow_x = msg.x
        follow_y = msg.y
        follow_theta = msg.theta

        diff_x = lead_x - follow_x
        diff_y = lead_y - follow_y

        desired_angle = math.atan2(diff_y, diff_x)
        angle_diff = desired_angle - follow_theta

        normalized_angle = math.atan2(
            math.sin(angle_diff),
            math.cos(angle_diff)
        )

        if abs(normalized_angle) > self.tolerance:

            if normalized_angle > 0:
                cmd.angular.z = 2.0 * min(abs(normalized_angle), 1.5)
            else:
                cmd.angular.z = -2.0 * min(abs(normalized_angle), 1.5)

        dist = (diff_x**2 + diff_y**2)**0.5

        if dist > 0.5:
            if abs(normalized_angle) < 0.8:
                cmd.linear.x = 1.5 * min(dist, 1.5)
        else:
            cmd.linear.x = 0.0
            error_theta = self.leader_pose.theta - follow_theta

            error_theta = math.atan2(
                math.sin(error_theta),
                math.cos(error_theta)
            )
            cmd.angular.z = 2.0 * error_theta

        self.pub.publish(cmd)


    def leader_pose_save(self, msg: Pose):
        self.leader_pose = msg


def main(args=None):
    rclpy.init(args=args)
    node = TurtleController()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
