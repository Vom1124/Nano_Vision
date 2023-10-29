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

# Logging in as sudo user
os.system("sudo -k") # First exiting the sudo mode if already in sudo mode
sudoPassword = "123"
os.system("echo '\e[7m \e[91m Logging in as sudo user...\e[0m'")
os.system("echo %s | sudo -i --stdin" %(sudoPassword))
os.system("echo '\n \e[5m \e[32m*Successfully logged in as sudo user!*\e[0m'")
current_username = getpass.getuser()


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

    
    videoWrite = videoWriter(fps, w, h)
    # The true fps is calculcated after writing the video to the file which consumes significant time. 
    # In this setup it was found that the actual fps is around 22 whereas the acquired fps is 30.

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
        
        # Displaying the image in a new window
        cv2.imshow('Infrared Stream (Press "q" to stop streaming)', display_frame)

        # Writing the video to a file
        videoWrite.write(display_frame)
        
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

  print("sda status" + str(isMountsda) + "\nsdb status" + \
      str(isMountsdb) + "\nsdc status" + str(isMountsdc) + \
            "\nsdd status" + str(isMountsdd))

  # Now creating a mountpoint name for the USB manually
  if isMountsda==True or isMountsdb==True or isMountsdc==True:     
      #Removing/Unmounting (clearing) already existing mountpoint to avoid overlap in the mount status
      os.system("sudo umount /dev/sd* > /dev/null  2>&1") # the output will be null
      os.system("echo '\e[33mINFO: Mount status success: a USB drive is found.\
      The video stream will be saved to the inserted USB.\e[0m'")
      
      #Checking if mount point name already exists (Need to create only on the first run).
      isMountPointName = os.path.exists("/media/Nano_Vision/IR")

      os.system("sudo chown %s:%s /media/"%(current_username,current_username))
      os.system("sudo chown %s:%s /dev/sd*"%(current_username,current_username))
      
      if isMountPointName==True:
          try:
              os.system("sudo rm -r /media/Nano_Vision/*")
              os.system("mkdir /media/Nano_Vision/IR") # Creating a mount point name
          except:
              pass
      elif isMountPointName==False:      
          os.system("mkdir /media/Nano_Vision/IR") # Creating a mount point name
      '''
      The order of checking the mount is reversed to ensure that there 
      is no problem mounting with already preserved mountpoints by the system.
      For example, if sda is already mounted by the system for some port address, then the access to 
      mount the sda for USB drive won't exist. So, the further options will be checked, by in the mean time, the sda in the 
      alphabetical order will throw an error and stop the code. Therefore, the mount check is initiated with sdc.
      Only three /dev/sd* are used, as atmost three ports will be used simultaneously. 
      '''
      if isMountsdd:
          mountCommand = "sudo mount /dev/sdd1 /media/Nano_Vision/IR -o umask=022,rw,uid=1000,gid=1000"
      elif isMountsdc:
          mountCommand = "sudo mount /dev/sdc1 /media/Nano_Vision/IR -o umask=022,rw,uid=1000,gid=1000"   
      elif isMountsdb:
          mountCommand = "sudo mount /dev/sdb1 /media/Nano_Vision/IR -o umask=022,rw,uid=1000,gid=1000"
      elif isMountsda:
          mountCommand = "sudo mount /dev/sda1 /media/Nano_Vision/IR -o umask=022,rw,uid=1000,gid=1000"
      
      os.system(mountCommand)     
      videoWrite = cv2.VideoWriter("/media/Nano_Vision/IR?IROutput.avi", cv2.VideoWriter_fourcc(*'XVID'), fps, (w,h)) 
    
  else:
    print("WARNING: Mount status failure: no USB inserted to write the video. The stream will be saved to local drive instead.")
    videoWrite = cv2.VideoWriter("IROutput.avi", cv2.VideoWriter_fourcc(*'XVID'), fps, (w,h))
      
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
