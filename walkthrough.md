# MVP K-Beauty Scouting Pipeline

I have set up the complete MVP pipeline as a local Python project. You can now explore and modify the code directly in VS Code.

## Project Structure

*   `main.py`: The main orchestrator. Run this file to execute the pipeline end-to-end.
*   `sourcing.py`: (Module 1) Handles discovery of brands from Olive Young, YesStyle, and Reddit.
*   `evaluation.py`: (Module 2) Feeds the discovered brands into the Gemini API for scoring.
*   `export.py`: (Module 3) Takes the scored data, exports it to a local CSV, and attempts to push to Google Sheets.
*   `.env`: Environment variables configuration file.

## Setup Instructions

### 1. Set up your Gemini API Key
To enable actual LLM analysis instead of the mock data:
1. Open the `.env` file in VS Code.
2. Replace `your_api_key_here` with your actual Google Gemini API key.
*(If you run the script without a key, it will use a built-in mock evaluator so you can still test the pipeline flow!)*

### 2. Set up Google Sheets Integration (Optional for now)
By default, `export.py` will generate a `glide_kbeauty_shortlist.csv` locally. If you want it to push directly to Google Sheets:
1. Run `pip install gspread`.
2. Go to the [Google Cloud Console](https://console.cloud.google.com/), enable the Google Drive and Google Sheets APIs.
3. Create a Service Account, generate a JSON key, and save it in this directory as `credentials.json`.
4. Share your target Google Sheet with the Service Account email address.

## How to Run

To run the entire end-to-end pipeline, open your VS Code integrated terminal and run:

```bash
python main.py
```

## Next Steps
This MVP proves the architecture! For Phase 2, we can swap the simplified web scrapers for full Apify integration to grab hundreds of brands at once, or we can fine-tune the Gemini prompt to be even stricter about the "Masstige" price point.
