from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    ld = LaunchDescription()
    
    mount_node = Node(
        package='usb_mount',
        executable='mount',
        #name='/* node_name */',
        output='screen'
    )

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
    
    ld.add_action(mount_node)
    ld.add_action(rgb_node)
    ld.add_action(ir_node)   
    
    return ld
