'''
 @Author: Vishal Salaskar
 @Date: 2021-06-17
 @Last Modified by: Vishal Salaskar
 @Last Modified time: 2021-06-17 
 @Title : To register and call stored procedure 
'''

import uuid,os
import azure.cosmos.cosmos_client as cosmos_client


url = os.getenv('URL')
key = os.getenv('KEY')
database_name = os.getenv('DBNAME')
container_name = os.getenv('CNAME')

with open('spAddItem.js') as file:
    file_contents = file.read()

"""
To register a stored procedure 
"""
sproc = {
    'id': 'spAddItem',
    'serverScript': file_contents,
}
client = cosmos_client.CosmosClient(url, key)
database = client.get_database_client(database_name)
container = database.get_container_client(container_name)
created_sproc = container.scripts.create_stored_procedure(body=sproc)


"""
To call a stored procedure 

"""
new_id= str(uuid.uuid4())

# Creating a document for a container with "id" as a partition key.

new_item =   {
      "id": new_id, 
      "category":"Personal",
      "name":"Groceries",
      "description":"Pick up strawberries",
      "isComplete":False
   }
    

result = container.scripts.execute_stored_procedure(sproc=created_sproc,params=[[new_item]], partition_key=new_id) 
