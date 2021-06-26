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
    ret = [x for x in ret if os.path.basename(x)] 
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
        

def update_attr(c, file, stat):
    '''
    updates certain order attributes in Mongo 
    '''
    order = os.path.basename(file)[:-4]
    prev_stat = c.find_one({"easyName":order})['status']
    current_stat = os.path.basename(stat)[2:] # Printed

    if prev_stat != current_stat:
        c.update_one({"easyName":order},{"$set":{"status":current_stat}})
        update_date(c, order, current_stat)

    c.update_one({"easyName":order},{"$set":{"fileDirectory":file}})


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
    for stat in get_dir(root): # stat = 1-Printed
        for f in list_of_files(stat):
            update_attr(c, f, stat)

        if get_dir(stat):
            for sub in get_dir(stat):
                for f in list_of_files(sub):
                    update_attr(c, f, stat)
