#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  9 06:51:54 2022

@author: chrisyoung
"""

# Package contains function to read in CMT file and parse out MT info, 
# which is returned in "data", a list of dictionaries.

def read_cmt(filename):
    line_counter = 1
    f = open(filename, 'r')
    data = []
    for count, line in enumerate(f):
        line = line.strip()
        columns = line.split()
        # print(columns)        # for finding bad lines in CMT file!
        if line_counter == 1:
            source = {}                 #initialize dictionary
            source['cat'] = columns[0]
            source['date'] = columns[1]
            source['time'] = columns[2]
            source['lat'] = float(columns[3])
            source['lon'] = float(columns[4])
            source['depth'] = float(columns[5])
            source['mb'] = float(columns[6])
            source['ms'] = float(columns[7])
            line_counter+=1
        elif line_counter == 2:
            line_counter+=1
        elif line_counter == 3:
            line_counter+=1
        elif line_counter == 4:
            source['mom_exp'] = float(columns[0])
            source['mrr'] = float(columns[1])
            source['mrr_unc'] = float(columns[2])
            source['mtt'] = float(columns[3])
            source['mtt_unc'] = float(columns[4])
            source['mpp'] = float(columns[5])
            source['mpp_unc'] = float(columns[6])
            source['mrt'] = float(columns[7])
            source['mrt_unc'] = float(columns[8])
            source['mrp'] = float(columns[9])
            source['mrp_unc'] = float(columns[10])
            source['mtp'] = float(columns[11])
            source['mtp_unc'] = float(columns[12])
            line_counter+=1
        elif line_counter == 5:
            data.append(source)
            line_counter = 1      # reset line_counter for next group of 5
    f.close()
    return data