import json

from agents import Runner, trace, gen_trace_id
from search_agent_jm import search_agent, KeywordsOutput
#from planner_agent_jm import planner_agent, WebSearchItem, WebSearchPlan
from writer_agent_jm import writer_agent, ReportData
from email_agent_jm import email_agent
from arxiv_agent_jm import arxiv_agent, ArxivPapers
import asyncio

class ResearchManager:

    async def run(self, query: str):
        """ Run the deep research process, yielding the status updates and the final report"""
        trace_id = gen_trace_id()
        with trace("Research trace", trace_id=trace_id):
            print(f"View trace: https://platform.openai.com/traces/trace?trace_id={trace_id}")
            yield f"View trace: https://platform.openai.com/traces/trace?trace_id={trace_id}"
            print("Starting research...")
            search_keywords = await self.search_keywords(query)
            yield "Searches planned, starting to search..."     
            arxiv_results = await self.arxiv_searches(search_keywords)
            if not arxiv_results:
                arxiv_results = {}
            yield "Searches complete, writing report..."
            report = await self.write_report(query, arxiv_results)
            yield "Report written, sending email..."
            await self.send_email(report)
            yield "Email sent, research complete"
            yield report.markdown_report
        

    async def search_keywords(self, query: str) -> list[str]:
        """ Plan the searches to perform for the query """
        print("Planning searches...")
        result = await Runner.run(
            search_agent,
            f"Query: {query}",
        )
        print(f"Running keywords searches")
        return result.final_output_as(KeywordsOutput).keywords

    async def arxiv_searches(self, keywords: list[str]) -> dict[str, str] | None:
        """ Perform arxiv search for the query """
        input = json.dumps(keywords)
        try:
            result = await Runner.run(
                arxiv_agent,
                input,
            )
            return result.final_output_as(ArxivPapers).papers
        except Exception:
            return None

    async def write_report(self, query: str, search_results: dict[str, str]) -> ReportData:
        """ Write the report for the query """
        print("Thinking about report...")
        input = (
            f"Original query: {query}\n"
            f"ArXiv results (JSON): {json.dumps(search_results)}"
        )
        result = await Runner.run(
            writer_agent,
            input,
        )

        print("Finished writing report")
        return result.final_output_as(ReportData)
    
    async def send_email(self, report: ReportData) -> None:
        print("Writing email...")
        result = await Runner.run(
            email_agent,
            report.markdown_report,
        )
        print("Email sent")
        return report