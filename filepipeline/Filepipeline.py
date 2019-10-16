import sys
import datetime

"""
    We get daily files in the format mm-dd-yyyy-Data.txt
    We want to read these files and add the values in them
    We want to be able to run this as a batch

    we need to get as input : Start Date and End Date
    We want to enumerate all available files for those dates
        read the content
        convert content to Integer
        Add the content
    Display the total
"""

if len(sys.argv) != 3:
    print("please provide start date and end date in the format mm-dd-yyyy")
    quit()

startDateString = sys.argv[1]
endDateString = sys.argv[2]

try:
    myStartDate = datetime.datetime.strptime(startDateString,"%m-%d-%Y")
except ValueError as e:
    print(e)
    print("Please Enter proper StartDate in mm-dd-yyyy format")
    quit()

try:
    myEndDate = datetime.datetime.strptime(endDateString,"%m-%d-%Y")
except ValueError as e:
    print(e)
    print("Please Enter proper EndDate in mm-dd-yyyy format")
    quit()

print(myStartDate)
print(myEndDate)

fileNameBase = "-Data.txt"

filenameList = []
for index in range(myStartDate.day, myEndDate.day+1):
    name = "./files/" + myStartDate.strftime("%m") + "-" + str(index) + "-" + str(myStartDate.year) + fileNameBase
    filenameList.append(name)

print(filenameList)

sum = 0
#Process the files
for file in filenameList:
    dataFile = open(file,"r")
    value = int(dataFile.readline())
    print(value)
    sum += value
    dataFile.close()

print(sum)

