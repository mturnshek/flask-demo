import tweepy
import itertools

# Tweepy setup

# Since the application is read-only,
# I'm not particularly worried about keys.
consumer_key = "2JCopugatNJ0SVas4bT87B26G"
consumer_secret = "Rjrf0KAbXdKKHhEDUhrBIIewJaCjxpVv6tqqfN86HGKF7px8HT"
access_token = "4823441489-MoIRN3gH6KzxyXaC7f5zePEIsW2SzKNUUMRttxd"
access_token_secret = "0AAjTy3a79cPWG4Xm0OVyruvlbLxtHS9Dxzp2Kns5Vuf9"
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# Just an initial test, prints tweets from a user's feed
def print_user_feed():
    public_tweets = api.home_timeline()
    for tweet in public_tweets:
        print tweet.text


# Prints n tweets which contain search_tag
def collect_tweets_from_query(search_tag, n):
    # collects tweets
    all_tweets = tweepy.Cursor(
        api.search,
        q = search_tag,
        rpp = 100,
        result_type = "recent",
        include_entities = True,
        lang = "en"
    ).items()
    # grabs the first n items from all_tweets
    tweets = itertools.islice(all_tweets, n)
    return tweets