import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import sys
from flask import Flask, request, render_template
app = Flask(__name__)


@app.route('/')
def my_form():
    print("hello guys in myform");
    return render_template('frontendhtml.html')

@app.route('/', methods=['GET','POST'])
def my_form_post():
  print("hello guys")

  df = pd.read_csv("movie_dataset.txt")

  features = ['keywords','cast','genres','director']

  def combine_features(row):
      return row['keywords'] +" "+row['cast']+" "+row["genres"]+" "+row["director"]

  for feature in features:
      df[feature] = df[feature].fillna('')
  df["combined_features"] = df.apply(combine_features,axis=1)

  cv = CountVectorizer()
  count_matrix = cv.fit_transform(df["combined_features"])

  cosine_sim = cosine_similarity(count_matrix)

  def get_title_from_index(index):
      return df[df.index == index]["title"].values[0]
  def get_index_from_title(title):
      return df[df.title == title]["index"].values[0]

  # movie_user_likes = input("Enter the Movie for further recommendations\n")
  movie_user_likes = request.form.get('userinput')
  print("user movie " + movie_user_likes)
  movie_index = get_index_from_title(movie_user_likes)
  similar_movies = list(enumerate(cosine_sim[movie_index]))

  sorted_similar_movies = sorted(similar_movies,key=lambda x:x[1],reverse=True)[1:]

  i=0
  arr = []
  print("Top 5 similar movies to "+movie_user_likes+" are:\n")
  for element in sorted_similar_movies:
      print(get_title_from_index(element[0]))
      arr.append(get_title_from_index(element[0]))
      i=i+1
      if i>=5:
          break
    # variable = request.form.get['variable']
    # return "Your name is "+variable
    # return render_template("form.html")
  return render_template("form.html", result = arr)

if __name__ == "__main__":
    app.run()