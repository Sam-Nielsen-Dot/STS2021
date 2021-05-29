from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import twitter_samples, stopwords
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize
from nltk import FreqDist, classify, NaiveBayesClassifier
import pickle
from nltk.tokenize import word_tokenize
import csv

import re, string, random

def remove_noise(tweet_tokens, stop_words = ()):

    cleaned_tokens = []

    for token, tag in pos_tag(tweet_tokens):
        token = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|'\
                       '(?:%[0-9a-fA-F][0-9a-fA-F]))+','', token)
        token = re.sub("(@[A-Za-z0-9_]+)","", token)

        if tag.startswith("NN"):
            pos = 'n'
        elif tag.startswith('VB'):
            pos = 'v'
        else:
            pos = 'a'

        lemmatizer = WordNetLemmatizer()
        token = lemmatizer.lemmatize(token, pos)

        if len(token) > 0 and token not in string.punctuation and token.lower() not in stop_words:
            cleaned_tokens.append(token.lower())
    return cleaned_tokens

def get_all_words(cleaned_tokens_list):
    for tokens in cleaned_tokens_list:
        for token in tokens:
            yield token

def get_tweets_for_model(cleaned_tokens_list):
    for tweet_tokens in cleaned_tokens_list:
        yield dict([token, True] for token in tweet_tokens)

def load_model(id):
    #positive = depression
    #negative = no depression
    stop_words = stopwords.words('english')

    positive_tweet_tokens = []
    negative_tweet_tokens = []
    input_file = csv.DictReader(open(f"Datasets\\training_datasets\\{id}.csv", encoding="utf-8"))
    for row in input_file:
        if row["depressed"] == '1':
            positive_tweet_tokens.append(word_tokenize(row["text"]))
        else:
            negative_tweet_tokens.append(word_tokenize(row["text"]))

    #positive_tweet_tokens = twitter_samples.tokenized('positive_tweets.json')
    #negative_tweet_tokens = twitter_samples.tokenized('negative_tweets.json')

    positive_cleaned_tokens_list = []
    negative_cleaned_tokens_list = []

    for tokens in positive_tweet_tokens:
        positive_cleaned_tokens_list.append(remove_noise(tokens, stop_words))

    for tokens in negative_tweet_tokens:
        negative_cleaned_tokens_list.append(remove_noise(tokens, stop_words))

    all_pos_words = get_all_words(positive_cleaned_tokens_list)

    freq_dist_pos = FreqDist(all_pos_words)
    print(freq_dist_pos.most_common(10))

    positive_tokens_for_model = get_tweets_for_model(positive_cleaned_tokens_list)
    negative_tokens_for_model = get_tweets_for_model(negative_cleaned_tokens_list)

    positive_dataset = [(tweet_dict, "Positive")
                         for tweet_dict in positive_tokens_for_model]

    negative_dataset = [(tweet_dict, "Negative")
                         for tweet_dict in negative_tokens_for_model]

    dataset = positive_dataset + negative_dataset

    random.shuffle(dataset)


    switch_point = int(len(dataset) * 0.8)
    train_data = dataset[:switch_point]
    test_data = dataset[switch_point:]

    classifier = NaiveBayesClassifier.train(train_data)

    f = open(f"Models\\{id}.pickle", 'wb')
    pickle.dump(classifier, f)
    f.close()

    accuracy = classify.accuracy(classifier, test_data)

    print(accuracy)
    r = csv.reader(open('Datasets\\results.csv')) # Here your csv file
    lines = list(r)

    lines[i+1][7] = accuracy

    writer = csv.writer(open('Datasets\\results.csv', 'w', newline=""))
    writer.writerows(lines)

    

    print(classifier.show_most_informative_features(10))

#load_model(0)
if __name__ == "__main__":
    for i in range(0, 95):
        load_model(i)