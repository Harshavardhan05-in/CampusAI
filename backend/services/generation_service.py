from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

clinet = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))


def generate_answer(query, retrived_documents, retrived_metadats):
    context_parts = []

    for document, metadata in zip(retrived_documents, retrived_metadats):
        context_parts.append(
            f"""Source:{metadata["source"]} Page:{metadata["page"]} Context:{document}"""
        )

    context = "\n\n".join(context_parts)

    prompt = f""" You are Campus AI,An AI assiatnce for college students.
            Answer the users question using only the information provided in the context.
            Rules:
            1.Do not invent or assume information.
            2.Give a short direct answer.
            3.If the answer conatins multiple items,put each item on a separate line.
            4.Use this fromat for mutplie items:
                -Item one
                -Item two
                -Item three
            5.If the information cannot be found in the context,say "I couldn't find that information in the available college documents. 
            Context:{context}
            User Question : {query}
            Answer : """

    res = clinet.models.generate_content_stream(
        model="gemini-3.6-flash", contents=prompt
    )

    for chunk in res:
        if chunk.text:
            yield chunk.text
