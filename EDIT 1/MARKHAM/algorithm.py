from PyPDF2 import PdfFileWriter, PdfFileReader
from patternMod import find_pattern
from algoHelpers import is_order_original, order_reprint_name, append_data, ship_via
from datetime import datetime
# from jsonMod import load_json, add_to_json, update_values  (deprecated)
from prettyinfo import table, prettyInfo, print_to_console
import os

def read_file(c, c_via, file, extraction_info, move_to):
    '''
    file = emailed file (mail%^**&^%.pdf)
    json_data = loaded json data (load everytime before calling this function)
    jsonfile = main json file ("master_pick_tickets.json")
    extraction_info = used for console output
    move_to = Email attachment path
    
    orders_dict = tracks the indices of page(s) this function has to extract from file
    json_dict_to_add = for each file json data for all picktickets is loaded only once and then appended to jsonfile
    
    data extracted form each page:
    {
        originalPrint, 
        reprintDate, 
        dateReceived, 
        emailAttachment, 
        shipTo, 
        via, 
        fileDirectory, 
        status = "Printed", 
        shippedDate = None,
        billedDate = None,
        isExcelUpdated = False
        isShippedExcelUpdated = False, (removed)
        isBilledExcelUpdated = False, (removed)
    }
    
    if order_no already exists in previous email attachment, then "_reprint" is appended to order_no (eg. "7182345-00_reprint")
    '''

    ########### VARIABLES 
    orders_dict = {}
    json_dict_to_add = {}


    with open(file, 'rb') as readfile:
        input_file = PdfFileReader(readfile)
        pages = input_file.numPages

        
        for page in range(pages):
            file_writer = PdfFileWriter()
            get_page = input_file.getPage(page)
            

            master_text = get_page.extractText()
            narrowed_text = find_pattern(r'Order(.*)FOB', master_text, 0)


            ####################### ORDER NUMBER EXTRACTION ##########################
            ### FROM NARROWED_TEXT
            
            order_no = find_pattern(r'(\d{4,7})[-](\d{2})', narrowed_text, 0)


            ##################### SYSTEM GIVEN VALUES ###############################

            originalPrint = True
            dateReceived = datetime.now()
            emailAttachment = move_to
            month = datetime.now().strftime('%B-%Y')

            ################## HANDLES REPRINTS

            if is_order_original (c, order_no):
                order_no = order_reprint_name(c, order_no)
                originalPrint = False
            

            ##################### SHIP-TO EXTRACTION ######################################
            #### FORM MASTER_TEXT
            
            shipTo = find_pattern(r"ShipTo(.*)Order", master_text, 0)[8:].split(" ")[:3]
            shipTo = " ".join(shipTo)


            ###################### SHIP VIA EXTRACTION ###############################
            ##### FROM ALL_SHIP_VIA.json
            
            via = ship_via(c_via, narrowed_text)


            ################### addition of orderNo_via as default filename ############
            
            easyName = f"{order_no}_{via}"

            fileDirectory = os.getcwd() + rf"\{easyName}.pdf"

            ##################### PO NUMBER EXTRACTION #############################
            ##### FORM NARROWED_TEXT

            try:
                temp_po = find_pattern(r'(\d{4,7})[-](\d{2})(.*)(\d{2})[-][\s\S]*[-](\d{4})', narrowed_text, 3)
                PO = find_pattern(r'(\d{2})[-][\s\S]{3}[-](\d{4})(.*)', temp_po, 3)
            except Exception as e:
                PO = "NOT FOUND"
                print(repr(e))
            
            


            ######################## HANDLES MULTI-PAGE ORDERS
            try:
                orders_dict[order_no].append(page)
            except:
                orders_dict[order_no] = []
                orders_dict[order_no].append(page)

            
            ##################### OUTPUT THE EXTRACTED PDF FILE
            
            for each_page in orders_dict[order_no]:
                file_writer.addPage(input_file.getPage(each_page))
            
            file_writer.addBlankPage() ### Add a blank page
                
            with open(f"{easyName}.pdf", "wb") as f:
                file_writer.write(f)
                f.close()
                
            ######## Adding data
            try:
                json_dict_to_add[order_no] = append_data(originalPrint,
                                                         dateReceived, 
                                                         emailAttachment, 
                                                         shipTo, 
                                                         via,
                                                        fileDirectory, 
                                                        month,
                                                        PO,
                                                        easyName)
            except Exception as e:
                print(f"def read_file, Order:{order_no}, ERROR:{repr(e)}")
                
        for k, v in json_dict_to_add.items():

            add = {
                "_id" : k,
                "dateReceived" : v["dateReceived"],
                "originalPrint" : v["originalPrint"],
                "emailAttachment" : v["emailAttachment"],
                "shipTo" : v["shipTo"],
                "via": v["via"],
                "PO": v["PO"],
                "fileDirectory" : v["fileDirectory"],
                "status" : v["status"],
                "shippedDate" : v["shippedDate"],
                "invoicedDate" : v["invoicedDate"],
                "month" : v["month"],
                "easyName" : v["easyName"]
                }

            try:
                c.insert_one(add)
            except Exception as e:
                print(f"ALGO : ERROR while adding data to mongo ----{repr(e)}") 

            
        prettyInfo(file, pages, extraction_info)