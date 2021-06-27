from datetime import datetime
import re
# from jsonMod import load_json, add_to_json, update_values (deprecated)
        
    

def is_order_original (c, order_no):

    arg = c.find_one({"_id" : order_no})

    if arg:
        return arg["originalPrint"]


def order_reprint_name(c, order_no):

    regx = re.compile(f".*{order_no}.*", re.IGNORECASE)

    arg = list(c.find(({"_id" : regx})))

    for i in arg:
        order_no += "_reprint"

    return order_no 


def append_data(originalPrint, dateReceived, 
                emailAttachment, shipTo, via, fileDirectory, month, PO, easyName,
                status="Printed", shippedDate=None, invoicedDate=None):
    '''
    all mandatory data
    contains all the data {keys:values} required for each pick ticket.
    '''
    return_dict = {
                    "dateReceived" : dateReceived,
                    "originalPrint" : originalPrint,
                    "emailAttachment" : emailAttachment,
                    "shipTo" : shipTo,
                    "via": via,
                    "PO": PO,
                    "fileDirectory" : fileDirectory,
                    "status" : status,
                    "shippedDate" : shippedDate,
                    "invoicedDate" : invoicedDate,
                    "month" : month,
                    "easyName" : easyName,
                    }
    return return_dict



def ship_via(c, narrowed_text):
    '''
    jsonfile = main json file ("ALL_SHIP_VIA.json")
    narrowed_text = is narrowed_text in read_file() function 
    
    matches "via" with SX data for "ship via"
    '''
    try:
        arg = c.find_one({"_id": "via"})["Signode_Ship_Via"]
        via_return = "NOT FOUND"
        for via_name in arg:
            if via_name in narrowed_text:
                via_return = via_name
        return via_return
    except Exception as e:
        print(f'def ship_via, ERROR:{repr(e)}')

        
