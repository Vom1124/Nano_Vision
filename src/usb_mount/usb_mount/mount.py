import os
import getpass
import sys # Importing sys utils
import time # For computing the time

def mount():

    # Logging in as sudo user
    os.system("sudo -k") # First exiting the sudo mode if already in sudo mode
    sudoPassword = "123"
    os.system("echo '\e[7m \e[91m Logging in as sudo user...\e[0m'")
    os.system("echo %s | sudo -i --stdin" %(sudoPassword))
    os.system("echo '\n \e[5m \e[32m*Successfully logged in as sudo user!*\e[0m'")
    current_username = getpass.getuser()

    # Checking if USB drive is mounted
    isMountsda = os.path.exists("/dev/sda1")
    isMountsdb = os.path.exists("/dev/sdb1")
    isMountsdc = os.path.exists("/dev/sdc1")
    isMountsdd = os.path.exists("/dev/sdd1")

    print("sda status" + str(isMountsda) + "\nsdb status" + \
      str(isMountsdb) + "\nsdc status" + str(isMountsdc) + \
            "\nsdd status" + str(isMountsdd))

    # Now creating a mountpoint name for the USB manually
    if isMountsda==True or isMountsdb==True or isMountsdc==True or isMountsdd==True:     
      #Removing/Unmounting (clearing) already existing mountpoint to avoid overlap in the mount status
      os.system("echo 123 | sudo -S umount /dev/sd* > /dev/null  2>&1") # the output will be null
      os.system("echo '\e[33mINFO: Mount status success: a USB drive is found.\
      The video stream will be saved to the inserted USB.\e[0m'")
      
      #Checking if mount point name already exists (Need to create only on the first run).
      isMountPointName = os.path.exists("/media/Nano_Vision")

      os.system("echo 123 | sudo -S chown %s:%s /media/"%(current_username,current_username))
      os.system("echo 123 | sudo -S chown %s:%s /dev/sd*"%(current_username,current_username))
      
      if isMountPointName==True:
        try:
          os.system("echo 123 | sudo -S rm -r /media/Nano_Vision/*")
          os.system("mkdir /media/Nano_Vision/") # Creating a mount point name

        except:
          pass
      elif isMountPointName==False:      
        os.system("mkdir /media/Nano_Vision/") # Creating a mount point name
        
      '''
      The order of checking the mount is reversed to ensure that there 
      is no problem mounting with already preserved mountpoints by the system.
      For example, if sda is already mounted by the system for some port address, then the access to 
      mount the sda for USB drive won't exist. So, the further options will be checked, by in the mean time, the sda in the 
      alphabetical order will throw an error and stop the code. Therefore, the mount check is initiated with sdc.
      Only three /dev/sd* are used, as atmost three ports will be used simultaneously. 
      '''

      if isMountsdd:
          mountCommand = "echo 123 | sudo -S mount /dev/sdd1 /media/Nano_Vision/ -o umask=022,rw,uid=1000,gid=1000"
      elif isMountsdc:
          mountCommand = "echo 123 | sudo -S mount /dev/sdc1 /media/Nano_Vision/ -o umask=022,rw,uid=1000,gid=1000"
      elif isMountsdb:
          mountCommand = "echo 123 | sudo -S mount /dev/sdb1 /media/Nano_Vision/ -o umask=022,rw,uid=1000,gid=1000"
      elif isMountsda:
          mountCommand = "echo 123 | sudo -S mount /dev/sda1 /media/Nano_Vision/ -o umask=022,rw,uid=1000,gid=1000"


      os.system(mountCommand)
      os.system("echo '\e[7m Successfully mounted the USB to Nano Vision...\e[0m'")


def main():
    mount()


if __name__ == '__main__':
    main()
