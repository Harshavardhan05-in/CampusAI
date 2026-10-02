from services.pdf_service import extract_text_from_pdf
from services.chunking_service import create_chunks

path = "../knowledge_base/college_data.pdf"

pages = extract_text_from_pdf(path)

chunks = create_chunks(pages)

for chunk in chunks:
    print(chunk["page"])
    print("\n NEW PAGE CHUNKING")
