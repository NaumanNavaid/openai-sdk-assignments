import asyncio
from agents import (
    Agent,
    InputGuardrailTripwireTriggered,
    OutputGuardrailTripwireTriggered,
    Runner,
    set_tracing_disabled
)
from guardrail_function.input_guardrail import guardrial_input_function
from guardrail_function.output_guardrail import guardrail_output_function
from my_config.gemini_config import run_config


set_tracing_disabled(True)  # Disable tracing for cleaner output
# Agent with both input + output guardrails
guardrail_agent = Agent(
    name="GuardrailAgent",
    instructions="you are a helpful agent .",
    input_guardrails=[guardrial_input_function],     # ✅ input check
    output_guardrails=[guardrail_output_function],   # ✅ output check
)


async def main():
    while True:
        try:
            msg = input("Enter your question (or type 'exit' to quit): ")
            if msg.lower().strip() == "exit":
                print("Exiting...")
                break

            result = await Runner.run(guardrail_agent, msg, run_config=run_config)
            print(f"\n\nFinal output: {result.final_output}")

        except InputGuardrailTripwireTriggered:
            print(" Error: invalid prompt (blocked by input guardrail).")

        except OutputGuardrailTripwireTriggered as ex:
            print(" Error: unsafe response (blocked by output guardrail).")
            

asyncio.run(main())



