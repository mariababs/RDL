
# Description: 
# Get all of our data in a .tdms file but we can't really use it 
# since we have to do a bunch of stuff to it and it's like millions of cells
# of data that we don't need, so we need a program that'll take the .tdms
# and reduce the data and put it into a form thats easy to analyze.

from nptdms import TdmsFile as td
import os
import pandas as pd
import numpy as np 
import subprocess as sub
import time

def reduceData():
    
    path = input("Input path (x:\XXXX\XXX\XXX\): ")
    filename = input("Input file name (XXXXXX.tdms): ")
    tdmsDir = r'{}'.format(path + '\\' + filename)
    csvDir = r'{}'.format(path + filename[:-5] + '.csv')

    # create .csv of full data
    with td.open(tdmsDir) as tdms_file:
        td(tdmsDir).as_dataframe().to_csv(csvDir)
    print("Full .csv file created")

    # fix the column titles
    data = pd.read_csv(filename[:-5] + '.csv')
    headersOG = data.columns 
    headers_new = [None] * len(data.columns)
    i=0
    while i<len(headersOG):
        string = headersOG[i]
        headers_new[i] = string[17:-1]
        i+=1
    data.columns = headers_new

    # reduce the data
    indexColumns = headers_new[-13:]
    indexes = data.loc[:,indexColumns].to_numpy()
    rows = 0
    cols = 0
    x = 0
    while rows<len(indexes):
        cols = 0
        while cols<len(indexes[0]):
            if indexes[rows][cols] == 1.0:
                importantData_end = rows
                x += 1
                if x == 1:
                    importantData_start = rows

            cols+=1
        rows+=1

    start = str(importantData_start-100)
    end = str(importantData_end+100)
    data.loc[start:end].to_excel(filename[:-5] + '_output.xlsx', index=False)
    print("Reduced data saved in a .xlsx")

    return csvDir

def deleteBigFile(csvDir):
    if os.path.exists(csvDir):
        os.remove(csvDir)
    else:
        print("ERROR")
    
    print("Full size .csv deleted")

def main():
    sub.Popen('python -m pip install -r requirements.txt')
    time.sleep(5)
    filename = reduceData()
    # dataanalysis?
    deleteBigFile(filename)
    print("Done.")

if __name__ == "__main__":
    main()