import streamlit as st
import json
import os
from backend.resume_parser import parse_resume
from backend.resume_matcher import match_resume_to_job

# Configure page
st.set_page_config(page_title="AI Resume Screener", layout="wide")
st.title("📄 AI Resume Screener")


# Define tabs
tabs = ["Resume Parsing", "Resume Matching", "Experience Scoring", "Interview Evaluation"]
selected_tab = st.sidebar.radio("Select Feature", tabs)

if selected_tab == "Resume Parsing":
    st.subheader("📑 Resume Parsing")
    uploaded_file = st.file_uploader("Upload Resume", type=["pdf", "docx"])
    
    if uploaded_file:
        temp_dir = "temp"
        os.makedirs(temp_dir, exist_ok=True)
        temp_path = os.path.join(temp_dir, uploaded_file.name)
        
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        st.write("Processing...")
        parsed_data = parse_resume(temp_path)
        
        if "error" in parsed_data:
            st.error(parsed_data["error"])
        else:
            st.success("Resume processed successfully!")
            
            # Display results
            cols = st.columns(2)
            with cols[0]:
                st.subheader("Contact Info")
                st.write(f"**Email:** {parsed_data['email']}")
                st.write(f"**Phone:** {parsed_data['phone']}")
                st.write(f"**LinkedIn:** {parsed_data['linkedin']}")
                st.write(f"**GitHub:** {parsed_data['github']}")
                
                st.subheader("Skills")
                st.write(", ".join(parsed_data["skills"]))
            
            with cols[1]:
                st.subheader("Education")
                st.text(parsed_data["education"])
                
                st.subheader("Experience")
                st.text(parsed_data["work_experience"])
            
            st.subheader("Summary")
            st.write(parsed_data["summary"])
            
            # Download button
            json_data = json.dumps(parsed_data, indent=4)
            st.download_button("Download JSON", json_data, "resume_data.json", "application/json")
        
        os.remove(temp_path)

elif selected_tab == "Resume Matching":
    st.subheader("🔍 Resume Matching")
    
    uploaded_file = st.file_uploader("Upload Resume for Matching", type=["pdf", "docx"])
    job_desc = st.text_area("Paste Job Description")
    
    if uploaded_file and job_desc:
        temp_path = os.path.join("temp", uploaded_file.name)
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        parsed_data = parse_resume(temp_path)
        
        if "error" not in parsed_data:
            match_result = match_resume_to_job(parsed_data["text"], job_desc)
            
            st.subheader("Matching Results")
            cols = st.columns(2)
            
            with cols[0]:
                st.metric("Match Score", f"{match_result['score']:.2f}")
                st.write(f"**Match:** {'✅ Yes' if match_result['match'] else '❌ No'}")
            
            with cols[1]:
                st.subheader("Matched Skills")
                if match_result['matched_skills'][0] == "No Matching Skills Found":
                    st.warning("No skills matched")
                else:
                    st.write(", ".join(match_result['matched_skills']))
        
        os.remove(temp_path)