# Nano_Vision : This repository is an example to acquire RGB and IR streams, saving the streams to an external USB, using Jetson Nano.

####  OS: ROS2 Humble Running in XUbuntu (Ubuntu for Jetson Nano).
####  Cameras: Allied Vision Alvium 1800 U-508c for RGB stream and FLIR ADK for IR stream.

### Pre-Requisites:

  1) Vmbpy:
     Vmbpy library needs to be installed in order to use the Allied Vision camera(s) in ROS2. To use VmbPy an installation of Vimba X and Python >= 3.7 are required.

     a) Download VimbaX SDK: Download "VimbaX_Setup-2023-1-Linux64.tar.gz" file from their page
     
         https://www.alliedvision.com/en/products/software/vimba-x-sdk/

     b) Installing VimbaX SDK: Follow the instruction from their page

         https://cdn.alliedvision.com/fileadmin/content/documents/products/software/software/Vimba/appnote/Vimba_installation_under_Linux.pdf
         
     c) Installing Vmbpy: A ready-to-install packaged `.whl` file of VmbPy can be found as part of the Vimba X installation (under VimbaX_2023-1/api/python), or be downloaded from their page

         https://github.com/alliedvision/VmbPy/releases
     The `.whl` can be installed as usual via the `pip3 install` command.

     Note: Once the VimbaX SDK and Vmbpy are installed, proceed to the next steps, as all the necessary files and folders will be saved in the required folders once this repository is cloned.

  
  2) OpenCV:
        OpenCV is used to process and display the images for both the IR and RGB streams. It can be installed with

         pip3 install opencv-contrib-python
  3) USB Utils:
        The launch file uses NTFS formatted USB stick in order to write the streams into the USB drive. But if for some reason the USB is formatted as FAT or exFAT filesystem, then the "utils" for exfat needs to be installed in the Jetson Nano, as by default it doesn't have exfat utils installed.

### Setting up the repository:
  After installing the pre-requisites successfully, clone this repository either as a separate ROS2 workspace or else clone the packages and build it manually.

    git clone https://github.com/Vom1124/Nano_Vision.git && \
      cd Nano_Vision && \
      colcon build --symlink-install

### Starting the nodes:
  To start the streams, simply start the IR stream by running the code below in a terminal
  
    ros2 run IRCamera ir_grab
  
  Similarly, start the RGB stream by running the following code in a new terminal
  
    ros2 run RGBCamera rgb_grab

  Two individual streams should be open in separate windows. Both streams will be saved to an external USB drive if inserted or else will save it from the directory the nodes are run.

  
  
     
