import numpy as np
import pandas as pd
import nltk
import re
import string
import tkinter as tk
from tkinter import font
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from fuzzywuzzy import process

# Load dataset
data = pd.read_csv("netflixData.csv")
data = data[["Title", "Description", "Content Type", "Genres"]].dropna()

# Define a custom text cleaning function
def clean_text(text):
    text = str(text).lower().strip()
    text = re.sub(r"https?://\S+|www\.\S+", "", text)  # Remove URLs
    text = re.sub(r"<.*?>+", "", text)  # Remove HTML tags
    text = re.sub(r"\n", " ", text)  # Remove new lines
    text = re.sub(r"[^a-zA-Z0-9#& ]", "", text)  # Keep letters, numbers, # and &
    return text

# Apply text cleaning
data["Cleaned_Title"] = data["Title"].apply(clean_text)

# Compute TF-IDF and similarity matrix
tfidf_matrix = TfidfVectorizer(stop_words="english").fit_transform(data["Genres"])
similarity = cosine_similarity(tfidf_matrix)

# Create a lookup table for cleaned titles
indices = pd.Series(data.index, index=data["Cleaned_Title"]).drop_duplicates()

def get_closest_title(title):
    cleaned_title = clean_text(title)
    closest_match = process.extractOne(cleaned_title, data["Cleaned_Title"].tolist())
    return closest_match[0] if closest_match else None

def netFlix_recommendation(title):
    title = get_closest_title(title)
    print("Closest Match Found:", title)  # Debugging line
    if not title:
        return "Movie not found"
    
    index = indices.get(title, None)
    print("Index in dataset:", index)  # Debugging line
    if index is None:
        return "Title not found in the dataset."
    
    similarity_scores = list(enumerate(similarity[index]))
    similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
    similarity_scores = similarity_scores[1:11]  # Exclude itself
    movie_indices = [i[0] for i in similarity_scores]

    return data["Title"].iloc[movie_indices]

    
    return data["Title"].iloc[movie_indices]

# GUI with Tkinter
def recommend_movie():
    title = e1.get()
    result = netFlix_recommendation(title)
    if isinstance(result, str):
        result_label.config(text=result)
    else:
        result_label.config(text='\n'.join(result))

master = tk.Tk()
master.geometry('520x520') 
master.configure(bg='white')  

tk.Label(master, text="Enter a movie title 🎬", bg='#f0f0f0', fg='black').grid(row=0, column=0, columnspan=2)

e1 = tk.Entry(master)
e1.grid(row=1, column=0, columnspan=2)

button = tk.Button(master, text='Recommend 🍿', command=recommend_movie, bg='#d3d3d3', fg='black')
button.grid(row=2, column=0, columnspan=2)

result_label = tk.Label(master, text="", bg='#f0f0f0', fg='black', justify='left')
result_label.grid(row=3, column=0, columnspan=2)

bold_font = font.Font(weight="bold")
result_label['font'] = bold_font

master.mainloop()