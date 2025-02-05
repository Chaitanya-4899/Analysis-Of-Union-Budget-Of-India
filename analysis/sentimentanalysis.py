import os
from django.conf import settings
import fitz  # PyMuPDF
import re
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
from wordcloud import WordCloud
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.util import ngrams
from collections import Counter
from textblob import TextBlob

nltk.download('stopwords')
nltk.download('punkt')

# Helper function to extract text from a PDF
def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text += page.get_text()
    return text

# Helper function to preprocess text
def preprocess_text(text):
    text = " ".join(text.split())
    text = re.sub(r'[^a-zA-Z\s\.]', '', text)
    text = text.lower()
    return text

def analyze_sentiments(pdf_path):
    raw_text = extract_text_from_pdf(pdf_path)
    preprocessed_text = preprocess_text(raw_text)
    
    # Tokenization
    sentences = sent_tokenize(preprocessed_text)
    words = word_tokenize(preprocessed_text)

    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    filtered_sentences = [" ".join([word for word in sentence.split() if word not in stop_words]) for sentence in sentences]
    filtered_words = [word for word in words if word not in stop_words and word.isalpha()]

    # Word Frequency Analysis
    word_freq = Counter(filtered_words)
    most_common_words = word_freq.most_common(20)

    # Save Word Frequency Plot
    plt.figure(figsize=(10, 6))
    word_freq_dict = {" ".join(word) if isinstance(word, tuple) else word: freq for word, freq in Counter(filtered_words).most_common(20)} #words
    plt.bar(word_freq_dict.keys(), word_freq_dict.values(), color='skyblue')
    plt.xticks(rotation=45, ha="right")
    plt.title("Top 20 Most Common Words")
    plt.xlabel("Words")
    plt.ylabel("Frequency")
    plt.tight_layout()
    # Define the visualizations directory path
    visualizations_dir = os.path.join(settings.BASE_DIR, 'visualizations')
    # Ensure the directory exists
    os.makedirs(visualizations_dir, exist_ok=True)
    # Define the full path to save the plot
    word_freq_path = os.path.join(visualizations_dir, 'word_frequency.png')
    # Save the plot
    plt.savefig(word_freq_path)
    plt.close()

    # Save Word Cloud Visualization
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(preprocessed_text)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.tight_layout()
    word_cloud_path = os.path.join(visualizations_dir, 'word_cloud.png')
    plt.savefig(word_cloud_path)
    plt.close()

    # Bigram Analysis
    bigrams = list(ngrams(filtered_words, 2))
    bigram_freq = Counter(bigrams)
    most_common_bigrams = bigram_freq.most_common(20)

    # Save Bigram Frequency Plot
    plt.figure(figsize=(10, 6))
    bigram_freq_dict = {" ".join(bigram): freq for bigram, freq in Counter(bigrams).most_common(20)}
    plt.bar(bigram_freq_dict.keys(), bigram_freq_dict.values(), color='lightgreen')
    plt.xticks(rotation=45, ha="right")
    plt.title("Top 20 Most Common Bigrams")
    plt.xlabel("Bigrams")
    plt.ylabel("Frequency")
    plt.tight_layout()
    bigram_freq_path = os.path.join(visualizations_dir, 'bigram_frequency.png')
    plt.savefig(bigram_freq_path)
    plt.close()

    # Sentiment Analysis
    sentence_sentiments = [TextBlob(sentence).sentiment.polarity for sentence in filtered_sentences]
    sentiment = TextBlob(preprocessed_text).sentiment

    # Plot Sentiment Polarity Distribution
    plt.figure(figsize=(10, 5))
    plt.hist(sentence_sentiments, bins=20, edgecolor='black')
    plt.title('Sentiment Polarity Distribution')
    plt.xlabel('Sentiment Polarity')
    plt.ylabel('Frequency')
    plt.tight_layout()
    sentiment_dist_path = os.path.join(visualizations_dir, 'sentimentPolarityDistribution.png')
    plt.savefig(sentiment_dist_path)
    plt.close()

    # Calculate contextual sentiment polarities for top words and bigrams for further analysis
    word_polarities = {}
    for word, freq in most_common_words:
        word_str = "".join(word)
        polarities = []
        for sentence in sentences:
            if word in sentence:
                polarity = TextBlob(sentence).sentiment.polarity
                polarities.append(polarity)
        if polarities:
            word_polarities[word] = polarities

    #return word_polarities
    bigram_polarities = {}
    for bigram, freq in most_common_bigrams:
        bigram_str = " ".join(bigram)
        polarities = []
        for sentence in sentences:
            if bigram_str in sentence:
                polarity = TextBlob(sentence).sentiment.polarity
                polarities.append(polarity)
        if polarities:
            bigram_polarities[bigram_str] = polarities

    #return bigram_polarities

    #Plot top words contextual sentiment polarities
    plt.figure(figsize=(12, 8))
    words = list(word_polarities.keys())
    polarity_values = [word_polarities[word] for word in words]
    plt.boxplot(polarity_values, vert=False, patch_artist=True, labels=words)
    plt.axvline(x=0, color='red', linestyle='--', linewidth=1)
    plt.title("Contextual Sentiment Polarity Box Plot of Top 20 Words")
    plt.xlabel("Sentiment Polarity")
    plt.tight_layout()
    word_polarity_path = os.path.join(visualizations_dir, 'topWordsPolarities.png')
    plt.savefig(word_polarity_path)
    plt.close()

    #Plot top bigrams contextual sentiment polarities
    plt.figure(figsize=(12, 8))
    bigrams = list(bigram_polarities.keys())
    polarity_values = [bigram_polarities[bigram] for bigram in bigrams]
    plt.boxplot(polarity_values, vert=False, patch_artist=True, labels=bigrams)
    plt.title("Contextual Sentiment Polarity Box Plot of Top 20 Bigrams")
    plt.xlabel("Sentiment Polarity")
    plt.axvline(x=0, color='red', linestyle='--', linewidth=1)
    plt.tight_layout()
    bigram_polarity_path = os.path.join(visualizations_dir, 'topBigramsPolarities.png')
    plt.savefig(bigram_polarity_path)
    plt.close()


    return word_freq_path, word_cloud_path, bigram_freq_path, most_common_words, most_common_bigrams, sentence_sentiments, sentiment, sentiment_dist_path, word_polarity_path, bigram_polarity_path

