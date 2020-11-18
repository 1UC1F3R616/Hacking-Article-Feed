# 2
# link- https://blog.intigriti.com/category/bugbytes/

'''
Articles to be fetched won't be crossing 1 page in what I am implementing
'''

# imports
import os
import datetime
from pymongo import MongoClient
from bs4 import BeautifulSoup as soup
import requests

# DB setup
URI = os.getenv('MONGODB_URL')
client = MongoClient(URI)
db = client['hackArticles']
bug_bytes_articles = db['bug_bytes_articles']


# Bot send message function
def send_message(API_KEY, CHAT_ID, message):
    url = "https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}".format(API_KEY, CHAT_ID, message)
    send = requests.get(url)
    
    return send.status_code

##################################################################SCRAPER CODE####################################
'''
url
scraper
result
'''
articles = [] # nested list of [title, url]

URL = 'https://blog.intigriti.com/category/bugbytes/'

def scraper():
    html = requests.get('https://blog.intigriti.com/category/bugbytes/').text
    page_soup = soup(html, 'html.parser')

    site_name = page_soup.title.text
    
    raw_articles = page_soup.findAll('h2', class_='blog-entry-title')

    for raw_article in raw_articles:
        articles.append([raw_article.a.text, raw_article.a['href']])

    message = {
        'site_name': site_name,
        'articles': articles[::-1]
    }

    return message

def result(API_KEY, CHAT_ID):
    try:
        articles = scraper().get('articles')
        for article in articles:
            if bug_bytes_articles.find_one({'title': article[0], 'CHAT_ID':CHAT_ID}) is None: # add in the database and send to telegram
                bug_bytes_articles.insert_one({
                    'title': article[0],
                    'url': article[1],
                    'CHAT_ID': CHAT_ID,
                    "date": datetime.datetime.utcnow()
                })

                #message = '{}\n\n{}\n\n{}'.format('bugbytes Archives - Intigriti', article[0].replace('/', '%2F'), article[1].replace('/', '%2F'))
                message = article[1].replace('/', '%2F')
                print(send_message(API_KEY, CHAT_ID, message))

    except Exception as e:
        print('[!] Failure for bug bytes articles')
        print(str(e))

##################################################################SCRAPER CODE####################################