# K-Beauty Brand Scouting Pipeline for Glide (MVP)

This document outlines the revised workflow and implementation roadmap for an MVP pipeline to automatically scout, evaluate, and shortlist international K-Beauty brands for the Indian market.

## 1. Evaluation Criteria

The criteria to determine if a K-Beauty brand is a "good fit" for Glide:

1.  **Market Fit & Product Relevance:** Suitable for Indian climate/skin, featuring trending hero ingredients.
2.  **Brand Popularity & Momentum:** Strong global traction and organic demand in India.
3.  **Pricing & Unit Economics:** "Masstige" segment (affordable-premium).
4.  **Market Availability:** Must not already have an exclusive distribution tie-up in India.

## 2. Pipeline Modules (MVP Scope)

We will build this MVP using **Python scripts**, making it easy to run locally, debug, and chain together. The output will be directly pushed to **Google Sheets**.

### Module 1: Sourcing (Brand Discovery)
*   **Goal:** Generate a raw list of potential K-Beauty brands.
*   **Implementation:** A Python script that extracts a list of K-Beauty brands. For the MVP, we can scrape a popular K-Beauty retailer (like Olive Young Global) or use a curated seed list of brands extracted via Apify or standard web scraping (e.g., BeautifulSoup/Playwright).

### Module 2: Evaluation & Scoring
*   **Goal:** Filter and rank the brands based on our criteria.
*   **Implementation:** A Python script that integrates with the **Gemini API**. It takes each brand from Module 1, optionally searches for some brief context (or uses the LLM's internal knowledge if the brand is known), and asks Gemini to assign a "Glide Launch Readiness Score" out of 100, along with a brief justification regarding Indian market fit, estimated pricing, and current availability.

### Module 3: Google Sheets Export
*   **Goal:** Generate a ranked shortlist.
*   **Implementation:** A Python script using the `gspread` library (or `google-api-python-client`) to write the evaluated brands, their scores, and justifications into a formatted Google Sheet, sorted from highest score to lowest.

## 3. Recommended Tools (MVP)

*   **Language:** Python
*   **Sourcing:** `BeautifulSoup`, `requests`, or a lightweight Playwright script (or Apify if dealing with heavy JavaScript rendering).
*   **LLM / AI Analysis:** **Google Gemini API** (`google-generativeai` Python SDK).
*   **Output:** **Google Sheets** API (`gspread`).

## 4. Implementation Roadmap (Module by Module)

*   **Phase 1: Sourcing Module.** Write the Python script to fetch a raw list of K-Beauty brands and save it to a local CSV/JSON file.
*   **Phase 2: Evaluation Module.** Write the script to read the raw list, query the Gemini API for each brand to get a score and analysis, and save the enriched data locally.
*   **Phase 3: Export Module.** Write the script to authenticate with Google Sheets and upload the final ranked data.
