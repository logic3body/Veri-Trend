import json
import math
import os


CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config", "heat_max_values.json")


def normalize_heat(heat, source):
    if heat is None or heat == "" or heat == 0:
        return 0.0

    if isinstance(heat, str):
        heat = _parse_chinese_number(heat)
        if heat is None:
            return 0.0

    heat = float(heat)

    max_values = _load_max_values()
    max_val = max_values.get(source, 1000000)

    if heat > max_val:
        max_val = heat
        _save_max_values({**max_values, source: max_val})

    log_val = math.log10(heat + 1)
    log_max = math.log10(max_val + 1)

    normalized = (log_val / log_max) * 100 if log_max > 0 else 0.0
    return round(normalized, 1)


def _parse_chinese_number(value: str) -> float | None:
    value = value.strip()
    try:
        return float(value)
    except ValueError:
        pass

    wan_match = value.replace("万", "").replace("万", "")
    try:
        num = float(wan_match)
        return num * 10000
    except ValueError:
        return None


def _load_max_values() -> dict:
    if not os.path.exists(CONFIG_PATH):
        return {}
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def _save_max_values(data: dict):
    os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    print(normalize_heat(1000000, "weibo"))