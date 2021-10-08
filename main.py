import tweepy
import csv
import re
import nltk
import pandas as pd
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
#nltk.download('vader_lexicon')

stopWords = set(stopwords.words('english'))
clearTweets = []

mykeys = open('twitterkeys.txt', 'r').read().splitlines()

api_key = mykeys[0]
api_key_secret = mykeys[1]
access_token = mykeys[2]
access_token_secret = mykeys[3]

auth_handler = tweepy.OAuthHandler(consumer_key=api_key, consumer_secret=api_key_secret)
auth_handler.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth_handler, wait_on_rate_limit=True)

search_term = 'navalny putin'
tweet_amount = 50

#csvFile = open('navalny_final.csv', 'a')
#csvWriter = csv.writer(csvFile)

arr = []
tweet_list = []
counter = 0
cc = 0

for tweets in tweepy.Cursor(api.search, q=search_term, tweet_mode='extended', lang='en').items(tweet_amount):
    if 'retweeted_status' in dir(tweets):
        tweet = tweets.retweeted_status.full_text
        cc += 1
    else:
        print(tweets.full_text)
        arr = [tweets.full_text]
        tweet_list.append(arr)
        counter += 1
        #print(arr)
        #csvWriter.writerow([tweets.full_text.encode('utf_8')])
#print(mas)
print(counter)
print(cc)
wordsInTweet = []

for row in tweet_list:
    wordsInTweet.append( ''.join(row).split())

for wordlist in wordsInTweet:
    wordlistFiltered = []
#   print(wordlist)
    for word in wordlist:
        if word not in stopWords:
            word = re.sub(r"[#@ð,.?“:].*" "|[0-9]*" "|http.*" "|www.*" r"|\\.*\\.*" "|/.*/.*", "", word)
            if word != '':
                wordlistFiltered.append(word)
                   #print(word)
    if wordlistFiltered:
        clearTweets.append(wordlistFiltered)

print(clearTweets)



df = pd.DataFrame.from_dict(clearTweets)
df.head(10)

Politic_review = []
analyzer = SIA()
positive = 0
neutral = 0
negative = 0
compound = 0
for phrase in clearTweets:
    tweetString=""
    for word in phrase:
         tweetString += word+" "
    sa = analyzer.polarity_scores(tweetString)
    print(tweetString, sa)
    # Politic_review.append(sa)
    com = analyzer.polarity_scores(tweetString)["compound"]
    pos = analyzer.polarity_scores(tweetString)["pos"]
    neu = analyzer.polarity_scores(tweetString)["neu"]
    neg = analyzer.polarity_scores(tweetString)["neg"]
    Politic_review.append({"Compound": com,
                   "Positive": pos,
                   "Negative": neg,
                   "Neutral": neu
                   })
    if neu != 1.000:
        positive = positive+pos
        neutral = neutral + neu
        negative = negative + neg
        compound = compound + com

sentiments_score = pd.DataFrame.from_dict(Politic_review)
df = df.join(sentiments_score)
df.head()
print(positive, neutral, negative, compound)

df = pd.DataFrame({'polarity': ['positive', 'neutral', 'negative','compound' ], 'value': [positive, neutral, negative, compound]})
colors = ['#1b9e77', '#6890F0', '#fdaa48','#A890F0']
df.plot.bar(x='polarity', y='value', color=colors);
plt.show()