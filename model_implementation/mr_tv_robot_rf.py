print "Starting up..."

## twitter bot "Mr TV Robot"
# these libraries are for the bot
import tweepy

# these libraries are for the model
import pandas as pd
import numpy as np
import urllib2
import json
from bs4 import BeautifulSoup
from time import sleep
import requests
from datetime import datetime, timedelta
import pickle

print "Libraries are loaded"

# boilerplate code for twitter
consumer_key = 'FeKvVKDbKwYh71ecwaaM4ShjZ'
consumer_secret_key = 'H5dOOSSCHCNPu8bisXL0cHhj6txG6EF8xuc9kwerm3c5wHDQ2E'
access_token = 	'877244005343522816-HFRbUWiu26rQqYrf8GtJtoKjYCeipsu'
access_token_secret = 'dRZSuWQnyyFt37kfv3cnx9ORCEPmg42pU7qKUEYrWCFt5'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret_key)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

print "Twitter authenticated"


## functions I'll need

def bleach(string):
    temp = ""
    string = str(string)
    for i in string:
        if i in ["1","2","3","4","5","6","7","8","9","0","."]:
            temp += i
    if len(temp) > 0:
        return float(temp)

def combine_list(list):
    temp = ""
    for i in list:
        temp += " " + i
    return temp

def get_api_from_id(title_id):
    this_url = "http://www.omdbapi.com/?i=" + title_id + "&plot=full&r=json&apikey=9f5296af"
    req = requests.get(this_url)
    return req.json()
    sleep(2)

def df_from_api(title_id):
    df = pd.DataFrame(data=[title_id], columns=['imdb_id'])
    df['json'] = df['imdb_id'].apply(get_api_from_id)
    df['name'] = df['json'].apply(lambda x: x['Title'])
    df['genres'] = df['json'].apply(lambda x: str.lower(str(x['Genre'])))
    df['seasons'] = df['json'].apply(lambda x: bleach(x['totalSeasons']))
    df['runtime'] = df['json'].apply(lambda x: bleach(x['Runtime']))
    df['release_date'] = df['json'].apply(lambda x: x['Released'])
    sleep(2)
    return df

def parse_genres(df):
    genre_names = ['action', u'adventure', u'animation', u'biography', u'comedy',
           u'crime', u'documentary', u'drama', u'family', u'fantasy',
           u'game', u'history', u'horror', u'music', u'musical', u'mystery',
           u'news', u'reality', u'romance', u'sci', u'short', u'sport', u'talk',
           u'thriller', u'war', u'western']
    for i in genre_names:
        df['is_%s' % i] = df['genres'].apply(lambda x: 1 if i in x.lower() else 0)

def scrape_network(id):
    words = ""
    url = "http://www.imdb.com/title/" + id + "/companycredits?ref_=ttspec_sa_5"
    soup = BeautifulSoup(urllib2.urlopen(url), "html5lib")
    simpleLists = soup.find_all('ul', {'class': 'simpleList'})
    try:
        for li in simpleLists[1]('li'):
            for a in li('a'):
                words += (a.get_text() + '\n')
        return words.split("\n")[0]
    except:
        return "unknown"
    sleep(2)


def access_keyword_page(imdbID):
    return 'http://www.imdb.com/title/' + imdbID + '/keywords?ref_=tt_stry_kw'

def scrape_keywords(imdbID):
    soup_for_keywords = BeautifulSoup(urllib2.urlopen(access_keyword_page(imdbID)), "html5lib")
    temp_keywords = []
    for div in soup_for_keywords('div', {'id':'keywords_content'}):
        for text in div('div', {'class':'sodatext'}):
            for a in text('a'):
                temp_keywords.append(a.get_text())
    return temp_keywords
    sleep(2)

def parse_keywords(df):
    keywords_to_use_2 = [u'adult', u'african', u'alien',
           u'american', u'angel', u'anim', u'base', u'best', u'black', u'book',
           u'boy', u'boyfriend', u'brother', u'california', u'celebr', u'charact',
           u'child', u'citi', u'comedi', u'comedian', u'comic', u'cult',
           u'daughter', u'death', u'detect', u'doctor', u'evil', u'famili',
           u'father', u'femal', u'fiction',u'friend', u'friendship',
           u'gay', u'girl', u'girlfriend', u'hero', u'humor',
           u'husband', u'interraci', u'interview', u'investig', u'joke',
           u'life', u'live', u'love', u'male', u'man', u'marriag', u'mother',
           u'murder',u'offic', u'parent', u'parodi',
           u'play', u'polic', u'power', u'protagonist', u'relationship', u'satir',
           u'school', u'secret',u'sex', u'share', u'sister', u'sitcom',
           u'social', u'son', u'spoken', u'spoof', u'stand', u'student',
           u'superhero', u'supernatur', u'surreal', u'teenag',
           u'versu', u'villain', u'violenc', u'wife', u'woman',
           u'york']
    for i in keywords_to_use_2:
        df['keyword_%s' % i] = df['keywords'].apply(lambda x: 1 if i in x else 0)

def parse_dates(df):
    df['release_date'] = df['release_date'].apply(lambda x: datetime.strptime(x, '%d %b %Y'))
    df['release_month'] = df['release_date'].apply(lambda x: x.strftime('%m'))
    df['release_weekday'] = df['release_date'].apply(lambda x: x.strftime('%w'))
    df['release_monthday'] = df['release_date'].apply(lambda x: x.strftime('%d'))
    df['started_sunday'] = df['release_weekday'].apply(lambda x: 1 if int(x)==0 else 0)
    df['started_monday'] = df['release_weekday'].apply(lambda x: 1 if int(x)==1 else 0)
    df['started_tuesday'] = df['release_weekday'].apply(lambda x: 1 if int(x)==2 else 0)
    df['started_wednesday'] = df['release_weekday'].apply(lambda x: 1 if int(x)==3 else 0)
    df['started_thursday'] = df['release_weekday'].apply(lambda x: 1 if int(x)==4 else 0)
    df['started_friday'] = df['release_weekday'].apply(lambda x: 1 if int(x)==5 else 0)
    df['started_saturday'] = df['release_weekday'].apply(lambda x: 1 if int(x)==6 else 0)
    df['started_january'] = df['release_month'].apply(lambda x: 1 if int(x)==1 else 0)
    df['started_february'] = df['release_month'].apply(lambda x: 1 if int(x)==2 else 0)
    df['started_march'] = df['release_month'].apply(lambda x: 1 if int(x)==3 else 0)
    df['started_april'] = df['release_month'].apply(lambda x: 1 if int(x)==4 else 0)
    df['started_may'] = df['release_month'].apply(lambda x: 1 if int(x)==5 else 0)
    df['started_june'] = df['release_month'].apply(lambda x: 1 if int(x)==6 else 0)
    df['started_july'] = df['release_month'].apply(lambda x: 1 if int(x)==7 else 0)
    df['started_august'] = df['release_month'].apply(lambda x: 1 if int(x)==8 else 0)
    df['started_september'] = df['release_month'].apply(lambda x: 1 if int(x)==9 else 0)
    df['started_october'] = df['release_month'].apply(lambda x: 1 if int(x)==10 else 0)
    df['started_november'] = df['release_month'].apply(lambda x: 1 if int(x)==11 else 0)
    df['started_december'] = df['release_month'].apply(lambda x: 1 if int(x)==12 else 0)
    df['first_year'] = df['release_date'].apply(lambda x: int(x.strftime('%Y')))
    df['started_on_first'] = df['release_monthday'].dropna().apply(lambda x: 1 if x==1 else 0)

def parse_runtime(df):
    df['runtime'].fillna(value=0, inplace=True)
    df['half_hour'] = df['runtime'].apply(lambda x: 1 if (int(x)<= 30) and (int(x)>= 20) else 0)
    df['full_hour'] = df['runtime'].apply(lambda x: 1 if (int(x)<= 60) and (int(x)>= 40) else 0)

def parse_network(df):
    networks = ['ABC', 'NBC', 'CBS', 'Fox', 'Nickelodeon', 'Cartoon', 'Comedy', 'MTV',
               'HBO', 'Disney', 'WB']
    for i in networks:
        df['from_' + i] = df['network'].apply(lambda x: 1 if i in x else 0)

def define_features(df):
    df2 = df
    df2.drop(['name', 'runtime', 'imdb_id', 'json', 'genres', 'seasons', 'release_date', 'network', 
              'keywords', 'release_month', 'release_weekday'], inplace=True, axis=1)
    return df2

def get_tv_prediction(imdb_id):
    df1 = df_from_api(imdb_id)
    print "queried the api"
    df1['keywords'] = df1['imdb_id'].apply(lambda x: combine_list(scrape_keywords(x)))
    sleep(2)
    df1['network'] = df1['imdb_id'].apply(lambda x: (str(scrape_network(x))))
    sleep(2)
    print "scraped all data"
    parse_keywords(df1)
    parse_network(df1)
    parse_dates(df1)
    parse_genres(df1)
    parse_runtime(df1)
    print "parsed all data"
    name = df1['name'].values[0]
    print "this show is: ", name
    df2 = define_features(df1)
    print "defined features"
    print "loading model"
    model_pickle_path = '/home/pi/mr_tv_robot/gsrf_pickle2.pkl'
    model_unpickle = open(model_pickle_path, 'rb')
    rf_model= pickle.load(model_unpickle)
    print "loaded model"
    predict_proba = str(rf_model.predict_proba(df2)[0][0]*100)[0:5] + '%'
    print "prediction is: ", predict_proba, " renewal"
    print "model ran successfully"
    return [name, predict_proba]
    print "returned predictions"


## twitter bot

old_tweets = []
while True:
#for i in [1]:
    print "starting new cycle"
    tweets = tweepy.Cursor(api.search,q='@mr_tv_robot').items(15)
    for tweet in tweets:
        imdbid = (tweet.text).split(' ')[1]
        sn = tweet.user.screen_name
        full_tweet = sn + tweet.text
        if full_tweet in old_tweets:
            print 'skipping old tweet'
        else:
            print "Tweet: ", tweet.text 
            try:
                print "getting predictions"
                predictions = get_tv_prediction(imdbid)
                print "predictions: ", predictions
                new_tweet = ".@%s Beep-boop. The model predicts that '%s' has a %s chance of being renewed." %(sn, predictions[0], predictions[1])
                print "ready to tweet: ", new_tweet
                try:
                    api.update_status(new_tweet, sn)
                    print "successfully tweeted"
                    old_tweets.append(full_tweet)
                    print "old tweets updated"
                except:
                    print "twitter won't let me post this"
                    old_tweets.append(full_tweet)
                    print "old tweets updated"
            except:
                print "invalid tweet"
                try:
                    error_tweet = "@%s Sorry, I couldn't figure out '%s'" %(sn, imdbid)
                    api.update_status(error_tweet, sn)
                    old_tweets.append(full_tweet)
                    print "old tweets updated"
                except:
                    print "twitter won't let me post an error tweet"
                    old_tweets.append(full_tweet)
                    print "old tweets updated"
    print "Sleeping for 15 minutes"
    sleep(600)
    print "Sleeping for 5 minutes"
    sleep(60)
    print "4 more minutes until new cycle"
    sleep(60)
    print "3 more minutes until new cycle"
    sleep(60)
    print "2 more minutes until new cycle"
    sleep(30)
    print "1 more minute until new cycle"
    sleep(30)
    print "30 more seconds..."
    sleep(30)


