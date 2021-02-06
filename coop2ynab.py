#!/usr/bin/env python3

#Input is a csv file in format supplied by co-operative bank 
#Output is a csv file in format required by YNAB 4

# Input file is selected by the user at runtime via a GUI
# Output file location may be passed as an argument

from sys import exit
from sys import argv
import csv
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import tkinter.messagebox
import re
import datetime
import os.path
import csv

#Initialise variables
firstdatestr = '02/09/2016'
oldlinecount = 0
visaformat = False

#Set output file name
if len(argv) == 2:
    outfilepath = argv[1]
else: outfilepath = 'ynab.csv'

#Get input file name
tkinter.Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
# show an "Open" dialog box and return the path to the selected file
filename = askopenfilename(filetypes=[("CSV files","*.csv")],initialdir = 'C:/Users/Paul/Downloads/') 


# Get from user the date of the first record to be processed
firstdatestr=input('From date in dd/mm/yyyy: ')
firstdateobj = datetime.datetime.strptime(firstdatestr, '%d/%m/%Y')


#open the input
try:
    infile = open(filename, "r")
    infile.close
except:
    print("Can't open file at",filename)


#open the output
try:
    outfile = open(outfilepath, "wb")
    outfile.close
except:
    print("Can't open file at",outfilepath)

# In python2 a b for binary mode prevents an extra return in the row terminator
# removed in python 3
with open (outfilepath,'w', newline='') as outfile:
    outwriter = csv.writer(outfile,)
    with open(filename) as csvfile:
        statement = csv.reader(csvfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL,lineterminator='')
        linecount = 0
        for entry in statement:
            linecount = linecount + 1
            try:
                date = entry[0]
                description = entry[1]
                transactiontype = entry[2]
                income = entry[3]
                expense = entry[4]
                balance = entry[5]
            except:
                try:
                    # Visa format
                    date = entry[0]
                    description = entry[1]
                    transactiontype = ""
                    income = entry[2]
                    expense = entry[3]
                    balance = ""
                    visaformat = True
                except:   
                    print("file format looks wrong")
                    exit(0)
            if linecount == 1:
                #check the file format
                if ((date == "Date") and (description == "Description")):#	Category	Memo	Money In	 Money Out	 Balance
                    #write the header
                    header = ['Date','Payee','Category','Memo','Outflow','Inflow']
                    outwriter.writerow(header)
                else:
                    print("file header looks wrong")
                    exit(0)
            else:
                #this is a data line, check date format
                if re.search(r'/[0-9][0-9]\/[0-9][0-9]\/20[0-9][0-9]/', date):
                    print("The date format is not supported at line %s , should be DD/MM/YYYY", linecount) 
                #this is a valid transaction line
                # is line too old?
                try:
                    dateobj = datetime.datetime.strptime(date, '%Y-%m-%d')
                except:
                    #maybe the file was saved as csv from Excel
                    try:
                        dateobj = datetime.datetime.strptime(date, '%d/%m/%Y')
                    except:
                        print('Could not convert date', linecount, date)
                        continue
                if dateobj < firstdateobj:
                    #skip line
                    if oldlinecount == 0:
                        print('Line is too old', linecount,date)
                    oldlinecount = oldlinecount + 1
                    continue
                if transactiontype=="CHEQUE":
                    description = "Cheque Number " + description
                if transactiontype=="ATM":
                    transactiontype = description
                    description = "Transfer:Cash"
                if visaformat:
                    if expense != '':
                        expense = float(expense)*(-1)
                
                outline = [dateobj.strftime('%d/%m/%Y'),description,'',transactiontype,expense,income]
                print(linecount,outline)
                outwriter.writerow(outline)
                
       
    
print('found this many old lines',oldlinecount)
print('output sent to',outfilepath)
