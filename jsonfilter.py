# --- JSON Filter Function ---
def extract_reviews_from_json(json_data, countries=['us', 'in', 'cn'], ratings=[1, 2, 3, 4, 5]):
    reviews_list = []
    ratings_str = [str(r) for r in ratings]  # Ensure keys are strings

    for country in countries:
        country_reviews = json_data.get("reviews", {}).get(country, {})
        for rating in ratings_str:
            rating_reviews = country_reviews.get(rating, [])
            for review in rating_reviews:
                reviews_list.append(review.get("review", ""))

    return reviews_list
# Example usage:
# json_data = {     
#     "reviews": {
#         "us": {   
#             "1": [{"review": "Terrible app!"}],
#             "2": [{"review": "Not great."}],  
#             "3": [{"review": "Average."}],
#             "4": [{"review": "Good."}],
#             "5": [{"review": "Excellent!"}]
#         },..
#         "in": {
#             "1": [{"review": "Bad app!"}],                
#             "2": [{"review": "Could be better."}],
#             "3": [{"review": "Okay."}],
#             "4": [{"review": "Good."}],
#             "5": [{"review": "Great!"}]            
#         }
#     }    
# }
# reviews = extract_reviews_from_json(json_data)
# print(reviews)    