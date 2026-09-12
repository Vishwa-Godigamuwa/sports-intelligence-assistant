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
from agents.retrieval_agent import DataRetrievalAgent
from agents.analytics_agent import DataAnalyticsAgent
from agents.response_agent import ResponseGenerationAgent

from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")


query_agent = QueryUnderstandingAgent(api_key)
retrieval_agent = DataRetrievalAgent(api_key)
analytics_agent = DataAnalyticsAgent(api_key)
response_agent = ResponseGenerationAgent(api_key)

question = """
I am a beginner batsman aged 16.
Create a batting improvement plan.
"""

query_result = query_agent.analyse_query(
    selected_sport="Cricket",
    selected_feature="Batting Improvement",
    available_features=[
        "Batting Improvement",
        "Bowling Improvement"
    ],
    user_question=question
)

print("QUERY RESULT")
print(query_result)

retrieval_result = retrieval_agent.retrieve_information(
    sport="cricket",
    feature="Batting Improvement",
    question=question
)

print("Retrieval Result")
print(retrieval_result)

analytics_result = analytics_agent.analyse(
    sport="Cricket",
    feature="Batting Improvement",
    question=question,
    extracted_information=query_result[
        "extracted_information"
    ],
    knowledge_base=retrieval_result[
        "combined_content"
    ]
)

print("\nANALYTICS RESULT")
print(analytics_result)

final_response = response_agent.generate_response(
    sport="Cricket",
    feature="Batting Improvement",
    question=question,
    analytics_result=analytics_result,
    retrieved_content=retrieval_result[
        "combined_content"
    ]
)

print("\nFINAL RESPONSE")
print(final_response)
