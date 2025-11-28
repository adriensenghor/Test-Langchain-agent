from langchain_anthropic import ChatAnthropic

def get_model(temperature=0):
    # Claude 3.5 Sonnet est le meilleur ratio coût/intelligence
    return ChatAnthropic(
        model="claude-3-5-sonnet-latest",
        temperature=temperature
    )