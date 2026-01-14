import pypdf
import sys

def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file."""
    try:
        reader = pypdf.PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        return f"Error extracting text: {str(e)}"

if __name__ == "__main__":
    pdf_path = "resume.pdf"
    text = extract_text_from_pdf(pdf_path)
    print(text)