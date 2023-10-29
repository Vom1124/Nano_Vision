"""
This code is written and modified by Vomsheendhur Raju, NDSU, Fargo, ND on 07/04/2023.

BSD 2-Clause License
Copyright (c) 2022, Allied Vision Technologies GmbH
All rights reserved.
"""
'''
The code was originally re-written using the original source code provided by the Allied Vision Technologies. 
'''
"""
This  node grabs the image from the Allied Vision 1800 U-508c camera and streams it in a separate window.
Some modification to the image is done to display asyncrhonously. The streamed video will be saved wither in home directory or in a USB stick if one is inserted. 


The inserted USB stick's UUID mountpoint name is changed to VOM within this code, which needs to be done in order to succesfully access the USB directory to save the stream.
"""

import os
import getpass
import logging
import queue
from functools import partial 

import sys
import time
import threading
from typing import Optional, Tuple

from vmbpy import *
import cv2

# Logging in as sudo user
os.system("sudo -k") # First exiting the sudo mode if already in sudo mode
sudoPassword = "123"
os.system("echo '\e[7m \e[91m Logging in as sudo user...\e[0m'")
os.system("echo %s | sudo -i --stdin" %(sudoPassword))
os.system("echo '\n \e[5m \e[32m*Successfully logged in as sudo user!*\e[0m'")
current_username = getpass.getuser()


# True resolution of the 1800 U-508c
w = 2464 # Width of the stream/ resize frame
h = 2056 # Height of the stream/ resize frame
#Setting the display window size
w_d = 640
h_d = 480
frame_queue = queue.Queue(maxsize=10) # globally defining the frame queue to start the counter

def print_preamble():
    print('///////////////////////////////////////////////////')
    print('/// VmbPy Asynchronous Grab with OpenCV Example ///')
    print('///////////////////////////////////////////////////\n')


def print_usage():
    print('Usage:')
    print('    python rgb_grab.py [camera_id]')
    print('    python rgb_grab.py [/h] [-h]')
    print()
    print('Parameters:')
    print('    camera_id   ID of the camera to use (using first camera if not specified)')
    print()


def abort(reason: str, return_code: int = 1, usage: bool = False):
    print(reason + '\n')

    if usage:
        print_usage()

    sys.exit(return_code)


# def parse_args() -> Optional[str]:
#     args = sys.argv[1:]
#     argc = len(args)

#     for arg in args:
#         if arg in ('/h', '-h'):
#             print_usage()
#             sys.exit(0)

#     if argc > 1:
#         abort(reason="Invalid number of arguments. Abort.", return_code=2, usage=True)

#     return None if argc == 0 else args[0]


# def get_camera(camera_id: Optional[str]) -> Camera:
#     with VmbSystem.get_instance() as vmb:
#         if camera_id:
#             try:
#                 return vmb.get_camera_by_id(camera_id)

#             except VmbCameraError:
#                 abort('Failed to access Camera \'{}\'. Abort.'.format(camera_id))

#         else:
#             cams = vmb.get_all_cameras()
#             if not cams:
#                 abort('No Cameras accessible. Abort.')

#             return cams[0]

def setupCamera(cam: Camera):

    with cam:
        
        # Try to adjust GeV packet size. This Feature is only available for GigE - Cameras.
        try:
            stream = cam.get_streams()[0]
            stream.GVSPAdjustPacketSize.run()

            while not stream.GVSPAdjustPacketSize.is_done():
                pass

        except (AttributeError, VmbFeatureError):
            pass
            
        # Change the pixel format
        try:
            cam.set_pixel_format(PixelFormat.Bgr8)
        except (AttributeError, VmbFeatureError):
            pass

        # Enable auto exposure time setting if camera supports it
        cam.ExposureAuto.set(False)
        cam.ExposureTime.set(10000)
        # except (AttributeError, VmbFeatureError):
            # pass

        # Enable white balancing if camera supports it
        try:
            cam.BalanceWhiteAuto.set(True)
        except (AttributeError, VmbFeatureError):
            pass

        # Modify Height and Width of the streams
        try:
            cam.Height.set(2056)
            cam.Width.set(2464)
        except (AttributeError, VmbFeatureError):
            pass

        # Set the Acquisition mode
        try:
            cam.AcquisitionMode.set('Continuous')
        except (AttributeError, VmbFeatureError):
            pass
            
            
        # Set the Gain
        try:
            cam.GainAuto.set(False)
            cam.Gain.set(3)
        except (AttributeError, VmbFeatureError):
            pass
            
        # Set the Gamma
        try:
            cam.Gamma.set(2.4) #within [0.4000000059604645, 2.4000000953674316].
        except (AttributeError, VmbFeatureError):
            pass
      
        #Set the FPS
        try:
            cam.AcquisitionFrameRateEnable.set(False)
            cam.AcquisitionFrameRate.set(12.809)#within [1.0369063602411188e-05, 12.809259414672852]
        except (AttributeError, VmbFeatureError):
            pass

        
         
        



def frame_handler(cam, stream, frame):
    
    if frame.get_status() == FrameStatus.Complete:
        #print('{} acquired {}'.format(cam, frame), flush=True)        
        #print(dir(frame))
        try:
            frame_queue.put_nowait(frame)

        except queue.Full:
            print('[INFO]: Queue is full; frame dropped')

    cam.queue_frame(frame)



def processingImage(cam):
    
    fps =  int (cam.AcquisitionFrameRate.get()) # getting the fps
    videoWrite = videoWriter(fps)
    try:
        #print(dir(cam))
        cam.start_streaming(frame_handler, buffer_count = 5)
        
        #start_time = time.time()
        #frame_count=0
        
        while True :
            if frame_queue.qsize()>0:
                try:
                    current_frame = frame_queue.get_nowait()
                    display_frame = current_frame.as_opencv_image()
                    
                    #frame_count+=1
                    # Displaying the fps in the image stream
                    #fps_true = int((frame_count)/(time.time()-start_time))
                    cv2.putText(display_frame, 'Acquired frame id={}' .format(current_frame.get_id()) + ' with fps=' + str(fps), (20,2000), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0,255,20), 3, cv2.LINE_AA)
                    
                    display_frame_scaled = cv2.resize(display_frame, (w_d,h_d))                    
                    cv2.imshow('RGB Stream (Press "q" to Stop the Stream)', display_frame_scaled)
                    
                    videoWrite.write(display_frame_scaled)

                except queue.Empty:
                    pass

            if (cv2.waitKey(1) == ord('q')):
                break        
                  
    finally:
        cam.stop_streaming()
        

def videoWriter(fps):

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
        isMountPointName = os.path.exists("/media/Nano_Vision/RGB")

        os.system("sudo chown %s:%s /media/Nano_Vision"%(current_username,current_username))
        os.system("sudo chown %s:%s /dev/sd*"%(current_username,current_username))
        
        if isMountPointName==True:
            try:
                os.system("sudo rm -r /media/Nano_Vision/*")
                os.system("mkdir /media/Nano_Vision/RGB") # Creating a mount point name
            except:
                pass
        elif isMountPointName==False:      
            os.system("mkdir /media/Nano_Vision/RGB") # Creating a mount point name
        '''
        The order of checking the mount is reversed to ensure that there 
        is no problem mounting with already preserved mountpoints by the system.
        For example, if sda is already mounted by the system for some port address, then the access to 
        mount the sda for USB drive won't exist. So, the further options will be checked, by in the mean time, the sda in the 
        alphabetical order will throw an error and stop the code. Therefore, the mount check is initiated with sdc.
        Only three /dev/sd* are used, as atmost three ports will be used simultaneously. 
        '''
        if isMountsdd:
            mountCommand = "sudo mount /dev/sdd1 /media/Nano_Vision/RGB -o umask=022,rwx,uid=1000,gid=1000"
        elif isMountsdc:
            mountCommand = "sudo mount /dev/sdc1 /media/Nano_Vision/RGB -o umask=022,rwx,uid=1000,gid=1000"   
        elif isMountsdb:
            mountCommand = "sudo mount /dev/sdb1 /media/Nano_Vision/RGB -o umask=022,rwx,uid=1000,gid=1000"
        elif isMountsda:
            mountCommand = "sudo mount /dev/sda1 /media/Nano_Vision/RGB -o umask=022,rwx,uid=1000,gid=1000"
        
        os.system(mountCommand)    
        videoWrite = cv2.VideoWriter("/media/Nano_Vision/RGB/RGBOutput.avi", cv2.VideoWriter_fourcc(*'XVID'), fps, (w_d,h_d)) 
        
    else:
        print("WARNING: Mount status failure: no USB inserted to write the video. The stream will be saved to local drive instead.")
        videoWrite = cv2.VideoWriter("RGBOutput.avi", cv2.VideoWriter_fourcc(*'XVID'), fps, (w_d,h_d))

    
      
    return videoWrite
    

def main():
    print_preamble()
    with VmbSystem.get_instance() as vmb:
        cams = vmb.get_all_cameras()
        if not cams:
            abort('No Cameras accessible. Abort.')

        with cams[0] as cam:
            print("--> Camera has been opened (%s)" % cam.get_id())
            setupCamera(cam)
            processingImage(cam)

if __name__== '__main__':
    main()
