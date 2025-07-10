import os
from backend.resume_parser import parse_resume

def test_parser(file_path):
    """Test the resume parser with detailed output"""
    print(f"\n{'='*40}")
    print(f"Testing file: {os.path.basename(file_path)}")
    
    result = parse_resume(file_path)
    
    print("\n=== PARSING RESULTS ===")
    print(f"Email: {result.get('email', 'Not found')}")
    print(f"Phone: {result.get('phone', 'Not found')}")
    print(f"LinkedIn: {result.get('linkedin', 'Not found')}")
    print(f"GitHub: {result.get('github', 'Not found')}")
    
    print("\n=== SKILLS ===")
    print(', '.join(result.get('skills', [])) or "No skills found")
    
    print("\n=== EDUCATION ===")
    print(result.get('education', 'No data'))
    
    print("\n=== WORK EXPERIENCE ===")
    print(result.get('work_experience', 'No data'))
    
    print("\n=== SUMMARY ===")
    print(result.get('summary', 'No summary'))
    
    return result

if __name__ == "__main__":
    # Test with different resume formats
    test_files = [
        "test_resumes/madhur_resume",  # Your resume
        "test_resumes/minimal_resume"   # A minimal test case
    ]
    
    for file_path in test_files:
        if os.path.exists(file_path):
            test_parser(file_path)
        else:
            print(f"File not found: {file_path}")