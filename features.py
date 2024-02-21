from bs4 import BeautifulSoup
from nrclex import NRCLex
from spellchecker import SpellChecker
import nltk
import lxml
import re
#testing function to return the body   - add to feature list if you want it to run         
def test(message,title=0):
    
    if title==1:
       return 'title'
    else: 
        #code to find feature here
        value=message
        return message.get_payload()
#for each message, get the text and html - replace the new line characters and return plain text
def getText(message):
    for part in message.walk():
           if part.get_content_type()=='text/html':
                payload=part.get_payload(decode=True)
                soup=BeautifulSoup(payload,"lxml")
                return soup.get_text().replace("\n"," ").replace("\t"," ").replace('\xa0'," ")
           if part.get_content_type()=='text':
                payload=part.get_payload(decode=True)
                soup=BeautifulSoup(payload,"lxml")
                return soup.get_text().replace("\n"," ").replace("\t"," ").replace('\xa0'," ")

def length(message,title=0):
    if title==1:
        name="LengthOfAddress"
        return name
    else:
        header=message.get('From',"") #email address
        match =re.match(r'(.+)?\s*<(.+?)>', str(header))
        if match:
            addr=match.group(2)
        else:
            addr=str(header)
        total=len(addr)
        return total
def numbersinEmailAddr(message,title=0):
    if title==1:
        name="NumbersInEmailAddress"
        return name
    else:

        header=message.get('From',"") #Header
        
        match = re.match(r'(.+)?\s*<(.+?)>', str(header)) #seperate sender name from email
        if match:
            addr=match.group(2)  # get email
        else:
            addr=str(header)# get email
        count=0
        for num in addr:
            if num.isdigit(): #count the numbers
                count+=1
        return count



def avgWordLength(message,title=0):
    if title==1:
        name="AverageWordLength"
        return name
    else:
        body=getText(message)
        if body==None:
            return 0
        words=body.split()
        total_length=0
        for word in words:
            total_length = total_length+len(word)
        if len(words)==0:
            return 0
        avglength=round(total_length/len(words),2)  #length of all words / number of words

        return avglength


#read in the keywords
keywords=[]
with open('keywords.txt','r',encoding='utf-8') as file:
            for keyword in file:
                keywords.append(keyword.strip()) # get each keyword

def keywordCount(message,title=0):
    if title==1:
        name="KeywordCount"
        return name
    else:
        
        text=getText(message) #get body text
        
        count=0
        if text==None:
            return 0
        for word in keywords:
            if word in text:
                count+=1

        return count

def spellingMistakes(message,title=0):
    if title==1:
        name="SpellingMistakes"
        return name
    else:
        text=getText(message)
        if text==None:
            return 0
        text_obj=NRCLex(text)
        spelling=SpellChecker()
        mistakes=spelling.unknown(text_obj.words)
        return len(mistakes)



def capitalLetters(message,title=0):
    if title==1:
        name="CapitalLetters"
        return name
    else:
        count=0
        text=getText(message)
        if text==None:
            return 0
        for word in text:
            for char in word:
               if char.isupper():
                count+=1
        return count

def linkLength(message,title=0):
    if title==1:
        name="URL Length"
        return name
    else:
        for part in message.walk():

            if part.get_content_type()=='text/html':
                payload=part.get_payload(decode=True)
                soup=BeautifulSoup(payload,"lxml")
                link=soup.find('a')
                if link is not None:

                    href=link.get('href')
                    if href is not None:

                        return len(href)
                    
    return 0

def numbersinLink(message,title=0):
    if title==1:
        name="NumbersInURL"
        return name
    else:
        for part in message.walk():
            if part.get_content_type()=='text/html':
                payload=part.get_payload(decode=True)
                soup=BeautifulSoup(payload,"lxml")
                link=soup.find('a')
                if link is not None:

                    href=link.get('href')
                    if href is not None:

                        count=0
                        for num in href:

                            if num.isdigit():
                            #count the numbers
                                count+=1
                        return count
                    
    return 0
def fakeLinks(message,title=0):
    fakelinkcount=0
    if title==1:
        name="FakeLinks"
        return name
    else:
        for part in message.walk():

            if part.get_content_type()=='text/html':
                payload=part.get_payload(decode=True)
                soup=BeautifulSoup(payload,"lxml")
                link=soup.find('a')
                if link is not None and link.get('onmouseover'):
                    fakelinkcount+=1

            return fakelinkcount

def emotion(message):
    affect_tags = {
    'anger': 0,
    'anticipation': 0,
    'disgust': 0,
    'fear': 0,
    'joy': 0,
    'negative': 0,
    'positive': 0,
    'sadness': 0,
    'surprise': 0,
    'trust': 0
    }
    
    text=getText(message)
    if text==None:
        text="0"
    text_obj=NRCLex(text) #analyise text for emotions
    for key, value in text_obj.affect_frequencies.items():
        affect_tags[key]=value
        
    return affect_tags

def pos(message):
    pos_tags = {
    'CC': 0,
    'CD': 0,
    'DT': 0,
    'EX': 0,
    'FW': 0,
    'IN': 0,
    'JJ': 0,
    'JJR': 0,
    'JJS': 0,
    'LS': 0,
    'MD': 0,
    'NN': 0,
    'NNS': 0,
    'NNP': 0,
    'NNPS': 0,
    'PDT': 0,
    'POS': 0,
    'PRP': 0,
    'PRP$': 0,
    'RB': 0,
    'RBR': 0,
    'RBS': 0,
    'RP': 0,
    'SYM': 0,
    'TO': 0,
    'UH': 0,
    'VB': 0,
    'VBD': 0,
    'VBG': 0,
    'VBN': 0,
    'VBP': 0,
    'VBZ': 0,
    'WDT': 0,
    'WP': 0,
    'WP$': 0,
    'WRB': 0,
    '.':0,
    ':':0,
    '(':0,
    ')':0,
    ',':0,
    '``':0,
    '$':0,
    '#':0,
    '"':0,
    ';':0,
    '?':0,
    '@':0,
    "''": 0
    }
   
    tag_freq={}
    text=getText(message)
    if text==None:
        text="0"
    words=nltk.tokenize.word_tokenize(text)
    tagged=nltk.tag.pos_tag(words)
    for word, tag in tagged:
        if tag not in tag_freq:
            tag_freq[tag]=0
        tag_freq[tag]+=1
    for key, value in tag_freq.items():
        pos_tags[key]=value
        
    return pos_tags


