import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

# Note: The first time you run this, you need to download the required NLTK datasets.
# If you get an error, uncomment the two lines below and run the script once.
# nltk.download('punkt')
# nltk.download('stopwords')
nltk.download('punkt_tab')

def process_text():
    # 1. The input sentence
    text = "The quick brown foxes are running very fast and they played happily."
    print("Original Text:", text)
    print("-" * 30)

    # 2. Tokenization: Breaking the sentence into individual words
    tokens = word_tokenize(text)
    print("Tokens:\n", tokens)
    print("-" * 30)

    # 3. Stopwords: Removing common words that don't add much meaning
    # Getting the list of English stopwords
    stop_words = set(stopwords.words('english'))
    
    # Keeping only the words that are NOT in the stop_words list
    filtered_tokens = []
    for word in tokens:
        if word.lower() not in stop_words: # using .lower() to handle capital letters
            filtered_tokens.append(word)
            
    print("After removing stopwords:\n", filtered_tokens)
    print("-" * 30)

    # 4. Stemming: Reducing words to their base form
    stemmer = PorterStemmer()
    
    stemmed_words = []
    for word in filtered_tokens:
        stemmed_word = stemmer.stem(word)
        stemmed_words.append(stemmed_word)

    print("After Stemming (base forms):\n", stemmed_words)

# Run the function
if __name__ == "__main__":
    process_text()