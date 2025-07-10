import pdfplumber
import docx
import re
import spacy
import os
import json
from transformers import pipeline
from fuzzywuzzy import fuzz  # For fuzzy matching

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
WORK_KEYWORDS = ["work experience", "experience", "employment", "professional experience", "career history"]
EDUCATION_KEYWORDS = ["education", "degree", "university", "college", "bachelor", "master", "phd", "school", "academic background", "certifications"]

# Expanded Skills Database (including science-based skills)
SKILLS_DATABASE = {
    # Programming and Software Development
    "Python", "Java", "C++", "JavaScript", "Node.js", "SQL", "React", "Docker", "Kubernetes",
    "Flask", "Django", "Git", "REST API", "GraphQL", "Pandas", "NumPy", "Scikit-learn",
    "PyTorch", "TensorFlow", "OpenCV", "Linux", "Bash", "Jenkins", "Ansible", "Azure",
    "Google Cloud", "AWS", "Spark", "Hadoop", "Tableau", "Power BI", "Agile", "Scrum", "Kanban",

    # Data Science and Machine Learning
    "Machine Learning", "Data Science", "Deep Learning", "Natural Language Processing", "NLP",
    "Computer Vision", "Big Data", "Artificial Intelligence", "Data Structures", "Data Analysis",
    "Data Visualization", "Statistical Modeling", "Predictive Analytics", "Reinforcement Learning",

    # Physics and Subfields
    "Physics", "Classical Mechanics", "Quantum Mechanics", "Electromagnetism", "Thermodynamics",
    "Statistical Mechanics", "Astrophysics", "Cosmology", "Particle Physics", "Nuclear Physics",
    "Optics", "Solid State Physics", "Plasma Physics", "Fluid Dynamics", "Relativity", "Quantum Field Theory",

    # Mathematics and Subfields
    "Mathematics", "Linear Algebra", "Calculus", "Differential Equations", "Probability", "Statistics",
    "Number Theory", "Geometry", "Topology", "Discrete Mathematics", "Numerical Analysis", "Optimization",
    "Game Theory", "Mathematical Modeling", "Complex Analysis", "Real Analysis", "Abstract Algebra",

    # Other Technical Skills
    "Cybersecurity", "DevOps", "Cloud Computing", "Blockchain", "IoT", "Robotics", "Embedded Systems",
    "Signal Processing", "Control Systems", "Biophysics", "Computational Biology", "Bioinformatics"
}

# Initialize Lemmatizer
lemmatizer = WordNetLemmatizer()

# Function to extract text from PDFs
def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text(x_tolerance=1, y_tolerance=1)  # Adjust tolerance for better extraction
            if page_text:
                text += page_text + "\n"
    return text.strip()

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

# Function to extract phone number
def extract_phone(text):
    match = re.findall(r"\+?\d{1,3}[-.\s]?\d{2,4}[-.\s]?\d{2,4}[-.\s]?\d{4}", text)
    return match[0] if match else "Not Found"

def extract_links(text):
    linkedin_match = re.search(r"(https?://)?(www\.)?linkedin\.com/[a-zA-Z0-9\-_/]+", text)
    github_match = re.search(r"(https?://)?(www\.)?github\.com/[a-zA-Z0-9\-_/]+", text)

    linkedin_url = linkedin_match.group() if linkedin_match else "Not Found"
    github_url = github_match.group() if github_match else "Not Found"

    return {
        "linkedin": linkedin_url,
        "github": github_url
    }


# Function to extract skills using lemmatization and exact matching
def extract_skills(text):
    extracted_skills = set()
    doc = nlp(text)

    # Lemmatize the text and split into tokens
    lemmatized_tokens = [lemmatizer.lemmatize(token.text.lower()) for token in doc]

    # Check for exact matches in the skills database
    for skill in SKILLS_DATABASE:
        # Lemmatize the skill and split into tokens
        skill_tokens = [lemmatizer.lemmatize(word.lower()) for word in skill.split()]
        # Check if all tokens of the skill are present in the text
        if all(token in lemmatized_tokens for token in skill_tokens):
            extracted_skills.add(skill)

    return list(extracted_skills) if extracted_skills else ["Not Found"]

# Function to extract sections (Work Experience & Education) with fuzzy matching
def extract_section(text, keywords):
    section_data = []
    lines = text.split("\n")
    
    capturing = False
    for line in lines:
        clean_line = line.strip()

        # Fuzzy matching for section headers (case-insensitive)
        if any(fuzz.partial_ratio(keyword.lower(), clean_line.lower()) > 80 for keyword in keywords):
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

# Function to generate AI-powered resume summary (Properly Formatted)
def generate_resume_summary(text):
    # Remove contact details before summarization
    text = re.sub(r"\S+@\S+", "", text)  # Remove emails
    text = re.sub(r"\(?\+?\d{1,3}[-.\s]?\d{2,4}[-.\s]?\d{2,4}[-.\s]?\d{4}\)?", "", text)  # Remove phone numbers

    short_text = text[:1000]  # Limit input text for better accuracy

    try:
        summary = summarizer(short_text, max_length=100, min_length=30, do_sample=False)
        formatted_summary = summary[0]['summary_text']

        # Format output with bullet points
        structured_summary = "\n- " + "\n- ".join(formatted_summary.split(". "))  

        return structured_summary.strip()
    
    except Exception as e:
        print(f"⚠️ Error generating summary: {e}")
        return "Summary not available"

# Main function to parse resume
def parse_resume(file_path):
    # Check if the file is a PDF or DOCX
    ext = os.path.splitext(file_path)[-1].lower()
    if ext not in [".pdf", ".docx"]:
        return {"error": "Unsupported file format. Only PDF and DOCX files are allowed."}

    text = extract_text_from_pdf(file_path) if ext == ".pdf" else extract_text_from_docx(file_path) if ext == ".docx" else None
    if not text: return {"error": "Unsupported file format"}

    text = clean_text(text)
    
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

    print(json.dumps(parsed_data, indent=4))
    return parsed_data

if __name__ == "__main__":
    file_path = "D:/resume_screener/backend/data/sample_resume.pdf"  # Replace with your file path
    print(f"Parsing resume: {file_path}")
    result = parse_resume(file_path)
    if "error" in result:
        print(result["error"])