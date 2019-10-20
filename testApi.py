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


def get_tweets(api=None, screen_name=None):
    timeline = api.GetUserTimeline(screen_name=screen_name, count=20, include_rts=False, exclude_replies=True)
    cleanedTimeline = []
    #earliest_tweet = min(timeline, key=lambda x: x.id).id
    #print("getting tweets before:", earliest_tweet)
    for tweet in timeline:
        parsedLine = ('@{screenname}: {text}\n\n <3 {favorites}   {time}\n\n\n'.format(screenname=screen_name.encode('utf-8'), text=tweet.text.encode('utf-8'), favorites=tweet.favorite_count, time=tweet.created_at))
        cleanedTimeline.append(parsedLine)
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

    return cleanedTimeline


if __name__ == "__main__":
    api = twitter.Api(consumer_key=os.getenv('CON_KEY'),
                  consumer_secret=os.getenv('CON_SECRET'),
                  access_token_key=os.getenv('ACCESS_KEY'),
                  access_token_secret=os.getenv('ACCESS_SECRET'))    
    screen_name = sys.argv[1]
    print(screen_name)
    timeline = get_tweets(api=api, screen_name=screen_name)

    with open('testfiles/timeline.txt', 'w+') as f:
        #f.write(timeline)
        for tweet in timeline:
            print(tweet)
            f.write(tweet)
        #    f.write('\n')
