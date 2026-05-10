import time
import warnings
import requests


def fetch_baidu_hotlist():
    url = "https://top.baidu.com/board?tab=realtime"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": "https://top.baidu.com/",
    }
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()
        html = resp.text
    except Exception as e:
        warnings.warn(f"Failed to fetch baidu hotlist: {e}")
        return []

    json_str = _extract_json(html)
    if not json_str:
        warnings.warn("Failed to extract baidu hotlist JSON")
        return []

    import json
    try:
        data = json.loads(json_str)
    except Exception as e:
        warnings.warn(f"Failed to parse baidu JSON: {e}")
        return []

    cards = data.get("data", {}).get("cards", [])
    if not cards:
        return []
    content = cards[0].get("content", [])
    if not content:
        return []

    result = []
    for i, item in enumerate(content):
        word = item.get("word", "")
        hot_score_str = item.get("hotScore", "0")
        try:
            hot_value = int(hot_score_str)
        except ValueError:
            hot_value = 0

        tag_map = {"1": "新", "3": "热", "16": "沸"}
        hot_tag = item.get("hotTag", "0")
        label = tag_map.get(hot_tag, "")

        result.append({
            "title": word,
            "hot_value": hot_value,
            "url": item.get("url", ""),
            "source": "baidu",
            "rank": i + 1,
            "label": label,
        })

    time.sleep(1)
    return result


def _extract_json(html: str) -> str:
    marker = 'data:{"data":{'
    idx = html.find(marker)
    if idx == -1:
        return ""
    start = idx + len('data:')
    depth = 0
    i = start
    while i < len(html):
        ch = html[i]
        if ch == '{':
            depth += 1
        elif ch == '}':
            depth -= 1
            if depth == 0:
                return html[start:i+1]
        i += 1
    return ""


if __name__ == "__main__":
    print(fetch_baidu_hotlist())