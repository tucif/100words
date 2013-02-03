import urllib2
from collections import Counter

#List of tuples of the kind: (a,1),(b,2),...(z,26) saved into a dict
values  = dict((chr(x+96),x) for x in xrange(1,27))
#We need to change user agent for wikipedia to answer the request
defaultHeaders = {'User-Agent':"Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11"}
wikiRandom = 'http://en.wikipedia.org/wiki/Special:Random'

def get_word_value(word, targetValue):
  value = 0
  for letter in word:
    #Little optimization to avoid parsing words that won't make it
    if(value > targetValue):
      return value
    try:
      value += values[letter]
    except KeyError:
      #Invalid character, invalid word
      return -1 
  return value

def get_words_of_value(lineIterator,targetValue):
  words =[]
  try:  
    while True:
      line = lineIterator.next()
      for word in line.split():
        wordValue = get_word_value(word, targetValue)      
        if wordValue == targetValue:
          words.append(word)
  except:
    pass 

  return words

def get_page_text_iterator(pageUrl):
  req = urllib2.Request(wikiRandom,headers=defaultHeaders)
  res = urllib2.urlopen(req)
  print res.url
  return res

def find_words(targetValue,maxRequests=100):
  allWords = Counter() 
  pages = 0
  print "Finding words of %d value"%(targetValue)
  while pages < maxRequests:
    pages += 1
    print "%d words on %d pages"%(len(allWords),pages),
    pageResponse = get_page_text_iterator(wikiRandom)
    allWords.update(get_words_of_value(pageResponse, targetValue))
    pageResponse.close()  
  wordsOnPages = (len(allWords),pages)
  print "Found %d words of value %d on %d wikipedia pages" % (wordsOnPages[0],targetValue, wordsOnPages[1])
  print allWords.most_common() 
  return wordsOnPages 
  

def main():
  totals = [0,0]
  for i in xrange(100,101):
    (wordsCount, pagesCount) = find_words(i)
    totals[0] += wordsCount 
    totals[1] += pagesCount
  print "Made %d requests and retrieved %d valid words"
  
def todo():
  pass

if __name__ == "__main__":
  main()
