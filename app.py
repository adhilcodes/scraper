import pyrebase
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# setting up firebase realtime database

# Setting the configuration for the app
config = {
    "apiKey": "AIzaSyCS-fqlvMs8jX9UFMOnvFxFgtAxupZCLKM",
    "authDomain": "db-padanam.firebaseapp.com",
    "databaseURL": "https://db-padanam-default-rtdb.firebaseio.com",
    "projectId": "db-padanam",
    "storageBucket": "db-padanam.appspot.com",
    "messagingSenderId": "854372348586",
    "appId": "1:854372348586:web:6d6e3e70d7843f742956d3",
    "measurementId": "G-8402SDDHM3"
}

firebase = pyrebase.initialize_app(config)

# Get a reference to the database service
db = firebase.database()






# scraper function
website_link = 'https://www.cee.kerala.gov.in/keam2021/notification'
link_class = 'col-sm-10'

def scraper(website_link, link_class):

    ''' Args : website_link - link of website to be crawled
               link_class   - class name for job link on website
               Returns : jobs_link - list of jobs '''

    # getting content of website and parsing it
    
    website_request = requests.get(website_link, verify=False)
    website_content = BeautifulSoup(website_request.content, 'html.parser')
    
    # extracting the class of notifications 

    jobs_link = website_content.find_all(class_ = link_class)
    scraped_data =  jobs_link[0]

    link = scraped_data.find('a').get('href')
    title = scraped_data.text.splitlines()[0]
    msg = {"title": title,"link": link}

    # uploading to firebase realtime database
    db.child("Live data").set(msg)




# fetcher/scheduler function
def scheduler():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    
    if current_time == "2:00:00" or current_time == "5:00:00":
        scraper()


scheduler()
