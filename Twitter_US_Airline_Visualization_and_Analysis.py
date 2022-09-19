#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt

st.title("Sentiment Analysis of Tweets about US Airlines")
st.sidebar.title("Sentiment Analysis of Tweets about US Airlines")
st.markdown("This is a Streamlit Dashboard")

Data_Url = ("Tweets.csv")
def load_data():
    data=pd.read_csv(Data_Url)
    data['tweet_created'] = pd.to_datetime(data['tweet_created'])
    return data
data = load_data()
st.sidebar.subheader("Show random tweet")
random_tweet = st.sidebar.radio('Sentiment',('positive','neutral','negative'))
st.sidebar.markdown(data.query('airline_sentiment==@random_tweet')[["text"]].sample(n=1).iat[0,0])

st.sidebar.markdown('Number of Tweets by Sentiment')
select = st.sidebar.selectbox('Visualization Technique',['Histogram','Pie chart'],key='1')
sentiment_count = data['airline_sentiment'].value_counts()
sentiment_count = pd.DataFrame({'Sentiment':sentiment_count.index, 'Tweets':sentiment_count.values})

#if not st.sidebar.checkbox("Hide",True):
st.markdown("Number of tweets by sentiment")
if select == "Histogram":
    fig = px.bar(sentiment_count,x = 'Sentiment', y = 'Tweets', color = 'Tweets')
    st.plotly_chart(fig)
else:
    fig = px.pie(sentiment_count,values='Tweets',names='Sentiment')
    st.plotly_chart(fig)

st.sidebar.subheader("Breakdown airline tweets by sentiment")
choice = st.sidebar.multiselect('Pick airline',('US Airways','United','American','Southwest','Delta','Vigin America'),key = '0')
if len(choice)>0:
    choice_data = data[data.airline.isin(choice)]
    fig_choice = px.histogram(choice_data,x='airline',y='airline_sentiment',histfunc='count', color = 'airline_sentiment', facet_col ='airline_sentiment',labels = {'airline_sentiment':'Tweets'} )
    st.plotly_chart(fig_choice)

st.sidebar.header("Word Cloud")
word_sentiment = st.sidebar.radio('Display word cloud for which sentiment?',('positive','neutral','negative'))
if not st.sidebar.checkbox('Close',True,key = '3'):
    st.header('Word cloud for %s sentiment' % (word_sentiment))
    df = data[data['airline_sentiment']==word_sentiment]
    words = ' '.join(df['text'])
    process_words = ' '.join([word for word in words.split() if 'http' not in word and not word.startswith('@') and word!='RT'])
    wordcloud = WordCloud(stopwords=STOPWORDS, background_color = 'white', height = 650,width = 800).generate(process_words)
    plt.imshow(wordcloud)
    plt.xticks([])
    plt.yticks([])
    st.pyplot()

