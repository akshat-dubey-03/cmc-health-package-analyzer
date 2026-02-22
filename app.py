import streamlit as st
from scraper import scrape_health_packages
from llm_analyzer import analyze_packages

st.set_page_config(page_title="CMC Health Package Analyzer", page_icon="🚀")

st.title("🚀 CMC Health Package Analyzer")
st.markdown("Paste a health package URL below to analyze pricing and recommendations.")

url = st.text_input("Enter URL", placeholder="https://www.docopd.com/en-in/lab/cmc-vellore")

if st.button("Analyze"):
    if not url:
        st.warning("⚠️ Please enter a URL first.")
    else:
        with st.spinner("🔍 Scraping health packages..."):
            scraped = scrape_health_packages(url)

        if scraped.startswith("Error") or scraped.startswith("No health"):
            st.error(scraped)
        else:
            st.success(f"✅ Scraped {scraped.count(chr(10)) + 1} package entries!")
            with st.expander("📄 Raw Scraped Data"):
                st.text(scraped)

            with st.spinner("🧠 Analyzing with LLM..."):
                result = analyze_packages(scraped)

            st.markdown("---")
            st.markdown("## 📊 Analysis Results")
            st.markdown(result)