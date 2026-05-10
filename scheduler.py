import os
import time
import sqlite3
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler

# 添加项目路径
import sys
sys.path.insert(0, os.path.dirname(__file__))

from crawler.hotlist.weibo import fetch_weibo_hotlist
from crawler.hotlist.baidu import fetch_baidu_hotlist
from crawler.hotlist.zhihu import fetch_zhihu_hotlist


DB_PATH = os.path.join(os.path.dirname(__file__), "data", "hotlist.db")


def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS hotlist_snapshots (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            source TEXT NOT NULL,
            title TEXT NOT NULL,
            hot_value INTEGER,
            rank INTEGER,
            label TEXT
        )
    """)
    conn.execute("CREATE INDEX IF NOT EXISTS idx_source_time ON hotlist_snapshots(source, timestamp)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_title ON hotlist_snapshots(title)")
    conn.commit()
    conn.close()


def fetch_and_store():
    sources = {
        "weibo": fetch_weibo_hotlist,
        "baidu": fetch_baidu_hotlist,
        "zhihu": fetch_zhihu_hotlist,
    }
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn = sqlite3.connect(DB_PATH)

    for source, func in sources.items():
        print(f"Fetching {source}...")
        items = func()
        if not items:
            print(f"  {source}: no data fetched")
            time.sleep(1)
            continue

        for item in items:
            conn.execute(
                """INSERT INTO hotlist_snapshots
                   (timestamp, source, title, hot_value, rank, label)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (ts, source, item["title"], item["hot_value"], item["rank"], item["label"])
            )
        print(f"  {source}: stored {len(items)} items")
        time.sleep(1)

    conn.commit()
    conn.close()
    print(f"Snapshot saved at {ts}")


def run_scheduler(interval_minutes=30):
    init_db()
    print("Database initialized")

    # 首次立即执行一次
    print("Fetching initial data...")
    fetch_and_store()

    scheduler = BlockingScheduler()
    scheduler.add_job(fetch_and_store, "interval", minutes=interval_minutes)
    print(f"Scheduler started. Fetching every {interval_minutes} minutes.")
    scheduler.start()


if __name__ == "__main__":
    run_scheduler()