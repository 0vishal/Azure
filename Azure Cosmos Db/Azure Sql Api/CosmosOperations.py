"""
@Author: Vishal Salaskar
@Date: 2021-06-15
@Last Modified by: Vishal Salaskar
@Last Modified time: 2021-06-15
@Title : perform basic operation on azure cosmodb
"""

from azure.cosmos import CosmosClient
import azure.cosmos.exceptions as exceptions
from azure.cosmos.partition_key import PartitionKey
import datetime
import config 
import os, log

class CosmosDb:

    
    def __init__(self):
        endpoint=os.getenv('endpoint')
        key=os.getenv('key')
        self.client = CosmosClient(endpoint, key)
        self.database_name = os.getenv('dbname')
        self.container_name = os.getenv('containername')
        self.database = self.client.get_database_client(self.database_name)
        self.container = self.database.get_container_client(self.container_name)

    def insert_data(self):
        """
		Description
 		Function To insert items in a container
		"""    
        try:
            data = [("vishal","salaskar"),("sarvesh","salaskar")]

            for i,value in enumerate(data):
                self.container.upsert_item(
                    {
                        'id': 'item{0}'.format(i),
                        'firstname': value[0],
                        'lastname': value[1]
                    }
                )
            log.logger("successfully inserted values")    
        except Exception as error:
            print(error,"\n Already exists")

    def read_items(self):
        """
		Description
 		Function To read items from the container
		"""
        try:
            print('\n1.3 - Reading all items in a container\n')
            item_list = list(self.container.read_all_items(max_item_count=10))

            print('Found {0} items'.format(item_list.__len__()))

            for value in item_list:
                print('Item Id: {0} {1} {2}'.format(value.get('id'),value.get('firstname'),value.get('lastname'))) 
            log.logger("read the items successfull")      
        except Exception as error:
            print(error)

    def delete_items(self):
        """
		Description
 		Function To delete item from the items in container
		"""
        try:
            print('Deleting Item by Id\n')
            id = input("Enter the id to be deleted")
            response = self.container.delete_item(item=id)
            print('Deleted item\'s Id is {0}'.format(id)) 
            log.logger("item successfully deleted")                    
        except Exception as error:
            print(error)
