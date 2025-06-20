from google_play_scraper import reviews, app
from datetime import datetime, timedelta
import json
import time

# --- Constants ---
LANG = 'en'
COUNTRIES = ['us', 'in', 'cn']
REVIEW_LIMIT = 5000
MIN_REVIEW_LENGTH = 100
YEARS_BACK = 3

# --- Time filter ---
cutoff_date = datetime.now() - timedelta(days=YEARS_BACK * 365)


def scrape_app_reviews(app_id):
    final_reviews = {}

    # --- Fetch app name ---
    try:
        app_info = app(app_id, lang=LANG, country="us")
        app_name = app_info.get("title", "Unknown App")
    except Exception as e:
        print(f"❌ Failed to fetch app name: {e}")
        app_name = "Unknown App"

    def fetch_reviews_for_country(country):
        token = None
        total_reviews = 0
        country_reviews = {1: [], 2: [], 3: [], 4: [], 5: []}

        while True:
            try:
                result, token = reviews(
                    app_id,
                    lang=LANG,
                    country=country,
                    count=200,
                    continuation_token=token
                )
            except Exception as e:
                print(f"❌ Error for {country}: {e}")
                break

            # Filter reviews
            new_valid_reviews = 0
            for r in result:
                if r['at'] >= cutoff_date and len(r['content']) >= MIN_REVIEW_LENGTH:
                    country_reviews[r['score']].append({
                        'at': r['at'].isoformat(),
                        'review': r['content']
                    })
                    new_valid_reviews += 1

            total_reviews += len(result)
            print(f"[{country.upper()}] Total fetched: {total_reviews}, Valid in this batch: {new_valid_reviews}")

            if new_valid_reviews == 0 or not token or total_reviews >= REVIEW_LIMIT:
                break

            time.sleep(1)

        flat_count = sum(len(v) for v in country_reviews.values())
        return country_reviews if flat_count > 0 else None

    # --- Loop over countries ---
    for country in COUNTRIES:
        print(f"\n🌍 Fetching reviews from {country.upper()}...")
        country_result = fetch_reviews_for_country(country)
        if country_result:
            final_reviews[country] = country_result
        else:
            print(f"⚠️  No valid reviews found for {country.upper()}")

    # --- Save to JSON if data is found ---
    if final_reviews:
        output = {
            "app_name": app_name,
            "app_id": app_id,
            "reviews": final_reviews
        }

        file_name = f'{app_id}_grouped_reviews.json'
        with open(file_name, 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=2)

        print(f"\n✅ Done! Saved to '{file_name}'")
    else:
        print(f"\n⛔ No reviews found from any country for {app_id}. File not saved.")
