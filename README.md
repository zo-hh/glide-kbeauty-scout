# Glide K-Beauty Brand Scout 

Welcome to the **Glide K-Beauty Brand Scout**! This is an AI-powered pipeline designed specifically to automate the scouting, evaluation, and shortlisting of South Korean beauty brands for market launch in India. 

This project was built for analytical precision, combining live web scraping with Large Language Model (LLM) reasoning to evaluate brands on a strict rubric of market fit, social traction, pricing, and innovation.

---

## Live Demo
The project is fully deployed on Streamlit Community Cloud! You can interact with the live dashboard and run AI evaluations here:
**https://glide-kbeauty-scout-mamsfnvqwshvulzxo6su2w.streamlit.app/**

---

## Documentation
For a very detailed, step-by-step breakdown of how the AI pipeline works, how the scores are calculated, and what each Python file does, please read the [DOCUMENTATION.md](./DOCUMENTATION.md) file included in this repository.

Additionally, you can review the [implementation_plan.md](./implementation_plan.md) for a high-level overview of the final architecture, and the [walkthrough.md](./walkthrough.md) for a quick user guide on navigating the dashboard.

---

##  Project Features
*   **Interactive Dashboard:** A sleek, custom-styled frontend built with Streamlit that permanently saves your evaluation state.
*   **Live Web Scraping:** Uses the Apify Google Search API to dynamically pull the most recent market context, SEO descriptions, and trending data for any brand.
*   **Groq AI Evaluation:** Passes the scraped context into a lightning-fast `llama-3.1-8b-instant` model to score the brand strictly out of 40 points (normalized to a `/10` Glide Fit Score).
*   **Analytical Justifications:** The LLM does not guess; it outputs a strict JSON object with calculated risk levels and a 2-sentence business justification for its scores.
*   **Data Export:** A native 1-click button to download the entire AI evaluation table as a clean CSV file.

---

## Running it Locally

If you want to run the pipeline on your own computer instead of the cloud:

### 1. Install Dependencies
Make sure you have Python installed, then run:
```bash
pip install -r requirements.txt
```

### 2. Setup API Keys
Create a file named `.env` in the root folder and add your API keys:
```text
GROQ_API_KEY=your_groq_key_here
APIFY_API_TOKEN=your_apify_key_here
```

### 3. Launch the Dashboard
Run the Streamlit application:
```bash
streamlit run app.py
```

---
*Developed by Zuhrat Ul Wardh.*
