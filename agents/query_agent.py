import json
import google.generativeai as genai


class QueryUnderstandingAgent:

    def __init__(self, api_key):
        genai.configure(api_key=api_key)

        self.model = genai.GenerativeModel(
            model_name="gemini-3.1-flash-lite"
        )

    def analyse_query(
        self,
        selected_sport,
        selected_feature,
        available_features,
        user_question
    ):

        prompt = f"""
You are a Query Understanding Agent for a Sports Intelligence Assistant.

Selected Sport:
{selected_sport}

Selected Feature:
{selected_feature}

Available Features for the Sport:
{', '.join(available_features)}

User Question:
{user_question}

Your responsibilities:

1. Determine whether the question is relevant to the selected feature.

2. If NOT relevant:
   - Set relevance=false
   - Identify the most suitable feature
   - Generate an error message

3. Detect missing information.

Examples:

Feature = Batting Improvement

Question:
"Create a batting improvement plan"

Missing:
- skill level
- age
- experience level
- goal

Feature = Bowling Improvement

Question:
"How can I bowl faster?"

No missing information.

4. Extract any information provided by the user.

Example:

Question:
"I am a beginner batsman aged 16. Create a batting improvement plan."

Extract:
- skill_level = beginner
- age = 16
- goal = not mentioned

5. Return ONLY valid JSON.

Format:

{{
   "relevance": true,
   "suggested_feature": null,
   "missing_information": [],
   "error_message": "",
   "extracted_information": {{
       "skill_level": "",
       "age": "",
       "goal": "",
       "experience": ""
   }}
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
                "relevance": False,
                "suggested_feature": None,
                "missing_information": [],
                "error_message": "Unable to analyse the query.",
                "extracted_information": {}
            }
