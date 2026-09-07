import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

from agents.retrieval_agent import DataRetrievalAgent
from dotenv import load_dotenv


load_dotenv()

agent = DataRetrievalAgent(
    api_key=os.getenv("GEMINI_API_KEY"),
    database_path="database"
)

result = agent.retrieve_information(
    sport="cricket",
    feature="Batting Improvement",
    question="How can I improve my cover drive?"
)

print("\n=== RETRIEVAL AGENT TEST ===\n")

print("Source:")
print(result["source"])

print("\nCombined Content:\n")
print(result["combined_content"])
