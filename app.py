import streamlit as st
import pandas as pd
import plotly.express as px
from collections import Counter
import re

# Set Streamlit wide mode
st.set_page_config(layout="wide")

# Load data
uploaded_file = "review_new.csv"
df = pd.read_csv(uploaded_file, encoding='ISO-8859-1')

# Placeholder translation function
def translate_to_english(text):
    # This is a placeholder. Replace with an actual translation API if needed.
    return text

# Prepare data
# Translate reviews to English
df['Review'] = df['Review'].fillna('').apply(translate_to_english)

# Add quarter column based on Review Date
df['Review Date'] = pd.to_datetime(df['Review Date'], errors='coerce')
df['Quarter'] = df['Review Date'].dt.to_period('Q')

# Header
st.title("Review Hotel Dashboard")

# Chart 1: Table of top 10 frequent words in the "Review" column
st.subheader("Top 10 Frequent Words in Reviews")

# Extract and count words from the "Review" column
reviews_text = ' '.join(df['Review'].dropna())
words = re.findall(r'\b\w+\b', reviews_text.lower())
word_counts = Counter(words)
top_words = word_counts.most_common(10)

# Create a DataFrame for display
top_words_df = pd.DataFrame(top_words, columns=['Word', 'Frequency'])

# Display table in Streamlit
st.table(top_words_df)

# Add further charts or analysis as needed

# Example: Display data summary
st.subheader("Data Summary")
st.write(df.describe())
