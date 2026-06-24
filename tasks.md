# K-Beauty MVP Pipeline Tasks

- `[x]` **Module 1: Sourcing (Brand Discovery)**
  - `[x]` Create Python script `sourcing.py`
  - `[x]` Implement retailer scraping (Olive Young/YesStyle "Trending"/"New Arrivals")
  - `[x]` Implement secondary sourcing (Reddit / Search)
  - `[x]` Deduplicate brands and export to `brands_list.json`
- `[x]` **Module 2: Evaluation & Scoring**
  - `[x]` Create Python script `evaluation.py`
  - `[x]` Setup Gemini API integration
  - `[x]` Implement evaluation prompt based on Glide criteria
  - `[x]` Process `brands_list.json` and output scored results
- `[x]` **Module 3: Google Sheets Export**
  - `[x]` Create Python script `export.py`
  - `[x]` Setup `gspread` / Google Sheets API integration
  - `[x]` Format and upload the ranked shortlist
