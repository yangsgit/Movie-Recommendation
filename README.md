# Movie-Recommendation
Python movie recommendation programs. 


'program directory' has two programs. 
First is recommendation, according the movie you give, it recommends movies you may like. 
The algorithm is calculate cosine-distence of reviews to find closest reviews. Then find closest movies.

Second program is a movie customized search engine.You can search movie based on key words.
Still based on reviews. Firstly, find sentences in reviews containing key words, use vader framework to calculate the polarity score of each word.Then add them up to get total score. Finally, sort each movie by their score to get top related movies.



'Data preparation' directory has several python crawler program, which scrape the data from IMDB website. There is also a 'reviews_data_work.py' preprocessing the review text.

'data set' directory has 4 .csv, which are scraped from IMDB website by program in 'Data preparation'. 
