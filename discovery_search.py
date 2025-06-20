from google_play_scraper import search, app
import json
import time

def parse_downloads(installs_str):
    """Convert '1,000,000+' to integer 1000000"""
    return int(installs_str.replace('+', '').replace(',', '').strip())

def search_and_filter_apps(keyword, max_results=30, min_downloads=100_000, min_rating=4.0):
    # Step 1: Search apps
    results = search(
        keyword,
        lang="en",
        country="us",
        n_hits=max_results
    )

    filtered_apps = []

    # Step 2: Fetch full app data and filter
    for entry in results:
        app_id = entry['appId']
        try:
            app_data = app(app_id, lang="en", country="us")

            installs = parse_downloads(app_data.get("installs", "0"))
            rating = app_data.get("score", 0)

            if installs >= min_downloads and rating >= min_rating:
                filtered_apps.append({
                    "app_name": app_data["title"],
                    "app_id": app_data["appId"],
                    "installs": installs,
                    "rating": rating
                })

            time.sleep(0.5)  # avoid getting rate-limited

        except Exception as e:
            print(f"⚠️ Error loading app {app_id}: {e}")

    # Save results to file
    file_name = f"filtered_apps_{keyword.replace(' ', '_')}.json"
    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump(filtered_apps, f, ensure_ascii=False, indent=2)

    print(f"\n✅ Found {len(filtered_apps)} filtered apps. Saved to {file_name}")
    return filtered_apps

