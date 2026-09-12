import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

from agents.response_agent import ResponseGenerationAgent
from dotenv import load_dotenv

load_dotenv()

agent = ResponseGenerationAgent(
    api_key=os.getenv("GEMINI_API_KEY")
)

analytics_result = {
    "performance_score": 68,
    "readiness_level": "Intermediate",

    "strengths": [
        "Good hand-eye coordination"
    ],

    "weaknesses": [
        "Footwork",
        "Shot Selection"
    ],

    "improvement_priority": [
        "Footwork",
        "Timing",
        "Shot Selection"
    ],

    "weekly_training_hours": 8,

    "training_plan": {
        "weekly_sessions": "4",
        "duration_per_session": "2 Hours",
        "recommended_drills": [
            "Net Practice",
            "Throw Downs",
            "Shadow Batting"
        ]
    }
}

response = agent.generate_response(
    sport="Cricket",
    feature="Batting Improvement",
    question="Create a batting improvement plan",
    analytics_result=analytics_result,
    retrieved_content="""
    Batting requires
    timing,
    footwork and
    concentration.
    """
)

print("\n=== RESPONSE AGENT TEST ===\n")
print(response)
