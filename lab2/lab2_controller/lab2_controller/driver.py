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
		self.req_pending = False 
		self.moving = False
		self.stop_timer = None

	def pose_callback(self, msg):
		self.current_pose = msg
		if self.req_pending or self.moving:
			return
		if abs(msg.linear_velocity) > 0.01 or abs(msg.angular_velocity) > 0.01:
			return
		if not self.client.service_is_ready():
			return

		self.req_pending = True 
		req = A501247.Request()
		req.xcurrent = msg.x
		req.ycurrent = msg.y 
		self.client.call_async(req).add_done_callback(self.response_callback)

	def response_callback(self, future):
		try:
			response = future.result()
		except Exception as e:
			self.get_logger().error(str(e))
			self.req_pending = False
			return 

		if response.distance < 0.1:
 			self.req_pending = False
 			return

		err = response.angle - self.current_pose.theta
		err = math.atan2(math.sin(err), math.cos(err))
		
		cmd = Twist()
		cmd.angular.z = 4.0 * err 
		if abs(err) <= 0.1:
			cmd.linear.x = min(2.0, 2.0 * response.distance)
		self.publisher.publish(cmd)
		self.moving = True 
		self.stop_timer = self.create_timer(0.2, self.stop_cb)

	def stop_cb(self):
		self.destroy_timer(self.stop_timer)
		self.publisher.publish(Twist())
		self.moving = False 
		self.req_pending = False


 
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
