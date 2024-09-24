import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk

def preprocess_text(text):
    # Convert to lowercase
    text = str(text)
    text = text.lower()
    
    # Remove special characters and numbers
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    
    # Tokenize the text
    tokens = word_tokenize(text)
    
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word not in stop_words]
    
    # Join the tokens back into a string
    processed_text = ' '.join(tokens)
    
    return processed_text