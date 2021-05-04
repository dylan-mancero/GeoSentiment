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
geoList = {
    "UK_GEO" : "54.364115800619615,-3.7233340937396093,505km",#lat,long and radius of usa, using googlemaps measurerer
    "USA_GEO" : "54.19653024080003,-98.03399875931424,2500km",
    "AUS_GEO" : "-27.606338814377246,135.2637427077579,2000km",
    "JAMAICA_GEO" : "18.13788732831686,-77.24297002881919,128km",
    "NEWZEALAND_GEO" : "-41.876952864666166,173.64569158277476,854km",
    "INDIA_GEO" : "20.09904976266362,79.35616263260019,1300km",
    "NIGERIA_GEO" : "8.574482569303768,7.542770727835754,500km"
}

analyzer = vader.SentimentIntensityAnalyzer() #Analyzer object from vader

def starter(input, country1, country2):
    country_1_tweets = tweepy.Cursor(api.search, q=str(input),geocode = geoList[country1], lang = 'en',tweet_mode='extended').items(200)
    country_2_tweets = tweepy.Cursor(api.search, q=str(input),geocode = geoList[country2], lang = 'en',tweet_mode='extended').items(200)
 
    country_1_tweets = list(map(FullTextHandler, country_1_tweets))
    country_2_tweets = list(map(FullTextHandler, country_2_tweets))
    
    country_1_senti = list(map(lambda tweet: analyzer.polarity_scores(tweet), country_1_tweets))
    country_2_senti = list(map(lambda tweet: analyzer.polarity_scores(tweet), country_2_tweets))

    country_1_score = generateScores(country_1_senti)
    country_2_score = generateScores(country_2_senti)
    
    return country_1_score, country_2_score

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