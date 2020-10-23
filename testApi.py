import twitter
from dotenv import load_dotenv
import os
import sys
import json 

load_dotenv()
api = twitter.Api(consumer_key=os.getenv('CON_KEY'),
                  consumer_secret=os.getenv('CON_SECRET'),
                  access_token_key=os.getenv('ACCESS_KEY'),
                  access_token_secret=os.getenv('ACCESS_SECRET'))


def get_tweets(api=None, screen_name=None, howManyTweets=None):
    listLen = 0
    pullCount = howManyTweets
    try:
        checkUserExists = api.GetUser(screen_name=screen_name,return_json=True)
    except twitter.error.TwitterError as err:
        return ["Error: " + parseTwitterError(err)]

    checkTimeline = ''
    try:
        checkTimeline = api.GetUserTimeline(screen_name=screen_name, count=200)
    except twitter.error.TwitterError as err:
        return ["Error: " + parseTwitterError(err)]

    if (len(checkTimeline) == 0):
        return ["Error: This user has no tweets."]
    else:
        while listLen == 0:
            timeline = api.GetUserTimeline(screen_name=screen_name, count=pullCount, include_rts=False, exclude_replies=True)
            listLen = len(timeline)
            if listLen > 0:
                cleanedTimeline = []
                for tweet in timeline:
                    parsedLine = ('{screenname}: {text}\n\n <3 {favorites}   {time}\n\n\n'.format(screenname=screen_name.encode('utf-8'), text=tweet.text.encode('utf-8'), favorites=tweet.favorite_count, time=tweet.created_at))
                    cleanedTimeline.append(parsedLine)
                return cleanedTimeline
            else:
                return ["Error: User has no original tweets."]

    #earliest_tweet = min(timeline, key=lambda x: x.id).id
    #print("getting tweets before:", earliest_tweet)
        #print(parsedLine)
    #while True:
        #tweets = api.GetUserTimeline(
        #    screen_name=screen_name, max_id=earliest_tweet, count=200
        #)
        #new_earliest = min(tweets, key=lambda x: x.id).id

        #if not tweets or new_earliest == earliest_tweet:
        #    break
        #else:
        #    earliest_tweet = new_earliest
        #    print("getting tweets before:", earliest_tweet)
        #    timeline += tweets

    #return cleanedTimeline

def parseTwitterError(twitterError=None):
    errorDict = twitterError.message[0]
    return errorDict.get('message')

if __name__ == "__main__":
    api = twitter.Api(consumer_key=os.getenv('CON_KEY'),
                  consumer_secret=os.getenv('CON_SECRET'),
                  access_token_key=os.getenv('ACCESS_KEY'),
                  access_token_secret=os.getenv('ACCESS_SECRET'))    
    screen_name = sys.argv[1]
    if not screen_name.startswith('@'):
        screen_name = "@" + screen_name
    print("Getting latest tweet from " + screen_name + "...\n")
    cleanedTimeline = get_tweets(api=api, screen_name=screen_name, howManyTweets=1)


    with open('testfiles/timeline.txt', 'w+') as f:
        #f.write(timeline)
        for tweet in cleanedTimeline:
            f.write(tweet)

    for tweet in cleanedTimeline:
        print(tweet)
