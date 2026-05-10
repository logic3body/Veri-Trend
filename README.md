<<<<<<< HEAD
# Spider — 热榜爬虫框架

微博热榜 + 新闻正文提取 + 热度归一化。

## 环境

```bash
conda create -n spider python=3.10
conda install -n spider requests trafilatura -c conda-forge
conda activate spider
```

## 目录结构

```
spider/
├── crawler/
│   ├── hotlist/          # 各数据源热榜爬取
│   │   ├── weibo.py
│   │   ├── baidu.py
│   │   └── zhihu.py
│   └── detail.py         # 新闻正文提取
├── heat_normalizer.py    # 热度归一化
└── config/
    └── heat_max_values.json
```

## 模块

### 微博热榜 crawler/hotlist/weibo.py

```python
from crawler.hotlist.weibo import fetch_weibo_hotlist

hotlist = fetch_weibo_hotlist()
# [{title, hot_value, url, source, rank, label}, ...]
```

返回字段：title / hot_value / url / source='weibo' / rank / label

### 百度热榜 crawler/hotlist/baidu.py

```python
from crawler.hotlist.baidu import fetch_baidu_hotlist

hotlist = fetch_baidu_hotlist()
```

返回字段：title / hot_value / url / source='baidu' / rank / label

### 知乎热榜 crawler/hotlist/zhihu.py

```python
from crawler.hotlist.zhihu import fetch_zhihu_hotlist

hotlist = fetch_zhihu_hotlist()
```

返回字段：title / hot_value / url / source='zhihu' / rank / label

### 正文提取 crawler/detail.py

```python
from crawler.detail import fetch_article_text

text = fetch_article_text("https://36kr.com/p/123456")
# 36kr 用正则提取 <article>；其他域名用 trafilatura
```

- URL 必须以 `https://` 开头，否则返回空串
- 提取失败返回 `"trafilatura failed: {reason}"`

### 热度归一化 heat_normalizer.py

```python
from heat_normalizer import normalize_heat

score = normalize_heat(1000000, "weibo")   # int → float 0-100
score = normalize_heat("12.5万", "zhihu")  # 支持中文"万"字
```

- log10 压缩 + min-max 归一化
- 各站点历史最大值动态更新，写入 `config/heat_max_values.json`
- 缺失值返回 0.0

## 扩展新数据源

在 `crawler/hotlist/` 下新增 `zhihu.py`，实现 `fetch_zhihu_hotlist()` 函数，返回同构数据结构即可。
=======
# Veri-Trend
一个通过数据分析和行为模式识别，来评估社交媒体热搜榜单“真实性”的检测系统（刚刚完成数据爬取部分，发现已经有现有的更好用的工具，暂时留作备份）
>>>>>>> 7305eff152bd16d332dfa324b8f4e85db69c4b6a
