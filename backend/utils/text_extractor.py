import pytesseract
import PyPDF2
from PIL import Image
from pdf2image import convert_from_path


def extract_text_from_file(filepath):
    """Extract text from a file (PDF or image), using OCR for scanned PDFs."""
    ext = filepath.rsplit(".", 1)[1].lower()
    text = ""
    try:
        if ext == "pdf":
            # First, try to extract text directly
            with open(filepath, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                for page in reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"

            # If direct extraction yields little or no text, perform OCR
            if len(text.strip()) < 100:  # Threshold to decide if we need OCR
                print("Direct text extraction insufficient, performing OCR on PDF.")
                text = ""
                images = convert_from_path(filepath)
                for i, image in enumerate(images):
                    text += pytesseract.image_to_string(image) + "\n"

        elif ext in ["png", "jpg", "jpeg"]:
            text = pytesseract.image_to_string(Image.open(filepath))

    except Exception as e:
        print(f"Error during text extraction from {filepath}: {e}")
        return None

    return text
