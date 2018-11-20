from bs4 import BeautifulSoup
import requests
import pandas as pd
import json
import csv

t1000_url = "https://www.imdb.com/search/title?groups=top_1000&view=simple&sort=user_rating,asc&start={}&ref_=adv_nxt"
t1000_file = "/Users/yangli/Desktop/top1000_ids.csv"
omdb_api = "http://www.omdbapi.com/?apikey=9e1c784d&plot=full&i={}"
key = "29123d68"
csvfile = '/Users/yangli/Desktop/movie_info.csv'


def scrape_t1000_movie_name():
    top1000_names = []

    for i in range(0, 20):
        url_one_page = t1000_url.format(i * 50 + 1)
        select_50movies_name(top1000_names, url_one_page)
    mypd = pd.DataFrame(top1000_names)
    mypd.to_csv(t1000_file)


def scrape_t1000_movie_info():
    data = pd.read_csv(t1000_file)
    ids = data['0']
    for movie_id in ids:
        valid_url = omdb_api.format(movie_id)
        r = requests.get(valid_url)
        jdata = r.json()
        append_reviews(jdata)


def append_reviews(movie_dict):
    with open(csvfile, 'a') as f:
        writer = csv.DictWriter(f, fieldnames=movie_dict.keys())
        if f.tell() == 0:
            writer.writeheader()
            writer.writerow(movie_dict)
        else:
            writer.writerow(movie_dict)


def select_50movies_name(top1000_names, url_one_page):
    page = requests.get(url_one_page)
    soup = BeautifulSoup(page.content, 'html.parser')
    if page.status_code == 200:
        movie_list = soup.select("div.lister-item-image")
        for _, movie in enumerate(movie_list):
            img = movie.find_all('img')
            id = img[0]['data-tconst']
            top1000_names.append(id)


scrape_t1000_movie_info()