from data.ioe_crawler import run_spider
import json, os
DATA_PATH = '/home/machina/saneora/api/data/'
if not os.path.exists(DATA_PATH):
        DATA_PATH = "/home/saneora/api/data/"





# runs spider - save first page of exam.ioe.edu.np to new_notices.json
def new_notifications_view(update_old_notices = True):
    run_spider()    #saves scraped notices to api/data/new_notices.json
    unique_new_notices = filter_new_from_old_notices(update_old_notices)   # returns unique_new notices
    print('notifications')
    return {'new_notices':unique_new_notices}
    #return notifications

#nnot = get_new_notification('req')
#print('\n\n\n Notis:' +  str(nnot) +'\n\n\n')


# gets new notices from new_notices.json using notices.json
# return new notices
# add new notices to notices.json
def filter_new_from_old_notices(update_old):
    with open(DATA_PATH + 'old_notices.json', 'r') as file:
        old_notices = json.load(file)
    with open(DATA_PATH + 'new_notices.json', 'r') as file:
        newly_scrapped = json.load(file)
    unique_new = []
    
    # checking if notices already exist in database
    for notice in reversed(newly_scrapped):
        print(notice['title'])
        if not notice in old_notices:
            print('\nadding\n')
            unique_new.append(notice)
    
    if update_old == True and unique_new!=[]:
        # store if unique_new notices list not empty
        update_old_notices(old_notices + unique_new)

    print(unique_new)
    return(unique_new)

def update_old_notices(unique_new):
    # update old notices
    with open(DATA_PATH + 'old_notices.json', 'w') as file:
        json.dump(unique_new, file, indent = 4)
    print('\n updated \n')

def get_saved_notifications(how_many:int):
    with open(DATA_PATH + 'old_notices.json', 'r') as file:
        notices = json.load(file)
    return {"notices" : notices}

