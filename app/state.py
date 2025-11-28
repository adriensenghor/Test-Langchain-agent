from typing import TypedDict, Annotated, List, Optional
from langchain_core.messages import BaseMessage
import operator

# total=False makes all keys optional
class RealEstateProfile(TypedDict, total=False):
    where: str      # Location
    when: str       # Timing/Date
    budget: str     # Budget amount
    how: str        # Financing method

def merge_profile(current: RealEstateProfile, update: RealEstateProfile) -> RealEstateProfile:
    """Merges profile updates, keeping existing values if update is None."""
    # Ensure current is a dict (it might be None initially)
    current_dict = dict(current) if current else {}
    
    if not update:
        return current_dict
    
    # Update only with non-None values
    for key, value in update.items():
        if value is not None and value != "":
            current_dict[key] = value
            
    return current_dict

class LeadScore(TypedDict, total=False):
    score: int           # Score de 0 à 100
    reasoning: str       # Pourquoi ce score ?

class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], operator.add]
    profile: Annotated[RealEstateProfile, merge_profile]
    score: LeadScore     # Regroupé comme profile