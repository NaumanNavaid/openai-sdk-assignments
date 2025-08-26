from instructions.dynamic_instructions import dynamic_instruction
from agents import Agent

hotel_assistant = Agent(
    name="Hotel Assistant",
    instructions=dynamic_instruction
)

