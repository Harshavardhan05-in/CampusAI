from services.embedding_service import create_embedding
from services.vector_store import collection


def search_documnets(query, top_k=3):
    query_embedding = create_embedding(query)

    result = collection.query(query_embeddings=[query_embedding], n_results=top_k)

    documents = result["documents"][0]
    metadatas = result["metadatas"][0]
    distances = result["distances"][0]

    threshold = 0.75

    filtered_documents = []
    filtered_metadatas = []
    filtered_distances = []

    for documnet, metadata, distance in zip(documents, metadatas, distances):
        if distance <= threshold:
            filtered_documents.append(documnet)
            filtered_metadatas.append(metadata)
            filtered_distances.append(distance)

    return {
        "documents": [filtered_documents],
        "metadatas": [filtered_metadatas],
        "distances": [filtered_distances],
    }
