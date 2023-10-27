from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    ld = LaunchDescription()
    ir_node = Node(
        package='ir_camera',
        executable='ir_grab',
        #name='/* node_name */',
        output='screen'
    )

    rgb_node = Node(
        package='rgb_camera',
        executable='rgb_grab',  
        output='screen'
    )
    
    ld.add_action(ir_node)
    ld.add_action(rgb_node)
    
    return ld
