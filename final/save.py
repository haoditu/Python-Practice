"""
Once the data is imported use Pandas to do the following:
    - Clean and Scrub the data as required
    - Identify the Top 5 customers based on $ spent
    - Identify the Top 3 products being sold
    - Daily trend of sales per products (data and graph)
    - Daily trend of sales per customer (data and graph)
    - Average sales per day by product (qty) (data and Graph)
    - Average sales per day by $(data and Graph)
    - Average sales per day by customer on $ spent(data and Graph)

"""
import sys
import datetime
import pandas as pd
import sqlite3 as sql
from sqlite3 import Error

if len(sys.argv) != 3:
    print("please provide start date and end date in the format mm-dd-yyyy")
    quit()

startDateString = sys.argv[1]
# print(startDateString)
endDateString = sys.argv[2]
# print(endDateString)

try:
    myStartDate = datetime.datetime.strptime(startDateString,"%Y-%m-%d")
except ValueError as e:
    print(e)
    print("Please Enter proper StartDate in yyyy-mm-dd format")
    quit()

try:
    myEndDate = datetime.datetime.strptime(endDateString,"%Y-%m-%d")
except ValueError as e:
    print(e)
    print("Please Enter proper EndDate in yyyy-mm-dd format")
    quit()

# print(myStartDate)
# print(myEndDate)

fileNameBase = "-SalesData.csv"

filenameList = []
for index in range(myStartDate.day, myEndDate.day+1):
    name =  str(myStartDate.year) + "-" + myStartDate.strftime("%m") + "-" + str(0) + str(index) + fileNameBase
    filenameList.append(name)
  

print(filenameList)

# Process the files
for file in filenameList:
    try:
        dataFile = pd.read_csv(file)
        for index,row in dataFile.iterrows():
            tuples = (row[0], row[1], row[2],row[3])
            print(tuples)
    except FileNotFoundError:
        continue
    


customer = pd.read_csv('CustomerData.csv')

