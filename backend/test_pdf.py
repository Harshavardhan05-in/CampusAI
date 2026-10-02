from services.pdf_service import extract_text_from_pdf

path = "../knowledge_base/college_data.pdf"

pages = extract_text_from_pdf(path)

print(type(pages))

for page in pages:
    print(f"\n--- PAGE {page['page']} ---")
    print(f"Source: {page['source']}")
    print(page["text"])
