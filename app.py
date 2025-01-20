import streamlit as st
import pandas as pd
import plotly.express as px
from collections import Counter
import matplotlib.pyplot as plt
import seaborn as sns
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re

# Download NLTK data
nltk.download('punkt')
nltk.download('stopwords')

# Set Streamlit wide mode
st.set_page_config(layout="wide")

# Load data
uploaded_file = 'review_new.csv'
df = pd.read_csv(uploaded_file, encoding='ISO-8859-1')

# Convert "Review Date" to datetime and categorize into quarters
df['Review Date'] = pd.to_datetime(df['Review Date'], errors='coerce')
df['Quarter'] = df['Review Date'].dt.to_period('Q')

# Translate data to English (dummy translation for this example)
def translate_to_english(text):
    # Placeholder for translation logic (e.g., using Google Translate API)
    return text

df['Translated Review'] = df['Review'].apply(lambda x: translate_to_english(str(x)))

# Header
st.title("Hotel Review Dashboard")

# Display raw data
st.subheader("Raw Data")
st.dataframe(df.head())

# Extract and count most frequent words from reviews
stop_words = set(stopwords.words('english'))
def preprocess_text(text):
    text = re.sub(r'[^a-zA-Z\s]', '', text.lower())
    tokens = word_tokenize(text)
    filtered_words = [word for word in tokens if word not in stop_words]
    return filtered_words

all_words = []
for review in df['Translated Review'].dropna():
    all_words.extend(preprocess_text(review))

word_counts = Counter(all_words)
most_common_words = word_counts.most_common(10)

# Create a DataFrame for the top 10 words
top_words_df = pd.DataFrame(most_common_words, columns=['Word', 'Frequency'])

# Display table of the most frequent words
st.subheader("Top 10 Frequent Words")
st.table(top_words_df)

# Chart for the top 10 words
st.subheader("Word Frequency Chart")
fig = px.bar(top_words_df, x='Word', y='Frequency', title='Top 10 Words in Reviews', color='Frequency', color_discrete_sequence=colors)
st.plotly_chart(fig)
