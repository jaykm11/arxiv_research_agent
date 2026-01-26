
import asyncio
import os
from typing import Dict, List

import arxiv
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from agents import Agent, Runner, trace, function_tool, ModelSettings

load_dotenv(override=True)
if os.getenv("OPEN_API_KEY") and not os.getenv("OPENAI_API_KEY"):
    os.environ["OPENAI_API_KEY"] = os.environ["OPEN_API_KEY"]

client = arxiv.Client()


def _clean_summary(text: str) -> str:
    return " ".join(text.split())


@function_tool
def arxiv_search(keywords: List[str], max_results: int = 10) -> Dict[str, str]:
    if not keywords:
        return {}

    query = " OR ".join(f'all:"{term}"' for term in keywords)
    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.Relevance,
    )

    papers: Dict[str, str] = {}
    for result in client.results(search):
        papers[result.title] = _clean_summary(result.summary)
        if len(papers) >= max_results:
            break
    return papers


class ArxivPapers(BaseModel):
    papers: Dict[str, str] = Field(
        description="Map of paper title to abstract for the top results."
    )


INSTRUCTIONS = (
    "You are an ArXiv research agent. The user will provide a JSON array of keywords "
    "or phrases. Call the arxiv_search tool with that list and return the results "
    "as a JSON object with a single key 'papers' mapping titles to abstracts."
)

arxiv_agent = Agent(
    name="ArXiv agent",
    instructions=INSTRUCTIONS,
    tools=[arxiv_search],
    model="gpt-4o-mini",
    model_settings=ModelSettings(tool_choice="required"),
    output_type=ArxivPapers,
)


async def main():
    with trace("ArXiv research"):
        result = await Runner.run(
            arxiv_agent,
            '["quantum computing", "fault tolerance", "superconducting qubits"]',
        )
    print(result.final_output_as(ArxivPapers).papers)


if __name__ == "__main__":
    asyncio.run(main())
