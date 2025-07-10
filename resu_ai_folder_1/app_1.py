from flask import Flask, render_template, request, jsonify
import os
from backend.resume_parser import parse_resume
from backend.resume_matcher import match_resume_to_job
import numpy as np
import sys
import io

# Fix encoding for Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

app = Flask(__name__, static_folder="static", static_url_path="/static")

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def convert_numpy_types(obj):
    if isinstance(obj, dict):
        return {k: convert_numpy_types(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_numpy_types(i) for i in obj]
    elif isinstance(obj, (np.float32, np.float64)):
        return float(obj)
    elif isinstance(obj, (np.int32, np.int64)):
        return int(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, np.bool_):
        return bool(obj)
    else:
        return obj

@app.route("/static/<path:filename>")
def static_files(filename):
    return app.send_static_file(filename)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "resume" not in request.files:
            return jsonify({"error": "No file uploaded"}), 400
            
        resume = request.files["resume"]
        if resume.filename == "":
            return jsonify({"error": "No selected file"}), 400
            
        file_path = os.path.join(UPLOAD_FOLDER, resume.filename)
        resume.save(file_path)
        
        try:
            parsed_data = parse_resume(file_path)
            if "error" in parsed_data:
                return jsonify({"error": parsed_data["error"]}), 400
                
            job_description = request.form.get("job_description", "")
            if job_description:
                match_result = match_resume_to_job(parsed_data["text"], job_description)
                parsed_data.update(match_result)
            
            clean_data = convert_numpy_types(parsed_data)
            return jsonify(clean_data)
            
        except Exception as e:
            return jsonify({"error": str(e)}), 500
            
        finally:
            if os.path.exists(file_path):
                os.remove(file_path)
    
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)