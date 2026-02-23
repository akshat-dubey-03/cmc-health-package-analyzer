# 🚀 CMC Health Package Analyzer

## 🚀 Live Demo

Use the app directly here:
https://cmc-health-package-analyzer-ndufwpzn9eyzq4l2cbpfem.streamlit.app/

## 📌 Overview
An LLM-powered healthcare package analyzer that:

- Scrapes real-time health package data
- Extracts structured information
- Compares pricing and parameters
- Generates ratings & recommendations

---

## 🧠 Problem Statement
Patients often struggle to compare health checkup packages based on:

- Price differences  
- Number of tests included  
- Discount percentages  
- Overall value  

This tool automates extraction and provides structured comparison with recommendations.

---

## 🛠 Tech Stack
- Python  
- Requests  
- BeautifulSoup  
- OpenAI / LLM API  
- Prompt Engineering  
- Streamlit (for web interface – optional upgrade)

---

## ⚙️ Architecture
User → Scraper → Cleaned Text → LLM Analyzer → Structured Output
// how it works on the backend part 
User → Streamlit UI  
→ Scraper Module  
→ LLM Analyzer (OpenRouter API)  
→ Structured Markdown Output  
→ Recommendation Engine

## 📊 Features

- Extracts all available health packages
- Calculates discount percentage
- Generates value-based star ratings
- Provides recommendations for:
  - Young adults
  - Senior citizens
  - Budget users

---

##  Sample Output (Full Scrollable Version)

You can view the complete real output here:

https://akshat-dubey-03.github.io/cmc-health-package-analyzer/



## 🔮 Future Improvements

- Deploy as production web app
- Add filtering and sorting
- Add vector search for package comparison
- Add cost analytics dashboard


## 👨‍💻 Author

Akshat Dubey  
CSE (AI & Data Engineering) Student  
Aspiring AI Engineer

