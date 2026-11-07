import rclpy
import math
from rclpy.node import Node 
from lab2_interfaces.srv import A501247

class NavigatorNode(Node):

	def __init__(self):
		super().__init__("navigator")
		self.targets_list = [[2.0, 3.0], [5.0, 4.0], [4.0, 2.0], [5.0, 4.0]]
		self.current_target = 0
		self.srv = self.create_service(A501247, 'get_target', self.compute_traj_callback)

	def compute_traj_callback(self, request, response):
		if self.current_target >= len(self.targets_list):
			return response
		else:
			t_x, t_y = self.targets_list[self.current_target]
			d_x = t_x - request.xcurrent
			d_y = t_y - request.ycurrent
		
			response.distance = (d_x**2 + d_y**2)**0.5
			response.angle = math.atan2(d_y, d_x)
		
			if response.distance < 0.1:
				self.current_target += 1
		return response

def main(args=None): 
	rclpy.init(args=args)
	node = NavigatorNode()
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

