# -*- coding: utf-8 -*-

from BeautifulSoup import BeautifulSoup
from PIL import Image
import pyscreenshot
import pytesseract
import urllib2
import threading

answers = pyscreenshot.grab(bbox=(554, 400, 400, 187))
answers.save('answers.png')
aText = pytesseract.image_to_string(Image.open('answers.png'))
aSText = aText.split('\n')

question = pyscreenshot.grab(bbox=(552, 240, 325, 150))
question.save('question.png')
qText = pytesseract.image_to_string(Image.open('question.png'))

qTextCleaned = qText.replace('\n',' ')
qTextCleaned = qTextCleaned.replace(u'“','')
qTextCleaned = qTextCleaned.replace(u'”','')
qTextCleaned = qTextCleaned.replace('"','')

qTextCleaned = urllib2.quote(qTextCleaned, safe='')

url = "https://www.ask.com/web?q=" + qTextCleaned
page = urllib2.urlopen(url)
soup = BeautifulSoup(page.read())
links = soup.findAll("a", href=True)

aCount1 = 0
aCount2 = 0
aCount3 = 0

def scanURL(link):
	global aCount1
	global aCount2
	global aCount3

	if link["href"].startswith('https://'):
		try:
			result = urllib2.urlopen(link["href"])
			pageStuff = result.read()
		
			aCount = pageStuff.count(str(aSText[0]))
			aCount1 += aCount
			aCount = pageStuff.count(str(aSText[2]))
			aCount2 += aCount
			aCount = pageStuff.count(str(aSText[4]))
			aCount3 += aCount
		except urllib2.HTTPError as err:
			print(err)

for link in links:
    t = threading.Thread(target=scanURL(link))
    t.daemon = True
    t.start()

print(chr(27) + "[2J")

print('Question: ' + qText + '\n')
print('Answers: ' + aSText[0] + ',' + aSText[2] + ',' + aSText[4] + '\n')

print ('\nAnswer: ' + aSText[0] + ' - ' + str(aCount1))
print ('Answer: ' + aSText[2] + ' - ' + str(aCount2))
print ('Answer: ' + aSText[4] + ' - ' + str(aCount3) + '\n')