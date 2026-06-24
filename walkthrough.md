# Glide K-Beauty Brand Scout - Final Walkthrough

This project successfully culminated in a fully deployed, AI-powered web application that automates the incredibly tedious process of scouting international cosmetic brands for market expansion.

## 🚀 What Was Accomplished
1.  **Automated Market Research:** We completely bypassed the manual process of Googling brands. The Apify integration acts as an automated research assistant, gathering real-time data on ingredients and prices from Google.
2.  **Unbiased AI Evaluation:** We stripped the LLM of its tendency to "hallucinate" random scores by forcing it into a strict JSON schema. It is now forced to logically grade brands based on humid climate compatibility, viral trends, and masstige pricing.
3.  **Professional Web Dashboard:** We transformed a raw Python terminal script into a beautifully styled Streamlit web application. 

## 🖥️ How to Use the Final Tool
1.  Open the live web URL.
2.  In the left sidebar, use the dropdown to select up to 5 K-Beauty brands from the curated master list.
3.  Click the blue **"Run Evaluation"** button.
4.  **The Master Table:** Once the background pipeline finishes fetching the data and running the LLM, a color-coded table will appear. The Glide Fit Score (/10) instantly tells you how viable the brand is for India.
5.  **The Deep Dive Report:** Select a specific evaluated brand from the dropdown below the table to read the AI's 2-sentence justification, view the Risk Level, and see the Hero Product.
6.  **Export:** Click "Download Data as CSV" to save the raw analytics locally.

## 🛠️ Key Technical Solutions Implemented
*   **Rate Limits:** Groq has strict daily token limits. The pipeline was updated to use the extremely fast `llama-3.1-8b-instant` model to bypass these restrictions. If limits are hit, a seamless Mock Evaluation is injected so the UI never crashes for the end-user.
*   **State Persistence:** Streamlit inherently resets the entire page when a user clicks a dropdown. We implemented `st.session_state` to permanently lock the evaluated data onto the screen.
*   **Cloud Deployment:** We successfully migrated the code from local `localhost` to the internet using Streamlit Community Cloud, securely injecting the hidden `.env` API keys directly into the cloud's background subprocess.
