from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='turtlesim',
            executable='turtlesim_node',
            namespace='ns1_501247',
            name='sim',
            output='screen'
        ),
        Node(
            package='mybestcontroller',
            executable='lab1_controller',
            namespace='ns1_501247',
            output='screen'
        ),
        Node(
            package='turtlesim',
            executable='turtlesim_node',
            namespace='ns2_501247',
            name='sim',
            output='screen'
        ),
        Node(
            package='mybestcontroller',
            executable='lab1_controller',
            namespace='ns2_501247',
            output='screen'
        ),
    ])
