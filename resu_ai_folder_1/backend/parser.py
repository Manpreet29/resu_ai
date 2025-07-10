import pdfplumber
import docx
import re
import spacy
import os
import json
from transformers import pipeline
from fuzzywuzzy import fuzz
from google.colab import files  # For file uploads in Google Colab

# Check if NLTK is installed and download required data
try:
    from nltk.stem import WordNetLemmatizer
    import nltk
except ImportError:
    print("⚠️ Error: The 'nltk' library is not installed. Please install it using 'pip install nltk'.")
    exit(1)

try:
    nltk.download('wordnet')
    nltk.download('omw-1.4')
except Exception as e:
    print(f"⚠️ Error downloading NLTK data: {e}")
    exit(1)

# Load NLP Model
nlp = spacy.load("en_core_web_sm")

# Load Free Summarization Model (Hugging Face BART)
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# Keywords for Sections (Work Experience & Education)
WORK_KEYWORDS = ["work experience", "experience", "employment", "professional experience", 
    "career history", "work history", "job experience", "positions held", 
    "professional background"]
EDUCATION_KEYWORDS = [ "education", "degree", "university", "college", "bachelor", "master", 
    "phd", "school", "academic background", "certifications", "academics", 
    "educational qualifications", "academic history"]

# Expanded Skills Database (including science-based skills)
SKILLS_DATABASE = {
    # Programming and Software Development
    "Python", "Java", "C++", "JavaScript", "Node.js", "SQL", "React", "Docker", "Kubernetes",
    "Flask", "Django", "Git", "REST API", "GraphQL", "Pandas", "NumPy", "Scikit-learn",
    "PyTorch", "TensorFlow", "OpenCV", "Linux", "Bash", "Jenkins", "Ansible", "Azure",
    "Google Cloud", "AWS", "Spark", "Hadoop", "Tableau", "Power BI", "Agile", "Scrum", "Kanban",
    # Other Technical Skills
    "Machine Learning", "Data Science", "Artificial Intelligence", "Cybersecurity", "Cloud Computing",
    "Blockchain", "IoT", "Robotics"
}

# Initialize Lemmatizer
lemmatizer = WordNetLemmatizer()

# Function to extract text from PDFs
def extract_text_from_pdf(pdf_path):
    import pdfplumber
    try:
        text = ""
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text.strip()
    except Exception as e:
        print(f"❌ PDF Extraction Error: {e}")
        return None  # fallback if the PDF is broken

# Function to extract text from DOCX
def extract_text_from_docx(docx_path):
    doc = docx.Document(docx_path)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text.strip()

# Function to clean extracted text (remove unwanted characters)
def clean_text(text):
    text = re.sub(r"\(cid:\d+\)", "", text)  # Remove PDF artifacts
    text = re.sub(r"\s+", " ", text).strip()  # Normalize spaces
    return text

# Function to extract email
def extract_email(text):
    match = re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)
    return match[0] if match else "Not Found"

# Function to extract phone number (IMPROVED)
def extract_phone(text):
    match = re.findall(r'(\+?\d[\d\s\-().]{7,}\d)', text)
    return match[0] if match else "Not Found"

# Function to extract LinkedIn and GitHub links (IMPROVED)
def extract_links(text):
    linkedin = re.findall(r"https?://(?:www\.)?linkedin\.com/[^\s,\)\]]+", text)
    github = re.findall(r"https?://(?:www\.)?github\.com/[^\s,\)\]]+", text)

    linkedin_link = linkedin[0] if linkedin else "Not Found"
    github_link = github[0] if github else "Not Found"

    return {"linkedin": linkedin_link, "github": github_link}

# Function to extract skills using lemmatization and exact matching
def extract_skills(text):
    extracted_skills = set()
    doc = nlp(text)

    # Lemmatize the text and split into tokens
    lemmatized_tokens = [lemmatizer.lemmatize(token.text.lower()) for token in doc]

    # Check for exact matches in the skills database
    for skill in SKILLS_DATABASE:
        skill_tokens = [lemmatizer.lemmatize(word.lower()) for word in skill.split()]
        if all(token in lemmatized_tokens for token in skill_tokens):
            extracted_skills.add(skill)

    return list(extracted_skills) if extracted_skills else ["Not Found"]

# Function to extract sections (Work Experience & Education)
def extract_section(text, keywords):
    section_data = []
    lines = text.split("\n")
    
    capturing = False
    for line in lines:
        clean_line = line.strip()

        # Fuzzy matching for section headers (case-insensitive)
        if any(fuzz.partial_ratio(keyword.lower(), clean_line.lower()) > 0 for keyword in keywords):
            capturing = True
            continue  # Skip the section title itself

        # Stop capturing if another section starts
        if capturing and any(fuzz.partial_ratio(keyword.lower(), clean_line.lower()) > 80 for keyword in (WORK_KEYWORDS + EDUCATION_KEYWORDS)):
            break  

        if capturing and clean_line:
            section_data.append(clean_line)

    return "\n".join(section_data) if section_data else "Not Found"

def extract_work_experience(text):
    return extract_section(text, WORK_KEYWORDS)

def extract_education(text):
    return extract_section(text, EDUCATION_KEYWORDS)

# Function to generate AI-powered resume summary
def generate_resume_summary(text):
    # Remove contact details before summarization
    text = re.sub(r"\S+@\S+", "", text)  # Remove emails
    text = re.sub(r"\(?\+?\d{1,3}[-.\s]?\d{2,4}[-.\s]?\d{2,4}[-.\s]?\d{4}\)?", "", text)  # Remove phone numbers

    short_text = text[:1000]  # Limit input text for better accuracy

    try:
        summary = summarizer(short_text, max_length=100, min_length=30, do_sample=False)
        
        if summary and isinstance(summary, list) and 'summary_text' in summary[0]:
            formatted_summary = summary[0]['summary_text']
            structured_summary = "\n- " + "\n- ".join(formatted_summary.split(". "))
            return structured_summary.strip()
        else:
            return "Summary not available"

    except Exception as e:
        print(f"⚠️ Error generating summary: {e}")
        return "Summary not available"

# Function to parse resume
def parse_resume(file_path):
    # Check file extension
    ext = os.path.splitext(file_path)[-1].lower()
    if ext not in [".pdf", ".docx"]:
        return {"error": "Unsupported file format. Only PDF and DOCX files are allowed."}

    # Try to extract text
    try:
        text = extract_text_from_pdf(file_path) if ext == ".pdf" else extract_text_from_docx(file_path)
    except Exception as e:
        print(f"❌ Error extracting text: {e}")
        return {"error": "Failed to read the resume. Please upload a valid PDF or DOCX file."}

    if not text:
        return {"error": "No readable text found in the resume."}

    # Clean the text
    text = clean_text(text)

    # Parse resume data
    try:
        parsed_data = {
            "email": extract_email(text),
            "phone": extract_phone(text),
            "linkedin": extract_links(text)["linkedin"],
            "github": extract_links(text)["github"],
            "skills": extract_skills(text),
            "work_experience": extract_work_experience(text),
            "education": extract_education(text),
            "summary": generate_resume_summary(text),
        }

        return parsed_data

    except Exception as e:
        print(f"❌ Resume parsing error: {e}")
        return {"error": "An error occurred while parsing the resume."}

# Uploading the resume file
uploaded = files.upload()

# Access the uploaded file
for file_name in uploaded.keys():
    print(f"Uploaded file: {file_name}")
    result = parse_resume(file_name)
    if "error" in result:
        print(result["error"])
    else:
        print(json.dumps(result, indent=4))
