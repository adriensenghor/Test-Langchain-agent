from pydantic import BaseModel, Field
from typing import Optional
from app.state import AgentState
from app.model import get_model
from langsmith import traceable  # si tu veux tracer

# Structure de sortie du score (interne au scoring)
class ScoreResult(BaseModel):
    score: Optional[float] = Field(description="Score de 0.0 à 1.0, ou null si pas assez d'informations pour scorer")
    comment: str = Field(description="Raisonnement concis. Si score <0.3 (désengagement explicite), mentionner 'drop'. Si score est null, expliquer pourquoi.")

def score_node(state: AgentState):
    # 1. Récupération des données
    if not state.get("messages"):
        return {}  # Pas de message → pas de score
    
    last_message = state["messages"][-1]
    # Gérer le cas où content peut être une string ou autre chose
    raw_message = getattr(last_message, "content", str(last_message))
    if not isinstance(raw_message, str):
        raw_message = str(raw_message)
    
    profile = state.get("profile", {})  # TypedDict est déjà un dict
    
    # 2. Config du modèle
    model = get_model(temperature=0)
    scorer = model.with_structured_output(ScoreResult)
    
    # 3. Prompt spécialisé
    system_prompt = """
You are a real estate assistant helping people buy property in Spain. The user messages are in French, but you are evaluating their lead quality.

Score the lead's maturity (0.0 to 1.0) based on the following weighted criteria:

**SCORING CRITERIA:**
1. **Need Clarity (0.25):** Defined property type vs. vague idea.
2. **Explicit Budget (0.25):** Stated range/amount vs. "no idea".
3. **Market Realism (0.15):** Budget aligns with Spanish market reality.
4. **Location (0.15):** Specific city/region vs. generic "Spain".
5. **Timing/Intent (0.20):** <6 months/concrete project vs. pure curiosity.

**MODIFIERS (+/- 0.10):**
- **Bonus:** Financing ready, asks technical questions, known deadline.
- **Malus:** Vagueness, hesitation, impossible requests, refusal to answer.

**CRITICAL RULES:**
- **If you don't have enough information to score:** Return `null` for the score and explain why in the comment.
- **Score < 0.3 and "drop" ONLY for explicit disengagement:** A score below 0.3 should ONLY be given when the user explicitly expresses they want to stop or are not interested. Examples: "Je ne veux pas continuer", "stop", "arrêtez", "je ne suis plus intéressé", "annuler", etc. In these cases, always mention "drop" in the comment.
- **Minimum score of 0.3 for engaged users:** If the user is providing ANY information (even vague) about their real estate project (location, budget, timing, property type, etc.), the minimum score is 0.3. Only give scores below 0.3 if the user explicitly wants to stop the conversation.
- **Minimum score of 0.75 if 3+ fields are filled:** If at least 3 out of the 4 profile fields are filled (where, when, budget, how), the minimum score is 0.75. This indicates a well-qualified lead.

**SCORE INTERPRETATION:**
- **0.0 - 0.29:** Drop - ONLY when user explicitly wants to stop (mention "drop" in comment)
- **0.3 - 0.74:** Medium quality - User is engaged and providing information, continue qualification
- **0.75 - 1.0:** High quality - Strong lead with clear requirements (minimum 0.75 if 3+ fields filled)

ACTUAL PROFILE : {profile}
RECEIVED MESSAGE (in French) : "{user_message}"
"""
    
    # 4. Appel
    prompt = system_prompt.format(
        profile=profile,
        user_message=raw_message
    )
    result = scorer.invoke([{"role": "user", "content": prompt}])
    
    # Logger dans LangSmith (optionnel mais utile)
    score_data = {
        "score": result.score,  # Peut être None maintenant
        "reasoning": result.comment
    }
    
    # 5. Retour vers l'état global (groupé comme profile)
    return {
        "score": score_data
    }