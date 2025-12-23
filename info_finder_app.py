import os
import streamlit as st
from search_utils import search_repo, wiki_search_summary

WORKSPACE_ROOT = os.path.dirname(__file__)

st.set_page_config(page_title="Info Finder", layout="wide")
st.title("Info Finder — 在本地或 Wikipedia 搜尋資訊")

query = st.text_input("輸入查詢內容", value="", placeholder="例如：人工智慧、Python list comprehension")
source = st.radio("搜尋來源", ("Local repo", "Wikipedia"))

if st.button("Search") and query.strip():
    q = query.strip()
    if source == "Local repo":
        with st.spinner("搜尋本機專案檔案..."):
            results = search_repo(q, root=WORKSPACE_ROOT, max_results=50)
        if not results:
            st.info("在本專案中找不到相關結果。")
        else:
            st.markdown(f"**找到 {len(results)} 筆結果（最多顯示 50 筆）**")
            for path, lineno, line in results:
                st.markdown(f"- **{path}** — 行 {lineno}")
                st.code(line)
    else:
        with st.spinner("向 Wikipedia 查詢..."):
            title, summary = wiki_search_summary(q)
        if not title:
            st.info("Wikipedia 查無結果。可嘗試更換關鍵字。")
        else:
            st.header(title)
            st.write(summary)
            st.markdown(f"[在 Wikipedia 上查看]({'https://en.wikipedia.org/wiki/' + title.replace(' ', '_')})")

st.markdown("---")
st.write("使用說明：在上方輸入關鍵字，選擇 `Local repo` 可搜尋專案檔案；選擇 `Wikipedia` 則回傳維基摘要。")