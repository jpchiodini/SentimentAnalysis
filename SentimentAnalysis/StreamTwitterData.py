#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import numpy as np
import datetime

#Variables that contains the user credentials to access Twitter API
access_token = "726981854557933568-aCMv2qJ1glUVKJe443vcbCM9GK98wi1"
access_token_secret = "AbvwUnKMOJb4TgKYwFCC7EQm9E73yPRMbqK3nRfMTpgle"
consumer_key = "Hoj9r94uiC1LHacz9lQ6lejyi"
consumer_secret = "I6bg9Y7rfmuYBGqYvWOsJlLdMdHeeGV2sdyXaBG1Q579Ay8UXj"


#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):
    
    Iteration = 0

    def on_data(self, data):            
        try:
            self.Iteration+=1
            print str(self.Iteration) + " " + str(datetime.datetime.now())            
            with open('tweetData.json', 'a') as f:
                f.write(data)
                return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True

    def on_error(self, status):
        self.Iteration += 1
        print self.Iteration
        print status
        if status == 420:
            #returning False in on_data disconnects the stream
            return False


if __name__ == '__main__':
     
    #This handles Twitter authetification and the connection to Twitter
    #Streaming API
    l = StdOutListener()   

    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)   

    #This line filter Twitter Streams to capture data by the keywords:
    #'python', 'javascript', 'ruby'
    import csv
    with open("NASDAQ.txt") as f:
        reader = csv.reader(f, delimiter="\t")
        d = list(reader)    
    
    #unzip the tuple list
    list1, list2 = zip(*d)

    Indices = list(list1[1:len(list1)])   
      
    string = '$'
    my_new_list = [string + x for x in Indices]
    print my_new_list
    
    stream.filter(track=my_new_list[1:400])
    #stream.filter(track=[])    