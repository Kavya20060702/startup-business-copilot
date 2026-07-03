import os
from typing import Dict, Any

try:
    from pypdf import PdfReader
    PYPDF_AVAILABLE = True
except ImportError:
    PYPDF_AVAILABLE = False

try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False

UPLOADS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "uploads")

def parse_uploaded_file(file_path: str) -> Dict[str, Any]:
    os.makedirs(UPLOADS_DIR, exist_ok=True)
    ext = os.path.splitext(file_path)[1].lower()
    
    extracted_text = ""
    parsed_metrics = {}

    if ext == ".pdf":
        if PYPDF_AVAILABLE and os.path.exists(file_path):
            try:
                reader = PdfReader(file_path)
                pages_text = []
                for page in reader.pages:
                    text = page.extract_text()
                    if text:
                        pages_text.append(text)
                extracted_text = "\n".join(pages_text)
            except Exception as e:
                extracted_text = f"Error reading PDF: {str(e)}"
        else:
            extracted_text = "[MOCK FILE PARSER] Pitch deck PDF uploaded successfully. Extracted core mission: Next-gen enterprise automation platform."

    elif ext == ".csv":
        if PANDAS_AVAILABLE and os.path.exists(file_path):
            try:
                df = pd.read_csv(file_path)
                extracted_text = f"Parsed CSV with columns: {list(df.columns)}. Rows count: {len(df)}"
                parsed_metrics["columns"] = list(df.columns)
            except Exception as e:
                extracted_text = f"Error reading CSV: {str(e)}"
        else:
            extracted_text = "[MOCK FILE PARSER] Financial CSV uploaded successfully. Revenue growth tracking 120% YoY."
    else:
        extracted_text = "Unsupported file type uploaded."

    return {
        "filename": os.path.basename(file_path),
        "extracted_text": extracted_text[:2000], # return first 2000 chars
        "parsed_metrics": parsed_metrics
    }
