import pymongo
import os,log,json

from pymongo.message import query

class MongoDb:

        def __init__(self):
                database_name = os.getenv('mdbname')
                collection_name = os.getenv('mcollection')
                connection = os.getenv('mconnection')
                self.client = pymongo.MongoClient(connection)
                self.db = self.client[database_name]
                self.collection = self.db[collection_name]

        def insert_data(self):
                """
		Description
 		Function To insert document in collections
	        """
                try:
                        customerlist = [{"_id":"1","custid": "100","custname":"vishal","company": "WIP"},
                                        {"_id":"2","custid": "101","custname":"sarvesg","company": "HCP"},
                                        {"_id":"3","custid": "102","custname":"Karan","company": "TCS"},
                                        {"_id":"4","custid": "103","custname":"rahul","company": "GVT"},
                                        {"_id":"5","custid": "104","custname":"kartik","company": "PVG"}]
                        with open('customerdata.json') as file:
                                file_data = json.load(file)                

                        self.collection.insert_many(file_data)
                        print("Values Inserted ")
                        log.logger("successfully inserted values") 
                except Exception as error:
                        print(error,"Already exists")
                        log.logger("values already exists") 

        def read_data(self):
                """
		Description
 		Function To read documents in the collections
	        """
                try:
                        for value in self.collection.find():
                                print(value)
                        log.logger("successfully read values from collection")                         
                except Exception as error:
                        print(error)   

        def update_data(self):
                """
		Description
 		Function To update document in collection
	        """
                try:    
                        select_id = input("select the id to be updated")
                        company_name = input("select the company name ")
                        query = { "_id": select_id }
                        newvalues = { "$set": { "company": company_name } }
                        self.collection.update_one(query,newvalues)
                        
                        for value in self.collection.find():
                            print(value) 
                        log.logger("successfully updated values")       
                except Exception as error:
                        print(error)
                        print("Already updated")

        def delete_data(self):
                """
		Description
 		Function To delete document in container
	        """
                try:    
                        select_id = input("select the id to be deleted")
                        query = { "_id": select_id }
                        self.collection.delete_one(query)

                        for value in self.collection.find():
                                print(value)
                        log.logger("successfully deleted document")        
                except Exception as error:
                        print(error)                                