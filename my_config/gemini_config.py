from agents import OpenAIChatCompletionsModel, RunConfig
import os
from dotenv import load_dotenv
from openai import AsyncOpenAI

load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")
gemini_base_url = os.getenv("GEMINI_BASE_URL")
gemini_base_model = os.getenv("GEMINI_MODEL_NAME")

#

client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url=gemini_base_url,
)

model = OpenAIChatCompletionsModel(
    openai_client=client,
    model=str(gemini_base_model),
)

run_config = RunConfig(
    model=model,
)