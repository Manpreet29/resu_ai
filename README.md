# Resu.ai – Resume Parser & Matcher  

**Technologies Used:** Python | NLP (spaCy, NLTK, Transformers) | Regex | FuzzyWuzzy | pdfplumber | docx | PyMuPDF  

---

## 📌 Overview  
Resu.ai is an **AI-powered resume parsing and matching system** that extracts structured information from unstructured resumes (PDF/DOCX) and matches them against job descriptions.  

The system leverages **Natural Language Processing (NLP), semantic similarity models, and fuzzy matching** to evaluate candidate-job fit.  
It is designed with scalability in mind, making it extendable to **Applicant Tracking Systems (ATS)** or **cloud-based recruitment platforms**.  

---

## 🚀 Features  
- 📄 **Resume Parsing** – Extracts text and metadata from PDF/DOCX resumes.  
- 🔍 **Entity & Skill Extraction** – Identifies key details like Name, Contact Info, Skills, Education, and Experience.  
- 🤝 **Resume–JD Matching** – Uses **semantic similarity (Transformers)** + **fuzzy matching** for relevance scoring.  
- 📊 **Structured Output** – Generates results in **JSON/CSV** formats for downstream analytics.  
- ☁️ **Scalable Design** – Modular pipeline, ready for cloud/ATS integration.  

---

## 🛠️ Tech Stack  
- **Languages:** Python  
- **Libraries/Frameworks:**  
  - `spacy`, `nltk` – NLP preprocessing, tokenization, NER  
  - `transformers` – Semantic similarity models  
  - `fuzzywuzzy` – Approximate string matching  
  - `pdfplumber`, `docx`, `fitz (PyMuPDF)` – Resume file parsing  
  - `json`, `re`, `os`, `zipfile` – Data handling & utilities  

---

## ⚙️ Installation & Setup  
1. Clone the repository:  
```bash
git clone https://github.com/Manpreet29/resu_ai
cd resu_ai
```

2. Install dependencies:
 ```bash
 pip install -r requirements.txt
 ```

3. Run the application:
```bash
python main.py --resume data/sample_resume.pdf --jd data/sample_jd.txt
```

---

📊 Example Output

Input: resume.pdf + job_description.txt

![WhatsApp Image 2025-09-16 at 8 01 52 PM](https://github.com/user-attachments/assets/b1dff0b1-3239-4ed4-af9d-2a914a318b00)

![WhatsApp Image 2025-09-16 at 8 01 49 PM](https://github.com/user-attachments/assets/d2f61f9f-ab2f-4ac9-a849-70075929d082)

![WhatsApp Image 2025-09-16 at 8 01 50 PM](https://github.com/user-attachments/assets/8f234ff1-f1fc-4054-a4ae-8d8dbd44c3d0)

![WhatsApp Image 2025-09-16 at 8 01 50 PM (1)](https://github.com/user-attachments/assets/0e05485c-6a01-4c08-82f2-6f68b669333e)

![WhatsApp Image 2025-09-16 at 8 01 50 PM (2)](https://github.com/user-attachments/assets/695bf41b-923c-4852-b4b9-82a9e112180e)

![WhatsApp Image 2025-09-16 at 8 01 51 PM](https://github.com/user-attachments/assets/f7a99851-48d7-4cf8-a685-8a29268b110f)

![WhatsApp Image 2025-09-16 at 8 01 51 PM (1)](https://github.com/user-attachments/assets/07f58ddb-6ec9-4436-9b28-4b2b563e5c5d)
