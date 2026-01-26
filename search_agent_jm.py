import asyncio
import os

from dotenv import load_dotenv
from pydantic import BaseModel, Field
from agents import Agent, WebSearchTool, ModelSettings, Runner, trace

load_dotenv(override=True)
if os.getenv("OPEN_API_KEY") and not os.getenv("OPENAI_API_KEY"):
    os.environ["OPENAI_API_KEY"] = os.environ["OPEN_API_KEY"]

INSTRUCTIONS = (
    "You are a research assistant. Given a search term, you search the web for that term and "
    "produce 3 keywords or phrases that are relevant to the search term and can be used to search arxiv for related research papers. These will be used to search arxiv for related research papers."
    "The keywords or phrases should be concise and to the point. They should be no more than 3 words long. "
    "The keywords or phrases should be relevant to the search term. "
    "The keywords or phrases should be unique and not generic. "
    "The keywords or phrases should be specific to the search term. "
    "The keywords or phrases should be not be too broad. "
    "The keywords or phrases should be not be too narrow. "
    "The keywords or phrases should be not be too general. "
)


class KeywordsOutput(BaseModel):
    keywords: list[str] = Field(description="3 concise keyword phrases for arXiv searching.")


search_agent = Agent(
    name="Search agent",
    instructions=INSTRUCTIONS,
    tools=[WebSearchTool(search_context_size="low")],
    model="gpt-4o-mini",
    model_settings=ModelSettings(tool_choice="required"),
    output_type=KeywordsOutput,
)

"""
async def main():
    with trace("Help in a task"):
        result = await Runner.run(
            search_agent, "What is the latest research on quantum computing?"
        )
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
"""