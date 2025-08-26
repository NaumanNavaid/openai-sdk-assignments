from agents import TResponseInputItem, input_guardrail, RunContextWrapper, GuardrailFunctionOutput, Runner
from my_agent.guardrail_agent import negative_input_guardrail_agent
from my_config.gemini_config import run_config

@input_guardrail
async def customer_support_input_guardrail(
    ctx: RunContextWrapper,
    agent,
    user_input: "str | list[TResponseInputItem]"
) -> GuardrailFunctionOutput:
    """
    Runs user input through the Negative Input Guardrail Agent.
    If negative/offensive language is detected, tripwire is triggered.
    Otherwise, allow the input to pass unchanged.
    """

    # Run the input guardrail agent to check sentiment
    result = await Runner.run(
        negative_input_guardrail_agent,
        input=user_input,
        context=ctx.context,
        run_config=run_config,
    )

    guardrail_output = result.final_output  # Expected to be a NegativeSentimentOutput object

    # Decide if we trigger tripwire
    triggered = getattr(guardrail_output, "is_negative", False)

    return GuardrailFunctionOutput(
        output_info=guardrail_output,    # full structured info (is_negative, reason, sanitized_text)
        tripwire_triggered=triggered     # True if negativity was detected
    )
