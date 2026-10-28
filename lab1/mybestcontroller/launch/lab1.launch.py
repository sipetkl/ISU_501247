from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import ExecuteProcess, TimerAction

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='turtlesim',
            executable='turtlesim_node',
            name='sim'
        ),
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
        Node(
            package='mybestcontroller',
            executable='lab1_controller',
            name='controller_leader',
            namespace='ns1_501247'
        ),
        Node(
            package='mybestcontroller',
            executable='lab1_controller',
            name='controller_follower',
            namespace='ns2_501247'
        )
    ])
