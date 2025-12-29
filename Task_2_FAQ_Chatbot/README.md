# Task 2: FAQ Chatbot
**CodeAlpha Artificial Intelligence Internship**

## 🎯 Project Overview
An AI-powered FAQ Chatbot that answers user questions by matching them with
predefined FAQs using Natural Language Processing (NLP).

---

## 🌐 Live Demo
👉 https://codealpha-faq-chatbot-bc2k.onrender.com/

---

## 🛠️ Technologies Used
- Python (Flask)
- NLTK
- TF-IDF & Cosine Similarity
- HTML, CSS, JavaScript
- JSON

---

## 📋 Features
- Real-time chat interface
- Confidence score for each response
- Fallback responses for unknown queries
- Responsive web design
- Custom NLP pipeline

---

## 🚀 How to Run

### ▶️ Run Locally

#### Quick Start
```bash
python setup.py
python app.py
```
Manual Setup
bash
Copy code
pip install -r requirements.txt
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
python app.py
Open in browser:

Local: http://localhost:5000

Live: https://codealpha-faq-chatbot-bc2k.onrender.com/

🧪 Testing
bash
Copy code
python test_chatbot.py
📁 Project Structure
arduino
Copy code
Task_2_FAQ_Chatbot/
├── app.py
├── faqs.json
├── requirements.txt
├── setup.py
├── test_chatbot.py
├── templates/
│   └── index.html
├── static/
│   ├── style.css
│   └── script.js
└── README.md
🎓 Learning Outcomes
NLP fundamentals

Text similarity techniques

Flask-based web development

Frontend–backend integration

Deployment using Render
