import os
import google.generativeai as genai


class DataRetrievalAgent:

    def __init__(self, api_key, database_path="database"):
        genai.configure(api_key=api_key)

        self.model = genai.GenerativeModel(
            "gemini-3.1-flash-lite"
        )

        self.database_path = database_path

    # ------------------------
    # Load local knowledge file
    # ------------------------
    def load_local_data(self, sport, feature):

        filename = (
            feature.lower()
            .replace(" ", "_")
            + ".txt"
        )

        filepath = os.path.join(
            self.database_path,
            sport.lower(),
            filename
        )

        if not os.path.exists(filepath):
            return None

        with open(filepath, "r", encoding="utf-8") as file:
            return file.read()

    # ------------------------
    # Check whether local data
    # is sufficient
    # ------------------------
    def evaluate_local_content(
        self,
        local_content,
        question
    ):

        prompt = f"""
You are a sports knowledge evaluator.

User Question:
{question}

Local Knowledge:
{local_content}

Determine whether the local knowledge
contains enough information to answer
the user's question.

Return ONLY:

YES

or

NO
"""

        response = self.model.generate_content(prompt)

        answer = response.text.strip().upper()

        return answer == "YES"

    # ------------------------
    # Web Search Fallback
    # ------------------------
    def search_web(self, question):

        prompt = f"""
You are a sports expert.

Answer the following question using your sports knowledge.

Question:
{question}

Provide a detailed and accurate answer.
"""

        response = self.model.generate_content(prompt)

        return response.text

    # ------------------------
    # Main Retrieval Method
    # ------------------------
    def retrieve_information(
        self,
        sport,
        feature,
        question
    ):

        result = {
            "source": "",
            "local_content": "",
            "external_content": "",
            "combined_content": ""
        }

        local_content = self.load_local_data(
            sport=sport,
            feature=feature
        )

        if local_content is None:

            external_content = self.search_web(question)

            result["source"] = "web"
            result["external_content"] = external_content
            result["combined_content"] = external_content

            return result

        sufficient = self.evaluate_local_content(
            local_content,
            question
        )

        if sufficient:

            result["source"] = "local"

            result["local_content"] = local_content

            result["combined_content"] = local_content

            return result

        external_content = self.search_web(question)

        combined = f"""
LOCAL DATABASE INFORMATION

{local_content}

--------------------------------------------------

ADDITIONAL INFORMATION

{external_content}
"""

        result["source"] = "local+web"

        result["local_content"] = local_content

        result["external_content"] = external_content

        result["combined_content"] = combined

        return result

