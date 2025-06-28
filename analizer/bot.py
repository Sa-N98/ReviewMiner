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
    
    def generate_report(self, country_code:str, rating:int):
        reviews = ''
        for i,review in enumerate(self.data['reviews'][country_code][str(rating)]):
            reviews += (f'{i+1} {review["review"]} \n')
        print(reviews)

         # Set the filename
        filename = f"report_{self.data['app_id']}_{country_code}_{rating}.md"
        directory = "app_reports"
        if not os.path.exists(directory):
            os.makedirs(directory)
        path = os.path.join(directory, filename)
    # Open the file for writing
        with open(path, "w", encoding="utf-8") as f:
            # Stream output and write to file
            for chunk in chain.stream({"reviews": reviews}):
                print(chunk.content, end="", flush=True)
                f.write(chunk.content)
