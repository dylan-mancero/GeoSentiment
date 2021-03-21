import tweepy
import vaderSentiment.vaderSentiment as vader
from itertools import zip_longest

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
 
    britishTweets = list(map(FullTextHandler, britishTweets))
    usaTweets = list(map(FullTextHandler, usaTweets))
    
    britishSentiment = list(map(lambda tweet: str(analyzer.polarity_scores(tweet)), britishTweets))
    usaSentiment = list(map(lambda tweet: str(analyzer.polarity_scores(tweet)), usaTweets))

    f = open("tests.txt", "w", encoding="utf-8")
    count = 0
    for Tweet,Senti in zip_longest(britishTweets, britishSentiment):
        f.write(str(count) + " " + Tweet + "-->" + Senti + "\n")
        count += 1

    f.write("\n\nUSA.............\n\n")
    count = 0

    for Tweet,Senti in zip_longest(usaTweets, usaSentiment):
        f.write(str(count) + " " + Tweet + "-->" + Senti + "\n")
        count += 1
 
def FullTextHandler(Tweet):
    try:
        return str(Tweet.retweeted_status.full_text)
    except AttributeError:  # Not a Retweet
        return str(Tweet.full_text)