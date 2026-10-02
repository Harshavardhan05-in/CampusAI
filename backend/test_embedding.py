from services.embedding_service import create_embeddings_for_chunks
from services.chunking_service import create_chunks
from services.pdf_service import extract_text_from_pdf


path = "../knowledge_base/college_data.pdf"

pages = extract_text_from_pdf(path)

chunks = create_chunks(pages)

embeddings = create_embeddings_for_chunks(chunks)

print(embeddings[0]["page"])
