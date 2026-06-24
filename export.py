import json
import os
import pandas as pd

# Attempt to import gspread for Google Sheets
try:
    import gspread
    GSPREAD_AVAILABLE = True
except ImportError:
    GSPREAD_AVAILABLE = False

def export_to_csv(data, filename="glide_kbeauty_shortlist.csv"):
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    print(f"[+] Saved {len(data)} brands locally to {filename}")

def export_to_google_sheets(data, sheet_name="Glide K-Beauty Shortlist"):
    if not GSPREAD_AVAILABLE:
        print("[-] gspread not installed. Please `pip install gspread`.")
        return False
        
    creds_file = "credentials.json"
    if not os.path.exists(creds_file):
        print(f"[-] Google Sheets credentials '{creds_file}' not found.")
        print("    Please create a Service Account in GCP and download the JSON.")
        return False
        
    try:
        gc = gspread.service_account(filename=creds_file)
        
        # Try to open existing, or create new
        try:
            sh = gc.open(sheet_name)
        except gspread.SpreadsheetNotFound:
            print(f"[*] Creating new Google Sheet: {sheet_name}")
            # Note: This creates the sheet in the Service Account's drive.
            # You must share the sheet with your personal email!
            sh = gc.create(sheet_name)
            
        worksheet = sh.sheet1
        
        # Clear existing data
        worksheet.clear()
        
        # Prepare data for insertion (list of lists)
        header = ["Brand", "Score", "Hero Product", "Est Price", "Key Ingredients", "Justification"]
        rows = [header]
        for item in data:
            rows.append([
                item.get("Brand", ""), 
                item.get("Score", 0), 
                item.get("Hero_Product", ""), 
                item.get("Est_Price", ""), 
                item.get("Key_Ingredients", ""), 
                item.get("Justification", "")
            ])
            
        worksheet.update(range_name='A1', values=rows)
        print(f"[+] Successfully exported {len(data)} rows to Google Sheet: '{sheet_name}'")
        print(f"    URL: {sh.url}")
        return True
    except Exception as e:
        print(f"  [!] Failed to export to Google Sheets: {e}")
        return False

def run_export(input_file="evaluated_brands.json"):
    if not os.path.exists(input_file):
        print(f"Input file {input_file} not found! Run evaluation.py first.")
        return

    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    if not data:
        print("No data to export.")
        return
        
    print(f"Loaded {len(data)} evaluated brands for export.")
    
    # Always save a local copy as backup
    export_to_csv(data)
    
    # Attempt Google Sheets export
    success = export_to_google_sheets(data)
    if not success:
        print("[*] Skipped Google Sheets export. You can rely on the local CSV for now.")

if __name__ == "__main__":
    run_export()
