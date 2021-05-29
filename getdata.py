import requests
import pandas as pd
import os
import csv

def make_request(query):
    bearer_token = os.environ.get('BEARER_TOKEN')
    headers = {"Authorization": "Bearer {}".format(bearer_token)}

    url = "https://api.twitter.com/2/tweets/search/recent?query=from:TwitterDev"
    response = requests.request("GET", url, headers=headers).json()

    df = pd.DataFrame(response['data'])
    df.to_csv('response_python.csv')

#parameters for each dataset

#depression set
key_words = [
    ["depression", "suicide", "mental illness", "severe anxiety", "depression medication"],
    ["sad", "unhappy", "stressed", "anxious", "miserable"],
    ["anciety", "stress", "despondent", "suicidal", "depressed"],
    ["dog", "president", "child", "nostalgic", "marvel"]
]

query_type = ["hashtag", "plain text"]

#not depressed set

not_depressed_set_type = ["random", "positive"]

#for these use nltk provided random or positive tweet datasets

#apply these filters after the data has been obtained

#only use results with a verified negative sentiment using the pretrained sentiment analysis model
negative_sentiment_filter = [True, False]

#only use results with personal pronouns in them (me, I, we, him, her, us)
personal_pronouns = [True, False]


#id, key_words, query_type, not_depressed_set_type, negative_sentiment_filter, personal_pronouns, testing_accuracy, user_accuracy, forum_accuracy
def generate_results():
    id = 0
    with open('Datasets\\results.csv', 'a', newline='') as file:
        writer = csv.writer(file)

        for k in range(0, len(key_words)):
            words = key_words[k]
            for qt in query_type:
                #get around 5000 posts using these 2 parameters
                for set_type in not_depressed_set_type:
                    # get the set type here
                    for neg_sent in negative_sentiment_filter:
                        # filter by negative sentiment here
                        for pron in personal_pronouns:
                            # remove posts without personal pronouns
                            writer.writerow([id, k, qt, set_type, neg_sent, pron, 0, 0, 0])
                            id += 1

generate_results()


