# from langchain_openai import ChatOpenAI
# from langchain.prompts import PromptTemplate
# from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
# from dotenv import load_dotenv
# import os

# # Load environment variables from .env file
# load_dotenv()

# # --- Prompt Template ---
# template = """You are a helpful UX reviewer.

# Analyze the following app store reviews and provide insights about the user interface and user experience design.

# Question: {question}
# Answer:"""

# prompt = PromptTemplate(template=template, input_variables=["question"])

# # --- LLM Setup (Using OpenRouter-compatible model with streaming) ---
# llm = ChatOpenAI(
#     openai_api_key=os.getenv("OPENROUTER_API_KEY"),
#     base_url=os.getenv("OPENROUTER_BASE_URL"),
#     model="deepseek/deepseek-r1-0528:free",  # Change to another if needed
#     streaming=True,
#     callbacks=[StreamingStdOutCallbackHandler()]
# )

# # --- Chain prompt and model using modern Runnable syntax ---
# chain = prompt | llm

# # --- Example Review Text ---
# question = """Here are some app reviews:
# 1. "This app is very confusing and cluttered. I couldn’t find the settings easily."
# 2. "The UI is super intuitive and I love the minimalist design."
# 3. "Takes too long to load and navigation is poor."
# 4. "Very sleek layout, easy to use even for my parents!"
# 5. "Too many ads and buttons everywhere, it's overwhelming."

# What are the top things users like and dislike about the app’s UI/UX design?
# """

# # --- Run the chain ---
# chain.invoke({"question": question})


from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from dotenv import load_dotenv
import os

# --- Load environment variables ---
load_dotenv()

# --- LLM Setup (OpenRouter-compatible with streaming output) ---
llm = ChatOpenAI(
    openai_api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url=os.getenv("OPENROUTER_BASE_URL"),
    model="deepseek/deepseek-r1-0528:free",
    streaming=True,
    callbacks=[StreamingStdOutCallbackHandler()]
)

# --- Prompt Template (incremental synthesis) ---
prompt_template = PromptTemplate(
    template="""You are a UX research analyst analyzing app store reviews using a Design Thinking approach (empathize and define stages).

You have already reviewed some earlier feedback and formed initial insights. You're now receiving more reviews and need to update your understanding.

🎯 Focus only on:
1. What users **like** about the app's user experience and interface (UI/UX)
2. What **recurring pain points** users have with the UI/UX

🧹 Ignore technical or irrelevant complaints (e.g., crashes, login failures, payment bugs, device issues, etc.)

🔇 Do **not** suggest solutions or improvements. Just describe patterns and insights from the reviews.

Please use this structure:

## ❤️ What Users Like (Updated)
- [Insight or theme with number of mentions if clear]

## ⚠️ Pain Points (Updated)
- [Issue or theme with number of mentions if clear]

### Review Stats table (Updated)
- Total Positive Reviews: [count]
- Most Liked Feature: [summarized feature]
- Total Negative Reviews: [count]
- Most Common Complaint: [summarized issue]

🧠 Please update your findings based on this new batch of reviews. If new patterns emerge, add them. If older patterns are reinforced, mention that too.

Use this structure in your table response:

## Review Stats (Updated)
- Total Positive Reviews: ...
- Most Liked Feature: ...
- Total Negative Reviews: ...
- Most Common Complaint: ...

Earlier summary:
{summary}

New batch of reviews:
{reviews}
""",
    input_variables=["summary", "reviews"]
)

# --- Chain Setup ---
chain = prompt_template | llm

# --- Function to process in chunks ---
def analyze_in_reviews(all_reviews: list, chunk_size: int = 300):
    running_summary = "(None yet – this is the first batch.)"

    for i in range(0, len(all_reviews), chunk_size):
        chunk = all_reviews[i:i + chunk_size]

        if len(chunk) < 100:
            print(f"\n⏩ Skipping small batch of {len(chunk)} reviews.")
            continue

        print(f"\n\n🚀 Processing batch {i//chunk_size + 1} ({len(chunk)} reviews)...\n")
        chunk_text = "\n".join(f"- {r}" for r in chunk)

        response = chain.invoke({
            "summary": running_summary,
            "reviews": chunk_text
        })

        # Optionally update running summary (if you're saving it)
        running_summary = response.content if hasattr(response, 'content') else response  # Works with or without streaming

    print("\n✅ All chunks processed.")
    return running_summary

# --- Example Usage ---
# reviews_data = ["This app is very confusing...", "UI is amazing...", ...]  # Load your reviews here
# final_summary = analyze_in_chunks(reviews_data)
# print("\n\nFinal UX Summary:\n", final_summary)

