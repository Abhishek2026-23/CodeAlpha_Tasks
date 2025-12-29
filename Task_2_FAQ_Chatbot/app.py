from flask import Flask, render_template, request, jsonify
import json
import nltk
import string
import numpy as np
import re
import math
from collections import Counter

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    nltk.download('punkt_tab')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

app = Flask(__name__)

class FAQChatbot:
    def __init__(self, faq_file='faqs.json'):
        self.load_faqs(faq_file)
        self.stop_words = set(stopwords.words('english'))
        self.prepare_faq_vectors()
    
    def load_faqs(self, faq_file):
        """Load FAQ data from JSON file"""
        try:
            with open(faq_file, 'r', encoding='utf-8') as f:
                self.faqs = json.load(f)
        except FileNotFoundError:
            print(f"FAQ file {faq_file} not found!")
            self.faqs = []
    
    def preprocess_text(self, text):
        """Clean and preprocess text"""
        # Convert to lowercase
        text = text.lower()
        
        # Remove punctuation
        text = text.translate(str.maketrans('', '', string.punctuation))
        
        # Tokenize and remove stop words
        tokens = word_tokenize(text)
        tokens = [token for token in tokens if token not in self.stop_words and len(token) > 2]
        
        return tokens
    
    def calculate_tf_idf(self, tokens, all_documents):
        """Calculate TF-IDF for tokens"""
        tf_idf = {}
        doc_count = len(all_documents)
        
        # Calculate term frequency
        token_count = len(tokens)
        for token in set(tokens):
            tf = tokens.count(token) / token_count
            
            # Calculate document frequency
            df = sum(1 for doc in all_documents if token in doc)
            
            # Calculate IDF
            idf = math.log(doc_count / (df + 1))
            
            # Calculate TF-IDF
            tf_idf[token] = tf * idf
        
        return tf_idf
    
    def cosine_similarity(self, vec1, vec2):
        """Calculate cosine similarity between two vectors"""
        # Get all unique tokens
        all_tokens = set(vec1.keys()) | set(vec2.keys())
        
        # Create vectors
        v1 = [vec1.get(token, 0) for token in all_tokens]
        v2 = [vec2.get(token, 0) for token in all_tokens]
        
        # Calculate dot product
        dot_product = sum(a * b for a, b in zip(v1, v2))
        
        # Calculate magnitudes
        magnitude1 = math.sqrt(sum(a * a for a in v1))
        magnitude2 = math.sqrt(sum(a * a for a in v2))
        
        # Avoid division by zero
        if magnitude1 == 0 or magnitude2 == 0:
            return 0
        
        return dot_product / (magnitude1 * magnitude2)
    
    def prepare_faq_vectors(self):
        """Prepare TF-IDF vectors for all FAQ questions"""
        if not self.faqs:
            return
        
        # Preprocess all FAQ questions
        self.faq_tokens = []
        for faq in self.faqs:
            tokens = self.preprocess_text(faq['question'])
            self.faq_tokens.append(tokens)
        
        # Calculate TF-IDF for each FAQ
        self.faq_vectors = []
        for tokens in self.faq_tokens:
            tf_idf = self.calculate_tf_idf(tokens, self.faq_tokens)
            self.faq_vectors.append(tf_idf)
    
    def get_response(self, user_question, threshold=0.3):
        """Get chatbot response for user question"""
        if not self.faqs or not self.faq_vectors:
            return "Sorry, I don't have any FAQ data loaded.", 0.0
        
        # Preprocess user question
        user_tokens = self.preprocess_text(user_question)
        user_vector = self.calculate_tf_idf(user_tokens, self.faq_tokens + [user_tokens])
        
        # Calculate similarity with all FAQ questions
        similarities = []
        for faq_vector in self.faq_vectors:
            similarity = self.cosine_similarity(user_vector, faq_vector)
            similarities.append(similarity)
        
        # Find the best match
        if not similarities:
            return "Sorry, I don't understand your question. Could you please rephrase it?", 0.0
        
        best_match_idx = similarities.index(max(similarities))
        best_similarity = similarities[best_match_idx]
        
        # Return response based on similarity threshold
        if best_similarity >= threshold:
            return self.faqs[best_match_idx]['answer'], best_similarity
        else:
            return "Sorry, I don't understand your question. Could you please rephrase it?", best_similarity

# Initialize chatbot
chatbot = FAQChatbot()

@app.route('/')
def index():
    """Render the main chatbot interface"""
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat requests"""
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({
                'response': 'Please enter a question.',
                'confidence': 0.0
            })
        
        # Get chatbot response
        response, confidence = chatbot.get_response(user_message)
        
        return jsonify({
            'response': response,
            'confidence': round(confidence, 2)
        })
    
    except Exception as e:
        return jsonify({
            'response': 'Sorry, something went wrong. Please try again.',
            'confidence': 0.0
        }), 500

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)