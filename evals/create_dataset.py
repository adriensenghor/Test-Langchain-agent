import json
from langsmith import Client

# Initialisation du client (lit vos clés .env automatiquement)
client = Client()

def create_dataset():
    dataset_name = "Immo Extraction Benchmark"
    
    # 1. Vérifier si le dataset existe déjà pour éviter les doublons
    if client.has_dataset(dataset_name=dataset_name):
        print(f"Le dataset '{dataset_name}' existe déjà.")
        return

    # 2. Création du dataset
    dataset = client.create_dataset(
        dataset_name=dataset_name,
        description="Dataset de test pour l'extraction de données immobilières (Anthropic)"
    )
    
    # 3. Chargement du JSON
    try:
        with open("data/dataset.json", "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print("Erreur: Le fichier data/dataset.json est introuvable.")
        return

    # 4. Création des exemples dans LangSmith
    inputs = [item["inputs"] for item in data]
    outputs = [item["outputs"] for item in data]
    
    client.create_examples(
        inputs=inputs,
        outputs=outputs,
        dataset_id=dataset.id,
    )
    
    print(f"Succès ! {len(data)} exemples uploadés dans le dataset '{dataset_name}'.")

if __name__ == "__main__":
    create_dataset()