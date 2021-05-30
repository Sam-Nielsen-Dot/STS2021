from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import twitter_samples, stopwords
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize
from nltk import FreqDist, classify, NaiveBayesClassifier
import pickle

import re, string, random
import csv

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

def classify(text, classifier):
    

    custom_tokens = remove_noise(word_tokenize(text))

    
    

    #returnStr = classifier.classify(dict([token, True] for token in custom_tokens))
    dist = classifier.prob_classify(dict([token, True] for token in custom_tokens))

    for label in dist.samples():
        #print("%s: %f" % (label, dist.prob(label)))
        if label == "Positive" and dist.prob(label) > 0.95:
            return "Positive"
    return "Negative"


def get_classifier(id):
    f = open(f"Models\\{id}.pickle", 'rb')
    classifier = pickle.load(f)
    f.close()
    return classifier

def train_positive(id):
    classifier = get_classifier(id)
    positive_tweets = twitter_samples.strings('positive_tweets.json')
    total_right = 0
    total_wrong = 0
    for tweet in positive_tweets:
        if classify(tweet, classifier) == "Negative":
            total_right += 1
        else:
            total_wrong += 1
    accuracy = float((total_right/len(positive_tweets)))

    #r = csv.reader(open('Datasets\\results.csv')) # Here your csv file
    #lines = list(r)

    #lines[id+1][8] = accuracy

    #writer = csv.writer(open('Datasets\\results.csv', 'w', newline=""))
    #writer.writerows(lines)

    print(accuracy)

def train_negative(id):
    classifier = get_classifier(id)
    positive_tweets = twitter_samples.strings('negative_tweets.json')
    total_right = 0
    total_wrong = 0
    for tweet in positive_tweets:
        if classify(tweet, classifier) == "Negative":
            total_wrong += 1
        else:
            total_right += 1
    accuracy = float((total_right/len(positive_tweets)))
    r = csv.reader(open('Datasets\\results.csv')) # Here your csv file
    lines = list(r)

    lines[id+1][9] = accuracy

    writer = csv.writer(open('Datasets\\results.csv', 'w', newline=""))
    writer.writerows(lines)

    print(accuracy)

def test_all(text):
    
    for i in range(0, 96):
        classifier = get_classifier(i)
        print(f"{i} - {classify(text, classifier)}")

def test(id):
    classifier = get_classifier(id)
    while True:
        text = input("Text: ")
        print(classify(text, classifier))


def not_depressed_test():
    passed = []
    text_samples = ['i am happy', ' I enjoy life', 'it is so wonderful to be alive']
    for i in range(0, 96):
        classifier = get_classifier(i)
        for text in text_samples:
            add = True
            if classify(text, classifier) == "Positive":
                add = False
        if add:
            passed.append(i)
    return passed

def depressed_test():
    passed = []
    text_samples = ['i hate my life', ' I want to die, going on is too difficult', 'it sucks to be alive, why cant it just end']
    for i in range(0, 96):
        classifier = get_classifier(i)
        for text in text_samples:
            add = True
            if classify(text, classifier) == "Negative":
                add = False
        if add:
            passed.append(i)
    return passed

def reddit_test(id):
    classifier = get_classifier(id)
    total = 0
    with open('Datasets\\testing_datasets\\reddit.csv', mode='r', newline="", encoding="utf-8") as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter="|")
        total_right = 0
        for row in csv_reader:
            total+= 1
            classification = classify(row['text'], classifier)
            if row['depressed'] == '1' and classification == "Positive":
                total_right += 1
            elif row['depressed'] == '0' and classification == "Negative":
                total_right += 1
    return float(total_right/total)

def reddit_test_all():
    toadd = []
    for i in range(0, 95):
        print(i)
        accuracy = reddit_test(i)
        toadd.append(accuracy)
    r = csv.reader(open('Datasets\\results.csv')) # Here your csv file
    lines = list(r)
    
    for i in range(0, 95):
        lines[i+1][10] = toadd[i]

    writer = csv.writer(open('Datasets\\results.csv', 'w', newline=""))
    writer.writerows(lines)
        


            



