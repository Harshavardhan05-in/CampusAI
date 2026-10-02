import os
from dotenv import load_dotenv
from google import genai


load_dotenv()

client = genai.Client(api_key=os.getenv("GOOGLE API KEY"))


def create_embedding(text):
    res = client.models.embed_content(model="gemini-embedding-001", contents=text)

    return res.embeddings[0].values


def create_embeddings_for_chunks(chunks):

    embed_chunks = []

    for chunk in chunks:
        embed = create_embedding(chunk["text"])

        embed_chunks.append(
            {
                "text": chunk["text"],
                "page": chunk["page"],
                "source": chunk["source"],
                "embedding": embed,
            }
        )

    return embed_chunks
