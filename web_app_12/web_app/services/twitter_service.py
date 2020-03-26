import os
from dotenv import load_dotenv
import tweepy

load_dotenv()

consumer_key = os.getenv("TWITTER_API_KEY", default="OOPS")
consumer_secret = os.getenv("TWITTER_API_SECRET", default="OOPS")
access_token = os.getenv("TWITTER_ACCESS_TOKEN", default="OOPS")
access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET", default="OOPS")

def twitter_api_client():
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    print("AUTH", type(auth))

    api = tweepy.API(auth)
    print("API", type(api)) #> <class 'tweepy.api.API'>
    return api

if __name__ == "__main__":
    #breakpoint()
    #public_tweets = api.home_timeline()
    #for tweet in public_tweets:
    #    print(tweet.text)

    # get information about a twitter user:

    api = twitter_api_client()

    screen_name = "elonmusk"

    print("--------------")
    print("USER...")
    user = api.get_user(screen_name)
    print(type(user)) #> <class 'tweepy.models.User'>
    print(user.screen_name)
    print(user.followers_count)
    pprint(user._json)

    print("--------------")
    print("STATUSES...")
    # get that user's tweets:
    # see: http://docs.tweepy.org/en/latest/api.html#API.user_timeline
    statuses = api.user_timeline(screen_name, tweet_mode="extended", count=150, exclude_replies=True, include_rts=False)

    for status in statuses:
        print(type(status)) #> <class 'tweepy.models.Status'>
        #pprint(status._json)
        #breakpoint()
        print(status.full_text)



# elon = client.get_user("elonmusk")
#
# print("---------------------------------------------------------------")
# print(f"RECENT TWEETS BY @{elon.screen_name} ({elon.followers_count} FOLLOWERS / {elon.friends_count} FOLLOWING):")
# print("---------------------------------------------------------------")
#
# elon_tweets = elon.timeline(
#     count=200,
#     exclude_replies=True,
#     include_rts=False,
#     tweet_mode='extended'
# )
#
# for tweet in elon_tweets:
#     created_on = tweet.created_at.strftime("%Y-%m-%d")
#     print(" + ", tweet.id_str, created_on, tweet.full_text)