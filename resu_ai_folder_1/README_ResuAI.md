# Resu.AI — AI-Powered Resume Screener & Interview Evaluator

Resu.AI is a smart, semi-adaptive platform that combines AI-powered resume parsing and mock interview evaluation. It helps recruiters, students, and job-seekers by automating resume analysis and simulating intelligent interview assessments.

---

## 🚀 Features

✅ Resume Parsing:
- PDF and DOCX support
- Extracts Name, Email, Phone, GitHub, LinkedIn, Skills, Education, Experience
- NLP-enhanced section detection
- Uses spaCy, NLTK, fuzzy matching, and Hugging Face Transformers (BART) for summarization

✅ Resume Evaluation:
- Sentence-BERT-based similarity scoring
- Skill-experience impact analysis
- Resume formatting and bias detection (planned)

✅ Interview Evaluation:
- Whisper API for speech-to-text
- Real-time interview question generation
- Adaptive question flow (planned)
- Feedback & scoring based on confidence, clarity, relevance (planned)

✅ Additional Planned Features:
- AI-generated job descriptions
- Collaborative hiring features
- Dynamic weighting for resume components
- MongoDB-based data persistence
- Full MERN stack frontend integration

---

## 🧠 Tech Stack

| Layer        | Tools Used                                                                 |
|--------------|----------------------------------------------------------------------------|
| Backend      | Flask (Python), BERT/Sentence-BERT, Hugging Face Transformers, Whisper API |
| Frontend     | HTML, CSS, JavaScript (MERN stack planned)                                |
| NLP/AI       | spaCy, NLTK, Transformers, FuzzyWuzzy                                      |
| Database     | MongoDB (planned)                                                          |
| Deployment   | Render/Heroku/ngrok (optional)                                             |

---

## 🛠️ Setup Instructions

### 🔧 Prerequisites
- Python 3.8 or higher
- Git (optional, for cloning)
- Virtual environment (recommended)

### 🧩 Installation

1. Clone the repo or extract the `.zip`:
   ```bash
   git clone https://github.com/your-username/resuai.git
   # or unzip resuai_project_v1.zip
   cd resuai_project_v1
   ```

2. Create & activate virtual environment:
   ```bash
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   # macOS/Linux:
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the Flask app:
   ```bash
   python app.py
   ```

5. Visit:
   [http://localhost:5000](http://localhost:5000)

---

## 📂 Folder Structure

```
resuai_project_v1/
│
├── app.py / app_1.py       # Main Flask backend
├── backend/                # Business logic & model integration
├── frontend/               # Static assets & planned React frontend
├── static/                 # CSS, JS, images
├── templates/              # Jinja2 templates for UI
├── uploads/                # Uploaded resumes
├── data/                   # Sample resumes / datasets
├── logs/                   # Logging and debug info
├── temp/                   # Temporary files
├── requirements.txt        # All dependencies
└── README.md               # This file
```

---

## 🤝 Contributing
Pull requests and feedback are welcome! Please open an issue first to discuss any major changes.

---

## 📜 License
MIT License — free to use and modify.

---

> Created with ❤️ by Mr. Madhur Kaushik
