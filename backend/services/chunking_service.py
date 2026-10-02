import re


# This Function Takes Array of pages from our pdf(which is cleaned , processed and structed) and make it into chunks and return all those chunks as an array
def create_chunks(pages, chunk_size=500):

    chunks = []

    for page in pages:
        text = page["text"]

        sections = text.split("\n")

        current_chunk = ""

        for section in sections:
            section = section.strip()

            if not section:
                continue

            if len(current_chunk) + len(section) + 1 <= chunk_size:
                current_chunk = current_chunk + section + "\n"
            else:
                if current_chunk.strip():
                    chunks.append(
                        {
                            "text": current_chunk.strip(),
                            "page": page["page"],
                            "source": page["source"],
                        }
                    )
                current_chunk = section + "\n"

        if current_chunk.strip():
            chunks.append(
                {
                    "text": current_chunk.strip(),
                    "page": page["page"],
                    "source": page["source"],
                }
            )
    return chunks
