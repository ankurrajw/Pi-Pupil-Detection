# Raspberry Pi Detector

This repository contains files for the Raspberry Pi detector.
It has the files for **dataset creation** as well as the **detection methods**.

## Detectors

* Ellipse Fitting - *detector_ellipse.py*
* Hough Circles - *detector_hough.py*
* HAAR - *detector_haar.py*

## Dataset creation scripts
Use theres scripts to create near eye pupil image datasets.

* Marker location - *dataset_marker_locations.py*
5 fixed positional markers are shown to the participant and they observe each marker sequentially to create a dataset for fixed locations.

* Free movement - *dataset_experiment_free_movement.py*
The participants are not limited to seeing fixed markers and are encouraged to look in different directions


## Naming convention for dataset creation

**dataset_experiment_file_name** - files that correspond to dataset creation

**detector_file_name** - files that correspond to detection strategies

## Errors
**open cv-resource busy** - The resource (camera stream) is currently being used by another application or 
there is no/less daley between two immediate image captures within the current project.

If it is the later case try to add some delay between the image captures
