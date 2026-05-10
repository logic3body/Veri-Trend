import time
import json
import urllib.parse
import warnings
import requests


def fetch_weibo_hotlist():
    url = "https://weibo.com/ajax/side/hotSearch"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": "https://weibo.com/",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "X-Requested-With": "XMLHttpRequest",
    }
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        warnings.warn(f"Failed to fetch weibo hotlist: {e}")
        return []

    realtime = data.get("data", {}).get("realtime", [])
    result = []
    for i, item in enumerate(realtime):
        word = item.get("word", "")
        num = item.get("num", 0)
        label = item.get("label", "")

        if item.get("url"):
            item_url = item["url"]
        else:
            item_url = f"https://s.weibo.com/weibo?q={urllib.parse.quote(word)}"

        result.append({
            "title": word,
            "hot_value": num,
            "url": item_url,
            "source": "weibo",
            "rank": i + 1,
            "label": label,
        })

    time.sleep(1)
    return result


if __name__ == "__main__":
    print(fetch_weibo_hotlist())