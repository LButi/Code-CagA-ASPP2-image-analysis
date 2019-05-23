# Code-CagA-ASPP2-image-analysis
Contains python and ijm files
# Python and ImageJ Scripts for CagA-ASPP2-image-analysis

This repository contains the corresponding Python code and ImageJ scripts used to analyse the CagA-ASPP2 image screening carried out in the following publication:

CagA-ASPP2 complex mediated loss of cell polarity favours H.pylori colonisation of human gastric organoids 

## Downloading the Code

The code can be download either by cloning this repository `git clone https://github.com/LButi/Code-CagA-ASPP2-image-analysis.git` or by downloading the .zip file under the release tab in the banner above.

## Running the Code

The main script to run the code is provided by the `Python_code.py` script. This script can be run in terminal assuming you have a valid Python installation as follows

```
python Python_code.py --rootfolder=="The root folder path where your data is" --imagejfolder="The folder path where your ImageJ version 1.x folder is" --macrofolder="The folder path where your macros are" --resultsfolder="Folder name of where the analysis results will end up (will be put in rootfolder)"
```

## Summary of the Individual Scripts
Script Name | Function
------------| -------------
`Count_Dot_Area.ijm` | ImageJ macro for counting the CagA foci
`Count_Nuclei.ijm` | ImageJ macro for nuclei counting
`Python_code.py` | main python file for calling the ImageJ macros for batch processing

## Citing
If you find this code useful please cite the following publication:

CagA-ASPP2 complex mediated loss of cell polarity favours H.pylori colonisation of human gastric organoids
