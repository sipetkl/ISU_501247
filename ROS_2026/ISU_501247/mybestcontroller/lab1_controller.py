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

        # Публикатор скорости своей черепахи (относительное имя!)
        self.cmd_pub = self.create_publisher(Twist, 'turtle1/cmd_vel', 10)

        # Подписка на координаты собственной черепахи (относительное имя!)
        self.pose_sub = self.create_subscription(
            Pose, 'turtle1/pose', self.own_pose_callback, 10
        )
        self.current_pose = None

        if 'ns1' in self.ns:
            # --- ВЕДУЩАЯ ЧЕРЕПАХА (№1) ---
            self.role = 'leader'
            # Точки варианта 7: (2,3), (5,4), (4,2), (5,4)
            self.target_points = [(2.0, 3.0), (5.0, 4.0), (4.0, 2.0), (5.0, 4.0)]
            self.target_idx = 0
            self.start_time = None
            self.finished = False

            # Топик для вывода времени (абсолютное имя)
            self.result_pub = self.create_publisher(Float64, '/result_501247', 10)
        else:
            # --- ВЕДОМАЯ ЧЕРЕПАХА (№2) ---
            self.role = 'follower'
            self.target_pose = None
            # Подписка на координаты первой черепахи
            self.leader_sub = self.create_subscription(
                Pose, '/ns1_501247/turtle1/pose', self.leader_pose_callback, 10
            )

        # Главный цикл регулятора с частотой 20 Гц (каждые 0.05 сек)
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

            # Проверка достижения промежуточной точки (радиус погрешности 0.15)
            if dist < 0.15:
                self.target_idx += 1
                if self.target_idx >= len(self.target_points):
                    self.finished = True
                    elapsed = time.time() - self.start_time
                    self.get_logger().info(f'Ведущая черепаха завершила путь за {elapsed:.2f} сек!')

                    # Публикуем результат в топик
                    res = Float64()
                    res.data = float(elapsed)
                    self.result_pub.publish(res)
                    return

            # Вычисление угла и нормализация ошибки
            target_angle = math.atan2(dy, dx)
            angle_err = math.atan2(
                math.sin(target_angle - self.current_pose.theta),
                math.cos(target_angle - self.current_pose.theta)
            )

            # П-регулятор: разворот и движение вперед
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

            # Следуем за первой черепахой, если расстояние больше 0.08
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
