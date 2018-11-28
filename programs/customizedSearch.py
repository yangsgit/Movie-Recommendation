import pandas as pd
from nltk import sent_tokenize
from nltk.corpus import wordnet as wn
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import operator

id_reviews = "/Users/yangli/Desktop/Data_in_csv/id_review2.csv"
movie_info = "/Users/yangli/Desktop/Data_in_csv/movie_info.csv"

key_words = {'plot': ['plot', 'scenario', 'story', 'script', 'tale'],
             'actor': ['perform', 'act', 'acting', 'actor', 'performance'],
             'vision': ['shot', 'frames', 'picture', 'visual', 'vision', 'photography'],
             'music': ['music', 'song', 'sound', 'background'],
             'love': ['love', 'romance', 'music', 'lover', 'romantic', 'song']}


genres_global = ['Action', 'Adventure', 'Animation', 'Biography', 'Comedy', 'Crime', 'Drama', 'Family', 'Fantasy', 'Film-Noir', 'History', 'Horror', 'Music', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Sport', 'Thriller', 'War', 'Western']


def find_synsets(input):
    for synset in wn.synsets(input):
        print(synset.name())
        print(synset.lemma_names())


def get_genres(df_movie_info):
    genres = df_movie_info['Genre']
    list_genres = []
    for row in genres:
        rows = row.split(", ")
        list_genres += rows
    list_genres = set(list_genres)
    print(list_genres)


def load_data():
    df_id_reviews = pd.read_csv(id_reviews, header=0)
    df_movie_info = pd.read_csv(movie_info, header=0)
    return df_id_reviews, df_movie_info


"""
input: df : movie_info,  list : genres
output: list : id
"""


def select_genre(df_movie_info, genres):
    dict_genre = {}
    for idx, genre in enumerate(genres):
        dict_genre[idx] = genre
    print(str(dict_genre))
    print("Please select genre by index, each input is separated by space: ")
    input_genre = input()
    selected_genre = []
    for index in input_genre.split():
        selected_genre.append(dict_genre.get(int(index)))

    list_index = []
    for idx, row in df_movie_info.iterrows():
        count = 0
        for i in range(len(selected_genre)):
            if selected_genre[i] in row['Genre']:
                count += 1
            if len(selected_genre) == count:
                list_index.append(idx)
    return list_index


"""
input : df : {id, reivews}, dic : key words
return : list of (id, score) sorted by polarity_score
"""
def score_all_movie_by_keys(df, dimensions):
    id_score = {}
    keys = dimensions
    for _, row in df.iterrows():
        review = row['reviews']
        movie_score = score_movie_by_keys(review, keys)
        id_score[row['movie_id']] = movie_score
    sorted_id_score = [(key, id_score[key]) for key in sorted(id_score, key=id_score.get, reverse=True)]
    return sorted_id_score


"""
input: review for one movie, and keys needed to score on
output: score sum of this movie
"""
def score_movie_by_keys(review, keys):
    sentences = sent_tokenize(review)
    sid = SentimentIntensityAnalyzer()
    cents_contains_key = []
    all_score = 0
    for sentence in sentences:
        for key in keys:
            if key in sentence:
                cents_contains_key.append(sentence)

    for text in cents_contains_key:
        ss = sid.polarity_scores(text)
        all_score += ss['compound']
    return all_score

def select_dimension():
    dimensions = {}
    for index, key in enumerate(key_words.keys()):
        dimensions[index] = key
    print(dimensions)
    print("Please select one key word by index:")
    input_index = input()
    selected_dimension = []
    input_index = input_index.split()
    for idx in input_index:
        key = dimensions.get(int(idx))
        selected_dimension = selected_dimension + key_words[key]
    return selected_dimension

if __name__ == '__main__':
    df_id_reviews, df_movie_info = load_data()
    repeat = '1'
    while repeat == '1':
        list_id = select_genre(df_movie_info, genres_global)
        print("Got ", len(list_id), "results")
        sub_id_reviews = df_id_reviews.iloc[list_id, ]
        selected_dimension = select_dimension()
        list_id_score = score_all_movie_by_keys(sub_id_reviews, selected_dimension)
        list_id_score = list_id_score[0:20]
        for id_score in list_id_score:
            row = df_movie_info[df_movie_info['imdbID'] == id_score[0]]
            print("movie :", row['Title'].item(), "score :", id_score[1])
        print("\nInput 1 to continue 0 to quit: ")
        repeat = input()

