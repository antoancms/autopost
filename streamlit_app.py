import streamlit as st
from autoposter import fetch_article, summarize, post_to_wordpress

st.title("Link to WordPress Autoposter")

url = st.text_input("Source URL")
site_url = st.text_input("WordPress Site URL")
username = st.text_input("WordPress Username")
app_password = st.text_input("Application Password", type="password")
title = st.text_input("Post Title")

if st.button("Generate & Post"):
    if not all([url, site_url, username, app_password, title]):
        st.error("All fields are required")
    else:
        with st.spinner("Fetching and posting..."):
            try:
                article = fetch_article(url)
                summary = summarize(article)
                response = post_to_wordpress(site_url, username, app_password, title, summary)
                st.success(f"Posted! ID: {response.get('id')}")
                st.write(response)
            except Exception as exc:
                st.error(f"Failed: {exc}")
