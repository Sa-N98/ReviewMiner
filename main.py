from data_scrapper.discovery_search import search_and_filter_apps
from data_scrapper.reviewScrapper import scrape_app_reviews
from analizer.bot import ReportGenerator

# scrape_app_reviews('com.imdb.mobile')  
# scrape_app_reviews('com.tozelabs.tvshowtime') 
# scrape_app_reviews('com.moviebase')  

usa_report = ReportGenerator('data_scrapper/app_data/com.imdb.mobile_grouped_reviews.json')
for i in range(1, 6):
    print(f"Generating report for rating {i}...")
    usa_report.generate_report('us', i)

for i in range(1, 6):
    print(f"Generating report for rating {i}...")
    usa_report.generate_report('in', i)

for i in range(1, 6):
    print(f"Generating report for rating {i}...")
    usa_report.generate_report('cn', i)