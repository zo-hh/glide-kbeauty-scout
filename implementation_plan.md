# Glide K-Beauty Brand Scout - Final Implementation Plan

## Goal Description
The objective of this project was to construct an end-to-end, AI-driven market intelligence pipeline to assist Glide in identifying and shortlisting South Korean beauty brands for potential launch in the Indian masstige market. The pipeline automates web scraping, qualitative market evaluation using a Large Language Model (LLM), and provides an interactive Streamlit dashboard for business analysts.

## Final Architecture

### 1. Data Sourcing (`sourcing.py`)
*   **API Used:** Apify Google Search Scraper.
*   **Logic:** Executes dynamic search queries (e.g., `"{brand_name} korean skincare best seller price ingredients"`) to collect real-time SEO descriptions, trending keywords, and product snippets directly from Google's first page. This circumvents the knowledge cutoff date of traditional LLMs.

### 2. AI Evaluation Pipeline (`evaluation.py`)
*   **LLM Used:** Groq Cloud `llama-3.1-8b-instant`.
*   **Logic:** Ingests the scraped context and enforces a strict mathematical rubric. 
*   **Metrics Evaluated:**
    *   **Market Fit (10 pts):** Humid climate compatibility and ingredients (Centella, Niacinamide).
    *   **Social Traction (10 pts):** Viral and trend status.
    *   **Pricing (10 pts):** Masstige affordability ($15 - $35).
    *   **Innovation (10 pts):** Unique formulations and scientific backing.
*   **Score Normalization:** Computes a Total Score (/40) and divides by 4 to generate the final **Glide Fit Score (/10)**.
*   **Fallbacks:** Implements an automated DuckDuckGo Search fallback if Apify fails, and a Mock Evaluation engine if the Groq API daily rate limit is completely exhausted.

### 3. Interactive UI (`app.py`)
*   **Framework:** Streamlit Community Cloud.
*   **Logic:** Provides a clean "Master-Detail" UI. The main view is a custom-colored pandas dataframe highlighting the Glide Fit Score and Market Fit. The detail view is a "Deep Dive Report" select box that extracts the AI's 2-sentence analytical justification and the qualitative Risk Level (High/Medium/Low).

### 4. Data Extraction (`export.py`)
*   **Logic:** Bypasses complex Google Sheets API setups by offering a native, 1-click **Download CSV** button directly inside the Streamlit web app, allowing analysts to instantly export the AI's findings.
