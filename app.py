#!/usr/bin/env python
# coding: utf-8

# In[1]:


import streamlit as st
import pandas as pd
from io import StringIO

from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser
import re
import nltk
import string
import spacy
import heapq
#nltk.download('punkt')
#nltk.download('stopwords')
#nltk.download('wordnet')
from nltk.tokenize import word_tokenize
from nltk import pos_tag
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from nltk.stem import PorterStemmer
from wordcloud import WordCloud, STOPWORDS
from IPython.core.display import HTML
import matplotlib.pyplot as plt


# In[2]:


st.title('Sentimental Analysis of Book')

book=["The 7 Habits","Living in the Light","How to win Friends"]

choice=st.sidebar.selectbox("Select a book ",book)


# In[3]:
output_string = StringIO()
if choice=="The 7 Habits":
    with open('The 7 Habits.pdf', 'rb') as in_file:
        parser = PDFParser(in_file)
        doc = PDFDocument(parser)
        rsrcmgr = PDFResourceManager()
        device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        for page in PDFPage.create_pages(doc):
            interpreter.process_page(page)
elif choice=="Living in the Light":
    with open('Living in the Light.pdf', 'rb') as in_file:
        parser = PDFParser(in_file)
        doc = PDFDocument(parser)
        rsrcmgr = PDFResourceManager()
        device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        for page in PDFPage.create_pages(doc):
            interpreter.process_page(page)
elif choice=="How to win Friends":
    with open('How to win Friends.pdf', 'rb') as in_file:
        parser = PDFParser(in_file)
        doc = PDFDocument(parser)
        rsrcmgr = PDFResourceManager()
        device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        for page in PDFPage.create_pages(doc):
            interpreter.process_page(page)

print(output_string.getvalue())





# In[4]:


original_text=output_string.getvalue()


# In[5]:


original_text = re.sub(r'\s+', ' ', original_text)


# In[6]:


text = re.sub(r'[^\w\s]', '', original_text)


# In[7]:


en = spacy.load('en_core_web_sm')
stopwords = en.Defaults.stop_words


# In[8]:


def preprocess(text):
  formatted_text = text.lower()
  tokens = []
  for token in nltk.word_tokenize(formatted_text):
    tokens.append(token)
  #print(tokens)
  tokens = [word for word in tokens if word not in stopwords and word not in string.punctuation]
  formatted_text = ' '.join(element for element in tokens)

  return formatted_text


# In[9]:


formatted_text = preprocess(text)


# In[10]:


word_frequency = nltk.FreqDist(nltk.word_tokenize(formatted_text))
highest_frequency = max(word_frequency.values())


# In[11]:


for word in word_frequency.keys():
  #print(word)
  word_frequency[word] = (word_frequency[word] / highest_frequency)


# In[12]:


sentence_list = nltk.sent_tokenize(original_text)


# In[13]:


sentence_new=[]
for i in range(len(sentence_list)):
    if int(len(sentence_list[i]))<500:
        sentence_new.append(sentence_list[i])


# In[14]:


score_sentences = {}
for sentence in sentence_new:
  #print(sentence)
  for word in nltk.word_tokenize(sentence.lower()):
    #print(word)
    if sentence not in score_sentences.keys():
      score_sentences[sentence] = word_frequency[word]
    else:
      score_sentences[sentence] += word_frequency[word]


# In[15]:


best_sentences = heapq.nlargest(int(len(sentence_new) * 0.2), score_sentences, key = score_sentences.get)


# In[16]:


summary = ' '.join(best_sentences)


# In[17]:

if st.button("Click here for summary"):
	st.write(summary)


# In[18]:


len(text)


# In[19]:


len(summary)


# In[20]:


def clean(summary):
    # Removes all special characters and numericals leaving the alphabets
    text = re.sub('[^A-Za-z]+', ' ', summary) 
    return summary


# In[21]:


summary = re.sub(r'[^\w\s]', '', summary)


# In[22]:


from nltk.corpus import stopwords

stop_words = set(stopwords.words('english'))
 
word_tokens = word_tokenize(summary)
 
filtered_summary = [w for w in word_tokens if not w.lower() in stop_words]
 
filtered_summary = []
 
for w in word_tokens:
    if w not in stop_words:
        filtered_summary.append(w)


# In[23]:


my_stop_words=stopwords.words('english')

sw_list = ['\x92','rt','ye','yeah','haha','Yes','U0001F923','I','The']
my_stop_words.extend(sw_list)

no_stop_tokens=[word for word in filtered_summary if not word in my_stop_words]


# In[24]:


lower_words=[Text.lower() for Text in no_stop_tokens]
ps=PorterStemmer()
stemmed_tokens=[ps.stem(word) for word in lower_words]


# In[25]:


nlp=spacy.load('en_core_web_sm')
doc=nlp(' '.join(lower_words))


# In[26]:


lemmas=[token.lemma_ for token in doc]
clean_sum=' '.join(lemmas)




from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
#def sentiment_scores(clean_sum):
    
sid_obj = SentimentIntensityAnalyzer()
    
sentiment_dict = sid_obj.polarity_scores(clean_sum)
    #print("Overall sentiment dictionary is : ", sentiment_dict)
    #print("sentence was rated as ", sentiment_dict['neg']*100, "% Negative")
    #print("sentence was rated as ", sentiment_dict['neu']*100, "% Neutral")
    #print("sentence was rated as ", sentiment_dict['pos']*100, "% Positive")
    #print("Sentence Overall Rated As", end = " ")
Overall_sentiment = sentiment_dict
Negative = sentiment_dict['neg']*100
st.write('negative sentiment',Negative)
Neutral  = sentiment_dict['neu']*100
st.write('neutral sentiment',Neutral)
Positive = sentiment_dict['pos']*100
st.write('positive sentiment',Positive)
Overall_Rated =  end = " "
score=sentiment_dict['compound']
st.write('compound score',score)






if sentiment_dict['compound'] >= 0.05 :
    st.info("This Book has a Positive Sentiment")
    
    
elif sentiment_dict['compound'] <= - 0.05 :
    st.info("This Book has a Negative Sentiment")
else :
    st.info("This Book has a Neutral Sentiment")




exp_vals = [Positive,Negative,Neutral]
exp_labels = ["Positive","Negative","neutral"]


st.header('Pie Chart of Sentiments')
    
fig2 = plt.figure(figsize = (10, 5))
plt.axis("equal")
plt.pie(exp_vals,labels=exp_labels, shadow=False, autopct='%2.1f%%',radius=1.2,explode=[0,0,0],counterclock=True, startangle=45)
st.pyplot(fig2)












