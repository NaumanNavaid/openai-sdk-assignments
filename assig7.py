import os
from dotenv import load_dotenv
from tavily import TavilyClient
from agents import Agent, function_tool, Runner, set_tracing_disabled, InputGuardrailTripwireTriggered, OutputGuardrailTripwireTriggered
from my_config.gemini_config import model, run_config

load_dotenv()
set_tracing_disabled(True)

# ------------------------------
# Initialize Tavily Client
# ------------------------------
api_key = os.getenv("TAVILY_API_KEY")

# Initialize Tavily client
try:
    tavily_client = TavilyClient(api_key=api_key)
    # Test the connection with a simple query
    test_response = tavily_client.search("test", max_results=1)
    api_key_valid = True
    api_key_message = "Tavily client initialized successfully"
except Exception as e:
    api_key_valid = False
    api_key_message = f"Failed to initialize Tavily client: {str(e)}"
    tavily_client = None

# ------------------------------
# Check if query should trigger web search
# ------------------------------
def is_web_search_query(ctx, agent) -> bool:
    if not api_key_valid:
        return False
        
    text = (ctx.context.get("text_input") or "").lower()
    
    search_triggers = [
        "latest", "recent", "current", "today", "now", "202", "update",
        "news", "find", "search", "web", "internet", "online", "look up",
        "current events", "breaking news", "recent developments"
    ]
    
    question_words = ["what", "when", "where", "who", "how", "why"]
    if any(text.startswith(word) for word in question_words):
        return True
        
    return any(trigger in text for trigger in search_triggers)

# ------------------------------
# Tavily Web Search function using SDK
# ------------------------------
@function_tool(
    is_enabled=is_web_search_query,
    failure_error_function=lambda query, *args, **kwargs: f"Sorry, I couldn't retrieve results for '{query}' from the web.",
)
def tavily_search(query: str, max_results: int = 5):
    if not api_key_valid or tavily_client is None:
        return f"Web search unavailable: {api_key_message}"
    
    try:
        # Use the Tavily SDK to perform the search
        response = tavily_client.search(
            query=query,
            max_results=max_results,
            search_depth="advanced",  # or "basic" for faster results
            include_answer=True,
            include_images=False
        )
        
        # Format the results
        if response.get('answer'):
            result_text = f"📝 Direct Answer: {response['answer']}\n\n"
        else:
            result_text = ""
            
        if response.get('results'):
            result_text += "🔍 Search Results:\n\n"
            for i, result in enumerate(response['results'][:max_results], 1):
                title = result.get('title', 'No title')
                content = result.get('content', 'No content available')
                url = result.get('url', 'No URL')
                
                result_text += f"{i}. **{title}**\n"
                result_text += f"   {content[:150]}...\n"
                result_text += f"   📎 Source: {url}\n\n"
        else:
            result_text = "No results found for your query. Please try rephrasing or ask about a different topic."
            
        return result_text

    except Exception as e:
        return f"Error performing web search: {str(e)}. Please try again later."

# ------------------------------
# Web Search Agent
# ------------------------------
web_search_agent = Agent(
    name="Web Search Bot",
    instructions="""
You are a helpful web search assistant specializing in current information.

CAPABILITIES:
- When the user asks for something requiring up-to-date info, call the `tavily_search` tool.
- Analyze search results and provide concise, informative summaries.
- Always cite your sources when using web search results.
- If search results are limited, provide helpful context based on your knowledge.

GUIDELINES:
- Be concise but informative in your responses.
- Focus on the most relevant information from search results.
- If multiple sources conflict, mention this and provide balanced information.
- For technical topics, prioritize authoritative sources.
""",
    model=model,
    tools=[tavily_search],
    handoffs=[],
)

# ------------------------------
# Async Chat Loop
# ------------------------------
async def main():
    print("💬 Web Search Bot is running (type 'exit' to quit)...\n")
    
    if api_key_valid:
        print(f"Web search functionality is enabled!")
        print(f"API Key: {api_key[:10]}...{api_key[-4:]}" if api_key else "No API key")
    else:
        print(f"  WEB SEARCH DISABLED: {api_key_message}")
        print("To enable web search, check your Tavily API key in the .env file\n")
    
    current_agent = web_search_agent
    print(f"👉 Currently talking to: {current_agent.name}")
    print("\nTry asking about current events, news, or recent developments!\n")

    while True:
        try:
            text_input = input("You: ").strip()
            if text_input.lower() in ['exit', 'quit', 'bye']:
                print(" Exiting...")
                break
            if not text_input:
                continue

            result = await Runner.run(
                starting_agent=current_agent,
                input=text_input,
                run_config=run_config,
                context={"text_input": text_input}
            )

            print(f"\n{current_agent.name}: {result.final_output}\n")

        except InputGuardrailTripwireTriggered:
             print("Blocked: Your message contained offensive or disallowed input.\n")

        except OutputGuardrailTripwireTriggered:
            print(" Blocked: Bot tried to generate unsafe content.\n")
        
        except Exception as e:
            print(f"Error: {str(e)}\n")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())