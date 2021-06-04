'''
@Author: Vishal Salaskar
@Date: 2021-06-4
@Last Modified by: Vishal Salaskar
@Last Modified time: 2021-06-4
@Title : Program to call the data factory operations functions
'''
import DFOperations as op


def Main():
    """
		Description
 		Function To call the data factory functions
	"""
    try:
        print("creating the data factory and linked service for operation")
        create = op.DFOperations()
        create.create_factory()
        create.create_linkedservice()
    except Exception as error:
        print("Already exist",error)

    print("Enter 1 for the operation ")
    option = input()
    try:
        if option==1:
            copy_data = op.DFOperations()
            copy_data.create_dataset()
            copy_data.run_pipeline()
        else:
            print("Invalid")   
    except Exception as e:
        print(e)         

