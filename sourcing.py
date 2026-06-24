import os
import json
import re
from dotenv import load_dotenv

try:
    from apify_client import ApifyClient
    APIFY_AVAILABLE = True
except ImportError:
    APIFY_AVAILABLE = False

load_dotenv()

def scrape_brands_with_apify():
    print("Scraping K-Beauty brands using Apify (Google Search Scraper)...")
    brands = set()
    
    apify_token = os.getenv("APIFY_API_TOKEN")
    if not APIFY_AVAILABLE or not apify_token or apify_token == "your_apify_token_here":
        print("  [-] Apify token not found or apify-client not installed.")
        print("  [-] Falling back to robust seed list for Phase 2 MVP.")
        return ["Torriden", "Round Lab", "Anua", "Skin1004", "Numbuzin", "Isntree", "Mixsoon", "TirTir", "Purito", "I'm From", "Amuse", "Rom&nd", "AOU"]
        
    try:
        client = ApifyClient(apify_token)
        
        # Prepare the Actor input
        run_input = {
            "queries": "top emerging korean skincare brands 2024\ntrending k-beauty brands list",
            "maxPagesPerQuery": 1,
            "resultsPerPage": 20,
        }
        
        print("  [*] Calling Apify actor: apify/google-search-scraper...")
        run = client.actor("apify/google-search-scraper").call(run_input=run_input)
        
        print("  [*] Fetching results from Apify dataset...")
        
        # Handle dict or Run object
        if isinstance(run, dict):
            ds_id = run.get("defaultDatasetId")
        else:
            ds_id = getattr(run, "default_dataset_id", getattr(run, "defaultDatasetId", None))
            
        full_text = ""
        for item in client.dataset(ds_id).iterate_items():
            for organic_result in item.get("organicResults", []):
                snippet = organic_result.get("description", "")
                title = organic_result.get("title", "")
                full_text += f"{title} {snippet}\n"
                
        print("  [*] Using Groq AI to extract strictly authentic K-Beauty brands from the search text...")
        import groq
        groq_client = groq.Groq(api_key=os.getenv("GROQ_API_KEY"))
        prompt = f"Extract a JSON list of strictly authentic, distinct K-Beauty (Korean skincare/makeup) brand names mentioned in the following text. Do NOT include generic words like 'cream', 'acid', 'skincare', 'bha'. Return ONLY a raw JSON array of strings, absolutely no markdown or other text. Text:\n{full_text}"
        
        response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1
        )
        
        output_text = response.choices[0].message.content.replace('```json', '').replace('```', '').strip()
        extracted_brands = json.loads(output_text)
        
        for b in extracted_brands:
            brands.add(b)
                        
    except Exception as e:
        print(f"  [!] Error calling Apify: {e}")
        print("  [-] Falling back to robust seed list.")
        return ["Torriden", "Round Lab", "Anua", "Skin1004", "Numbuzin", "Isntree", "Mixsoon", "TirTir", "Purito", "I'm From"]
        
    print(f"  [+] Extracted {len(brands)} potential brands from Apify search.")
    return list(brands)

def deduplicate_and_save(lists_of_brands, output_file="brands_list.json"):
    all_brands = []
    for brand_list in lists_of_brands:
        all_brands.extend(brand_list)
    
    # Basic cleanup
    cleaned_brands = set()
    for b in all_brands:
        clean_b = re.sub(r'[^a-zA-Z0-9\s-]', '', b).strip().upper()
        if len(clean_b) > 2 and clean_b not in ["NEW", "BEST", "SALE", "TRENDING"]:
            cleaned_brands.add(clean_b)
            
    # Shuffle the brands so we get a good mix instead of just A, B, and C
    import random
    final_list = list(cleaned_brands)
    random.seed(42) # deterministic but mixed
    random.shuffle(final_list)
    final_list = final_list[:20]
    
    print(f"\nFinal Deduplicated List: Found {len(final_list)} unique brands (capped at 20).")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(final_list, f, indent=4)
    print(f"Saved to {output_file}")
    
    return final_list

if __name__ == "__main__":
    apify_brands = scrape_brands_with_apify()
    deduplicate_and_save([apify_brands], output_file="brands_list.json")
