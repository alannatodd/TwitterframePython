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


def get_tweets(api=None, screen_name=None, how_many_tweets=None):
    list_len = 0
    try:
        check_user_exists = api.GetUser(screen_name=screen_name,return_json=True)
    except twitter.error.TwitterError as err:
        return ["Error: " + parse_twitter_error(err)]

    check_timeline = ''
    try:
        check_timeline = api.GetUserTimeline(screen_name=screen_name, count=200)
    except twitter.error.TwitterError as err:
        return ["Error: " + parse_twitter_error(err)]

    if (len(check_timeline) == 0):
        return ["Error: This user has no tweets."]
    else:
        while list_len == 0:
            timeline = None
            try:
                timeline = api.GetUserTimeline(screen_name=screen_name, count=how_many_tweets, include_rts=False, exclude_replies=True)
            except twitter.error.TwitterError as err:
                return ["Error: " + parse_twitter_error(err)]

            if len(timeline) > 0:
                return clean_timeline(timeline)
            else:
                print("User has no original tweets\n")
                
                retweets = None
                try:
                    retweets = api.GetUserTimeline(screen_name=screen_name, count=how_many_tweets, include_rts=True, exclude_replies=True)
                except twitter.error.TwitterError as err:
                    return ["Error: " + parse_twitter_error(err)]

                if len(retweets) > 0:
                    return clean_timeline(retweets)
                else:
                    print("User has not retweeted\n")

                    replies = None 
                    try:
                        replies = api.GetUserTimeline(screen_name=screen_name, count=how_many_tweets, include_rts=False, exclude_replies=False)
                    except twitter.error.TwitterError as err:
                        return ["Error: " + parse_twitter_error(err)]

                    if len(replies) > 0:
                        return clean_timeline(replies)
                    else:
                        return ["Error: No twitter activity to display for " + screen_name + "\n"]

def parse_twitter_error(twitter_error=None):
    error_dict = twitter_error.message[0]
    return error_dict.get('message')

def clean_timeline(timeline=None):
    cleaned_timeline = []          
    for tweet in timeline:
        cleaned_timeline.append('{screenname}: {text}\n\n <3 {favorites}   {time}\n\n\n'.format(screenname=screen_name.encode('utf-8'), text=tweet.text.encode('utf-8'), favorites=tweet.favorite_count, time=tweet.created_at))
        return cleaned_timeline

if __name__ == "__main__":
    api = twitter.Api(consumer_key=os.getenv('CON_KEY'),
                  consumer_secret=os.getenv('CON_SECRET'),
                  access_token_key=os.getenv('ACCESS_KEY'),
                  access_token_secret=os.getenv('ACCESS_SECRET'))    
    screen_name = sys.argv[1]
    if not screen_name.startswith('@'):
        screen_name = "@" + screen_name
    print("Getting latest tweet from " + screen_name + "...\n")
    cleaned_timeline = get_tweets(api=api, screen_name=screen_name, how_many_tweets=1)


    with open('testfiles/timeline.txt', 'w+') as f:
        #f.write(timeline)
        for tweet in cleaned_timeline:
            f.write(tweet)

    for tweet in cleaned_timeline:
        print(tweet)
