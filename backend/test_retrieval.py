from services.retrieval_service import search_documnets

text = "Who is the vice chancellor of this university?"

res = search_documnets(text)

for index in range(len(res["documents"])):
    print(f" \n --- RESULT {index + 1}")
    print(res["distances"][index])
    print(res["metadatas"][index]["page"])
    print(res["documents"][index])
