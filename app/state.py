from typing import TypedDict, Annotated, List, Optional
from langchain_core.messages import BaseMessage
import operator

class RealEstateProfile(TypedDict):
    budget: Optional[str]
    location: Optional[str]
    maturity: Optional[str]

class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], operator.add]
    profile: RealEstateProfile