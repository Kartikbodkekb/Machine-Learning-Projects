import os 
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool

load_dotenv()

# Initialize Web Search Tool for the Researcher
search_tool = SerperDevTool()

# 1. Initialize Agents via YAML configuration parsing
# (For simplicity in this single file, we load them manually, but CrewAI reads them beautifully)
import yaml

with open('config/agents.yaml', 'r') as f:
    agents_config = yaml.safe_load(f)

with open('config/tasks.yaml', 'r') as f:
    tasks_config = yaml.safe_load(f)

# Define Agents
job_researcher = Agent(
    config=agents_config['job_researcher'],
    tools=[search_tool],
    verbose=True
)

resume_specialist = Agent(
    config=agents_config['resume_specialist'],
    verbose=True
)

outreach_writer = Agent(
    config=agents_config['outreach_writer'],
    verbose=True
)

# Define Tasks
research_task = Task(
    config=tasks_config['research_task'],
    agent=job_researcher,
    output_file='outputs/discovered_jobs.md'
)

tailor_resume_task = Task(
    config=tasks_config['tailor_resume_task'],
    agent=resume_specialist,
    output_file='outputs/tailored_resume.md'
)

draft_outreach_task = Task(
    config=tasks_config['draft_outreach_task'],
    agent=outreach_writer,
    output_file='outputs/outreach_materials.md'
)

# Assemble the Crew
job_search_crew = Crew(
    agents=[job_researcher, resume_specialist, outreach_writer],
    tasks=[research_task, tailor_resume_task, draft_outreach_task],
    process=Process.sequential, # Tasks execute one after another
    verbose=True
)

# Kickoff Inputs
inputs = {
    'job_title': 'Machine Learning Engineer',
    'location': 'Remote, US',
    'baseline_resume': '''
    Alex Mercer
    Data Scientist with 2 years of experience building predictive models using Python, Scikit-Learn, and SQL.
    Managed data preprocessing pipelines, engineered features, and deployed a churn model reducing loss by 12%.
    Skills: Python, SQL, Tableau, Pandas, Git.
    '''
}

# Ensure output directory exists
os.makedirs('outputs', exist_ok=True)

# Run the system
print("🚀 Starting Multi-Agent Job Search Automation System...")
result = job_search_crew.kickoff(inputs=inputs)

print("\n🎯 Execution Complete! Check the 'outputs' directory for results.")