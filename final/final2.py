"""
You are provided a few datafiles and you are expected to do the following in a Object Oriented way
- Create a Pipeline to import the Cutomer Data File 
- Create a Pipeline to import the daily transaction data given a date range as input in the commandline
    - I should be able to run your overall program for 1 day, 2 days or 3 days. 
    - I might have additional datasets to run against as well with missing days inbetween
- Enable the programmer to add new customers to the database
- Enable the programmer to add additional sales to the database
- Once the data is imported use Pandas to do the following:
    - Clean and Scrub the data as required
    - Identify the Top 5 customers based on $ spent
    - Identify the Top 3 products being sold
    - Daily trend of sales per products (data and graph)
    - Daily trend of sales per customer (data and graph)
    - Average sales per day by product (qty) (data and Graph)
    - Average sales per day by $(data and Graph)
    - Average sales per day by customer on $ spent(data and Graph)
- Your program should write the data into a new Sqlite3 database and run from there.
"""
import sys
import datetime
import pandas as pd
import sqlite3 as sql
from sqlite3 import Error
import collections
import matplotlib.pyplot as plt

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
  

#print(filenameList)



# creating connection to sql
class Database:
    @staticmethod
    def GetConnection(dbName):
        try:
            conn = sql.connect(dbName)
            return conn
        except Error as e:
            print(e)
    
    @staticmethod
    def CloseConnection(conn):
        try:
            conn.close()
        except Error as e:
            print(e)
    
    @staticmethod
    def CreateTable(dbConnection, CreateTableSQL):
        try:
            cursor = dbConnection.cursor()
            cursor.execute(CreateTableSQL)
        except Error as e:
            print(e)

class CustomerID:

    def __init__(self, name, sex, age):
        self.__name = name
        self.__sex = sex
        self.__age = age

    #creating property: 
    @property
    def Name(self):
        return self.__name
    
    @Name.setter
    def Name(self,name):
        self.__name = name

    @property
    def Sex(self):
        return self.__sex
    
    @Sex.setter
    def Sex(self,sex):
        self.__sex = sex
        
    @property
    def Age(self):
        return self.__age
    
    @Age.setter
    def Age(self, age):
        self.__age = age

    def __str__(self):
        return "({0},{1},{2})".format( self.__name, self.__sex, self.__age)

class Sales: 

    def __init__ (self, customerid, purchase_date, purchase_item, total_amount):
        self.__customerid = customerid
        self.__purchase_date = purchase_date
        self.__purchase_item = purchase_item
        self.__total_amount = total_amount


    @property
    def Customerid (self):
        return self.__customerid

    @Customerid.setter
    def Customerid (self, customerid):
        self.__customerid = customerid

    @property
    def Purchase_date (self):
        return self.__purchase_date

    @Purchase_date.setter
    def Purchase_date (self, purchase_date):
        self.__purchase_date = purchase_date


    @property
    def Purchase_item (self):
        return self.__purchase_item

    @Purchase_item.setter
    def Purchase_item (self, purchase_item):
        self.__purchase_item = purchase_item

    
    @property
    def Total_amount (self):
        return self.__total_amount

    @Total_amount.setter
    def Total_amount (self, total_amount):
        self.__total_amount = total_amount

    def __str__ (self):
        return "({0},{1},{2},{3})".format(self.__customerid, self.__purchase_date, self.__purchase_item, self.__total_amount)

class SalesDataManger:
    @staticmethod
    def LoadSales(conn, sales):
        sqlBase = "INSERT INTO Sales (CustomerID, 'Purchase Date', 'Purchase Items','Total Amount') values (?,?,?,?)"

        try:
         cursor = conn.cursor()
         cursor.execute(sqlBase, sales)
         conn.commit()
         return cursor.lastrowid
        except Error as e:
            print(e)
    
    @staticmethod 
    def InsertSales(conn, sales):
        sqlBase = "INSERT INTO Sales (CustomerID, 'Purchase Date', 'Purchase Items','Total Amount') values (?,?,?,?)"

        try:
         cursor = conn.cursor()
         cursor.execute(sqlBase, (Sales.Customerid, Sales.Purchase_date, Sales.Purchase_date, Sales.Total_amount))
         conn.commit()
         return cursor.lastrowid
        except Error as e:
            print(e)




class CustomerIDDataManager:
    @staticmethod
    def LoadCustomer(conn,customer):
        sqlBase = "INSERT INTO Customer (ID, name, sex, age) values (?,?,?,?)"

        try:
         cursor = conn.cursor()
         cursor.execute(sqlBase, customer)
         conn.commit()
         return cursor.lastrowid
        except Error as e:
            print(e)

    @staticmethod 
    def InsertCustoemr(conn, custoemr):
        sqlBase = "INSERT INTO Customer (name, sex, age) values (?,?,?)"
        try:
         cursor = conn.cursor()
         cursor.execute(sqlBase, (CustomerID.Name, CustomerID.Sex, CustomerID.Age))
         conn.commit()
         return cursor.lastrowid
        except Error as e:
            print(e)





def Main():
    # Creating Customer database
    database = "Customer.db"
    dbConnection = Database.GetConnection(database)

    # Creating two tables, CustomerID and Sales
    CreateCustomerIDTableSQL =    """
                            CREATE TABLE IF NOT EXISTS Customer (
                                ID integer PRIMARY KEY,
                                name text NOT NULL,
                                sex text,
                                age decimal
                            );
                            """

    CreateSalesTableSQL =   """
                        CREATE TABLE IF NOT EXISTS Sales (
                            ID integer PRIMARY KEY,
                            CustomerID integer NOT NULL,
                            `Purchase Date` text NOT NULL,
                            `Purchase Items` text NOT NULL,
                            `Total Amount` money,
                            FOREIGN KEY (CustomerID) REFERENCES Customer (ID)
                        );
                        """

    if dbConnection is not None:
        Database.CreateTable(dbConnection,CreateCustomerIDTableSQL)
        Database.CreateTable(dbConnection,CreateSalesTableSQL)
    else:
        print("Error! Cannot Create Database Connection")

    # Load CustomerData.csv into database
    customer = pd.read_csv('CustomerData.csv')

    with dbConnection:
        for index, row in customer.iterrows():
            tuples = (row[0], row[1], row[2], row[3])
            CustomerIDDataManager.LoadCustomer(dbConnection, tuples)

    # Load SalesData into database
    # Process the files
    with dbConnection:
        for file in filenameList:
            try:
                dataFile = pd.read_csv(file)
                for index,row in dataFile.iterrows():
                    tuples = (row[0], row[1], row[2],row[3])
                    SalesDataManger.LoadSales(dbConnection, tuples)
            except FileNotFoundError:
                continue

    # Add new customer (need to clean before data analyze)
    customer = CustomerID('MyName','M', '22')
    CustomerIDDataManager.InsertCustoemr(dbConnection,customer)

    # Add new Sales (need to clean before data analyze)
    sale = Sales(11, '2019/03/23', 'Surfurce','2200')
    SalesDataManger.InsertSales(dbConnection,sale)

    # extract data from database
    query = """
        Select c.ID, c.name, s.CustomerID, s.[Purchase Date], s.[Purchase Items],s.[Total Amount]
        from Customer c left join Sales s 
        on c.ID = s.CustomerID
        order by c.ID
            """
    
    data = pd.read_sql_query(query, dbConnection)

    # Identify the Top 5 customers based on $ spent
    data['Total Amount'] = [x.strip('$') for x in data['Total Amount']]
    data['Total Amount'] = data['Total Amount'].astype('int64')
    TopMoneySpend = data.groupby(['name']).sum()
    TopMoneySpend = TopMoneySpend.sort_values(by = ['Total Amount'], ascending = False)
    del TopMoneySpend['ID']
    del TopMoneySpend['CustomerID']
    print("\n", "Top 5 customers based on $ spent: ", "\n",TopMoneySpend.head(5))

    # Identify the Top 3 products being sold
    TopProductSold = data.groupby(['Purchase Items']).count()
    TopProductSold = TopProductSold.drop(['ID', 'name', 'CustomerID', 'Purchase Date'], axis = 1)
    TopProductSold = TopProductSold.rename(index = str, columns = {"Total Amount": "Quantity"})
    TopProductSold = TopProductSold.sort_values(by = ['Quantity'], ascending = False)
    print("\n", "Top 3 products being sold: ", "\n",TopProductSold)

    #Daily trend of sales per products (data and graph)
    ProductTrend = data.groupby(['Purchase Date','Purchase Items']).count()
    ProductTrend = ProductTrend.reset_index(level = 'Purchase Items')
    ProductTrend = ProductTrend.drop(['ID', 'name', 'CustomerID'], axis = 1)
    ProductTrend = ProductTrend.rename(columns = {'Total Amount': 'Quantity'})
    print("\n", "Daily trend of sales per products: ", "\n",ProductTrend)

    # Graph 
    ProductTrend.plot(kind = 'bar')
    plt.xlabel('Date')
    plt.ylabel('Quantity')
    plt.title("Sales per day by product quantity")


    # Daily trend of sales per customer (data and graph)
    CustomerTrend = data.groupby(['Purchase Date','name']).sum()
    CustomerTrend = CustomerTrend.reset_index(level = 'name')
    CustomerTrend = CustomerTrend.drop(['ID','CustomerID'], axis = 1)
    print("\n", "Daily trend of sales per products: ", "\n",CustomerTrend)

    # Graph 
    CustomerTrend = CustomerTrend.drop(['name'], axis = 1)
    CustomerTrend.plot(kind = 'bar')
    plt.xlabel('Date')
    plt.ylabel('Customers')
    plt.title("Daily trend of sales per customer")



    # Average sales per day by product (qty) (data and Graph)
    AvgSales= data.groupby(['Purchase Date','Purchase Items']).count()
    del AvgSales['name']
    AvgSales = AvgSales.rename(index = str, columns = {"Total Amount": "Quantity"})
    AvgSales = AvgSales.groupby('Purchase Items').mean()
    AvgSales = AvgSales.sort_values(['Quantity'], ascending = False)
    print("\n", "Average sales per day by product (qty): ", "\n", AvgSales)

    AvgSales.plot(kind = 'bar', legend = False)
    plt.xlabel('Item')
    plt.ylabel('Average Quantity')
    plt.title("Average sales per day by product quantity")
 

    # Average sales per day by $(data and Graph)
    AvgDays = data.groupby(['Purchase Date']).sum()
    AvgDays = AvgDays.drop(['CustomerID'], axis = 1)
    AvgDays['Avg_Money'] = AvgDays['Total Amount']/AvgDays['ID']
    AvgDays = AvgDays.drop(['ID', 'Total Amount'], axis = 1)
    AvgDays = AvgDays.sort_values(['Avg_Money'], ascending = False)
    print("\n", "Average sales per day by $: ", "\n", AvgDays)

    # Graph
    AvgDays.plot(kind = 'bar', legend = False)
    plt.xlabel('Item')
    plt.ylabel('Average Quantity')
    plt.title("Average sales per day by $")


    # Average sales per day by customer on $ spent(data and Graph)
    AvgMoneySpend = data.groupby(['Purchase Date', 'name']).sum()
    AvgMoneySpend = AvgMoneySpend.reset_index(level = 'name')
    AvgMoneySpend = AvgMoneySpend.drop(['ID', 'CustomerID'], axis = 1)
    AvgMoneySpend = AvgMoneySpend.groupby('name').mean()
    print("\n", "Average sales per day by customer on $ spent: ", "\n", AvgMoneySpend)

    # Graph
    AvgMoneySpend.plot(kind = 'bar')
    plt.xlabel('Names')
    plt.ylabel('Average Money Spend')
    plt.title("Average sales per day by customer on $ spent")
    plt.show()

    Database.CloseConnection(dbConnection)
if __name__ == "__main__":
    Main()
