from main import main 
import os
from pathMod import enter_directory
import time 

def server(c, c_via, c_vars):

    ## ALL REQUIRED PATHS
    code_path = os.getcwd()

    picktickets_database = c_vars.find_one({"_id": "database"})['database']
    c_vars.update_one({"_id":"markham"},{"$set":{"code_path": code_path}})

    c_mar = c_vars.find_one({"_id": "markham"}) # c_vars now becomes specific to markham --> c_mar
    temp_path = c_mar["temp_path"]


    
    try:
        s = time.perf_counter()
        main(c, c_via, c_mar, temp_path, code_path, picktickets_database)
        f = time.perf_counter()
        
        print(f'Finished extraction in {round(f-s, 2)} s')

    
    except Exception as e:
        print(f"def server, Unknown Error occured, ERROR: {repr(e)}")


