# 1
# link- https://portswigger.net/research/articles

'''

'''

# imports
import os
import datetime
import urllib.parse
from pymongo import MongoClient
from bs4 import BeautifulSoup as soup
import requests

# DB setup
URI = os.getenv('MONGODB_URL')
client = MongoClient(URI)
db = client['hackArticles']
portswigger_research_articles = db['portswigger_research_articles']


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
BASE_URL = 'https://portswigger.net'

articles = [] # nested list of [title, url]
def scraper():
    html = requests.get('https://portswigger.net/research/articles').text
    page_soup = soup(html, 'html.parser')

    site_name = page_soup.title.text
    
    raw_articles = page_soup.findAll('a', class_='noscript-post') # latest 4 will come from this

    for raw_article in raw_articles:
        articles.append([raw_article.span.text, BASE_URL + raw_article['href']])

    message = {
        'site_name': site_name,
        'articles': articles[::-1]
    }

    return message

def result(API_KEY, CHAT_ID):
    try:
        articles = scraper().get('articles')
        for article in articles:
            if portswigger_research_articles.find_one({'title': article[0], 'CHAT_ID':CHAT_ID}) is None: # add in the database and send to telegram
                portswigger_research_articles.insert_one({
                    'title': article[0],
                    'url': article[1],
                    'CHAT_ID': CHAT_ID,
                    "date": datetime.datetime.utcnow()
                })

                message = urllib.parse.quote_plus(article[1])
                print(send_message(API_KEY, CHAT_ID, message))

    except Exception as e:
        print('[!] Failure for portswigger research articles')
        print(str(e))

##################################################################SCRAPER CODE####################################