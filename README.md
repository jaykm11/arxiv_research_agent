Deep Research (JM) - ArXiv pipeline

What it does
- Turns a user query into 3 keyword phrases
- Searches arXiv with those keywords
- Writes a referenced markdown report
- Sends the report via Brevo (optional)

Quick start
1) Create and activate a virtual environment
2) Install dependencies:
   pip install -r requirements.txt
3) Set environment variables in .env:
   OPENAI_API_KEY=your_key_here, 
   BREVO_API_KEY=your_key_here
4) Run:
   python deep_research_jm.py

Notes
- The email sender and recipient are hardcoded in email_agent_jm.py.
- If you do not want email delivery, comment out send_email in research_manager_jm.py.
