import google.generativeai as genai


class ResponseGenerationAgent:

    def __init__(self, api_key):

        genai.configure(api_key=api_key)

        self.model = genai.GenerativeModel(
            "gemini-3.1-flash-lite"
        )


    # =====================================================
    # MAIN RESPONSE GENERATION
    # =====================================================

    def generate_response(
        self,
        sport,
        feature,
        question,
        analytics_result,
        retrieved_content,
        account_type
    ):
        """
        Generates the main user-friendly coaching response.
        """

        # =================================================
        # FREE USER RESPONSE
        # =================================================

        if account_type == "Free":

            prompt = f"""
You are a Sports Intelligence Assistant.

SPORT:
{sport}

FEATURE:
{feature}

USER QUESTION:
{question}

Your task:

Provide ONLY a short preview response.

Include ONLY:

1. Short Player Assessment (maximum 2 sentences)
2. ONE main strength
3. ONE main weakness
4. THREE simple recommendations

STRICT RULES:

DO NOT INCLUDE:
- Performance Score
- Training Plan
- Weekly Schedule
- Improvement Priorities
- Recommended Drills
- Training Hours
- Progress Tracking
- Detailed Analysis
- Expert Recommendations
- Long Explanations
- Long Motivation

Keep response under 120 words.

Use this format:

## Player Assessment

## Main Strength

## Main Weakness

## Quick Recommendations

At the end display:

⭐ Upgrade to Premium to unlock:
• Personalized Training Plans
• Recommended Drills
• Performance Analytics
• Progress Tracking
• PDF Coaching Reports

Return only the final response.
"""

        # =================================================
        # PREMIUM USER RESPONSE
        # =================================================

        else:

            prompt = f"""
You are a Sports Intelligence Assistant.

SPORT:
{sport}

FEATURE:
{feature}

USER QUESTION:
{question}

SPORT KNOWLEDGE:
{retrieved_content}

ANALYTICS RESULT:
{analytics_result}

Your task:

1. Create a professional and friendly response.
2. Explain the player's current assessment.
3. Explain the performance score.
4. Describe strengths and weaknesses.
5. Explain improvement priorities.
6. Present the training plan clearly.
7. Provide recommendations.
8. Motivate the user.

Make the response easy to read using:

- Headings
- Bullet Points
- Short paragraphs

Do not return JSON.

Return only the final response.
"""

        response = self.model.generate_content(prompt)

        return response.text


    # =====================================================
    # FOLLOW-UP QUESTION RESPONSE
    # =====================================================

    def generate_followup_response(
        self,
        sport,
        feature,
        original_question,
        original_response,
        followup_question,
        chat_history=None
    ):
        """
        Generates an answer to a follow-up question using
        the original question, original coaching response,
        and previous follow-up conversation as context.
        """

        if chat_history is None:
            chat_history = []


        # =================================================
        # BUILD PREVIOUS CONVERSATION
        # =================================================

        conversation_text = ""

        for message in chat_history:

            role = message.get("role", "")
            content = message.get("content", "")

            if role == "user":

                conversation_text += (
                    f"\nUSER: {content}\n"
                )

            elif role == "assistant":

                conversation_text += (
                    f"\nSPORTS ASSISTANT: {content}\n"
                )


        # =================================================
        # FOLLOW-UP PROMPT
        # =================================================

        prompt = f"""
You are a Sports Intelligence Assistant continuing an
existing sports coaching conversation.

SPORT:
{sport}

FEATURE:
{feature}

ORIGINAL USER QUESTION:
{original_question}

ORIGINAL COACHING RESPONSE:
{original_response}

PREVIOUS FOLLOW-UP CONVERSATION:
{conversation_text}

NEW FOLLOW-UP QUESTION:
{followup_question}

Your task:

Answer the new follow-up question based on the original
coaching response and the previous conversation.

RULES:

1. Stay focused on the selected sport and feature.

2. Treat this as a continuation of the existing coaching
conversation.

3. Use the original coaching response as the main context.

4. Take previous follow-up questions and answers into
account when relevant.

5. Do not repeat the entire original coaching response.

6. Answer the user's specific follow-up question directly.

7. Keep the answer clear, helpful, and practical.

8. Use short paragraphs or bullet points when useful.

9. If the user asks to modify the original advice,
provide only the relevant modifications.

10. Do not return JSON.

Return only the follow-up response.
"""


        # =================================================
        # GENERATE FOLLOW-UP RESPONSE
        # =================================================

        response = self.model.generate_content(prompt)

        return response.text