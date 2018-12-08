from gensim.models import word2vec
import logging
import pandas as pd
import nltk, string
from nltk import sent_tokenize
import requests
from bs4 import BeautifulSoup
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from sklearn.metrics.pairwise import linear_kernel


omdb_api = "http://www.omdbapi.com/?apikey=9e1c784d&plot=full&t={}"
url_review_all = "https://www.imdb.com/title/{}/reviews?ref_=tt_urv"

id_reviews = "../Data_in_csv/id_review2.csv"
movie_info = "../Data_in_csv/movie_info.csv"
movies_score = "../Data_in_csv/movie_score.csv"
key_words = {'plot': ['plot', 'scenario', 'script', 'scriptwriter', 'screenplay', 'Writing'],
             'actor': ['perform', 'performance','actor','actress', 'role'],
             'vision': ['shot', 'frames', 'picture', 'visual', 'vision', 'photography', 'cinematography', 'scenery'],
             'music': ['music', 'musical', 'song', 'sound', 'background', 'soundtrack'],
             'design': ['costume', 'makeup', 'make up', 'clothes']
             }

emotinal_key_words = {'plot':  ['plot', 'scenario', 'script', 'scriptwriter', 'screenplay', 'Writing'],
                      'actor': ['actor','actress'],
                      'vision': ['shot', 'frames', 'picture', 'visual', 'vision', 'photography', 'cinematography', 'scenery'],
                      'music': ['music', 'musical', 'song', 'sound', 'background', 'soundtrack'],
                      'design': ['costume', 'makeup', 'make up', 'clothes'],
                      'thrill': ['horr', 'thrill', 'scary', 'scared', 'flinch', 'shock'],
                      'touched': ['romantic', 'cry', 'warm', 'touched', 'moved','tears'],
                      'happy': ['fun', 'humor', 'hilarious']
                      }


def load_data():
    df_id_reviews = pd.read_csv(id_reviews, header=0)
    df_movie_info = pd.read_csv(movie_info, header=0)
    return df_id_reviews, df_movie_info


def find_similar_words(data):
    data.head()
    sentences=[[token.strip(string.punctuation).strip() for token in nltk.word_tokenize(doc.lower())
                if token not in string.punctuation and len(token.strip(string.punctuation).strip()) >= 2]
               for doc in data['reviews']]
    print(sentences[0:2])
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    wv_model = word2vec.Word2Vec(sentences, min_count=5, size=200, window=10, workers=4)
    return wv_model


"""
input:  dataframe df_id_reviews
output: output df_id_reviews to .csv file
"""
def score_all_movie_by_keys(df_id_reivews):
    id_score_rows = []
    for _, row in df_id_reivews.iterrows():
        review = row['reviews']
        movie_score = score_movie_by_keys(review)
        movie_score['movie_id'] = row['movie_id']
        id_score_rows.append(movie_score)
    df_movie_score = pd.DataFrame(id_score_rows)
    df_movie_score = df_movie_score[['movie_id', 'actor', 'design', 'happy', 'music', 'plot', 'thrill', 'touched', 'vision']]
    df_movie_score.to_csv(movies_score2)

"""
input: review for one movie
output: dict  score sum of this movie
"""
def score_movie_by_keys(review):
    sentences = sent_tokenize(review)
    sid = SentimentIntensityAnalyzer()
    keyword_score = {'plot': 0,'actor': 0,'vision': 0,'music': 0,'design': 0,'thrill': 0,'touched': 0,'happy': 0}
    for key in keyword_score.keys():
        for sentence in sentences:
            for word in emotinal_key_words[key]:
                if word in sentence:
                    ss = sid.polarity_scores(sentence)
                    keyword_score[key] += ss['compound']
            keyword_score[key] = float("{0:.2f}".format(keyword_score[key]))
    return keyword_score



"""
input : list const movies' name
output:  df average score of all dimensions
"""
def score_new_movies(movie_titles):
    list_dict_dimension_score = []
    for movie_title in movie_titles:
        # 1 get the dict_id_reviews
        dict_id_reviews = find_seed_movie_reivew(movie_title)
        # 2 get the dict_dimension_score
        if dict_id_reviews is not None:
            dict_dimension_score = score_movie_by_keys(dict_id_reviews['reviews'])
            list_dict_dimension_score.append(dict_dimension_score)
    if len(list_dict_dimension_score) is 0:
        return None
    df_dimension_score = pd.DataFrame(list_dict_dimension_score)
    list_average_score = df_dimension_score.mean(axis=0)
    df_average_score = pd.DataFrame(list_average_score).transpose()
    print(df_average_score)
    return df_average_score

def find_seed_movie_reivew(movie_title):
    omdb_url = omdb_api.format(movie_title)
    r = requests.get(omdb_url)

    print("Finding movie...")
    if r.status_code is not 200:
        print("Can not find this movie, please check the movie name")
        return
    jdata = r.json()
    if jdata['Response'] == 'False':
        return
    movie_id = jdata['imdbID']
    movie_title = jdata['Title']
    print("Name :" + movie_title , "ID :" + movie_id)
    id_reviews_dict = {'movie_id': movie_id, 'movie_title':movie_title, 'reviews': ""}
    url_review_one = url_review_all.format(movie_id)

    print("Finding movie reviews...")
    page = requests.get(url_review_one)
    soup = BeautifulSoup(page.content, 'html.parser')
    review_list = soup.select('div.text.show-more__control')
    for review in review_list:
        text = review.contents[0]
        if isinstance(text, str):
            id_reviews_dict['reviews'] = id_reviews_dict['reviews'] + text
    return id_reviews_dict


if __name__ == '__main__':
    df_id_reviews, df_movie_info = load_data()
    df_movie_score = pd.read_csv(movies_score, header=0)
    df_movie_score = df_movie_score[['actor','design','happy','music','plot','thrill','touched','vision']]
    repeat = '1'
    while repeat == '1':
        print("\nplease input movies names, each name splited by ',':")
        string_seed_words = input()
        list_seed_words = string_seed_words.strip().split(",")
        df_average_score = score_new_movies(list_seed_words)
        cosine_similarity = linear_kernel(df_average_score, df_movie_score).flatten()
        indexs = sorted(range(len(cosine_similarity)), key=lambda i: cosine_similarity[i])[-20:]
        indexs = list(reversed(indexs))
        print(df_movie_info.iloc[indexs, 1])
        print("input 1 to continue or 0 to quit")
        repeat = input()


