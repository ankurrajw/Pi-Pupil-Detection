# Pi-Pupil-Detection
This repository contains code from the paper: 
Ankur Raj, Diwas Bhattarai, & Kristof Van Laerhoven (2023), "An Embedded and Real-Time Pupil Detection Pipeline". https://doi.org/10.5281/zenodo.7682640

And from my thesis: *Embedded Pupil Detection on a Raspberry Pi-based Wearable System*.

## Build your own Eye-Tracker
Our open-source hardware .stl files by Diwas Bhattarai can be found in [Hardware](https://github.com/Lifestohack/masterthesis-eye-tracker/tree/master/models) and be 3D-printed. It uses the Logitech c615 as a world camera and the MicroSoft HD 6000 or Raspberry Pi camera as an (IR-lit) eye camera.
![Image](overview.png)

## Basic requirements
Since the development was done offline (on Windows) and on the Raspberry Pi, parts of code can be run as standalone software.
To have the complete eye tracking experience with the [Eye-Tracker](https://github.com/Lifestohack/masterthesis-eye-tracker/tree/master/models), the eye tracking hardware has to be put together first (see above).

## Project structure
```
Pi-Pupil-Detection
│   README.md
└───Configuration
│   │- Shell Script for project config in Pi
│
└───Raspberry-Pi
│    │- Scripts used for pupil detection on Pi   
│    
└─── Windows
│    │- Pupil detectors and Workbench for modifying parameters for detection  
....

```
## Installing OpenCV and all dependencies on the Raspberry Pi:
Make the configuration-pi.sh script in the Configuration folder executable: 
```chmod a+x configuration-pi.sh```

And then execute it with:
```sudo ./configuration-pi.sh```

## Running the cameras:

