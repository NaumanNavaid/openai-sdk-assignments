from agents import input_guardrail,RunContextWrapper,GuardrailFunctionOutput,Runner
from my_agent.guardrail_agent import input_guardrail_agent, negative_input_guardrail_agent
from my_config.gemini_config import run_config

@input_guardrail
async def guardrial_input_function(ctx:RunContextWrapper,agent,input):

    result = await Runner.run(input_guardrail_agent, input=input, context=ctx.context, run_config=run_config)

    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=False if result.final_output.is_math else True
    )
    
 # guardrails/customer_support_guardrail.py

