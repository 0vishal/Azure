from CosmosOperations import CosmosDb


def main():
    """
		Description
 		Function To give option for operation on items in container
	"""
    try:
        cosmosdb_obj=CosmosDb()
        option=int(input("select option of operation\n0 : 1.insert data\n\n 2.read data\n 3.delete data \n"))
        if(option==1):
            cosmosdb_obj.insert_data()
        elif(option==2):
            cosmosdb_obj.read_items()
        elif(option==3):
            cosmosdb_obj.delete_items()
    except Exception as error:
        print(error)

main()