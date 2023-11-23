"""
This code is written and modified by Vomsheendhur Raju, NDSU, Fargo, ND on 07/04/2023.
"""

"""

This  node grabs the image from the IR camera and streams it in a separate window.
Some modification to the image is done to display fitting the current IR camera 3-d printed case. Change the rotation and colormap parameters accordingly. The streamed video is then saved to the USB drive with known UUID description. 

The inserted USB stick's UUID mountpoint name is changed to VOM within this code, which needs to be done in order to succesfully access the USB directory to save the stream.
"""

# Import the necessary libraries
import os
import getpass
import sys # Importing sys utils
import time # For computing the time

import rclpy # Python Client Library for ROS 2
from rclpy.node import Node # Handles the creation of nodes
from sensor_msgs.msg import Image # Image is the message type
import cv2 # OpenCV library
from cv_bridge import CvBridge # Package to convert between ROS and OpenCV Images



global fps 

class ImageGrabber(Node):
  """
  Create an ImageGrabber class, which is a subclass of the Node class.
  """
  # creating the videocapture object
  # and reading from the USB Cam
  # Change it to 0 or appropriate channel number to reflect the correct USB cam port
  
  
  def __init__(self):

    super().__init__('image_grabber')
    
    cap = cv2.VideoCapture(0) # Capturing the stream from cam id
    if not cap.isOpened():
      print("[Error]: Can not open the capture. Aborted! " +
      "Probably camera is disconnected; check the camera connection.", flush=True)
      sys.exit(0)

        
    w = int(cap.get(3)) # Width 
    h = int(cap.get(4)) # Height 
    fps = float(cap.get(5)) # FPS, check for the true FPS.
    
    # The true fps is calculcated after writing the video to the file which consumes significant time. 
    # In this setup it was found that the actual fps is around 22~30 whereas the acquired fps is 60.
    videoWrite = videoWriter(30, w, h) # Creating the videowrite object
    

    # Used to record the time when we processed last frame
    prev_frame_time = 0
  
    # Used to record the time at which we processed current frame
    new_frame_time = 0
  
    # Reading the video file until finished
    while(cap.isOpened()):

      # Capturing each frame
      ret, frame = cap.read()
      
      if ret == True:
        
        # Rotating the frame to accommodate the 3-d printed case and adding the JET colormap.
        display_frame = cv2.applyColorMap(cv2.rotate(frame,cv2.ROTATE_180), cv2.COLORMAP_JET)
  
     
        # Time when we finish processing for this frame
        new_frame_time = time.time()
  
        # Calculating the true fps
  
        # ps will be number of frame processed in given time frame
        # since there will be most of time error in writing the video to the file,
        # we will be subtracting it to get more accurate result
        fps = int( 1/(new_frame_time-prev_frame_time))

        # Displaying the fps in the image stream
        cv2.putText(display_frame, 'fps='+str(fps), (20,480), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 1, cv2.LINE_AA)
        
        videoWrite.write(display_frame) #writing the frame

        # Displaying the image in a new window
        cv2.imshow('Infrared Stream (Press "q" to stop streaming)', display_frame)

        # Writing the video to a file
        #videoWrite.write(display_frame)
        
        prev_frame_time = new_frame_time

        # Press 'Q' if you want to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):          
          os.system("sudo -k") # Exiting sudo user mode
          sys.exit(0) #Exiting the code.

      # Printing the message with fps
      #self.get_logger().info('Publishing video frame with fps (true)='+ str(fps_true))

def videoWriter(fps, w, h):  

    # Checking if USB drive is mounted
    isMountsda = os.path.exists("/dev/sda1")
    isMountsdb = os.path.exists("/dev/sdb1")
    isMountsdc = os.path.exists("/dev/sdc1")
    isMountsdd = os.path.exists("/dev/sdd1")

    if isMountsda==True or isMountsdb==True or isMountsdc==True or isMountsdd==True:     
      #Use the ROS2 node "usb_mount" to mount it. Otherwise, use the launch file to auto mount it. 
      videoWrite = cv2.VideoWriter("/media/Nano_Vision/IROutput.avi", cv2.VideoWriter_fourcc(*'XVID'), fps, (w,h)) 
    
    else:
      print("WARNING: Mount status failure: no USB inserted to write the video. The stream will be saved to local drive instead.")
      videoWrite = cv2.VideoWriter("/home/%s/IROutput.avi"%(current_username), cv2.VideoWriter_fourcc(*'XVID'), fps, (w,h))
      os.system("echo 123 | sudo -S chmod -R a+rwx /home/%s/IROutput.avi"%(current_username))
      os.system("echo 123 | sudo -S chown %s:%s /home/%s/IROutput.avi"%(current_username,current_username,current_username))

    return videoWrite

  
def main(args=None):
  
  # Initialize the rclpy library
  rclpy.init(args=args)
  
  
  # Create the node
  image_grabber = ImageGrabber()
  

  # Spin the node so the callback function is called.
  rclpy.spin(image_grabber)
  
  # Destroy the node explicitly
  # (optional - otherwise it will be done automatically
  # when the garbage collector destroys the node object)
  image_grabber.destroy_node()
  
  # Shutdown the ROS client library for Python
  rclpy.shutdown()
  
if __name__ == '__main__':
  main()
