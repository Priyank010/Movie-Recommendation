# Importing the libraries
import numpy as np
import pandas as pd
import pickle
import matplotlib as plt
import seaborn as sns

columns_name = ['user_id','item_id','ratings','timestamp']

df = pd.read_csv('u.data',sep = '\t',names = columns_name)
movie_titles = pd.read_csv('Movie_Id_Titles')

df = pd.merge(df,movie_titles,on='item_id')
ratings = pd.DataFrame(df.groupby('title')['ratings'].mean())
ratings['number_of_ratings'] = pd.DataFrame(df.groupby('title')['ratings'].count())
moviemat = df.pivot_table(index='user_id',columns='title',values='ratings')

user_ratings = moviemat[a]
similar_to = moviemat.corrwith(user_ratings)
corr_movie = pd.DataFrame(similar_to,columns = ['Correlation'])
corr_movie.dropna(inplace=True)
corr_movie = corr_movie.join(ratings['number_of_ratings'])
corr_movie[corr_movie['number_of_ratings']>100].sort_values('Correlation',ascending = False).head(5)

pickle.dump(corr_movie, open('model.pkl','wb'))