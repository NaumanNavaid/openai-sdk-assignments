from agents import Agent, Runner, set_tracing_disabled , function_tool
from dotenv import load_dotenv
from my_config.gemini_config import run_config
import os
import requests

load_dotenv()
set_tracing_disabled(True)  

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

@function_tool
def add_numbers(a:int ,b:int):
    result = a + b
    print("add_numbers function called")
    return result



@function_tool
def get_weather(city:str) -> str:
    url =f"https://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={city}"
    response= requests.get(url)
    if response.status_code == 200:
       data=  response.json()
       temp = data["current"]["temp_c"]
       condition = data["current"]["condition"]["text"]
       print("get_weather function called")
       return f"It's {temp}°C and {condition} in {city}."

    return "Error fetching weather data."

Agent= Agent(
    name="Mr. Weatherstein",
    instructions="""You are a helpful weather bot. Your name is Mr. Weatherstein. to get the weather, use the get_weather function.""",
    tools=[get_weather,
           add_numbers
    ],   
)

prompt = input("Enter your prompt: ")
result = Runner.run_sync(
    Agent,
    prompt,
    run_config=run_config)

print(result.final_output)