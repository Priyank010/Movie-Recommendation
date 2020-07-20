from flask import Flask, request, render_template
import pandas as pd

app = Flask(__name__)
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():
    '''
    For rendering results on HTML GUI
    '''
    columns_name = ['user_id','item_id','ratings','timestamp']

    df = pd.read_csv('u.data',sep = '\t',names = columns_name)
    movie_titles = pd.read_csv('Movie_Id_Titles')

    df = pd.merge(df,movie_titles,on='item_id')
    ratings = pd.DataFrame(df.groupby('title')['ratings'].mean())
    ratings['number_of_ratings'] = pd.DataFrame(df.groupby('title')['ratings'].count())
    moviemat = df.pivot_table(index='user_id',columns='title',values='ratings')
   # a = 'Star Wars (1977)'
    a = request.form.get("movie")
    #a = request.form.values()
    user_ratings = moviemat[a]
    similar_to = moviemat.corrwith(user_ratings)
    corr_movie = pd.DataFrame(similar_to,columns = ['Correlation'])
    corr_movie.dropna(inplace=True)
    corr_movie = corr_movie.join(ratings['number_of_ratings'])
    corr = corr_movie[corr_movie['number_of_ratings']>100].sort_values('Correlation',ascending = False).head(5)
   

    return render_template('index.html',output = corr)

if __name__ == "__main__":
    app.run(debug=True)
