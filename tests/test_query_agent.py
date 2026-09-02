import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

from agents.query_agent import QueryUnderstandingAgent
from dotenv import load_dotenv

load_dotenv()

agent = QueryUnderstandingAgent(
    api_key=os.getenv("GEMINI_API_KEY")
)

result = agent.analyse_query(
    selected_sport="Cricket",
    selected_feature="Batting Improvement",
    available_features=[
        "Batting Improvement",
        "Bowling Improvement"
    ],
    user_question="""
    I am a beginner batsman aged 16.
    Create a batting improvement plan.
    """
)

print("\n=== QUERY AGENT TEST ===\n")
print(result)
