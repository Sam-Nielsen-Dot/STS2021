import requests
import pandas as pd
import os
import csv
import twint
from sentiment_analysis.sentiment_utils import classify
import random
from absolang import absolutist, absolutist_index
from nltk.corpus import twitter_samples, stopwords
import pickle

f = open("sentiment_analysis\\sentiment_classifier.pickle", 'rb')
classifier = pickle.load(f)
f.close()

#def make_request(query):
#    bearer_token = os.environ.get('BEARER_TOKEN')
#    headers = {"Authorization": "Bearer {}".format(bearer_token)}

#    url = "https://api.twitter.com/2/tweets/search/recent?query=from:TwitterDev"
#    response = requests.request("GET", url, headers=headers).json()

#    df = pd.DataFrame(response['data'])
#    df.to_csv('response_python.csv')

print("Imports resolved")

def make_request(words, qt):
    print(f"request made for {words}")
    return_list = []
    for word in words:
        if qt == "hashtag":
            word = "#" + word
        #configuration
        config = twint.Config()
        config.Search = word
        config.Lang = "en"
        config.Limit = 1000
        config.Store_object = True
        config.Hide_output = True
        #running search
        twint.run.Search(config)
        tweets = twint.output.tweets_list
        for tweet in tweets:
            return_list.append(tweet.tweet)

    return return_list

#parameters for each dataset

#depression set
key_words = [
    ["depression", "suicide", "mental illness", "severe anxiety", "depression medication"],
    ["sad", "unhappy", "stressed", "anxious", "miserable"],
    ["anxiety", "stress", "despondent", "suicidal", "depressed"]
]

query_type = ["hashtag", "plain text"]

#not depressed set

not_depressed_set_type = ["random", "positive"]

#for these use nltk provided random or positive tweet datasets

#apply these filters after the data has been obtained

#only use results with a verified negative sentiment using the pretrained sentiment analysis model
negative_sentiment_filter = [False, True]

#only use results with personal pronouns in them (me, myself and I)
#http://www.tandfonline.com/doi/abs/10.1080/02699930441000030
personal_pronouns = [False, True]

#randomly dismisss posits without absolutist language at a higher frequency
absolutist_language = [False, True]

#id, key_words, query_type, not_depressed_set_type, negative_sentiment_filter, personal_pronouns, testing_accuracy, user_accuracy, forum_accuracy
def generate_results():
    id = 0
    
    for tab_error in range(0, 1):
        for k in range(0, len(key_words)):
            words = key_words[k]
            for qt in query_type:

                print(qt)
                #get around 5000 posts using these 2 parameters
                depressed_tweets = make_request(words, qt)
                
                for tab_error2 in ["single_list"]:
            
                    for neg_sent in negative_sentiment_filter:
                        print(neg_sent)
                        for pron in personal_pronouns:
                            print(pron)
                            for absolute in absolutist_language:
                                print(absolute)
                                # randomly dismiss posts without absolutist language and without pronouns if applicable
                                to_remove = []
                                for i in range(0, len(depressed_tweets)):
                                    tweet = depressed_tweets[i]
                                    chance = 100
                                    if neg_sent == True and classify(tweet, "sentiment_analysis\\sentiment_classifier.pickle", classifier) != "Negative":
                                        to_remove.append(tweet)
                                    else:
                                        new_tweet = " " + tweet.lower() + " "
                                        if pron == True and " me " not in new_tweet and " i " not in new_tweet and " myself " not in new_tweet:
                                            chance -= 70
                                        try:
                                            if absolute == True and absolutist(tweet) == False:
                                                chance -= 70
                                        except:
                                            chance -= 100
                                        if random.randint(0, 100) > chance:
                                            to_remove.append(tweet)
                                for i in to_remove:
                                    depressed_tweets.remove(i)

                                for set_type in not_depressed_set_type:
                                    # get the set type here
                                    print(set_type)
                                    if set_type == "random":
                                        not_depressed_tweets = twitter_samples.strings('tweets.20150430-223406.json')
                                    else:
                                        not_depressed_tweets = twitter_samples.strings('positive_tweets.json')
                                
                                    f = open(f'Datasets\\training_datasets\\{id}.csv', "w")
                                    with open(f'Datasets\\training_datasets\\{id}.csv', 'w', encoding="utf-8", newline='') as file:
                                            w = csv.writer(file)
                                            w.writerow(["text", "depressed"])
                                            for twitter_post in depressed_tweets:
                                                w.writerow([twitter_post, 1])
                                            for twitter_post in not_depressed_tweets:
                                                w.writerow([twitter_post, 0])

                                    with open('Datasets\\results.csv', 'a', newline='') as file:
                                        writer = csv.writer(file)
                                        writer.writerow([id, k, qt, set_type, neg_sent, pron, absolute, 0, 0, 0])
                                    print(id)
                                    id += 1
                                

generate_results()


