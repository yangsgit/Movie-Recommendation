import pandas as pd
from bs4 import BeautifulSoup
import requests
import csv
import json

key = "29123d68"
url_review_all = "https://www.imdb.com/title/{}/reviews?ref_=tt_urv"
payload = {'apikey': key, 'plot': 'full', 'r': 'json'}
id_review_file = '/Users/yangli/Desktop/id_review.csv'
top1000_ids_file = "/Users/yangli/Desktop/top1000_ids.csv"


def scrape_movie_reviews():
    df = pd.read_csv(top1000_ids_file)
    id_list = df['0']
    for id in id_list:
        id_reviews_dict = {'movie_id': id, 'reviews': ""}
        url_review_one = url_review_all.format(id)
        page = requests.get(url_review_one)
        soup = BeautifulSoup(page.content, 'html.parser')
        review_list = soup.select('div.text.show-more__control')
        for review in review_list:
            text = review.contents[0]
            if isinstance(text, str):
                id_reviews_dict['reviews'] = id_reviews_dict['reviews'] + text
        print(len(id_reviews_dict['reviews']))
        print(id_reviews_dict['movie_id'])
        print(id_reviews_dict['reviews'])
        append_reviews(id_reviews_dict)


def append_reviews(id_reviews_dict):
    with open(id_review_file, 'a') as f:
        writer = csv.DictWriter(f, fieldnames=['movie_id', 'reviews'])
        if f.tell() == 0:
            writer.writeheader()
            writer.writerow(id_reviews_dict)
        else:
            writer.writerow(id_reviews_dict)




