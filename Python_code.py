# -*- coding: utf-8 -*-
"""
Created on Wed Nov 18 16:41:12 2015

@author: dsangberg
"""

def moveFilesToFolders(infolder):
    import os
    import shutil
    
    #infolder = 'C:\Users\dsangberg\Documents\LudoDotCounting\CarlosNovResults'
    
    
    if not os.path.isdir(os.path.join(infolder, 'DAPI')) : os.mkdir(os.path.join(infolder, 'DAPI'))
    if not os.path.isdir(os.path.join(infolder, 'FITC')) : os.mkdir(os.path.join(infolder, 'FITC'))
    if not os.path.isdir(os.path.join(infolder, 'Cy5')) : os.mkdir(os.path.join(infolder, 'Cy5'))
    for file in os.listdir(infolder):
        if file.endswith(".tif"):
            #print os.path.join(infolder, 'DAPI', file)
            if 'DAPI' in file:
                shutil.move(os.path.join(infolder, file), os.path.join(infolder, 'DAPI', file))
            elif 'FITC' in file:
                shutil.move(os.path.join(infolder, file), os.path.join(infolder, 'FITC', file))
            elif 'Cy5' in file:
                shutil.move(os.path.join(infolder, file), os.path.join(infolder, 'Cy5', file))
            
def winpath(ins):
    splits = ins.split('\\')
    outs = splits[0]
    for i in range(1,len(splits)):
        outs = outs + '\\\\"' + splits[i] + '"'
    return outs

def fileNameParse(filename):
    letter = filename[0]
    well = filename[4:].split('(')[0]
    field = filename.split()[3]
    return letter+well+'-'+field

def getWellAvgs(datafolder, imagejfolder, macrofolder):
    
    
    import os
    from subprocess import check_output
    import csv
    
               
    #infolder = 'Q:\\Operetta\\Ludo Buti\\InCell\\17Nov15\\AGS_AGS ASPP2_1'
    # 'C:\Users\dsangberg\ImageJ1'

    macro1 = 'Count_Nuclei.ijm'
    macro2 = 'MacroCarlosModified.ijm'
    
    
    #print datafolder
    
    moveFilesToFolders(datafolder) 
     
    
    imagejpath = imagejfolder
    javapath = os.path.join(imagejpath, 'jre', 'bin', 'java')
    jarpath = os.path.join(imagejpath, 'ij.jar')
    dapifolder = os.path.join(datafolder, 'DAPI')
    fitcfolder = os.path.join(datafolder, 'FITC')
    macropath = macrofolder
    countnucmac = os.path.join(macropath, macro1)
    countdotmac = os.path.join(macropath, macro2)
    imagejnucstring = winpath(javapath) + ' -jar -Xmx1024m ' + winpath(jarpath) + ' -macro ' + winpath(countnucmac) + ' ' + winpath(dapifolder) + '\\\\' + ';' + winpath(datafolder) + '\\\\'
    #print imagejnucstring
    if not os.path.exists(os.path.join(datafolder, 'Summarynucleus.txt')) :
        check_output(imagejnucstring, shell=True)
    imagejdotstring = winpath(javapath) + ' -jar -Xmx1024m ' + winpath(jarpath) + ' -macro ' + winpath(countdotmac) + ' ' + winpath(fitcfolder) + '\\\\' + ';' + winpath(datafolder) + '\\\\'
    #print imagejdotstring
    if not os.path.exists(os.path.join(datafolder, 'DotSummary.txt')) :
    	check_output(imagejdotstring, shell=True)
    
    # Read Dot summary file
    dotdic = {}
    with open(os.path.join(datafolder, 'DotSummary.txt'), 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter='\t')
        reader.next() # Skip first meta row
        for row in reader:
            filename = row[0]
            area = row[4]
            filekey = fileNameParse(filename)
            dotdic[filekey] = area
    
    # Read Nuclei summary file
    nucdic = {}
    with open(os.path.join(datafolder, 'Summarynucleus.txt'), 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter='\t')
        reader.next() # Skip first meta row
        for row in reader:
            filename = row[0]
            counts = row[1]
            filekey = fileNameParse(filename)
            nucdic[filekey] = counts
    
    # Calc ratios and put in list dic. Also, write entries in csv file.
    minnuc = 20
    #maxdot = 2000
    #maxrat = 14
    ratiodic = {}
    with open(os.path.join(datafolder, 'Result.txt'), 'w') as f:
        writer = csv.writer(f, delimiter='\t')
        writer.writerow(['File', 'Dots', 'Nuclei', 'Dots/Nuclei', 'Included'])
        for i in range(ord('A'),ord('I')):
            for j in range(1,13):
                for k in range(1,10):
                    key = chr(i)+str(j)+'-'+str(k)
                    if key in dotdic:
                        dots = float(dotdic[key])
                        nucs = float(nucdic[key])
                        rat = 0
                        if nucs != 0:
                            rat = dots/nucs
                        truekey = key[0] + key[1:].split('-')[0] # e.g. A1, F4 etc
                        if nucs > minnuc:
                            if not truekey in ratiodic:
                                ratiodic[truekey] = []
                            ratiodic[truekey].append(rat)
                            writer.writerow([key, dots, nucs, rat, 1])
                        else:
                            writer.writerow([key, dots, nucs, rat, 0])
            
    # Calc averages
    avgdic = {}
    for key in ratiodic:
        avgdic[key] = sum(ratiodic[key])/len(ratiodic[key])
    
    return avgdic
    
def writeAndPlot(avgdic, folder, threshold, shouldPrint):
    import numpy as np
    import matplotlib.pyplot as plt

    norms = ['A1','A12','H1','H12']
    controls = ['B1','C1','D1','E1','F1','G1','B12','C12','D12','E12','F12','G12']
    normconst = 0
    for norml in norms:
        c = 0
	if norml in avgdic:
            c = avgdic[norml]
        normconst = normconst + c
    normconst = normconst/float(len(norms))
    #normconst = (avgdic['A1']+avgdic['A12']+avgdic['H1']+avgdic['H12'])/4.0
    bignormavgs = []
    littlenormavgs = []
    keys = []
    bigindices = []
    littleindices = []
    negcont = []
    negindices = []
    special = []
    spindices = []
    counter = 0
    
    #basefolder = os.path.basename(folder)
    #dirname = os.path.dirname(folder)
    
    with open(os.path.join(folder + '.txt'), 'w') as f:
        writer = csv.writer(f, delimiter='\t')
        writer.writerow(['Well', 'Average', 'Norm Avg', 'Above thresh'])
        for i in range(ord('A'),ord('I')):
            for j in range(12):
                counter = counter+1
                key = chr(i)+str(j+1)
                keys.append(key)
                
                if key in avgdic:
                    normav = avgdic[key]/normconst
                    
                    if key in norms:
                        negcont.append(normav)
                        negindices.append(counter)
                        writer.writerow([key, avgdic[key], normav, 0])
                    elif key in controls:
                        special.append(normav)
                        spindices.append(counter)
                        writer.writerow([key, avgdic[key], normav, int(normav>threshold)])
                    elif normav > threshold:
                        bignormavgs.append(normav)
                        bigindices.append(counter)
                        writer.writerow([key, avgdic[key], normav, 1])
                    else:
                        littlenormavgs.append(avgdic[key]/normconst)
                        littleindices.append(counter)
                        writer.writerow([key, avgdic[key], normav, 0])
                        if shouldPrint: print key
                else:
                    writer.writerow([key, 0, 0, 0])
                    littlenormavgs.append(0)
                    littleindices.append(counter)       
    
    # split it up
    #above_threshold = np.maximum(values - threshold, 0)
    #below_threshold = np.minimum(values, threshold)
    
    # and plot it
    fig, ax = plt.subplots()
    ax.bar(negindices, negcont, color="g")
    ax.bar(spindices, special, color="y")
    ax.bar(bigindices, bignormavgs, color="b")
    ax.bar(littleindices, littlenormavgs, color="r")
    ax.set_ylim([0,15])
    plt.xticks(range(1,97,12), ['A1','B1','C1','D1','E1','F1','G1','H1'])
    
    # horizontal line indicating the threshold
    ax.plot([0., 100], [threshold, threshold], "k-")
    ax.plot([0., 100], [4, 4], "k--")
    
    fig.savefig(os.path.join(folder + '.png'))
    
import argparse
import os
import csv


parser = argparse.ArgumentParser()
parser.add_argument("rootfolder", help="The root folder path where your data is")
#parser.add_argument("resultsfolder", help="The folder path where your results will end up")
parser.add_argument("imagejfolder", help="The folder path where your ImageJ version 1.x folder is")
parser.add_argument("macrofolder", help="The folder path where your macros are")
parser.add_argument("resultsfolder", help="Folder name of where the analysis results will end up (will be put in rootfolder)")
args = parser.parse_args()

if not os.path.isdir(os.path.join(args.rootfolder, args.resultsfolder)) :
    os.mkdir(os.path.join(args.rootfolder, args.resultsfolder))

threshold = 1.5

#relevantfolders = ['Plate1','Plate2','Plate3','Plate4','Plate5','Plate6','Plate7','Plate8','Plate9','Plate10','Plate11','Plate12','Plate13','Plate14','Plate15','Plate16']
# relevantfolders = ['Plate2','Plate13','Plate14','Plate15']
relevantfolders = ['Plate1','Plate2']
for subfolder in os.listdir(args.rootfolder):
    if os.path.isdir(os.path.join(args.rootfolder, subfolder)) and subfolder in relevantfolders:
        print subfolder
        experimentfolder = os.path.join(args.rootfolder, subfolder)
        repavgdic = {}
        #print experimentfolder
        foldcount = 0
        for folder in os.listdir(experimentfolder):
            if os.path.isdir(os.path.join(experimentfolder, folder)):
                foldcount = foldcount+1
                avgdic = getWellAvgs(os.path.join(experimentfolder, folder), args.imagejfolder, args.macrofolder)
                writeAndPlot(avgdic, os.path.join(args.rootfolder, args.resultsfolder, subfolder + '_' + folder), threshold, False)
                for key in avgdic:
                    if key not in repavgdic:
                        repavgdic[key] = 0
                    repavgdic[key] = repavgdic[key] + avgdic[key]
        
        for key in repavgdic:
            repavgdic[key] = repavgdic[key] / foldcount
        
        #print os.path.join(args.rootfolder, args.resultsfolder, subfolder)
        writeAndPlot(repavgdic, os.path.join(args.rootfolder, args.resultsfolder, subfolder + '_merged'), threshold, True)
        
        
        