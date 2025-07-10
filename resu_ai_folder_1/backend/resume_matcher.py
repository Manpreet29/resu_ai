from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import re
from typing import List, Dict

# Skills Database
SKILLS_DATABASE = {
    "Python", "Java", "C++", "JavaScript", "Node.js", "SQL", "React", "Docker", "Kubernetes",
    "Flask", "Django", "Git", "REST API", "GraphQL", "Pandas", "NumPy", "Scikit-learn",
    "PyTorch", "TensorFlow", "OpenCV", "Linux", "Bash", "Jenkins", "Ansible", "Azure",
    "Google Cloud", "AWS", "Spark", "Hadoop", "Tableau", "Power BI", "Agile", "Scrum", "Kanban",
    "Machine Learning", "Data Science", "Deep Learning", "Natural Language Processing", "NLP",
    "Computer Vision", "Big Data", "Artificial Intelligence", "Data Structures", "Data Analysis",
    "Data Visualization", "Statistical Modeling", "Predictive Analytics", "R"
}

# Load Model
model = SentenceTransformer('all-MiniLM-L6-v2')

def preprocess_text(text: str) -> str:
    if not text:
        return ""
    text = re.sub(r'[^\w\s.,;!?]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip().lower()
    return text

def encode_text(text: str):
    return model.encode(text, convert_to_tensor=True)

def get_similarity_score(text1: str, text2: str) -> float:
    text1 = preprocess_text(text1)
    text2 = preprocess_text(text2)
    
    if not text1 or not text2:
        return 0.0
    
    try:
        emb1 = encode_text(text1)
        emb2 = encode_text(text2)
        similarity = cosine_similarity(emb1.reshape(1, -1), emb2.reshape(1, -1))
        return float(similarity[0][0])
    except Exception as e:
        print(f"Similarity calculation error: {e}")
        return 0.0

def extract_skills_from_text(text: str) -> List[str]:
    text_lower = text.lower()
    skills = set()
    
    for skill in SKILLS_DATABASE:
        if re.search(rf'(?<!\w){re.escape(skill.lower())}(?!\w)', text_lower):
            skills.add(skill)
    
    return list(skills)

def get_matched_skills(resume_text: str, job_description: str) -> List[str]:
    resume_skills = set(extract_skills_from_text(resume_text))
    job_skills = set(extract_skills_from_text(job_description))
    
    matched = [
        skill for skill in resume_skills 
        if skill.lower() in {s.lower() for s in job_skills}
    ]
    
    return matched if matched else ["No Matching Skills Found"]

def match_resume_to_job(resume_text: str, job_description: str) -> Dict:
    similarity_score = get_similarity_score(resume_text, job_description)
    matched_skills = get_matched_skills(resume_text, job_description)
    
    return {
        "match": similarity_score >= 0.5,
        "score": similarity_score,
        "matched_skills": matched_skills
    }