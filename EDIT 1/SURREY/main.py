# import json 
# from datetime import date, datetime
import os
# import glob
# from PyPDF2 import PdfFileWriter, PdfFileReader
# try:
#     import re2 as re
# except ImportError:
#     import re
# from prettytable import PrettyTable

# from jsonMod import load_json, add_to_json, update_values  (deprecated)
from pathMod import paths, create_directory, enter_directory, verify_directory, move_files
from algorithm import read_file
# from algoHelpers import reprint_dates, if_order_as_originalPrint, if_order_exists_return_renamed, append_data, ship_via
# from patternMod import find_pattern
from prettyinfo import table, prettyInfo, print_to_console
from allFiles import list_of_files

# imports for updating json file
from updatesJson import get_dir, months, update_date, updates_to_json



def main(c, c_via, c_mar, pickticket_dir, code_dir, picktickets_database):

    try:
        temp_path = paths(fr"{pickticket_dir}")
        code_path = fr"{code_dir}"

        
        if os.getcwd() != temp_path["root_path"]:
            enter_directory(temp_path["root_path"])
        
        
            
        if not (verify_directory(temp_path["monthly_tickets"])):
            create_directory(temp_path["monthly_tickets"])
            
            for d in temp_path["in_month_dir"]:
                if not (verify_directory(d)):
                    create_directory(d)
            
            for d in temp_path['staged_dir']:
                if not verify_directory(d):
                    create_directory(d)

    # For email attachments 

        email_attachments = picktickets_database + c_mar["email_archive"]
        
        if os.getcwd() != email_attachments:
            enter_directory(email_attachments)


        if not (verify_directory((email_attachments + temp_path["email_archive"]))):
            create_directory(email_attachments + temp_path["email_archive"])

                    
        
        extraction_info = table()
        
        
        all_files = list_of_files(email_attachments)
        
        
        for file in all_files:
            
            if os.getcwd() != temp_path["in_month_dir"][0]: # enter into 1-Printed folder 
                enter_directory(temp_path["in_month_dir"][0])
                
            
            move_to = email_attachments + temp_path["email_archive"] + rf"\{os.path.basename(file)}"
            
            ############################################### Algorithm ###############################################
            read_file(c, c_via, file, extraction_info, move_to)
            
            #########################################################################################################
            
            if os.getcwd() != temp_path["root_path"]:
                enter_directory(temp_path["root_path"])
            
            move_files(file, move_to)
            
        
        print_to_console(extraction_info)


        if os.getcwd() != code_path:
            enter_directory(code_path)






        ##################### updating json for exporting valid database to web portal ##########################

        updates_to_json(c, temp_path["root_path"])

    except Exception as e:
        print(e)

    


