from services.generation_service import generate_answer
from services.retrieval_service import search_documnets

query = "Who are the required documents to get an outpass."
res = search_documnets(query)


retrived_documents = res["documents"][0]
retirved_metadata = res["metadatas"][0]

res = generate_answer(query, retrived_documents, retirved_metadata)

print(res)
