# Movie-Recommendation
Python movie recommendation programs. 


Directory Description:
1. Data preparation
3 scraper scripts:
(1) scrape_top_1000.py: this file is used to scrape the top 1000 movie from websites, and get the movie’s name.
(2) scrap_movies_reviews.py:this file is used to scrape 25 reviews per movie from the 1000 movies scraped and get the movie’s reviews.
(3) reviews_data_work.py: this file is used to process the review data, including token and get label.


2. dataset:
(1) top1000_ids.csv: this csv file includes 1000 movies id from the website.
(2) movie_info.csv: this file contains all the information about each movie, such as “title”,
“year”, “rated”, “released”, “runtime”.
(3) id_review2.csv:thisfilehasmovieidandmovie’sreview.
(4) id_cleaned_reviews.csv: this is the processed dataset, includes index, movie id and the
tokens.
(5) movie_score.csv: this file is a movie score based on the eight different features.
(4)Document: 1 tasklist

3. programs
This system contains three different recommendation algorithms, each of them is a python file.
(1) If you want to use it in terminal, you can setup a new terminal window, and then enter the “python_file”, after that you input “python <script name>” respectively in the terminal, press “enter” to run scripts
If you want to run it in the IDE, such as Pycharm, you need to establish a new project, then import these files into this project.
(2)when you run “recommendation.py”, you can input a movie’s name, and the system will return you 10 movies back.
(3)when you run “customizedSearch.py”, you need to input number according to prompts to select movie genres and movie features, and system will list 10 movies with highest score.
(4)When you run “featureFilter.py”, you need to input one or more movies’ titles, then system will firstly calculate a mean score of your inputs. Finally return you 10 movies.
