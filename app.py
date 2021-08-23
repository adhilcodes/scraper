import requests
import firebase_admin
from bs4 import BeautifulSoup
from datetime import datetime
from firebase_admin import credentials


# Setting the configuration for the app

path = './configuration.json'
cred = credentials.Certificate(path)
firebase = firebase_admin.initialize_app(cred)

# Get a reference to the database service

cred = credentials.Certificate(path)
firebase_admin.initialize_app(cred, {
    'databaseURL' : 'https://keam-scraper-default-rtdb.firebaseio.com'
})



# scraper function
def scraper(website_link, link_class):

    ''' Args : website_link - link of website to be crawled
               link_class   - class name for job link on website
               Returns : jobs_link - list of jobs '''

    # getting content of website and parsing it
    
    website_request = requests.get(website_link, verify=False)
    website_content = BeautifulSoup(website_request.content, 'html.parser')
    
    # extracting the class of notifications 

    jobs_link = website_content.find_all(class_ = link_class)
    return jobs_link

# print(scraper('https://www.cee.kerala.gov.in/keam2021/notification', 'col-sm-10')[1])



# fetcher/scheduler function
def scheduler():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    
    if current_time == "23:00:00":
        scraper()

scheduler()