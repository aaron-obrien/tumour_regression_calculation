# Tumour regression calculation tool (TURCAT)
User can shape and move a box around CT, MRI or PET scans of a tumour for images pre and post treatment. A tumour regression curve is then calculated to determine how effective treatment is.

## Description
Users initially specify a folder containing dicom (.dcm) images of medical scans at different stages of treatment. Each image will appear sequentially (following exiting the window of the previous image) with a red box in the centre, which can be moved and reshaped around the tumour using the mouse and arrow keys. A line graph is displayed after every image is analysed, showing the tumour regression over time, and then saved as .png file in the directory of the specified folder.

## Usage
Arrow keys to shorten/lengthen the box
  -Right arrow key makes the box 1 unit wider
  -Left arrow key makes the box 1 unit less wide
  -Up arrow key makes the box 1 unit taller
  -Down arrow key makes the box 1 unit shorter
Hold the control key with the use of any arrow key to reshape the box by 10 units (e.g. ctrl-right makes the box 10 units wider).
Click and drag the box around to move the box around the tumour.

Note: If the tumour regression curve is calculated in the same folder twice, the original image will be overwritten.

## Installation
Download the folder with the script, test images and test output

## Pre-requisite python modules
python3.8
matplotlib.pyplot
matplotlib.patches
pydicom
os

## Disclaimer
Please note this software is for research use only and not intended as a clinical device, or to aid any form of clinical judgement. 
