from langsmith import Client
from langchain.smith import RunEvalConfig, run_on_dataset
from app.graph import app as agent_app

# Définir un évaluateur personnalisé pour vérifier si le budget est bien capturé
def check_budget_capture(run, example):
    # Récupérer l'état final du profil dans le run
    agent_profile = run.outputs.get("profile", {})
    expected_budget = example.outputs.get("budget")
    
    if agent_profile.get("budget") == expected_budget:
        return {"key": "budget_accuracy", "score": 1}
    return {"key": "budget_accuracy", "score": 0}

client = Client()

eval_config = RunEvalConfig(
    custom_evaluators=[check_budget_capture]
)

# Lancer le test sur votre dataset "Immo Dataset"
run_on_dataset(
    client=client,
    dataset_name="Immo Dataset",
    llm_or_chain_factory=agent_app,
    evaluation=eval_config,
)