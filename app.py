import os
from flask import Flask, request, render_template, redirect, url_for
import fitz  # PyMuPDF for PDF reading

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10MB upload limit
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Placeholder question generation function
def generate_questions(text):
    # For now, simply split text into sentences and create dummy questions
    sentences = [s.strip() for s in text.split('.') if s.strip()]
    questions = [f"What is meant by: '{sentence}'?" for sentence in sentences[:5]]  # limit 5 questions
    return questions

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_pdf():
    if 'pdf_file' not in request.files:
        return "No file part", 400
    file = request.files['pdf_file']
    if file.filename == '':
        return "No selected file", 400
    if file and file.filename.lower().endswith('.pdf'):
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

        # Extract text and generate questions
        extracted_text = extract_text_from_pdf(file_path)
        questions = generate_questions(extracted_text)

        # Pass questions to template
        return render_template('questions.html', questions=questions)

    return "Invalid file format. Please upload a PDF.", 400

if __name__ == '__main__':
    app.run(debug=True)
