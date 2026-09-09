import json
import google.generativeai as genai


class DataAnalyticsAgent:

    def __init__(self, api_key):
        genai.configure(api_key=api_key)

        self.model = genai.GenerativeModel(
            "gemini-3.1-flash-lite"
        )

    def analyse(
        self,
        sport,
        feature,
        question,
        extracted_information,
        knowledge_base
    ):
        """
        Generates structured analytics using:
        - User Information
        - Retrieved Knowledge
        - User Goal
        """

        prompt = f"""
You are a Sports Analytics Agent.

SPORT:
{sport}

FEATURE:
{feature}

USER QUESTION:
{question}

USER PROFILE:
{json.dumps(extracted_information, indent=2)}

KNOWLEDGE BASE:
{knowledge_base}

Your task:

1. Analyse the athlete's current situation.
2. Identify strengths and weaknesses.
3. Recommend focus areas.
4. Suggest training frequency.
5. Create a short-term development plan.
6. Estimate expected improvement.
7. Provide personalised recommendations.

Return ONLY valid JSON.

Format:

{{
    "player_level": "",
    "current_assessment": "",
    "strengths": [],
    "weaknesses": [],
    "improvement_priority": [],
    "focus_areas": [],
    "weekly_training_hours": 0,
    "training_plan": {{
        "weekly_sessions": "",
        "duration_per_session": "",
        "recommended_drills": []
    }},
    "expected_progress": "",
    "recommendations": []
}}
"""

        response = self.model.generate_content(prompt)

        try:

            text = response.text.strip()

            text = text.replace("```json", "")
            text = text.replace("```", "")

            return json.loads(text)

        except Exception:

           
            return {
                "player_level": "Unknown",
                "current_assessment": "Unable to analyse.",
                "strengths": [],
                "weaknesses": [],
                "improvement_priority": [],
                "focus_areas": [],
                "weekly_training_hours": 0,
                "training_plan": {
                        "weekly_sessions": "",
                        "duration_per_session": "",
                        "recommended_drills": []
                    },
                "expected_progress": "",
                "recommendations": []
            }
