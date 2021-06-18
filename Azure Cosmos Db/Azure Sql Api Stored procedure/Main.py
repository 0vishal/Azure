'''
 @Author: Vishal Salaskar
 @Date: 2021-06-17
 @Last Modified by: Vishal Salaskar
 @Last Modified time: 2021-06-17 
 @Title : To call the stored procedure
'''
import StoredProcedure as sp 

def Main():
    """
    description
    function : To call the stored procedure
    """
    try:
        sp_obj = sp.StoredProcedure()
        input("registering stored procedure and Calling the procedure to insert Item \n")
        sp_obj.create_container()
        sp_obj.execute_container()
    except (ValueError,KeyboardInterrupt,Exception) as e:
        print(e)   

Main()
