import json
import os

class ContextRetriever:
    def __init__(self):
        # Load the mock knowledge base
        path = os.path.join("data", "knowledge_base.json")
        try:
            with open(path, "r") as f:
                self.kb = json.load(f)
        except FileNotFoundError:
            self.kb = []

    def retrieve(self, query_terms: list[str]) -> list[str]:
        """
        Simulates Vector Search. 
        Finds text chunks where keywords match the query terms.
        """
        results = []
        for entry in self.kb:
            # Check if any keyword in the entry matches our query terms (e.g. "Leo")
            if any(term.lower() in [k.lower() for k in entry["keywords"]] for term in query_terms):
                results.append(entry["text"])
        
        return results if results else ["General planetary alignment suggests balance."]
