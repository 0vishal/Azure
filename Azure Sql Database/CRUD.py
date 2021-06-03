'''
@Author: Vishal Salaskar
@Date: 2021-06-1
@Last Modified by: Vishal Salaskar
@Last Modified time: 2021-06-1
@Title : Program to connect to Azure Sql Database
'''
import pyodbc 
import os, log

class CRUD: 

    def __init__(self):
        server = os.getenv('SERVER')
        database = os.getenv('DATABASE')
        username = os.getenv('UID')
        password = os.getenv('PASSWORD')   
        driver= '{ODBC Driver 17 for SQL Server}'
        self.conn = pyodbc.connect('DRIVER='+str(driver)+';SERVER='+str(server)+';PORT=1433;DATABASE='+str(database)+';UID='+str(username)+';PWD='+str(password))

    def create(self):
        """
		Description
 		Function To create a table in sql database 
		"""
        try: 
            cursor = self.conn.cursor()
            cursor.execute("create table newcustomers (name varchar(55), organization varchar(55), mobile int)")
            self.conn.commit()
            #closing the  connection
            self.conn.close()
            log.logger("table successfully created")
        except Exception as e:
            print(e)    

    
    def read(self):
        """
		Description
 		Function To read the values from table newcustomers
		"""
        try:
            cursor = self.conn.cursor()
            cursor.execute("select * from newcustomers")

            myresult = cursor.fetchall()
            print(myresult)
            log.logger("data successfully read from table")
        except Exception as e:
            print(e)

    def insert(self):
        """
		Description
 		Function To insert the values in the table 
		"""
        try:
            print("Enter name")
            name=input()
            print("Enter organization")
            org=input()
            print("Enter mobile")
            number=input()
            cursor = self.conn.cursor()
            cursor.execute("insert into newcustomers (name, organization, mobile) values (?, ?, ?)",[name,org,number])
            self.conn.commit()
            print(cursor.rowcount , "record inserted.")
            log.logger("row successfully inserted in table")
        except Exception as e:
            print(e)

    def update(self):
        """
        Description
        Function To update value in database table
        """
        try:
            print("Enter the  value to edit 2.organization 3.mobile ")
            option =int(input())
            if option==1:
                    print("Edit organization:")
                    org= input()
                    print("Enter name of the person")
                    uname = input()
                    cursor = self.conn.cursor()
                    cursor.execute("update newcustomers set organization= ?  where name= ?",[org, uname])
                    self.conn.commit()
                    log.logger("table successfully updated")
            else:
                    print("Edit mobile")
                    number = input()
                    print("Enter name of the person")
                    uname = input()
                    cursor = self.conn.cursor()
                    cursor.execute("update newcustomrs set organization= ? where name= ?",[number,uname])
                    self.conn.commit()
                    log.logger("table successfully updated")
        except Exception as e:
	        print(e)

    def delete(self):
        """
	    Description
 	    Function To delete value in database table 
	    """
        try:
            print("Enter name to delete")
            name=input()
            cursor = self.conn.cursor()
            cursor.execute("delete from newcustomers where name= ?",[name])
            self.conn.commit()
            log.logger("row successfully deleted")

        except Exception as e:
            print(e)    

        

            



