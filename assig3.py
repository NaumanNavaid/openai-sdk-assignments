from agents import Agent, Runner, set_tracing_disabled, function_tool, ModelSettings
from dotenv import load_dotenv
from my_config.gemini_config import run_config

load_dotenv()
set_tracing_disabled(True)

@function_tool
def add_numbers(a:int ,b:int):
    result = a + b
    print("add_numbers function called")
    return result


Agent= Agent(
    name="Helpful Agent",
    instructions="""You are an helpful agent helping users to in what they want you have an add_numbers function that adds two numbers together. use it when you like""",
    tools=[
        add_numbers
    
    ],  
    model_settings=ModelSettings( tool_choice="auto")  # Automatically use tools when needed
)

prompt = input("Enter your prompt: ")

result = Runner.run_sync(
    Agent,
    prompt,
    run_config=run_config
)

print(result.final_output)