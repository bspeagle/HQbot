import urllib.parse
import urllib.error
import urllib.request
from bs4 import BeautifulSoup
import threading
import ssl
from google import google

aCount = [0,0,0]

def countAnswers(pageStuff, answer, count):
    aCountTotal = pageStuff.count(answer.encode())
    aCount[count] += aCountTotal

def scanURL(link, answers):
    global aCount
    
    if link.startswith('https://'):
        try:
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE

            result = urllib.request.urlopen(link, context=ctx)
            pageStuff = result.read()

            count = 0

            for answer in answers:
                countAnswers(pageStuff, answer, count)
                count += 1

        except urllib.error.HTTPError as err:
            print(err)
                
def answerQuestion(question, answers):
    getResults(question, answers)
        
    print(chr(27) + "[2J")
    
    count = 0
    for answer in answers:
        print(answer + ': ' + str(aCount[count]))
        count += 1

def getResults(question, answers):
    links = google.search(question, pages=1)
        
    for link in links:
        t = threading.Thread(target=scanURL(link.link, answers))
        t.daemon = True
        t.start()