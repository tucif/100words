import urllib2

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
      return value 
  return value

def get_words_of_value(lineIterator,targetValue):
  words =[]
  try:  
    while True:
      line = lineIterator.next()
      for word in line.split(" "):
        wordValue = get_word_value(word, targetValue)      
        if wordValue == targetValue:
          words.append((word,None))
  except:
    pass 

  return words100

def get_page_text_iterator(pageUrl):
  req = urllib2.Request(wikiRandom,headers=defaultHeaders)
  res = urllib2.urlopen(req)
  print res.url
  return res

def find_words(targetValue):
  allWords = {}    
  pages = 0
  print "Finding %d words of %d value"%(len(allWords),targetValue)
  while len(allWords) < targetValue:
    pages += 1
    print "%d words on %d pages"%(len(allWords),pages),
    pageResponse = get_page_text_iterator(wikiRandom)
    allWords.update(get_words_of_value(pageResponse, targetValue))
    pageResponse.close()  
  wordsOnPages = (len(allWords),pages)
  print "Found %d words on %d wikipedia pages" % wordsOnPages
  print allWords.keys()
  return wordsOnPages 
  

def main():
  totals = (0,0)
  for i in xrange(2,100):
    (wordsCount, pagesCount) = find_words(i)
  
  
def todo():
  pass

if __name__ == "__main__":
  main()
