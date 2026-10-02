import chromadb

client = chromadb.PersistentClient(path="./chroma_db")

collection = client.get_or_create_collection(name="campus_documents")


def store_embeddings(embed_chunks):

    for index, chunk in enumerate(embed_chunks):
        collection.add(
            ids=[f"chunk_{index}"],
            embeddings=[chunk["embedding"]],
            documents=[chunk["text"]],
            metadatas=[{"page": chunk["page"], "source": chunk["source"]}],
        )
