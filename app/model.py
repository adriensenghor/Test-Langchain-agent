from langchain.chat_models import init_chat_model

def get_model(temperature: float = 0.0):
    return init_chat_model(
        "claude-sonnet-4-5-20250929",  # or a valid Claude model id you have access to
        temperature=temperature,
        timeout=10,
        max_tokens=1000,
    )

