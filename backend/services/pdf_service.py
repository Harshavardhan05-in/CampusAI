import pymupdf as fitz
import re


# This functions takes one page and extarct each line from that page ad clean it and combine with the previous linie if it is a continuation and then return that page
def clean_text(text):
    text = re.sub(r"[ \t]+", " ", text)

    lines = text.split("\n")

    cleaned_lines = []

    for line in lines:
        line = line.strip()

        if not line:
            continue

        if cleaned_lines:
            previous_line = cleaned_lines[-1]

            is_continuation = (
                not line.startswith(
                    (
                        "-",
                        "*",
                    )
                )
                and not re.match(r"^\d+\.", line)
                and not re.match(r"^[a-z]\.", line)
                and not re.match(
                    r"^(Step|Important|Key|Exit|Note):", line, re.IGNORECASE
                )
                and not previous_line.endswith((".", ":", "?", "!"))
            )

            if is_continuation:
                cleaned_lines[-1] += " " + line
                continue

        cleaned_lines.append(line)

    return "\n".join(cleaned_lines)


# This fcution takes the entire pdf text and extarct each page from it and pass it to other function and then return the cleaned text in List Form
def extract_text_from_pdf(pdf_path):
    document = fitz.open(pdf_path)

    pages_text = []

    for page_num, page in enumerate(document, start=1):
        text = page.get_text()

        text = clean_text(text)

        pages_text.append({"text": text, "page": page_num, "source": pdf_path})

    document.close()

    return pages_text
