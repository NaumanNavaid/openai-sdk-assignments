# customer_support.py
from agents import Agent, RunContextWrapper, TContext, handoff, AgentHooks, ModelSettings
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX
from pydantic import BaseModel
from tools.my_tool import get_order_status  # <-- import your function tool
from my_config.gemini_config import model
from guardrail_function.second_input_guardrail import customer_support_input_guardrail
# -------------------------------
# Escalation Data Schema (for handoff)
# -------------------------------
class EscalationData(BaseModel):
    reason: str

class MyAgentHooks(AgentHooks):
    async def on_handoff(
        self,
        context: RunContextWrapper[TContext],
        agent: Agent,
        source: Agent,
    ) -> None:
        """Called when the agent is being handed off to. The `source` is the agent that is handing off to this agent."""
        
        # You know handoff happened here
        print(f"Handoff triggered! Source agent: {source.name}, Target agent: {agent.name}")

# -------------------------------
# HumanAgent (escalation target)

human_agent = Agent(
    name="Human Support Agent",
    instructions=(
        "You are a human support specialist. "
        "Be empathetic and helpful when queries are escalated. "
        "Address the customer's concern directly and ask clarifying questions if needed. "
        "You have the following knowledge: "
        "- Return Policy: Customers can return products within 30 days of purchase if they are unused and in original packaging. "
        "- Refund Policy: Refunds are processed within 5-7 business days after the returned item is inspected and approved. "
        "- Exchange Policy: Exchanges are allowed within 30 days for items in original condition. "
        "Do NOT escalate or hand off again. "
        "Stay with the customer until they confirm their issue is resolved by saying 'done', 'thank you', or 'resolved'."
    ),
    model=model,
     tools=[get_order_status],  
         input_guardrails=[customer_support_input_guardrail],  # ✅ check for offensive input
    model_settings=ModelSettings(tool_choice="auto")

)

# -------------------------------

# -------------------------------
bot_agent = Agent(
    name="Support Bot",
    instructions=f"""
You are the frontline support bot.

Capabilities:
- Answer simple product FAQs politely.
- If the query is about an order (tracking, status), call the `get_order_status` tool.
- If the customer wants to talk to a human or ask for a refund, hand off the conversation to the human agent.
When escalating, always provide a short reason string in the `reason` field.
""",
    model=model,
    tools=[get_order_status],  # ✅ attach the tool here
    handoffs=[human_agent],
    input_guardrails=[customer_support_input_guardrail],  # ✅ check for offensive input
    hooks=MyAgentHooks(),
    model_settings=ModelSettings(tool_choice="auto")
) 
