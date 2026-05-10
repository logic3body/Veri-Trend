import time
import warnings
import requests
import re


def fetch_zhihu_hotlist():
    url = "https://api.zhihu.com/topstory/hot-lists/total?limit=50"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": "https://www.zhihu.com/",
    }
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        warnings.warn(f"Failed to fetch zhihu hotlist: {e}")
        return []

    items = data.get("data", [])
    result = []
    for i, item in enumerate(items):
        target = item.get("target", {})
        title = target.get("title", "")
        detail_text = item.get("detail_text", "")
        hot_value = _parse_zhihu_heat(detail_text)
        raw_url = target.get("url", "")
        full_url = "https://www.zhihu.com" + raw_url if raw_url.startswith("/") else raw_url

        result.append({
            "title": title,
            "hot_value": hot_value,
            "url": full_url,
            "source": "zhihu",
            "rank": i + 1,
            "label": "",
        })

    time.sleep(1)
    return result


def _parse_zhihu_heat(detail_text: str) -> int:
    match = re.search(r'([\d.]+)\s*万', detail_text)
    if match:
        num_str = match.group(1)
        try:
            if '.' in num_str:
                return int(float(num_str) * 10000)
            return int(num_str) * 10000
        except ValueError:
            pass
    match = re.search(r'([\d,]+)', detail_text.replace(",", ""))
    if match:
        try:
            return int(match.group(1))
        except ValueError:
            pass
    return 0


if __name__ == "__main__":
    print(fetch_zhihu_hotlist())