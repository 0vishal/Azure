"""
@Author: Vishal Salaskar
@Date: 2021-06-15
@Last Modified by: Vishal Salaskar
@Last Modified time: 2021-06-15
@Title : perform basic operation on azure cosmosdb using mongo db 
"""

from MongoOperations import MongoDb


def main():
    """
		Description
 		Function To give option for operation on items in container
	"""
    try:
        mongodb_obj=MongoDb()
        option=int(input("select option of operation\n 1.insert data\n 2.read data\n 3.delete data \n"))
        if(option==1):
            mongodb_obj.insert_data()
        elif(option==2):
            mongodb_obj.read_items()
        elif(option==3):
            mongodb_obj.delete_items()
    except (Exception,ValueError) as error:
        print(error)

main()