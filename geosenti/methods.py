import tweepy
import vaderSentiment.vaderSentiment as vader
import itertools

analyzer = vader.SentimentIntensityAnalyzer() #Analyzer object from vader

keys = open("secretKeys.txt", "r")

lines = keys.readlines()

consumer_key = lines[0].rstrip()
consumer_secret  = lines[1].rstrip()
#consumer_key = "gV6FOnqOa0wstev3zljHrcJX6"
#consumer_secret = "uQ8YTRGsJdnAMGUztgGvchGsW3nJIF6RhxzmqYgrYuIS9fn65R"

UK_GEO = "54.364115800619615,-3.7233340937396093,505km"
USA_GEO = "54.19653024080003,-98.03399875931424,2500km"
auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)


api = tweepy.API(auth)

def starter(input):

    britishTweets = tweepy.Cursor(api.search, q=str(input),geocode = UK_GEO, lang = 'en',tweet_mode='extended').items(10)
    usaTweets = tweepy.Cursor(api.search, q=str(input),geocode = USA_GEO, lang = 'en',tweet_mode='extended').items(10)

    britishSentiment = map(TweetHandler, britishTweets)
    usaSentiment = map(TweetHandler, usaTweets)
    
    f = open("tests.txt", "w", encoding="utf-8")

    for Tweet,TweetSenti in itertools.zip_longest(britishTweets, britishSentiment):
        f.write(Tweet.full_text+", "+str(TweetSenti)+"\n")
    f.write("\n\nUSA.............")
    for Tweet,TweetSenti in itertools.zip_longest(usaTweets, usaSentiment):
        f.write(Tweet.full_text+", "+str(TweetSenti)+"\n")

    
def TweetHandler(Tweet):
    try:
        return analyzer.polarity_scores(Tweet.retweeted_status.full_text)
    except AttributeError:  # Not a Retweet
        return analyzer.polarity_scores(Tweet.full_text)
