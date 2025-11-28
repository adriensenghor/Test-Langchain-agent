from pydantic import BaseModel, Field
from typing import Optional
from app.state import AgentState, RealEstateProfile
from app.model import get_model
from app.prompts import SYSTEM_PROMPT

# Définition Pydantic pour l'extraction (Structured Output)
class ProfileUpdate(BaseModel):
    """Mise à jour des infos du profil immobilier."""
    budget: Optional[str] = Field(description="Budget mentionné (ex: 300k, 250000 euros)")
    location: Optional[str] = Field(description="Ville ou quartier recherché")
    maturity: Optional[str] = Field(description="Urgence du projet (ex: 6 mois, urgent)")

# --- NODE 1: EXTRACTEUR ---
def extract_info_node(state: AgentState):
    model = get_model(temperature=0)
    
    # On force Claude à sortir du JSON structuré selon ProfileUpdate
    extractor = model.with_structured_output(ProfileUpdate)
    
    # On lui donne juste le dernier message de l'utilisateur pour analyse
    last_message = state["messages"][-1]
    result = extractor.invoke([last_message])
    
    # On fusionne avec les données existantes
    current_profile = state.get("profile", {})
    new_profile = {
        "budget": result.budget or current_profile.get("budget"),
        "location": result.location or current_profile.get("location"),
        "maturity": result.maturity or current_profile.get("maturity"),
    }
    
    return {"profile": new_profile}

# --- NODE 2: CHATBOT ---
def chatbot_node(state: AgentState):
    model = get_model(temperature=0.7) # Un peu plus créatif pour la conversation
    
    # Formatter le prompt avec le profil actuel
    prompt = SYSTEM_PROMPT.format(profile=state["profile"])
    
    messages = [{"role": "system", "content": prompt}] + state["messages"]
    response = model.invoke(messages)
    
    return {"messages": [response]}