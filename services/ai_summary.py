# import os

# from google import genai

# from dotenv import load_dotenv

# load_dotenv()

# client = genai.Client(
#     api_key=os.getenv("GEMINI_API_KEY")
# )


# async def summarize_text(text: str):
#     response=client.models.generate_content(
#         model="gemini-2.5-flash",
#         contents = f"""
#                     Summarize this article in exactly 3 short bullet points.
#                      keep under 50 words {text}


#                       """)
    
#     return response.text    

#IMPLEMENTATION IN OPENAI
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

async def summarize_text(text: str):

    try:

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content":
                    "You are a technology news summarizer."
                },
                {
                    "role": "user",
                    "content":
                    f"""
                    Summarize this article in exactly 3 bullet points.

Maximum 60 words total.

Focus on:
- Key idea
- Important takeaway
- Business impact

Keep it concise.
                    

                    {text}
                    """
                }
            ]
        )

        return response.choices[0].message.content

    except Exception as e:

        return f"Error: {str(e)}"