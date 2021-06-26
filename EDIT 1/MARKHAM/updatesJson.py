import os
from datetime import datetime, date
# from jsonMod import load_json, add_to_json, update_values (deprecated)
from allFiles import list_of_files


def get_dir(root):
    '''
    list all the dir's in the specified root. (only dirs and no files)

    '''
    ret = []
    for f in os.listdir(root):
        p = os.path.join(root, f)
        if os.path.isdir(p):
            ret.append(p)
    return ret



def months(root):
    '''
    lists all the months within Markham 
    root is given as Markham/ 
    excludes the email archive 

    '''
    ret = get_dir(root)
    ret = [x for x in ret if os.path.basename(x)] # exclude email_archive
    return ret





def update_date(c, o, s):
    '''
    f = json filename
    o = order
    s = status
    '''
    if s=='Printed':
        c.update_one({"easyName":o},{"$set":{"shippedDate":None}})
        c.update_one({"easyName":o},{"$set":{"invoicedDate":None}})

    elif s=="Shipped":
        c.update_one({"easyName":o},{"$set":{"shippedDate":datetime.now()}})
        c.update_one({"easyName":o},{"$set":{"invoicedDate":None}})

    elif s=="Invoiced":
        c.update_one({"easyName":o},{"$set":{"invoicedDate": datetime.now()}})
        

def update_attr(c, file, stat, month):
    '''
    updates certain order attributes in Mongo 
    '''
    current_stat = os.path.basename(stat)[2:] # Printed
    order = os.path.basename(file)[:-4]

    c.update_one({"easyName":order},{"$set":{"status":current_stat}})

    c.update_one({"easyName":order},{"$set":{"fileDirectory":file}})

    c.update_one({"easyName":order},{"$set":{"month":os.path.basename(month)}})

    update_date(c, order, current_stat)


def updates_to_json(c, root):
    '''


    root = paths(code_vars["temp_path"])
    jf = json file for pick_tickets_signode


    algorithm:
    lists all months:
        lists all dirs (status) in month:
            lists all .pdf files:
                makes changes to status and "fileDirectory"

    '''
    for month in months(root):
        for stat in get_dir(month):
            if get_dir(stat):
                for d in get_dir(stat):
                    for f in list_of_files(d):
                        update_attr(c, f, stat, month)
            for f in list_of_files(stat):
                update_attr(c, f, stat, month)
