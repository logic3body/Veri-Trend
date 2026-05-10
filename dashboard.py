import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3

DB_PATH = os.path.join(os.path.dirname(__file__), "data", "hotlist.db")


def get_df(query, params=None):
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(query, conn, params=params)
    conn.close()
    return df


def latest_timestamp(source=None):
    conn = sqlite3.connect(DB_PATH)
    if source:
        cur = conn.execute("SELECT MAX(timestamp) FROM hotlist_snapshots WHERE source = ?", (source,))
    else:
        cur = conn.execute("SELECT MAX(timestamp) FROM hotlist_snapshots")
    val = cur.fetchone()[0]
    conn.close()
    return val


st.set_page_config(page_title="热榜趋势追踪", layout="wide")

st.title("热榜趋势追踪 Dashboard")

# 侧边栏导航
page = st.sidebar.radio("导航", ["热度趋势图", "实时热榜"])

if page == "热度趋势图":
    st.header("热度趋势图")

    keyword = st.text_input("输入关键词（逗号分隔多关键词）", placeholder="例如：特朗普, 疫苗")

    if keyword:
        keywords = [k.strip() for k in keyword.split(",") if k.strip()]

        dfs = []
        for kw in keywords:
            df = get_df(
                """SELECT timestamp, source, hot_value, title
                   FROM hotlist_snapshots
                   WHERE title LIKE ?
                   ORDER BY timestamp""",
                (f"%{kw}%",)
            )
            if not df.empty:
                df["keyword"] = kw
                dfs.append(df)

        if not dfs:
            st.info("未找到匹配数据")
        else:
            combined = pd.concat(dfs, ignore_index=True)
            fig = px.line(
                combined,
                x="timestamp",
                y="hot_value",
                color="source",
                facet_row="keyword" if len(keywords) > 1 else None,
                title=f"关键词: {keyword}",
                labels={"hot_value": "热度", "timestamp": "时间", "source": "数据源"}
            )
            fig.update_layout(height=300 * len(keywords))
            st.plotly_chart(fig, use_container_width=True)

            with st.expander("查看原始数据"):
                st.dataframe(combined)

elif page == "实时热榜":
    st.header("实时热榜")

    source = st.selectbox("选择数据源", ["全部", "weibo", "baidu", "zhihu"])

    if source == "全部":
        sources = ["weibo", "baidu", "zhihu"]
    else:
        sources = [source]

    for src in sources:
        ts = latest_timestamp(src)
        if not ts:
            st.subheader(f"微博 (无数据)")
            continue

        df = get_df(
            """SELECT rank, title, hot_value, label
               FROM hotlist_snapshots
               WHERE source = ? AND timestamp = ?
               ORDER BY rank""",
            (src, ts)
        )

        src_name = {"weibo": "微博", "baidu": "百度", "zhihu": "知乎"}[src]
        st.subheader(f"{src_name} 热搜  ({ts})")

        if not df.empty:
            df_display = df.copy()
            df_display["hot_value"] = df_display["hot_value"].apply(lambda x: f"{x:,}")
            st.dataframe(df_display, use_container_width=True, hide_index=True)
        else:
            st.info("无数据")

        st.divider()