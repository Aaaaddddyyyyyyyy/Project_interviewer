import os
from services.llm import llm



response = llm.invoke(
    "You are an AI interviewer. "
    "Introduce yourself in one short sentence."
)


print("\nAI INTERVIEWER RESPONSE:")
print(response.content)