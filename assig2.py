from agents import Agent, Runner,  set_tracing_disabled 
from dotenv import load_dotenv
from my_config.gemini_config import run_config
load_dotenv()
set_tracing_disabled(True)

agent: Agent= Agent(
name="Sir Bilal",
instructions="""You are a helpful FAQ bot. your name is Sir Bilal.""",
)

prompt = input("Enter your question: ")
result = Runner.run_sync(
    agent,
    prompt,
    run_config=run_config,
)
print(result.final_output)