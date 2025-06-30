from flask import Flask, request, jsonify
from flask_cors import CORS
import nltk
import re
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF
import numpy as np

app = Flask(__name__)
CORS(app)

# Download required NLTK data - Updated to include punkt_tab
def download_nltk_data():
    """Download all required NLTK data"""
    required_data = [
        'punkt',
        'punkt_tab',
        'stopwords'
    ]
    
    for data_name in required_data:
        try:
            nltk.data.find(f'tokenizers/{data_name}' if 'punkt' in data_name else f'corpora/{data_name}')
            print(f"✓ {data_name} already available")
        except LookupError:
            print(f"Downloading {data_name}...")
            nltk.download(data_name, quiet=True)
            print(f"✓ {data_name} downloaded")

# Download NLTK data at startup
download_nltk_data()

def clean_text(text):
    """Clean and preprocess text"""
    # Remove extra whitespace and newlines
    text = re.sub(r'\s+', ' ', text.strip())
    # Remove special characters but keep punctuation for sentences
    text = re.sub(r'[^\w\s.,!?;:]', '', text)
    return text

def summarize_text(text, sentences_count=3):
    """Summarize text using LSA summarizer"""
    try:
        # Clean the text
        cleaned_text = clean_text(text)
        
        # Create parser and tokenizer
        parser = PlaintextParser.from_string(cleaned_text, Tokenizer("english"))
        
        # Create LSA summarizer
        summarizer = LsaSummarizer()
        
        # Generate summary
        summary_sentences = summarizer(parser.document, sentences_count)
        
        # Convert to string
        summary = ' '.join([str(sentence) for sentence in summary_sentences])
        
        return summary if summary else "Unable to generate summary from the provided text."
    
    except Exception as e:
        print(f"Summarization error: {e}")
        return "Error occurred during summarization."

def extract_topics(text, num_topics=5):
    """Extract top topics using TF-IDF and NMF"""
    try:
        # Clean the text
        cleaned_text = clean_text(text)
        
        # Split into sentences for better topic extraction
        sentences = nltk.sent_tokenize(cleaned_text)
        
        if len(sentences) < 2:
            # If too few sentences, extract keywords using simple frequency
            words = nltk.word_tokenize(cleaned_text.lower())
            words = [word for word in words if word.isalpha() and len(word) > 3]
            word_freq = nltk.FreqDist(words)
            return [word for word, freq in word_freq.most_common(num_topics)]
        
        # Create TF-IDF vectorizer
        vectorizer = TfidfVectorizer(
            max_features=100,
            stop_words='english',
            ngram_range=(1, 2),
            min_df=1,
            max_df=0.8
        )
        
        # Fit and transform the text
        tfidf_matrix = vectorizer.fit_transform(sentences)
        
        # Use NMF for topic modeling
        nmf = NMF(n_components=min(num_topics, len(sentences)), random_state=42, max_iter=100)
        nmf.fit(tfidf_matrix)
        
        # Get feature names
        feature_names = vectorizer.get_feature_names_out()
        
        # Extract top words for each topic
        topics = []
        for topic_idx, topic in enumerate(nmf.components_):
            top_words_idx = topic.argsort()[-2:][::-1]  # Top 2 words per topic
            top_words = [feature_names[i] for i in top_words_idx]
            topics.extend(top_words)
        
        # Remove duplicates and return top topics
        unique_topics = list(dict.fromkeys(topics))
        return unique_topics[:num_topics]
    
    except Exception as e:
        print(f"Topic extraction error: {e}")
        # Fallback: simple keyword extraction
        words = nltk.word_tokenize(text.lower())
        words = [word for word in words if word.isalpha() and len(word) > 3]
        word_freq = nltk.FreqDist(words)
        return [word for word, freq in word_freq.most_common(num_topics)]

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "service": "AutoNotes ML Service"})

@app.route('/summarize', methods=['POST'])
def summarize():
    """Main endpoint for text summarization and topic extraction"""
    try:
        # Get JSON data from request
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({"error": "Missing 'text' field in request body"}), 400
        
        text = data['text'].strip()
        
        if not text:
            return jsonify({"error": "Text cannot be empty"}), 400
        
        if len(text) < 50:
            return jsonify({"error": "Text too short. Please provide at least 50 characters."}), 400
        
        # Generate summary
        summary = summarize_text(text, sentences_count=3)
        
        # Extract topics
        topics = extract_topics(text, num_topics=5)
        
        # Return response
        response = {
            "summary": summary,
            "topics": topics,
            "status": "success"
        }
        
        return jsonify(response)
    
    except Exception as e:
        print(f"Error in summarize endpoint: {e}")
        return jsonify({"error": "Internal server error occurred"}), 500

if __name__ == '__main__':
    print("Starting AutoNotes ML Service...")
    print("Downloading required NLTK data...")
    
    # Download NLTK data
    download_nltk_data()
    
    print("NLTK data ready!")
    print("ML Service running on http://localhost:5001")
    app.run(debug=True, host='0.0.0.0', port=5001)
