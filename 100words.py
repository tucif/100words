import urllib2

values  = dict((chr(x+96),x) for x in xrange(1,27))
defaultHeaders = {'User-Agent':"Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11"}
wikiRandom = 'http://en.wikipedia.org/wiki/Special:Random'
def get_word_value(word):
  value = 0
  for letter in word:
    #Little optimization to avoid parsing words that wont make it
    if(value > 100):
      return value
    value += values.get(letter,-100) #If letter is not on the valid dict, then we wont let that word get the score, thus -target
  return value

def get_100_words(lines):
  words100 =[]
  for line in lines:
    for word in line.split(" "):
      wordValue = get_word_value(word)      
      if wordValue == 100:
        words100.append((word,True))
  return words100

def get_page_text(pageUrl):
  req = urllib2.Request(wikiRandom,headers=defaultHeaders)
  res = urllib2.urlopen(req)
  print res.url
  return res.readlines()

def main():
  all100Words = {}    
  pages = 0
  while len(all100Words) < 100:
    pageText = get_page_text(wikiRandom)
    pages += 1
    all100Words.update(get_100_words(pageText))
  print "Found %d words on %d wikipedia pages"%(len(all100Words),pages)
  print all100Words

def todo():
  #Allow parameter of target word value
  #Improve the way we read the response, to not load all the page at once and reduce one for loop on get_100_words
  #LULZ: main should find N words of N size each. from 1 to whatever
  pass

if __name__ == "__main__":
  main()
