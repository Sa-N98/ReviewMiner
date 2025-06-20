from reviewScrapper import scrape_app_reviews
from discovery_search import search_and_filter_apps
from jsonfilter import extract_reviews_from_json
from analyser import analyze_in_reviews

import json

# Manually scrape specific apps

# scrape_app_reviews('com.imdb.mobile')        # IMDb
# scrape_app_reviews('com.tozelabs.tvshowtime')    # TV Time
# scrape_app_reviews('com.moviebase')    # MyShows
# scrape_app_reviews('com.jonathanantoine.TVST')
# scrape_app_reviews('com.zammly.moviefy')    #   com.zammly.moviefy

# Automated search and review scraping

# apps = search_and_filter_apps("movie tracker", max_results=50, min_downloads=100_000, min_rating=4.0)
# for app in apps:
#     print(f"{app['app_name']}")
#     scrape_app_reviews(app['app_id']) 

with open('com.imdb.mobile_grouped_reviews.json', 'r', encoding="utf-8") as f:
    reviews_data = json.load(f)

reviews_list =extract_reviews_from_json(reviews_data, countries=['us', 'in', 'cn'], ratings=[2, 3, 4])
final_summary = analyze_in_reviews(reviews_list, chunk_size=300)
# print("\n\nFinal UX Summary:\n", final_summary)

with open("final_ux_summary.md", "w", encoding="utf-8") as f:
    f.write(final_summary)
print("📄 Final summary saved to 'final_ux_summary.md'")