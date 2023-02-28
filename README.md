# Pi-Pupil-Detection
This repository contains code from the paper: 
Ankur Raj, Diwas Bhattarai, & Kristof Van Laerhoven (2023), "An Embedded and Real-Time Pupil Detection Pipeline". https://doi.org/10.5281/zenodo.7682640

And from my thesis: *Embedded Pupil Detection on a Raspberry Pi-based Wearable System*.

## Eye-Tracker-Hardware
Our open-source hardware .stl files by Diwas Bhattarai can be found in [Hardware](https://github.com/Lifestohack/masterthesis-eye-tracker/tree/master/models) and be 3D-printed. It uses the Logitech c615 as a world camera and the Raspberry Pi camera as an (IR-lit) eye camera.
![Image](overview.png)

## Basic requirement
Since the development was done on both Windows and Raspberry Pi, parts of code can be run as standalone software.
To have the complete eye tracking experience with the [eye tracker](https://github.com/Lifestohack/masterthesis-eye-tracker/tree/master/models), the eye tracker has to be put together first.

## Project structure
```
Pi-Pupil-Detection
│   README.md
└───Configuration
│   │- Shell Script for project config in Pi
│
└───Raspberry-Pi
│    │- Sripts used for pupil detection on Pi   
│    
└─── Windows
│    │- Pupil detectors and Workbench for modifying parameters for detection  
....

```
## Installing OpenCV and all dependencies on the Raspberry Pi:
Make the configuration-pi.sh script in the Configuration folder executable: 
```chmod a+x configration-pi.sh```

And then execute it with:
```sudo ./configuration-pi.sh```

## Running the cameras:

