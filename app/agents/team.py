from agno.agent import Agent
from agno.models.groq import Groq
from agno.team import Team
from agno.team.mode import TeamMode

from app.agents.tools import search_library
from app.config import GROQ_API_KEY, GROQ_MODEL

DISCLAIMER = (
    "Educational information only. This is not a diagnosis or treatment recommendation. "
    "Consult a qualified healthcare professional for personal medical advice."
)


def _model():
    if not GROQ_API_KEY:
        raise RuntimeError("GROQ_API_KEY is not configured. Add it to your .env file.")
    return Groq(id=GROQ_MODEL, api_key=GROQ_API_KEY)


def build_healthcare_team():
    model = _model()

    analyzer = Agent(
        name="Healthcare Query Analyzer",
        role="Clarify the user's educational healthcare or medical research question.",
        model=model,
        instructions=[
            "Identify the main topic and information need.",
            "Do not diagnose the user or infer a disease.",
            "Summarize the question for the research agent.",
        ],
    )

    researcher = Agent(
        name="Medical Research Agent",
        role="Find relevant background in the local educational research library.",
        model=model,
        tools=[search_library],
        instructions=[
            "Use search_library to look for relevant local notes.",
            "Clearly distinguish library content from general background knowledge.",
            "Never invent citations, statistics, or clinical guidelines.",
            "State when the local library has insufficient information.",
        ],
    )

    reviewer = Agent(
        name="Medical Answer Reviewer",
        role="Review the draft for clarity, uncertainty, and medical safety.",
        model=model,
        instructions=[
            "Review the team's draft and produce a clear, concise final educational answer.",
            "Do not diagnose, prescribe medicines, or recommend individualized treatment.",
            "Mention uncertainty and advise a qualified professional for personal results.",
            "Include this disclaimer: " + DISCLAIMER,
        ],
    )

    return Team(
        name="Medical Healthcare Assistant Team",
        mode=TeamMode.coordinate,
        model=model,
        members=[analyzer, researcher, reviewer],
        instructions=[
            "Coordinate the three specialist agents to answer the user's educational question.",
            "Use the analyzer to identify the question, the research agent to gather relevant context, "
            "and the reviewer to check the final response.",
            "Keep the response understandable to an undergraduate student.",
            "Never present the response as a diagnosis or personalized medical advice.",
        ],
        markdown=True,
    )


def ask_healthcare_team(question: str) -> str:
    team = build_healthcare_team()
    response = team.run(question)
    content = getattr(response, "content", None)
    if content:
        return str(content)
    return str(response)
