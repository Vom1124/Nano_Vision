from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    ld = LaunchDescription()
    
    irCameraNode = Node(       
        package="ir_camera",
        executable="ir_grab" 
    )
    
    ld.add_action(irCameraNode)
    
    return ld

