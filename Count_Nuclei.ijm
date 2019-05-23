// Batch count nuclei for Operetta
//
// This macro counts nuclei in Operetta output tiff files
// Works with single channel 16 bit images
//


//define what to measure
run("Set Measurements...", "area redirect=None decimal=3");

//define colours for back, fore and selection
run("Colors...", "foreground=black background=black selection=white");

//Source and destination folders
//dir1 = getDirectory("Choose Source Directory ");
//dir2 = getDirectory("Choose Destination Directory ");
arguments = getArgument()
arguments = split(arguments,";");
dir1 = arguments[0];
dir2 = arguments[1];
list = getFileList(dir1);
setBatchMode(false);
notice = "converted: \n";

//setup loop
for (i=0; i<list.length; i++) 
{
showProgress(i+1, list.length);

// open image
open(dir1+list[i]);

//set scale pixle = 0.2um
run("Properties...", "channels=1 slices=1 frames=1 unit=um pixel_width=0.2 pixel_height=0.2 voxel_depth=1");

//subtract background 
run("Subtract Background...", "rolling=50");
 
//light blur to remove noise and simplify
run("Gaussian Blur...", "sigma=2");

//Normalise
run("Enhance Contrast...", "saturated=0.4");

// threshold 
setAutoThreshold("Default");
//run("Threshold...");
setAutoThreshold("Triangle dark");
setOption("BlackBackground", false);
//run("Subtract...", "value=500");
run("Min...", "value=100");
run("Log");
run("Convert to Mask");

// fill holes in nuclei - probably not required
run("Fill Holes");

// seperate touching nuclei
run("Watershed");

//Count nuclei
run("Analyze Particles...", "size=30-Infinity circularity=0.20-1.00 summarize");

//clean up  
close();

notice = notice + dir1+list[i] + "\n";

//next loop
}

//save Summary window = Results
selectWindow("Summary");
saveAs("Text", dir2+"Summarynucleus.txt");

//save Log window = file name list - not required so save commented out
print(notice);
selectWindow("Log");
//saveAs("Text", dir2+"Filenames.txt");
run("Quit");

