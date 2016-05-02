#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

#Variables that contains the user credentials to access Twitter API 
access_token = "726981854557933568-aCMv2qJ1glUVKJe443vcbCM9GK98wi1"
access_token_secret = "AbvwUnKMOJb4TgKYwFCC7EQm9E73yPRMbqK3nRfMTpgle"
consumer_key = "Hoj9r94uiC1LHacz9lQ6lejyi"
consumer_secret = "I6bg9Y7rfmuYBGqYvWOsJlLdMdHeeGV2sdyXaBG1Q579Ay8UXj"


#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    def on_data(self, data):
        print data
        return True

    def on_error(self, status):
        print status


if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    stream.filter(track=['python', 'javascript', 'ruby'])