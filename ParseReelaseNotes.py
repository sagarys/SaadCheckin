#!/usr/bin/env python
import os
import requests
import sys
import pprint
import subprocess
import json

if len(sys.argv) == 2 :
    RELEASENOTESLCATION =sys.argv[1]
else :
    print("Please pass the releassenote complete location ")
    sys.exit(2)
    
FITID = "Siebel ID :"
PREREQUISISTES = "Pre-requisites"
OBSOLETED = "Obsoleted Patches"
BINARIESAFFECTED = "List all binaries of the fiery controller that are updated or added"
EOS = "======================"
PRODUCTNAME = "Product   :"
AFFECTEDMODULES = "List Affected Modules"
LISTOFLABELS = "(List all the labels specifically for the defect(s) mentioned above with"
fp = open(RELEASENOTESLCATION, "r")
line = fp.readline()
binaries = ''
configspecDetails = ""
ppds = False
while line:
    if PRODUCTNAME in line :
        subprocess.call("python PcickConfigspec.py https://saad.efi.com " + line.split(':')[-1].replace('\n','') )
    if AFFECTEDMODULES in line :
        if 'ppd' in str(line.split(':')[-1]).lower():
            ppds = True
            binaries = ',PPD'
    if FITID in line :
        configspecDetails = "##"
        configspecDetails = configspecDetails + line.split(':')[-1] + '\n'        
        configspecDetails = configspecDetails + '## Covers: None' + '\n'        
    if PREREQUISISTES in line :
        configspecDetails = configspecDetails + '## Prereqs: '
        configspecDetails = configspecDetails + line.split(':')[-1] + '\n'        
    if OBSOLETED in line :
        configspecDetails = configspecDetails + '## Obsoletes:  '        
        configspecDetails = configspecDetails + line.split(':')[-1] + '\n'        
    if BINARIESAFFECTED in line :
        line = fp.readline()
        while line:
            if EOS in line :
                break
            if ppds == True :
                if 'ppd' in str(line.split('/')[-1]).lower() or 'fcap_prod.jmf' in str(line.split('/')[-1]).lower(): 
                    line = fp.readline()
                    continue;
            binaries = binaries +','+line.split('/')[-1].rstrip()
            line = fp.readline()
        configspecDetails = configspecDetails + '## Modifies: '
        configspecDetails = configspecDetails + binaries[1:-1] + '\n'        
    if LISTOFLABELS in line :
        line = fp.readline()
        line = fp.readline()
        while line:
            if EOS in line :
                break
            if line != '' and line != '\n' :
                configspecDetails = configspecDetails + "element * " + line.strip() + '\n'
            line = fp.readline()    
    line = fp.readline()    
fp.close()
# print(configspecDetails.replace('\n\n','\n'))
configspec_path = "configspec.txt"

f = open(configspec_path, 'r')
lines = f.readlines()
lines.insert(0,configspecDetails.replace('\n\n','\n')+'\n')
f.close()

f = open(configspec_path, 'w')
f.writelines(lines)
f.close()
