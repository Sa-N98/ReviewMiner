import json
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from dotenv import load_dotenv
import os
import re


with open("analizer/template-2.txt", "r") as file:
    report_template = file.read()

load_dotenv()

# --- LLM Setup (OpenRouter-compatible with streaming output) ---
llm = ChatOpenAI(
    openai_api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url=os.getenv("OPENROUTER_BASE_URL"),
    model="deepseek/deepseek-r1:free",
    streaming=True,
    callbacks=[]
)

prompt_template = PromptTemplate(
    template= report_template,
    input_variables=["reviews"]
    )

chain = prompt_template | llm

# # 🚀 Streaming the output manually
# for chunk in chain.stream({"reviews": "hi"}):
#     print(chunk.content, end="", flush=True)



class ReportGenerator:
    def __init__(self, jason_file_path):
        with open(jason_file_path, "r", encoding="utf-8") as file:
            self.data = json.load(file)
        self.directory = "app_reports"
    
    def generate_report(self, country_code:str, rating:int):
        reviews = ''
        for i,review in enumerate(self.data['reviews'][country_code][str(rating)]):
            reviews += (f'{i+1} {review["review"]} \n')
        print(reviews)

         # Set the filename
        filename = f"report_{self.data['app_id']}_{country_code}_{rating}.md"
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)
        path = os.path.join(self.directory, filename)
    # Open the file for writing
        with open(path, "w", encoding="utf-8") as f:
            # Stream output and write to file
            for chunk in chain.stream({"reviews": reviews}):
                print(chunk.content, end="", flush=True)
                f.write(chunk.content)

    def generate_report_for_all_ratings(self, country_code:str):
        all_rating_report = ''
        if os.path.exists(self.directory):
            for rating in range(5, 0, -1):
                path = os.path.join(self.directory, f"report_{self.data['app_id']}_{country_code}_{rating}.md")
                if os.path.exists(path):
                    print(f"Adding Report for {country_code} with rating {rating}")
                    all_rating_report += '\n\n' + '# Rating ' + str(rating) + '\n\n'
                    with open(path, "r", encoding="utf-8") as file:
                        all_rating_report += file.read() + '\n\n\n'
        final_report_path = os.path.join(self.directory, f"report_{self.data['app_id']}_{country_code}_all_ratings.md")
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)

        with open(final_report_path, "w", encoding="utf-8") as f:
            f.write(all_rating_report)

                   




