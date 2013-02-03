from urllib2 import Request
from urllib2 import urlopen
from collections import Counter
import logging
import argparse

#List of tuples of the kind: (a,1),(b,2),...(z,26) saved into a dict
values  = dict((chr(x+96),x) for x in xrange(1,27))
#We need to change user agent for wikipedia to answer the request
defaultHeaders = {'User-Agent':"Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11"}
wikiRandom = 'http://en.wikipedia.org/wiki/Special:Random'

def get_word_value(word, targetValue):
  value = 0
  for character in word:
    #Little optimization to avoid parsing words that won't make it
    if(value > targetValue):
      return value
    try:
      value += values[character]
    except KeyError:
      #Invalid character, invalid word
      return -1 
  return value

def get_words_of_value(lineIterator,targetValue):
  words =[]
  try:  
    while True:
      line = lineIterator.next()
      for word in line.lower().split():
        wordValue = get_word_value(word, targetValue)      
        if wordValue == targetValue:
          words.append(word)
  except StopIteration:
    pass 

  return words

def get_page_text_iterator(pageUrl):
  req = Request(wikiRandom,headers=defaultHeaders)
  res = urlopen(req)
  logging.info(res.url)
  print '.'
  return res

def find_words(targetValue=100,maxRequests=100):
  allWords = Counter() 
  pages = 0
  logging.info("Finding words of %d value"%(targetValue))
  while pages < maxRequests:
    pages += 1
    logging.info("%d words on %d pages"%(len(allWords),pages))
    pageResponse = get_page_text_iterator(wikiRandom)
    allWords.update(get_words_of_value(pageResponse, targetValue))
    pageResponse.close()  
  wordsOnPages = (len(allWords),pages)
  print "\nFound %d words of value %d on %d wikipedia pages" % (wordsOnPages[0],targetValue, wordsOnPages[1])
  print allWords.most_common() 
  return wordsOnPages 
  

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument("-v","--value", help="Target value that the word's characters will add to", type=int, default=100)
  parser.add_argument("-r","--requests", help="Number of requests performed to retrieve data", type=int, default=100)
  args = parser.parse_args()
  results = find_words(args.value,args.requests)
  logging.info("Retrieved %d valid words from %d wikipedia pages"%results)
  
def todo():
  pass

if __name__ == "__main__":
  #logging.basicConfig(level=logging.INFO)
  main()
