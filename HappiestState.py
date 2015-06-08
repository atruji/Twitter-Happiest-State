import sys
import json
import string
from collections import defaultdict
import operator

def lines(fp):
   
    filtTweet=[]
   
    tweets=fp
   
    for i in tweets:
        
        tweet=i
        if type(tweet) is dict:
            if tweet.has_key("text"):
                unicode_string=tweet["text"]
                encoded_string=unicode_string.encode('utf-8')
                ftweet=encoded_string.split(" ")
                filtTweet.append(ftweet)
    return filtTweet

def main():
    afinnfile = open(sys.argv[1])
    
 
    scores = {} # initialize an empty dictionary
 
    for line in afinnfile:
        #print line
        term, score  = line.split("\t") 
        scores[term] = int(score)  # Convert the score to an integer.
    USlist=[]
    tweet_file = open(sys.argv[2])
    tweets=tweet_file.readlines()
    for i in tweets:
        a=json.loads(i)
        if type(a) is dict:
            if a.has_key("place"):
                if a["place"]!=None:
                    if a["place"]["country_code"]=='US':
                        USlist.append(a)
        
   
    filtTweet=lines(USlist)
    
    tweetdict=defaultdict(list)
    for m in filtTweet:
            sentvals=[]
            for n in m:
                #print n
                
                n=n.translate(string.maketrans("",""),string.punctuation)
                n=n.lower()
        
                if scores.has_key(n):
                   
                    sentvals.append(scores[n])
            tweetsent=sum(sentvals)
            #print tweetsent
            for q in USlist:
                
                place=q["place"]["full_name"].split(', ')
                state=place[1]
                if tweetdict.has_key(state):    
                    tweetdict[state].append(tweetsent)
                else:
                    tweetdict[state]=[tweetsent]
    for k in tweetdict:
        tweetdict[k]=sum(tweetdict[k])
    sorted_x = sorted(tweetdict.iteritems(), key=operator.itemgetter(1))
    print sorted_x[len(sorted_x)-1][0]
   
        

if __name__ == '__main__':
    main()
