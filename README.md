# Document-Forgery-Detection
# PS3: Document Forgery Detection System

This project detects potential tampering and forgery in documents using image processing techniques such as Error Level Analysis (ELA), OCR, duplicate detection, and metadata analysis.
# PS3: Document Forgery Detection System

A prototype system to detect document forgery by analyzing image inconsistencies, duplicated regions, extracted text, and metadata.
## Objective

To identify tampered or forged documents by:
- Detecting image manipulation (ELA)
- Extracting text using OCR
- Identifying duplicate signatures or seals
- Analyzing metadata
- Generating a forgery score
  ## Technologies Used

- Python
- OpenCV
- Tesseract OCR
- Streamlit
- Pillow (PIL)
- ## Project Structure

project/
├── ela_module/
├── ocr_module/
├── duplicate_module/
├── metadata_module/
├── ui_module/
└── main.py
## How to Run

1. Create virtual environment:
   python -m venv venv

2. Activate environment:
   venv\Scripts\activate

3. Install dependencies:
   pip install -r requirements.txt

4. Run application:
   python main.py
   OR
   streamlit run ui_module/app.py
   ## Team Members

- Student 1 (Samir) – ELA Module
- Student 2 (Neelam) – OCR Module
- Student 3 (Chanchal) – Duplicate Detection
- Student 4 (Zaid) – Metadata & Scoring
- Student 5 – UI
