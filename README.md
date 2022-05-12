# Project2
Summary Extraction along with sentiment analysis for book.
Steps taken:
1)	Import the required libraries (pdfminer,nltk etc.)
2)	Open the pdf file of book and extract the text from it with the help pdfminer.
3)	Cleaning the text with the help of re (Regular expression) by removing extra spacing and non alpha-numeric values.
4)	Removing stopwords with the help of Spacy library.
5)	Removing punctuations and then word tokenising the text for the making of word Frequency dictionary.
6)	Making sentences from the text with the help of  sentence tokenizer and arranging them in order w.r.t word frequency present in the sentence and selecting  top 15% sentences with the help of heapq.
7)	Joining the selected sentences to create the Summary of the book.
8)	With the help of html mark up the top 15% sentences from the text and print the whole text with markups on selcted sentences.
9)	With the help of  Vader ,sentiment analysis on the summary was done which showed the percentage of positivity, negativity and neutrality of it.
10)	Deployment was done with the help of streamlit.

The screenshot of deployment is present in the files for visualization.
