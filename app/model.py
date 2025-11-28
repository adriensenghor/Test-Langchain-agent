from langchain_anthropic import ChatAnthropic

def get_model(temperature=0):
    # Claude 3.5 Sonnet est le meilleur ratio coût/intelligence
    return ChatAnthropic(
        "claude-sonnet-4-5-20250929",
        temperature=temperature
    )