
from dotenv import load_dotenv
from agents import Agent, Runner, trace, function_tool, ModelSettings
from openai.types.responses import ResponseTextDeltaEvent
from typing import Dict
import os
import asyncio
##Brevo
import sib_api_v3_sdk
from sib_api_v3_sdk import Configuration, ApiClient, TransactionalEmailsApi

load_dotenv(override=True)

@function_tool
def send_email(subject: str, html_body: str) -> Dict[str, str]:
    config = Configuration()
    api_key = os.environ.get("BREVO_API_KEY")
    if not api_key:
        raise ValueError("BREVO_API_KEY is not set")
    config.api_key["api-key"] = api_key

    api_client = ApiClient(config)
    api_instance = TransactionalEmailsApi(api_client)

    email = sib_api_v3_sdk.SendSmtpEmail(
        to=[{"email": "jayitbhu@gmail.com"}],
        sender={"email": "jay.kr.mishra@gmail.com", "name": "Jay"},
        subject=subject,
        html_content=html_body
    )

    response = api_instance.send_transac_email(email)
    print("Sent! Message ID:", response.message_id)
    return {"status": "success", "message_id": response.message_id}

#send_email(subject="Test Email", html_body="<p>This is a test email</p>")

INSTRUCTIONS = """You are able to send a nicely formatted HTML email based on a detailed report.
You will be provided with a detailed report. You should use your tool to send one email, providing the 
report converted into clean, well presented HTML with an appropriate subject line."""

email_agent = Agent(
    name="Email agent",
    instructions=INSTRUCTIONS,
    tools=[send_email],
    model="gpt-4o-mini",
    model_settings=ModelSettings(tool_choice="required"),
)

"""
async def main():
    with trace("Help in a task"):
        result = await Runner.run(email_agent, "Help me with cooking an omelette")
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
"""
