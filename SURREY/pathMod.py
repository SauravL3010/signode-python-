from datetime import date, datetime
import os

def paths(root_path):
    '''
    root_path = takes in path where email_attachments are saved (must be r'str')
    
    all_paths = {} is a dictionary to all required directories 
    '''
    # today = date.today()

    # m = datetime.now().strftime('%B-%Y')

    # email_archive = root_path + '\\main'
    # email_archive = root_path + '\\MARKHAM_EMAIL_ARCHIVE'
    email_archive = '\\SURREY_EMAIL_ARCHIVE'


    # monthly_tickets = root_path + fr"\{m}"
    sub_dir = [fr"{root_path}\1-Printed", fr"{root_path}\2-Other", fr"{root_path}\3-Shipped", 
                fr"{root_path}\4-Invoiced",fr"{root_path}\5-Archived"]


    # staged_dir = [fr"{root_path}\2-East\1-Staged", fr"{root_path}\3-West\1-Staged", fr"{root_path}\4-Parts\1-Staged"]
    # staged_dir = []

    all_paths = {
        'root_path' : root_path,

        'email_archive' : email_archive,

        # 'monthly_tickets' : monthly_tickets,
        'sub_dir' : sub_dir,
        # 'staged_dir' : staged_dir,

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

