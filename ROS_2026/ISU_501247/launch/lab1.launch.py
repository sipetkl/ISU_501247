from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import ExecuteProcess, TimerAction

def generate_launch_description():
    return LaunchDescription([
        # 1. Запускаем симулятор
        Node(
            package='turtlesim',
            executable='turtlesim_node',
            name='sim'
        ),
        
        # 2. Ждем 2 секунды и спавним вторую черепаху через службу
        TimerAction(
            period=2.0,
            actions=[
                ExecuteProcess(
                    cmd=['ros2', 'service', 'call', '/spawn', 'turtlesim/srv/Spawn', 
                         "{x: 5.0, y: 2.0, theta: 0.0, name: 'turtle2'}"],
                    output='screen'
                )
            ]
        ),

        # 3. Контроллер Лидера (управляет turtle1)
        Node(
            package='mybestcontroller',
            executable='lab1_controller',
            name='controller_leader',
            namespace='ns1_501247'
        ),

        # 4. Контроллер Ведомого (управляет turtle2)
        Node(
            package='mybestcontroller',
            executable='lab1_controller',
            name='controller_follower',
            namespace='ns2_501247'
        )
    ])
