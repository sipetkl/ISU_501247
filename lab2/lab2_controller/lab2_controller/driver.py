import rclpy 
from rclpy.node import Node
from lab2_interfaces.srv import A501247
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist 
import math 

class DriverNode(Node):
	def __init__(self):
		super().__init__('driver')
		self.publisher = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
		self.subscriber = self.create_subscription(Pose, '/turtle1/pose', self.pose_callback, 10)
		self.client = self.create_client(A501247, 'get_target')
		self.current_pose = Pose()
	def pose_callback(self, msg):
		self.current_pose = msg 
		req = A501247.Request()
		req.xcurrent = msg.x
		req.ycurrent = msg.y 
		
		future = self.client.call_async(req)
		future.add_done_callback(self.response_callback)

	def response_callback(self, future):
		response = future.result()
		cmd = Twist()
		error_distance = response.distance
		error_angle = response.angle - self.current_pose.theta
		error_angle = math.atan2(math.sin(error_angle), math.cos(error_angle))
		if abs(error_angle) > 0.1:
			cmd.linear.x = 0.0
			cmd.angular.z = 4.0 * error_angle
		else:
			cmd.linear.x = 0.5 * error_distance
			cmd.angular.z = 4.0 * error_angle
		self.publisher.publish(cmd)
 
def main(args=None):

    rclpy.init(args=args)

    node = DriverNode()

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
