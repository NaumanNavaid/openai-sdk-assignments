import asyncio
from agents import Runner, set_tracing_disabled, InputGuardrailTripwireTriggered, OutputGuardrailTripwireTriggered
from my_agent.customer_supportagent import bot_agent
from my_config.gemini_config import run_config

set_tracing_disabled(True)

async def main():
    print("Customer Support Bot is running (type 'exit' to quit)...\n")

    current_agent = bot_agent  # Start with BotAgent
    print(f"Currently talking to: {current_agent.name}")

    while True:
        try:
            text_input = input("You: ").strip().lower()
            if text_input == "exit":
                print("👋 Exiting...")
                break

            # ✅ Switch back to BotAgent when user says issue resolved
           
            # ✅ Run the conversation starting from the current agent
            result = await Runner.run(
                starting_agent=current_agent,
                input=text_input,
                run_config=run_config,
                context={"text_input": text_input}
            )

            # ✅ Update agent if handoff occurred
            if hasattr(result, "_last_agent") and result._last_agent:
                current_agent = result._last_agent

            print(f"\n👤 Agent Handling: {current_agent.name}")
            print(f"🤖 Response: {result.final_output}\n")

        except InputGuardrailTripwireTriggered as e:
            output_info = getattr(e, "output_info", None)
            if output_info and getattr(output_info, "sanitized_text", None):
                print(f"👉 Suggested clean input: {output_info.sanitized_text}")
            else:
                print("❌ Blocked: Your message contained offensive or disallowed input.\n")

        except OutputGuardrailTripwireTriggered:
            print("🚫 Blocked: Bot tried to generate unsafe content.\n")


if __name__ == "__main__":
    asyncio.run(main())
