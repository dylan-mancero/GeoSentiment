import tweepy
import vaderSentiment.vaderSentiment as vader
from itertools import zip_longest

#Gets secret tokents needed for using the twitter API from a local textfile, which is gitignored for safety purposes.
keys = open("secretKeys.txt", "r")
lines = keys.readlines()
consumer_key = lines[0].rstrip()
consumer_secret  = lines[1].rstrip()
#sets up tweepy api object
auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)
api = tweepy.API(auth)

UK_GEO = "54.364115800619615,-3.7233340937396093,505km"#lat,long and radius of usa, using googlemaps measurerer
USA_GEO = "54.19653024080003,-98.03399875931424,2500km"

analyzer = vader.SentimentIntensityAnalyzer() #Analyzer object from vader

def starter(input):
    britishTweets = tweepy.Cursor(api.search, q=str(input),geocode = UK_GEO, lang = 'en',tweet_mode='extended').items(10)
    usaTweets = tweepy.Cursor(api.search, q=str(input),geocode = USA_GEO, lang = 'en',tweet_mode='extended').items(10)
 
    britishTweets = list(map(FullTextHandler, britishTweets))
    usaTweets = list(map(FullTextHandler, usaTweets))
    
    britishSentiment = list(map(lambda tweet: analyzer.polarity_scores(tweet), britishTweets))
    usaSentiment = list(map(lambda tweet: analyzer.polarity_scores(tweet), usaTweets))

    britishScore = generateScores(britishSentiment)
    usaScore = generateScores(usaSentiment)

    return britishScore, usaScore

def FullTextHandler(Tweet):
    #this method is used to extract the full text of a tweet object, because retweets are truncated.
    try:
        return str(Tweet.retweeted_status.full_text)
    except AttributeError:  # Not a Retweet
        return str(Tweet.full_text)

def generateScores(scores):
    scoreResults = {'pos':0, 'neg':0, 'neutral':0}

    for score in scores:
        compound = score['compound']

        if compound >= 0.05:
            current = scoreResults['pos']
            scoreResults['pos'] = current + 1
        elif compound <= -0.05:
            current = scoreResults['neg']
            scoreResults['neg'] = current + 1
        else:
            current = scoreResults['neutral']
            scoreResults['neutral'] = current + 1
    return scoreResults