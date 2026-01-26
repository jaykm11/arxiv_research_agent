from pydantic import BaseModel, Field
from agents import Agent

INSTRUCTIONS = (
    "You are a senior research writer. You will be given a dictionary of arXiv papers "
    "where each key is a paper title and each value is the abstract. "
    "Write a comprehensive synthesis of the abstracts into a cohesive report.\n"
    "Requirements:\n"
    "- Produce a short summary (2-3 sentences).\n"
    "- Produce a markdown report that includes a narrative overview and a References section.\n"
    "- Use bracketed numeric citations like [1], [2] throughout the report.\n"
    "- In References, list each paper with its title and a brief 1-sentence note.\n"
    "- Keep the tone professional and suitable for emailing.\n"
)


class ReportData(BaseModel):
    short_summary: str = Field(description="A short 2-3 sentence summary of the findings.")
    markdown_report: str = Field(description="Markdown report with references.")
    follow_up_questions: list[str] = Field(description="Suggested topics to research further.")


writer_agent = Agent(
    name="WriterAgentJM",
    instructions=INSTRUCTIONS,
    model="gpt-4o-mini",
    output_type=ReportData,
)
