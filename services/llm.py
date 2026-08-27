import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq


load_dotenv()


GROQ_API_KEY = os.getenv("GROQ_API_KEY")


if not GROQ_API_KEY:
    raise ValueError(
        "GROQ_API_KEY is missing. "
        "Check your .env file."
    )


llm = ChatGroq(model="openai/gpt-oss-120b")
