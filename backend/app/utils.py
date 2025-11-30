import pdfplumber


def parse_pdf(filepath):
    """
    Extract text from a PDF file using pdfplumber.
    """

    text = ""

    with pdfplumber.open(filepath) as pdf:
        for page in pdf.pages:
            content = page.extract_text()
            if content:
                text += content + "\n"

    return text