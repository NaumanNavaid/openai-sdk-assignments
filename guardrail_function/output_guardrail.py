from agents import output_guardrail, RunContextWrapper, GuardrailFunctionOutput, Runner
from my_agent.guardrail_agent import output_guardrail_agent
from my_config.gemini_config import run_config

@output_guardrail
async def guardrail_output_function(ctx: RunContextWrapper, agent, output: str):
    # Run the output guardrail agent
    result = await Runner.run(
        output_guardrail_agent,
        input=output,
        context=ctx.context,
        run_config=run_config
    )
    

    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=result.final_output.is_answer_69
    )
