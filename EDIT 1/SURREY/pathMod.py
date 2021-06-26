from datetime import date, datetime
import os

def paths(root_path):
    '''
    root_path = takes in path where email_attachments are saved (must be r'str')
    
    all_paths = {} is a dictionary to all required directories 
    '''
    # today = date.today()

    m = datetime.now().strftime('%B-%Y')

    # email_archive = root_path + '\\main'
    # email_archive = root_path + '\\MARKHAM_EMAIL_ARCHIVE'
    email_archive = '\\SURREY_EMAIL_ARCHIVE'


    monthly_tickets = root_path + fr"\{m}"
    in_month_dir = [fr"{monthly_tickets}\1-Printed", fr"{monthly_tickets}\2-Quarantine", fr"{monthly_tickets}\3-Shipped", fr"{monthly_tickets}\4-Invoiced",fr"{monthly_tickets}\5-POI"]


    staged_dir = [fr"{monthly_tickets}\1-Printed\1-Staged"]

    all_paths = {
        'root_path' : root_path,

        'email_archive' : email_archive,

        'monthly_tickets' : monthly_tickets,
        'in_month_dir' : in_month_dir,
        'staged_dir' : staged_dir,

    }
    return all_paths



def create_directory(path):
    '''
    path = directory to create (must be r'str')
    '''
    try:
        os.mkdir(path)
    except OSError:
        print ("Creation of the directory %s failed" % path)
        


def enter_directory(path):
    '''
    path = directory to enter(must be r'str')
    '''
    try: 
        os.chdir(path)
    except OSError:       
        print("Entering the directory %s failed" % path)
        
        
        
def verify_directory(path):
    '''
    path = directory to verify (must be r'str')
    '''
    return os.path.exists(path)



def move_files(src, dst):
    '''
    src = path to file (.pdf)
    dst = new path to file (.pdf)
    '''
    try:
        os.replace(src, dst)
    except:
        os.rename(src, dst)

