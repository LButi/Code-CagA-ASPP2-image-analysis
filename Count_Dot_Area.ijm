//Source and destination folders
//dir1 = getDirectory("Choose Source Directory ");
//dir2 = getDirectory("Choose Destination Directory ");
arguments = getArgument()
arguments = split(arguments,";");
dir1 = arguments[0];
dir2 = arguments[1];
list = getFileList(dir1);
setBatchMode(true);
notice = "converted: \n";

//setup loop
for (i=0; i<list.length; i++) 
{
showProgress(i+1, list.length);

// open image
open(dir1+list[i]);

setAutoThreshold("Default dark");
setThreshold(2000, 100000);
run("Set Measurements...", "area redirect=None decimal=3");
run("Analyze Particles...", "pixel summarize");
//clean up  
close();


notice = notice + dir1+list[i] + "\n";

//next loop
}

//save Summary window = Results
selectWindow("Summary");
saveAs("Text", dir2+"DotSummary.txt");

//save Log window = file name list - not required so save commented out
//print(notice);
//selectWindow("Log");
//saveAs("Text", dir2+"Filenames.xls");
run("Quit");