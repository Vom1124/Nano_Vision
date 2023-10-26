from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    ld = LaunchDescription()
    
    rgbCameraNode = Node(       
        package="rgb_camera",
        executable="rgb_grab" 
    )
    
    ld.add_action(rgbCameraNode)
    
    return ld

