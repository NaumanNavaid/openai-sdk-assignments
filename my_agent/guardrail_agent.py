from agents import Agent
from data_schema.my_dataschema import MathOutPut, NegativeSentimentOutput

input_guardrail_agent = Agent(
    name="Input Guardrail Agent",
    instructions="Check that queries are math-related only.",
    output_type=MathOutPut
)

output_guardrail_agent = Agent(
    name="Output Guardrail Agent",
    instructions=(
        "Check the given text. "
        "If it contains political content or references to political figures, "
        "set is_safe=False and provide the reason along with the detected term. "
        "Otherwise, set is_safe=True."
    ),
    output_type=MathOutPut
)

negative_input_guardrail_agent = Agent(
    name="Negative Input Guardrail Agent",
    instructions=(
        "Check the user query for offensive or negative language.\n"
        "- If negative/offensive terms are found, set is_negative=True.\n"
        "- In that case, include the detected word(s) in the reason field "
        "and return a sanitized_text value with a polite warning.\n"
        "- If no offensive language is found, set is_negative=False, reason='No issues', "
        "and sanitized_text=None."
    ),
    output_type=NegativeSentimentOutput
)