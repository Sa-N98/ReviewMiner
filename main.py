from data_scrapper.discovery_search import search_and_filter_apps
from data_scrapper.reviewScrapper import scrape_app_reviews
from analizer.bot import ReportGenerator
from concurrent.futures import ThreadPoolExecutor, as_completed

# scrape_app_reviews('com.imdb.mobile')  
# scrape_app_reviews('com.tozelabs.tvshowtime') 
# scrape_app_reviews('com.moviebase')  

app_report = ReportGenerator('data_scrapper/app_data/com.imdb.mobile_grouped_reviews.json')
# for i in range(1, 6):
#     print(f"Generating report for rating {i}...")
#     app_report.generate_report('us', i)
# app_report.generate_report_for_all_ratings('us')

# for i in range(1, 6):
#     print(f"Generating report for rating {i}...")
#     app_report.generate_report('in', i)
# app_report.generate_report_for_all_ratings('in')

# for i in range(1, 6):
#     print(f"Generating report for rating {i}...")
#     app_report.generate_report('cn', i)
# app_report.generate_report_for_all_ratings('cn')

# Helper function for per-rating generation
def generate_country_rating_report(country, rating):
    print(f"Generating report for rating {rating} in {country}...")
    app_report.generate_report(country, rating)

# Countries and ratings
countries = ['us', 'in', 'cn']
ratings = range(1, 6)

# Use ThreadPoolExecutor to run in parallel
with ThreadPoolExecutor(max_workers=10) as executor:
    futures = []

    # Submit all rating-specific tasks
    for country in countries:
        for rating in ratings:
            futures.append(executor.submit(generate_country_rating_report, country, rating))

    # Wait for all to complete
    for future in as_completed(futures):
        future.result()  # To raise any exception

# Run the "all ratings" summary sequentially (or also in parallel if needed)
for country in countries:
    print(f"Generating summary report for all ratings in {country}...")
    app_report.generate_report_for_all_ratings(country)

