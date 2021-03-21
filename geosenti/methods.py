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
    britishTweets = tweepy.Cursor(api.search, q=str(input),geocode = UK_GEO, lang = 'en',tweet_mode='extended').items(5)
    usaTweets = tweepy.Cursor(api.search, q=str(input),geocode = USA_GEO, lang = 'en',tweet_mode='extended').items(5)
 
    britishTweets = list(map(FullTextHandler, britishTweets))
    usaTweets = list(map(FullTextHandler, usaTweets))
    
    britishSentiment = list(map(lambda tweet: analyzer.polarity_scores(tweet), britishTweets))
    usaSentiment = list(map(lambda tweet: analyzer.polarity_scores(tweet), usaTweets))

    britishScore = {'pos':0, 'neg':0, 'neutral':0}
    usaScore = {'pos':0, 'neg':0, 'neutral':0}

    for score in britishSentiment:
        compound = score['compound']
        if compound >= 0.05:
            current = britishScore['pos']
            britishScore['pos'] = current + 1
        elif compound <= -0.05:
            current = britishScore['neg']
            britishScore['neg'] = current + 1
        else:
            current = britishScore['neutral']
            britishScore['neutral'] = current + 1
            
    for score in usaSentiment:
        compound = score['compound']
        if compound >= 0.05:
            current = usaScore['pos']
            usaScore['pos'] = current + 1
        elif compound <= -0.05:
            current = usaScore['neg']
            usaScore['neg'] = current + 1
        else:
            current = usaScore['neutral']
            usaScore['neutral'] = current + 1
    f = open('scoreTest.txt', 'w', encoding='utf-8')
    for score in britishSentiment:
        f.write(str(score) + "\n")
    f.write(str(britishScore))
    f.close
def FullTextHandler(Tweet):
    try:
        return str(Tweet.retweeted_status.full_text)
    except AttributeError:  # Not a Retweet
        return str(Tweet.full_text)