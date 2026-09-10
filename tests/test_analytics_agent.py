import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

from agents.analytics_agent import DataAnalyticsAgent
from dotenv import load_dotenv

load_dotenv()

agent = DataAnalyticsAgent(
    api_key=os.getenv("GEMINI_API_KEY")
)

knowledge = """
Batting requires
good footwork,
timing and shot selection.
"""

result = agent.analyse(
    sport="Cricket",
    feature="Batting Improvement",
    question="Create a batting improvement plan",
    extracted_information={
        "skill_level": "Beginner",
        "age": "16",
        "goal": "School Team",
        "experience": "1 Year"
    },
    knowledge_base=knowledge
)

print("\n=== ANALYTICS AGENT TEST ===\n")
print(result)
