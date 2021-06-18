'''
 @Author: Vishal Salaskar
 @Date: 2021-06-17
 @Last Modified by: Vishal Salaskar
 @Last Modified time: 2021-06-17 
 @Title : To register and call stored procedure 
'''

import uuid,os
import azure.cosmos.cosmos_client as cosmos_client

class StoredProcedure:

    def __init__(self):
            url = os.getenv('URL')
            key = os.getenv('KEY')
            self.database_name = os.getenv('DBNAME')
            self.container_name = os.getenv('CNAME')
            self.client = cosmos_client.CosmosClient(url, key)
            self.database = self.client.get_database_client(self.database_name)
            self.container = self.database.get_container_client(self.container_name) 

    def create_container(self):
        """
        description
        function : To register the stored procedure
        """
        try:        
            with open('spAddItem.js') as file:
                file_contents = file.read()

            sprocedure = {
                'id': 'spAddItem',
                'serverScript': file_contents,
            }     
            self.create_sproc = self.container.scripts.create_stored_procedure(body=sprocedure)
            print(self.create_sproc)
            self.get_sproc = self.container.scripts.get_stored_procedure(self.create_sproc)
            print(self.get_sproc)
        except Exception:    
            print("Already exists")


    def execute_container(self):  
        """
        description
        function : To execute the container
        """        
        try:      
            new_id= str(uuid.uuid4())
            #Creating a document for a container with "id" as a partition key.
            _id = input("Enter the id   ")
            name = input("Enter the name    ")
            lastname = input("Enter the lastname    ")
            income = input("Enter the income    ")
            new_item =   {
            "id": new_id, 
            "_id":_id,
            "name":name,
            "lastname":lastname,
            "income": income,
            "isComplete":False
            }
            result = self.container.scripts.execute_stored_procedure(sproc='spAddItem',params=[[new_item]], partition_key=lastname) 
        except Exception as error:
            print(error)    
