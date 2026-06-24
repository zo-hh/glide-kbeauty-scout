# Glide K-Beauty Brand Scout - Technical Documentation

## 1. Project Overview
The **Glide K-Beauty Brand Scout** is an AI-powered pipeline designed to automate the scouting, evaluation, and shortlisting of South Korean beauty brands for launch in the Indian market. It combines live web scraping, Large Language Model (LLM) analysis, and an interactive data dashboard to provide actionable business intelligence.

## 2. Core Architecture & Files

The pipeline is entirely modular and broken down into the following key files:

*   **`sourcing.py`**: 
    *   **Purpose**: Handles raw data collection.
    *   **Mechanism**: It interfaces with the **Apify API** (specifically the Google Search Scraper). For every brand, it executes a targeted search query: `"{brand_name} korean skincare best seller price ingredients"`. It collects the organic search snippets and meta-descriptions from the first page of Google to form a raw "context block" about the brand's current market standing.

*   **`evaluation.py`**:
    *   **Purpose**: The brain of the pipeline. It reads the raw context fetched by Apify and uses the **Groq LLM API** (`llama-3.1-8b-instant`) to evaluate it.
    *   **Mechanism**: It feeds the raw text into a highly structured prompt schema. It forces the LLM to output a strictly formatted JSON object containing specific numerical scores and analytical justifications. It also contains intelligent error-handling: if the API hits a "Tokens Per Day" rate limit, it automatically falls back to a locally generated "Mock Evaluation" so the pipeline never crashes.

*   **`app.py`**:
    *   **Purpose**: The user-facing frontend dashboard built using **Streamlit**.
    *   **Mechanism**: It houses the curated list of 90 prominent K-Beauty brands. When a user selects brands and clicks "Run Evaluation", this file dynamically triggers `evaluation.py` as a background subprocess. Once the evaluation finishes, it reads the results and renders a pristine, numerical Master Table, and a "Deep Dive Reports" dropdown section for detailed brand metrics. It uses `st.session_state` to permanently save the data so the UI doesn't disappear when interacted with.

*   **`export.py`**:
    *   **Purpose**: Data extraction.
    *   **Mechanism**: Contains the logic to convert the evaluated JSON data into tabular formats (like CSV) for offline analysis.

*   **`brands_list.json` & `evaluated_brands.json`**:
    *   **Purpose**: Intermediate communication files. `app.py` writes the selected brands to `brands_list.json`. `evaluation.py` reads that, processes them, and outputs the final scores to `evaluated_brands.json`. `app.py` then reads that final file to display the dashboard.

---

## 3. Evaluation Criteria & Mathematical Scoring Logic

The AI is strictly barred from "guessing" an overall score. Instead, it is forced to evaluate brands based on a highly specific rubric.

### The 4 Sub-Scores (out of 10 points each)
The LLM reads the scraped web data and assigns four independent scores from 0 to 10:
1.  **Market Fit (10 points):** Grades the brand based on its ingredient compatibility with India's humid climate. It actively looks for lightweight formulations and ingredients like Centella, Niacinamide, and BHA.
2.  **Social Traction (10 points):** Grades the brand based on global viral popularity. It scans the context for keywords like "TikTok viral", "cult favorite", or "bestseller".
3.  **Pricing (10 points):** Grades the brand on its affordability, specifically targeting the Indian masstige demographic (products ideally priced between $15 and $35).
4.  **Innovation (10 points):** Grades the brand on how unique or scientifically advanced their product formulations are (e.g., snail mucin, fermented ingredients).

### The Total Score (/40)
The script takes the four independent sub-scores provided by the LLM and mathematically adds them together. 
*(Formula: Market Fit + Social Traction + Pricing + Innovation = Total Score)*

### The Glide Fit Score (/10)
To provide analysts with a clean, standard 10-point scale, the Python code mathematically calculates the final **Glide Fit Score**. It takes the Total Score (out of 40) and divides it by 4.
*(Formula: Total Score / 4.0)*

### Risk Level
Alongside the numerical scores, the LLM is instructed to provide a qualitative risk assessment. It outputs a `Risk_Level` of either **"High"**, **"Medium"**, or **"Low"**. It determines this by analyzing the market saturation of the brand and the pricing risk (e.g., a highly expensive brand in a saturated market would be flagged as High risk for an Indian launch).

### Analyst Justification
To ensure the scores are trustworthy, the LLM is forced to write a highly analytical, 2-sentence business justification. It must explicitly state exactly why points were awarded or deducted across the four criteria, providing a transparent look into the AI's reasoning.
