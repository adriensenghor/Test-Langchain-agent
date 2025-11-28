from pydantic import BaseModel, Field
from typing import Optional
from app.state import AgentState, RealEstateProfile
from app.model import get_model
from app.prompts import SYSTEM_PROMPT

# Définition Pydantic pour l'extraction (Structured Output)
class ProfileUpdate(BaseModel):
    """Mise à jour des infos du profil immobilier."""
    where: Optional[str] = Field(
        description="Où la personne veut acheter. Si ce n'est pas précisé, laisse cette valeur vide."
    )
    when: Optional[str] = Field(
        description="Quand (délai, date, horizon). Si ce n'est pas précisé, laisse cette valeur vide."
    )
    budget: Optional[str] = Field(
        description="Budget mentionné (ex: 300k, 250000 euros). Si ce n'est pas précisé, laisse cette valeur vide."
    )
    how: Optional[str] = Field(
        description="Comment le projet sera financé (prêt, cash, etc.). Si ce n'est pas précisé, laisse cette valeur vide."
    )

# --- NODE 1: EXTRACTEUR ---
def extract_info_node(state: AgentState):
    model = get_model(temperature=0)
    
    extractor = model.with_structured_output(ProfileUpdate)
    last_message = state["messages"][-1]
    result = extractor.invoke([last_message])
    
    # Create update dict
    update = {
        "where": result.where,
        "when": result.when,
        "budget": result.budget,
        "how": result.how
    }
    
    # Filter out None values immediately
    # This ensures we send {"where": "Madrid"} instead of {"where": "Madrid", "budget": None}
    clean_update = {k: v for k, v in update.items() if v is not None and v != ""}
    
    return {"profile": clean_update}

# --- NODE 2: CHATBOT ---
def chatbot_node(state: AgentState):
    model = get_model(temperature=0.7) # Un peu plus créatif pour la conversation
    
    # Formatter le prompt avec le profil actuel
    prompt = SYSTEM_PROMPT.format(profile=state["profile"])
    
    messages = [{"role": "system", "content": prompt}] + state["messages"]
    response = model.invoke(messages)
    
    return {"messages": [response]}