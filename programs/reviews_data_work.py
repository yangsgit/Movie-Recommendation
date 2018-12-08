import pandas as pd
import nltk
from nltk.corpus import wordnet
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer


id_reviews_file = "/Users/yangli/Desktop/660_project/id_review2.csv"
id_cleaned_reviews_file = "/Users/yangli/Desktop/660_project/id_cleaned_reviews.csv"
stop_words = stopwords.words('english')

def handle_data():
    data = pd.read_csv(id_cleaned_reviews_file, header=0)
    print(data.head())
    new_reviews(data)



def new_reviews(data):
    reviews = data['reviews']
    reviews_token = []
    i = 0
    for text in reviews[0:10]:
        i += 1
        print(i)
        print(text)
        tokens = tokenize(text)
        print(tokens)
        reviews_token.append(tokens)
    data['reviews_token'] = reviews_token
    data.to_csv(id_cleaned_reviews_file, sep='\t')


def tokenize(text):
    stop_words = stopwords.words('english')
    pattern = r'[a-zA-Z][a-zA-Z0-9]*[a-zA-Z]'
    tokens = nltk.regexp_tokenize(text.lower(), pattern)
    wordnet_lemmatizer = WordNetLemmatizer()
    tagged_tokens = nltk.pos_tag(tokens)
    tokens = [wordnet_lemmatizer.lemmatize(word, get_wordnet_pos(tag)) for (word, tag) in tagged_tokens]
    tokens = [token for token in tokens if token not in stop_words]
    text = ' '.join(tokens)
    return text


def get_wordnet_pos(pos_tag):
    # if pos tag starts with 'J'
    if pos_tag.startswith('J'):
        # return wordnet tag "ADJ"
        return wordnet.ADJ

    # if pos tag starts with 'V'
    elif pos_tag.startswith('V'):
        # return wordnet tag "VERB"
        return wordnet.VERB

    # if pos tag starts with 'N'
    elif pos_tag.startswith('N'):
        # return wordnet tag "NOUN"
        return wordnet.NOUN

    elif pos_tag.startswith('R'):
        return wordnet.ADV
    else:
        # be default, return wordnet tag "NOUN"
        return wordnet.NOUN


