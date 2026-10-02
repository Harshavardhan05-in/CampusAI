from services.vector_store import collection, store_embeddings
from services.pdf_service import extract_text_from_pdf
from services.chunking_service import create_chunks
from services.embedding_service import create_embeddings_for_chunks

path = "../knowledge_base/college_data.pdf"

pages = extract_text_from_pdf(path)

chunks = create_chunks(pages)

embed = create_embeddings_for_chunks(chunks)

store_embeddings(embed)

print(collection.count())
