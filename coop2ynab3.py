#!/usr/bin/env python3

from sys import exit
import csv
from tkinter import *
from tkinter.filedialog import askopenfilename
import tkinter.messagebox
import re
import datetime



Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
# show an "Open" dialog box and return the path to the selected file
filename = askopenfilename(filetypes=[("CSV files","*.csv")],initialdir = 'C:/Users/Paul/Downloads/') 


firstdatestr = '02/09/2016'
oldlinecount = 0
visaformat = False



firstdatestr=input('From date in dd/mm/yyyy: ')
firstdateobj = datetime.datetime.strptime(firstdatestr, '%d/%m/%Y')

import csv



try:
    infile = open(filename, "r")
    infile.close
except:
    print("Can't open file at",filename)

outfilepath = 'C:/Users/Paul/Documents/finance/ynab.csv'
try:
    outfile = open(outfilepath, "wb")
    outfile.close
except:
    print("Can't open file at",outfilepath)

# b for binary mode prevents an extra return in the row terminator
with open (outfilepath,'wb') as outfile:
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
                if re.search('/[0-9][0-9]\/[0-9][0-9]\/20[0-9][0-9]/', date):
                    print("The date format is not supported at line %s , should be DD/MM/YYYY", linecount)  ;  
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
                    transactiontype = description;
                    description = "Transfer:Cash";
                if visaformat:
                    if expense != '':
                        expense = float(expense)*(-1)
                
                outline = [dateobj.strftime('%d/%m/%Y'),description,'',transactiontype,expense,income]
                print(linecount,outline)
                outwriter.writerow(outline)
                
       
    
print('found this many old lines',oldlinecount)
print('output sent to',outfilepath)



