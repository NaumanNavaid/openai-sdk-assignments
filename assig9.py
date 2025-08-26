# runner.py

from agents import Runner, set_tracing_disabled
from my_agent.hotel_assistant import hotel_assistant
from my_config.gemini_config import run_config

set_tracing_disabled(True)

if __name__ == "__main__":
    print("Hotel Assistant is running. Type 'exit' to quit.\n")

    while True:
        input_text = input("Enter your query: ").strip()
        if input_text.lower() in ["exit", "quit"]:
            print("Goodbye 👋")
            break

        res = Runner.run_sync(
            starting_agent=hotel_assistant,
            input=input_text,
            run_config=run_config,
            context={"user_input": input_text}
        )

        print(f"Assistant: {res.final_output}\n")
