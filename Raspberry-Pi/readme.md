# Raspberry Pi Detector

This repository contains files for the Raspberry Pi detector.
It has the files for **dataset creation** as well as the **detection methods**.

## Naming convention

**dataset_experiment_file_name** - files that correspond to dataset creation

**detector_file_name** - files that correspond to detection strategies

## Errors
**open cv-resource busy** - The resource (camera stream) is currently being used by another application or 
there is no/less daley between two immediate image captures within the current project.

If it is the later case try to add some delay between the image captures
