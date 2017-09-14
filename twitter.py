import json
import requests

# Dependencies
from keys import keys
from slack import Slack

#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

#This is a basic listener that receives tweets to stdout.
# Source code for class derived from: http://adilmoujahid.com/posts/2014/07/twitter-analytics/
class StdOutListener(StreamListener):

    def on_data(self, data):
        data  = json.loads(data)
        user  = data['user']['screen_name']
        tweet =  data['text']
        try:
            res = postToSlack(user, tweet, "#test")
            if res is not None:
                #print error occured
                print(res)
        except Exception as e:
            print e
        return True

    #If an error occurs
    def on_error(self, status):
        print status

# A function to create a new slack object, and then post to a particular channel
def postToSlack(user, message, channel):
   
    if keys.has_key('slack'):
         slack = Slack(keys['slack']['url'])
         slack.setChannel(channel)
         return slack.postToSlack(user, message)
    else:
        raise Exception('No slack webhook')

# A function to read twitter and based off the query 
def readTwitter(queries, channel):
    #Twitter Keys
    if keys.has_key('twitter'):
        twitter             = keys['twitter']
        CONSUMER_KEY        = twitter['CONSUMER_KEY']
        CONSUMER_SECRET     = twitter['CONSUMER_SECRET']
        ACCESS_TOKEN_KEY    = twitter['ACCESS_TOKEN_KEY']
        ACCESS_TOKEN_SECRET = twitter['ACCESS_TOKEN_SECRET']    
    else:
        raise Exception('No twitter keys')

    try:
        l = StdOutListener()
        auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET)
        stream = Stream(auth, l)

        #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
        stream.filter(track=queries)

    except Exception as e:
        print e

if __name__ == "__main__":
    #Set each query in array in array
    queries = []

    #Set Channel to post to
    channel = ""

    #Call function to start reading to twitter
    readTwitter(queries,channel)
