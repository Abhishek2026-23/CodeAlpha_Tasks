# Task 2: FAQ Chatbot  
**CodeAlpha Artificial Intelligence Internship**

## 🎯 Project Overview
An AI-powered FAQ Chatbot that answers user questions by matching them with
predefined FAQs using Natural Language Processing (NLP) techniques.

---

## 🌐 Live Demo
👉 [Live Demo – FAQ Chatbot](https://codealpha-faq-chatbot-bc2k.onrender.com/)

---

## 🛠️ Technologies Used
- **Backend:** Python + Flask  
- **NLP:** NLTK (Natural Language Toolkit)  
- **Similarity Algorithm:** TF-IDF + Cosine Similarity  
- **Frontend:** HTML5, CSS3, JavaScript  
- **Data Storage:** JSON  

---

## 🧠 How It Works
1. **Text Preprocessing**  
   - Converts user input to lowercase  
   - Removes punctuation  
   - Tokenizes text  

2. **TF-IDF Vectorization**  
   - Converts text into numerical vectors based on term importance  

3. **Similarity Matching**  
   - Uses cosine similarity to find the most relevant FAQ  

4. **Response Generation**  
   - Returns the best matching answer  
   - Provides a fallback message if no match is found  

---

## 📋 Features
✅ 15 comprehensive FAQs related to CodeAlpha internships  
✅ Real-time chat interface  
✅ Confidence score for each response  
✅ Fallback responses for unknown queries  
✅ Responsive web design  
✅ Custom NLP pipeline  

---

## 🚀 How to Run

### ▶️ Live Version
Access the deployed application here:  
👉 https://codealpha-faq-chatbot-bc2k.onrender.com/

### ▶️ Run Locally

#### Quick Start
```bash
python setup.py
python app.py
Manual Setup
bash
Copy code
pip install -r requirements.txt
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
python app.py
Then open in browser:

Local: http://localhost:5000

Live: https://codealpha-faq-chatbot-bc2k.onrender.com/

🧪 Testing
bash
Copy code
python test_chatbot.py
📁 Project Structure
csharp
Copy code
Task_2_FAQ_Chatbot/
├── app.py              # Main Flask application
├── faqs.json           # FAQ dataset (15 Q&A pairs)
├── requirements.txt    # Python dependencies
├── setup.py            # Automated setup script
├── test_chatbot.py     # Testing script
├── templates/
│   └── index.html      # Chat interface
├── static/
│   ├── style.css       # Styling
│   └── script.js       # Frontend logic
└── README.md           # Project documentation
🎨 Sample Questions
"What is CodeAlpha?"

"How long is the internship?"

"What are the requirements?"

"Is it paid or unpaid?"

"Can I work remotely?"

🔧 Technical Implementation
NLP Pipeline
Tokenization: NLTK word tokenization

Stopword Removal: Common English stopwords

TF-IDF Calculation: Term importance scoring

Cosine Similarity: Mathematical similarity measurement

Threshold Filtering: Minimum similarity threshold applied

API Endpoint
POST /chat

Accepts JSON input with user message

Returns chatbot response with confidence score

🌐 Deployment
This application is deployed on Render and is publicly accessible.

🎓 Learning Outcomes
This project demonstrates:

Natural Language Processing fundamentals

Text similarity algorithms

Web development using Flask

Frontend–backend integration

API design and testing

Deployment of AI-based applications
