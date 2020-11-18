import os
from time import sleep

# SECRETS
CHAT_ID =  os.getenv('CHAT_ID')
API_KEY = os.getenv('API_KEY')

# scraper import
from scrapes.bug_bytes import result as bug_bytes_result
from scrapes.portswigger_research import result as portswigger_research_result

# scraper run
def run_bot():
    bug_bytes_result(API_KEY=API_KEY, CHAT_ID=CHAT_ID)
    portswigger_research_result(API_KEY=API_KEY, CHAT_ID=CHAT_ID)

if __name__ == '__main__':
    while True:
        run_bot()
        sleep(1*60*60*6) # every 6 hours