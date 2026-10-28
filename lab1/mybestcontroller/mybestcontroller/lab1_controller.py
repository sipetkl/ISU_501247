import rclpy
from rclpy.node import Node

from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
from std_msgs.msg import Float64

import math


class MyController(Node):

    def __init__(self):
        super().__init__('controller')
            
        self.publisher = self.create_publisher(
            Twist,
            'turtle1/cmd_vel',
            10
        )

        if self.get_namespace() == '/ns1_501247':

            self.subscription = self.create_subscription(
                Pose,
                'turtle1/pose',
                self.pose_callback_1,
                10
            )

            self.result_publisher = self.create_publisher(
                Float64,
                '/result_501247',
                10
            )

        else:

            self.subscription_1 = self.create_subscription(
                Pose,
                '/ns1_501247/turtle1/pose',
                self.pose_turtle_1_save,
                10
            )

            self.subscription_2 = self.create_subscription(
                Pose,
                'turtle1/pose',
                self.pose_callback_2,
                10
            )

        self.start_time = self.get_clock().now()

        self.current_target = 0
        self.targets_list = [
            [2.0, 3.0],
            [5.0, 4.0],
            [4.0, 2.0],
            [5.0, 4.0]
        ]

        self.error = 0.05

        self.turtle1_pose = None

        self.finished = False


    def pose_callback_1(self, pose: Pose):

        cmd = Twist()

        if self.current_target >= len(self.targets_list):

            if not self.finished:

                elapsed = self.get_clock().now() - self.start_time

                seconds = elapsed.nanoseconds / 1e9

                result = Float64()
                result.data = float(seconds)

                self.result_publisher.publish(result)

                self.get_logger().info(
                    f'Finished in {seconds:.2f} seconds'
                )

                self.finished = True

            cmd.linear.x = 0.0
            cmd.angular.z = 0.0
            self.publisher.publish(cmd)
            
            if self.finished:
                result = Float64()
                elapsed = self.get_clock().now() - self.start_time
                result.data = float(elapsed.nanoseconds / 1e9)
                self.result_publisher.publish(result)

            return

        c_x = pose.x
        c_y = pose.y
        rad_c = pose.theta

        t_x, t_y = self.targets_list[self.current_target]

        dx = t_x - c_x
        dy = t_y - c_y

        rad_t = math.atan2(dy, dx)

        d_rad = rad_t - rad_c

        purp = math.atan2(
            math.sin(d_rad),
            math.cos(d_rad)
        )

        if abs(purp) > self.error:

            if purp > 0:
                cmd.angular.z = 1.5 * min(abs(purp), 2.0)
            else:
                cmd.angular.z = -1.5 * min(abs(purp), 2.0)

            self.publisher.publish(cmd)
            return

        distance = (dx**2 + dy**2)**0.5

        if distance > self.error:

            cmd.linear.x = 1.5 * min(distance, 1.5)

        else:
            self.get_logger().info(
                f'Target ({t_x}, {t_y}) reached, '
                f'distance = {distance:.5f}'
            )
            self.current_target += 1

        self.publisher.publish(cmd)
    

    def pose_callback_2(self, pose: Pose):

        if self.turtle1_pose is None:
            return
        
        cmd = Twist()

        t1_x = self.turtle1_pose.x
        t1_y = self.turtle1_pose.y

        t2_x = pose.x
        t2_y = pose.y
        rad_t2 = pose.theta

        dx = t1_x - t2_x
        dy = t1_y - t2_y

        rad_t = math.atan2(dy, dx)

        d_rad = rad_t - rad_t2

        angle = math.atan2(
            math.sin(d_rad),
            math.cos(d_rad)
        )

        if abs(angle) > self.error:

            if angle > 0:
                cmd.angular.z = 2.0 * min(abs(angle), 1.5)
            else:
                cmd.angular.z = -2.0 * min(abs(angle), 1.5)

        distance = (dx**2 + dy**2)**0.5

        if distance > 0.5:
            if abs(angle) < 0.8:
                cmd.linear.x = 1.5 * min(distance, 1.5)
        else:
            cmd.linear.x = 0.0
            angle_error = self.turtle1_pose.theta - pose.theta

            angle_error = math.atan2(
                math.sin(angle_error),
                math.cos(angle_error)
            )
            cmd.angular.z = 2.0 * angle_error

        self.publisher.publish(cmd)


    def pose_turtle_1_save(self, pose: Pose):

        self.turtle1_pose = pose


def main(args=None):

    rclpy.init(args=args)

    node = MyController()

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
