import trafilatura

def extract_article_text(url: str):

    downloaded = trafilatura.fetch_url(url)

    if not downloaded:
        return ""

    text = trafilatura.extract(downloaded)

    print(
        "Extracted Length:",
        len(text) if text else 0
    )

    return text or ""