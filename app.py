import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Set Streamlit wide mode
st.set_page_config(layout="wide")

# Load data
uploaded_file = "review_new_new.csv"
df = pd.read_csv(uploaded_file, encoding='ISO-8859-1')


# Preprocess data
df['Review Date'] = pd.to_datetime(df['Review Date'], format="%d/%m/%Y")
df['Month'] = df['Review Date'].dt.strftime('%B')
df['Quarter'] = df['Review Date'].dt.to_period('Q').astype(str)
df['Review Group'] = df['Review Site'].apply(lambda x: 'Google' if x == 'Google' else 'OTA')

# Filter options
hotel_filter = st.sidebar.multiselect("Select Hotel(s)", options=df['Hotel'].unique(), default=df['Hotel'].unique())
filtered_data = df[df['Hotel'].isin(hotel_filter)]

# Header
st.title("Review Hotel Dashboard")

# Chart 1: Stacked bar chart
st.header("Review Count by Review Site")
st.markdown("###")
chart1_data = filtered_data.groupby(['Hotel', 'Review Group'])['Review ID'].count().reset_index()
chart1_data.rename(columns={'Review ID': 'Review Count'}, inplace=True)
fig1 = px.bar(chart1_data, x='Hotel', y='Review Count', color='Review Group', text='Review Count',
              title="Stacked Bar Chart: Review Count by Hotel and Review Site",
              labels={'Review Count': 'Count of Reviews'}, barmode='stack', color_discrete_sequence=colors)
st.plotly_chart(fig1, use_container_width=True)

# Chart 2 and 3: Line charts with filters
st.header("Review Trends by Quarter")
chart2_chart3_col1, chart2_chart3_col2 = st.columns(2)

with chart2_chart3_col1:
    st.markdown("### Average Rating by Quarter")
    avg_rating_data = filtered_data.groupby(['Quarter', 'Review Group'])['Rating'].mean().reset_index()
    avg_rating_data['Overall'] = 'All'
    fig2 = px.line(avg_rating_data, x='Quarter', y='Rating', color='Review Group', title="Average Rating by Quarter",
                   markers=True, color_discrete_sequence=colors)
    st.plotly_chart(fig2, use_container_width=True)

with chart2_chart3_col2:
    st.markdown("### Count of Reviews by Quarter")
    count_review_data = filtered_data.groupby(['Quarter', 'Review Group'])['Review ID'].count().reset_index()
    fig3 = px.line(count_review_data, x='Quarter', y='Review ID', color='Review Group',
                   title="Count of Reviews by Quarter", markers=True, color_discrete_sequence=colors)
    st.plotly_chart(fig3, use_container_width=True)

# Chart 4 and 5: Scatter and Diverging bar charts
st.header("Review Comparisons")
chart4_chart5_col1, chart4_chart5_col2 = st.columns(2)

with chart4_chart5_col1:
    st.markdown("### Monthly Review Comparison (Google vs OTA)")
    monthly_ota_google = filtered_data.groupby(['Month', 'Review Group'])['Review ID'].count().reset_index()
    ota_google_pivot = monthly_ota_google.pivot(index='Month', columns='Review Group', values='Review ID').fillna(0).reset_index()
    ota_google_pivot.sort_values(by='Month', inplace=True)
    fig4 = px.scatter(ota_google_pivot, x='OTA', y='Google', text='Month',
                      title="Scatter Chart: OTA vs Google Reviews by Month",
                      labels={'OTA': 'OTA Reviews', 'Google': 'Google Reviews'}, color_discrete_sequence=colors)
    fig4.update_traces(textposition='top center')
    st.plotly_chart(fig4, use_container_width=True)

with chart4_chart5_col2:
    st.markdown("### Diverging Bar Chart of Reviews")
    diverging_data = monthly_ota_google.copy()
    diverging_data['Count'] = diverging_data.apply(
        lambda x: -x['Review ID'] if x['Review Group'] == 'Google' else x['Review ID'], axis=1)
    diverging_data['Direction'] = diverging_data['Review Group'].map({
        'Google': 'Left', 'OTA': 'Right'
    })
    fig5 = px.bar(diverging_data, x='Count', y='Month', color='Review Group', orientation='h',
                  title="Diverging Bar Chart: OTA and Google Reviews by Month",
                  labels={'Count': 'Review Count'}, color_discrete_sequence=colors)
    st.plotly_chart(fig5, use_container_width=True)

st.markdown("---")
