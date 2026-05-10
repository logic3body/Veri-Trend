import re


def fetch_article_text(url: str) -> str:
    if not url.startswith("https://"):
        return ""

    if "36kr.com" in url:
        return _fetch_36kr(url)

    return _fetch_trafilatura(url)


def _fetch_36kr(url: str) -> str:
    try:
        import requests
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        html = resp.text
    except Exception:
        return ""

    article_match = re.search(r'<article[^>]*>(.*?)</article>', html, re.DOTALL)
    if not article_match:
        return ""

    article_html = article_match.group(1)
    paragraphs = re.findall(r'<p[^>]*>(.*?)</p>', article_html, re.DOTALL)

    texts = []
    for p in paragraphs:
        text = re.sub(r'<[^>]+>', '', p).strip()
        if text:
            texts.append(text)

    return "\n".join(texts)


def _fetch_trafilatura(url: str) -> str:
    try:
        import trafilatura
        downloaded = trafilatura.fetch_url(url)
        if downloaded is None:
            return "trafilatura failed: fetched None"
        result = trafilatura.extract(downloaded)
        if result is None:
            return "trafilatura failed: extract returned None"
        return result
    except Exception as e:
        return f"trafilatura failed: {e}"


if __name__ == "__main__":
    print(fetch_article_text("https://36kr.com/p/123456"))