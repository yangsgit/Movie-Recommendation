from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
from sklearn.metrics.pairwise import linear_kernel
import requests
from bs4 import BeautifulSoup
from reviews_data_work import tokenize

id_cleaned_reviews_file = "/Users/yangli/Desktop/Data_in_csv/id_cleaned_reviews.csv"
movie_info_file = "/Users/yangli/Desktop/Data_in_csv/movie_info.csv"


url_review_all = "https://www.imdb.com/title/{}/reviews?ref_=tt_urv"
omdb_api = "http://www.omdbapi.com/?apikey=9e1c784d&plot=full&t={}"


def find_seed_movie_review(input_movie):
    omdb_url = omdb_api.format(input_movie)
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

    print("tokenizing reviews...")
    id_reviews_dict['reviews'] = tokenize(id_reviews_dict['reviews'])
    return id_reviews_dict


def get_reviews_dtm():
    id_reviews_df = pd.read_csv(id_cleaned_reviews_file, header=0)
    reviews_tokens = id_reviews_df['reviews_token']
    tfidf_vect = TfidfVectorizer(stop_words="english")
    dtm = tfidf_vect.fit_transform(reviews_tokens)
    return dtm, tfidf_vect


def find_top10_recommendation(reviews_dtm, tfidf_vect, id_reviews_dict):
    input_reviews = id_reviews_dict['reviews']
    input_vector = tfidf_vect.transform([input_reviews])
    cosine_similarity = linear_kernel(input_vector, reviews_dtm).flatten()
    indexs = sorted(range(len(cosine_similarity)), key=lambda i: cosine_similarity[i])[-21:]
    return indexs


def get_top10_titles(indexs):
    print("\nTop 10 movies recommended: ")
    idx = 0
    for index in reversed(indexs):
        if movie_titles[index] == id_reviews_dict['movie_title']:
            continue
        if idx >= 20:
            break
        idx += 1
        print("\n", idx, ":  " + movie_titles[index])


if __name__ == '__main__':
    movie_info = pd.read_csv(movie_info_file, header=0)
    movie_titles = movie_info['Title']
    repeat = 1
    reviews_dtm = None
    tfidf_vect = None
    while repeat == 1:
        print("Enter movie name as seed (or enter 0 to quit): ")
        original_name = input()
        if original_name == '0':
            break
        id_reviews_dict = find_seed_movie_review(original_name)
        if id_reviews_dict is None:
            print("Can not find movie.")
            continue
        if reviews_dtm is None:
            reviews_dtm, tfidf_vect = get_reviews_dtm()
        indexs = find_top10_recommendation(reviews_dtm, tfidf_vect, id_reviews_dict)
        get_top10_titles(indexs)

