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
    timeline = api.GetUserTimeline(screen_name=screen_name, count=200)
    earliest_tweet = min(timeline, key=lambda x: x.id).id
    print("getting tweets before:", earliest_tweet)

    while True:
        tweets = api.GetUserTimeline(
            screen_name=screen_name, max_id=earliest_tweet, count=200
        )
        new_earliest = min(tweets, key=lambda x: x.id).id

        if not tweets or new_earliest == earliest_tweet:
            break
        else:
            earliest_tweet = new_earliest
            print("getting tweets before:", earliest_tweet)
            timeline += tweets

    return timeline


if __name__ == "__main__":
    api = twitter.Api(consumer_key=os.getenv('CON_KEY'),
                  consumer_secret=os.getenv('CON_SECRET'),
                  access_token_key=os.getenv('ACCESS_KEY'),
                  access_token_secret=os.getenv('ACCESS_SECRET'))    
    screen_name = sys.argv[1]
    print(screen_name)
    timeline = get_tweets(api=api, screen_name=screen_name)

    with open('testfiles/timeline.json', 'w+') as f:
        for tweet in timeline:
            f.write(json.dumps(tweet._json))
            f.write('\n')
