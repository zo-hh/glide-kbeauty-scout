import time
from sourcing import scrape_brands_with_apify, deduplicate_and_save
from evaluation import process_evaluations
from export import run_export

def run_pipeline():
    print("="*50)
    import json
    import sys
    
    if len(sys.argv) > 1:
        mode = sys.argv[1].strip().lower()
        if mode == "single" and len(sys.argv) > 2:
            brand_input = sys.argv[2].strip()
        else:
            brand_input = "COSRX"
    else:
        mode = input("\nDo you want to evaluate a [single] brand, or run the full [batch]? (single/batch): ").strip().lower()
        if mode == "single":
            brand_input = input("Enter the brand name to evaluate: ").strip()
    
    if mode == "single":
        brand = brand_input
        print(f"\n--- [Single Brand Mode: {brand}] ---")
        # Overwrite brands_list.json directly
        with open("brands_list.json", "w", encoding="utf-8") as f:
            json.dump([brand], f, indent=4)
    else:
        # Module 1: Sourcing
        print("\n--- [Module 1: Sourcing] ---")
        apify_brands = scrape_brands_with_apify()
        deduplicate_and_save([apify_brands], output_file="brands_list.json")
    
    # Module 2: Evaluation
    print("\n--- [Module 2: Evaluation & Scoring] ---")
    process_evaluations(input_file="brands_list.json", output_file="evaluated_brands.json")
    
    # Module 3: Export
    print("\n--- [Module 3: Export] ---")
    run_export(input_file="evaluated_brands.json")
    
    print("\n" + "="*50)
    print("✅ PIPELINE COMPLETE!")
    print("="*50)

if __name__ == "__main__":
    run_pipeline()
