import pymongo
import os

class MongoDb:

        def __init__(self):
                database_name = os.getenv('mdbname')
                collection_name = os.getenv('mcollection')
                connection = os.getenv('mconnection')
                self.client = pymongo.MongoClient(connection)
                self.db = self.client[database_name]
                self.collection = self.db[collection_name]

        def insert_data(self):
                try:
                        customerlist = [{"_id":"1","custid": "100","custname":"vishal","company": "WIP"}
                        {"_id":"2","custid": "101","custname":"sarvesg","company": "HCP"}
                        {"_id":"3","custid": "102","custname":"Karan","company": "TCS"}
                        {"_id":"4","custid": "103","custname":"rahul","company": "GVT"}
                        {"_id":"5","custid": "104","custname":"kartik","company": "PVG"}]


                        self.collection.insert_many(customerlist)
                except Exception as error:
                        print(error, "Already exists")

        def read_data(self):
                try:
                        for value in self.collection.find():
                                print(value)                
                except Exception as error:
                        print(error)

        def update_data()                
