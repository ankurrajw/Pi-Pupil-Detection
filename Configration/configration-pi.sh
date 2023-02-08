#!/bin/sh

# software package for Pi-Pupil-Detection (Raspberry Pi 4)
clear
echo "Updating OS"
echo "========================================="
sudo apt update upgrade
echo "installing open cv python"
echo "========================================="
sudo apt install libopencv-dev python3-opencv -y
echo "installing gstreamer librearies"
echo "========================================="
sudo apt-get install libx264-dev libjpeg-dev -y
echo "installing gstreamer"
echo "========================================="
sudo apt-get install libgstreamer1.0-dev \
     libgstreamer-plugins-base1.0-dev \
     libgstreamer-plugins-bad1.0-dev \
     gstreamer1.0-plugins-ugly \
     gstreamer1.0-tools \
     gstreamer1.0-gl \
     gstreamer1.0-gtk3 -y
sudo apt-get install gstreamer1.0-qt5 -y
sudo apt-get install gstreamer1.0-pulseaudio -y
echo "installing git"
echo "========================================="
sudo apt install git-all -y
sudo apt install git-gui -y
echo "Real VNC"
echo "========================================="
sudo apt-get install real-vnc-server
#enable manually by going to raspi-config interface