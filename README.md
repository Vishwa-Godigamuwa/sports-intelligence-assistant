# Sports Intelligence Assistant

Sports Intelligence Assistant is an AI-powered sports coaching application built with Python and Streamlit. It helps athletes choose a sport and performance feature, ask coaching questions, and receive personalized guidance based on local sports knowledge, external AI reasoning, and structured analytics.

The system combines:

- A Streamlit web interface
- MongoDB-based user authentication
- Google Gemini-based AI agents
- Local sports knowledge files for training guidance
- Premium account flow for enhanced responses
- PDF report generation for coaching summaries

---

## System Overview

This project is designed to behave like a digital sports coach. A user signs in, selects a sport and a training feature, asks a question, and the system analyzes the request using a multi-agent AI workflow.

The core idea is:

1. Understand the user question and match it to the correct feature.
2. Retrieve relevant training knowledge from the local database.
3. Evaluate whether the local knowledge is sufficient.
4. Generate structured sports analytics.
5. Produce a user-friendly coaching answer.
6. Offer premium features such as detailed analysis and downloadable PDFs.

---

## Main Architecture

### 1. Frontend Layer

The user interface is built using Streamlit.

Key files:

- `app.py` — main application dashboard and AI workflow hub
- `main.py` — older application entry logic / fallback routing
- `pages/Login.py` — login screen
- `pages/Register.py` — account registration screen
- `pages/Premium.py` — premium upgrade page

The app uses session state to manage:

- login status
- current user
- original question and response
- follow-up conversation history
- selected sport and feature
- report data for PDF export

### 2. Authentication Layer

Authentication is implemented in the `auth` package.

Files:

- `auth/auth_manager.py`
- `auth/database.py`

Responsibilities:

- Register new users
- Hash passwords with bcrypt
- Log users in securely
- Check existing users by email
- Upgrade free accounts to premium
- Store user records in MongoDB

The MongoDB connection is created in `auth/database.py` and uses:

- `MONGODB_URI` from the environment
- TLS certificate validation via `certifi`
- a database named `sports_intelligence_assistant`
- a collection named `users`

### 3. AI Agent Layer

The intelligence of the app is built from four Gemini-powered agents.

#### Query Understanding Agent

File: `agents/query_agent.py`

The Query Understanding Agent checks:

- whether the user question is relevant to the selected sport/feature
- which feature is the correct match if the question is off-topic
- whether required profile details are missing
- what information the user has already provided, such as skill level, age, or goal

It returns structured JSON so the rest of the application can make decisions automatically.

#### Retrieval Agent

File: `agents/retrieval_agent.py`

The Retrieval Agent is responsible for gathering relevant coaching information.

It does the following:

- reads local training text files from `database/<sport>/<feature>.txt`
- checks whether the local content is sufficient for the user question
- uses the Gemini model to decide if external fallback information is needed
- combines local and external knowledge when necessary

This gives the app a hybrid approach: useful local knowledge plus AI expansion when needed.

#### Analytics Agent

File: `agents/analytics_agent.py`

This agent turns retrieved knowledge and extracted user details into structured performance analysis.

It produces structured output such as:

- player level
- current assessment
- strengths and weaknesses
- improvement priorities
- focus areas
- training hours per week
- training plan
- expected progress
- recommendations

This information is later used to generate the final answer and premium insights.

#### Response Generation Agent

File: `agents/response_agent.py`

This agent converts the technical analysis into natural-language advice for the user.

It generates two kinds of responses:

- Free user response: short preview, limited detail
- Premium user response: full coaching guidance with deeper analysis

It also supports follow-up conversations so the user can continue asking clarifying or improvement-based questions.

---

## Knowledge Base

The project includes a local knowledge library under the `database/` directory.

Example structure:

- `database/cricket/batting_improvement.txt`
- `database/cricket/bowling_improvement.txt`
- `database/football/dribbling_improvement.txt`
- `database/football/shooting_improvement.txt`
- `database/tennis/serve_improvement.txt`
- `database/volleyball/serving_improvement.txt`
- `database/volleyball/spiking_improvement.txt`

These text files act as the app’s domain training knowledge and are used as the first source of coaching content.

---

## Premium Flow

The app includes a premium upgrade concept.

### Free users see:

- condensed AI responses
- limited insight depth
- no full analytics package
- no PDF downloading

### Premium users unlock:

- comprehensive performance analysis
- richer training recommendations
- deeper coaching guidance
- PDF report generation

The upgrade flow is implemented in `pages/Premium.py` and `auth/auth_manager.py` and updates the user account type in MongoDB.

> The current premium upgrade is for demonstration purposes; it does not integrate with a real payment gateway yet.

---

## PDF Report Generation

File: `utils/pdf_generator.py`

This module creates a polished PDF coaching report using ReportLab.

The PDF includes:

- sports intelligence title
- personalized report header
- athlete question
- generated advice
- analytics fields like score and readiness
- structured sections for recommendations and next steps
- footer metadata

The app stores the report data in session state and can generate a downloadable report file such as `coaching_report.pdf`.

---

## User Journey

A normal user flow looks like this:

1. User opens the app and sees the dashboard.
2. User signs in or registers an account.
3. User selects a sport and improvement feature.
4. User enters a coaching or training question.
5. The `QueryUnderstandingAgent` validates the request.
6. The `RetrievalAgent` loads relevant local knowledge.
7. The `AnalyticsAgent` produces structured athlete analysis.
8. The `ResponseGenerationAgent` creates the final answer.
9. Premium users can download the PDF coaching report.
10. Follow-up questions can continue the coaching conversation contextually.

---

## Project Structure

```text
sports-intelligence-assistant/
├── app.py
├── main.py
├── README.md
├── .env
├── coaching_report.pdf
├── agents/
│   ├── __init__.py
│   ├── analytics_agent.py
│   ├── query_agent.py
│   ├── retrieval_agent.py
│   └── response_agent.py
├── auth/
│   ├── auth_manager.py
│   └── database.py
├── database/
│   ├── cricket/
│   ├── football/
│   ├── tennis/
│   └── volleyball/
├── pages/
│   ├── Login.py
│   ├── Premium.py
│   └── Register.py
├── tests/
│   ├── __init__.py
│   ├── test_analytics_agent.py
│   ├── test_pipeline.py
│   ├── test_query_agent.py
│   ├── test_response_agent.py
│   └── test_retrieval_agent.py
├── utils/
│   └── pdf_generator.py
└── test_pdf.py
```

---

## Environment Setup

Before starting the app, create a `.env` file in the project root with the following values:

```env
GEMINI_API_KEY=your_google_gemini_api_key
MONGODB_URI=mongodb+srv://<username>:<password>@<cluster-url>/<database>?retryWrites=true&w=majority
```

Important:

- `GEMINI_API_KEY` is required for Gemini AI generation.
- `MONGODB_URI` is required for the auth database.
- `MONGODB_URI` should point to a valid MongoDB cluster or local MongoDB instance.

---

## Installation

Install the required Python packages:

```bash
pip install streamlit python-dotenv pymongo certifi bcrypt google-generativeai reportlab
```

If you use an environment manager, you can also set up a virtual environment first.

---

## Running the Application

Start the Streamlit app from the project root:

```bash
streamlit run app.py
```

Open the local Streamlit URL in your browser to start using the system.

---

## Testing

The project contains agent and pipeline tests under the `tests/` folder. These help verify:

- query understanding behavior
- retrieval logic
- analytics output structure
- response generation
- end-to-end AI pipeline flow

Example:

```bash
python tests/test_query_agent.py
python tests/test_retrieval_agent.py
python tests/test_analytics_agent.py
python tests/test_response_agent.py
```

---

## Design Notes and Project Strengths

This system is useful because it mixes three important components:

- structured data from local sports knowledge
- AI reasoning from Gemini
- application logic from a workflow-driven Streamlit interface

This gives a practical “AI sports coach” experience without requiring a complex backend service.

The architecture is simple and modular, which makes it easy to extend with:

- more sports and training modules
- stronger user profile tracking
- payment integration
- database-backed coaching history
- admin dashboards
- real model evaluation
- more advanced personalization

---

## Current Limitations

A few important limitations are worth noting:

- Premium upgrade is a demo mechanism, not a real payment system
- Local knowledge is limited to the text files in `database/`
- The app relies on external AI responses from Gemini for main reasoning
- MongoDB must be available and correctly configured
- PDF generation depends on local system fonts and ReportLab support

---

## Summary

Sports Intelligence Assistant is a smart sports coaching web app that combines:

- athlete guidance
- AI-powered analysis
- structured training recommendations
- user authentication
- premium access flow
- downloadable coaching reports

It is a practical example of a multi-agent, knowledge-driven AI application tailored to coaching and sports improvement.
