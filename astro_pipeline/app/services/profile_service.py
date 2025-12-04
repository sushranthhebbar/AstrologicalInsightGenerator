import json
import os

class ProfileService:
    def __init__(self):
        path = os.path.join("data", "user_profiles.json")
        try:
            with open(path, "r") as f:
                self.db = json.load(f)
        except FileNotFoundError:
            self.db = {}

    def get_profile(self, name: str) -> dict:
        return self.db.get(name, {"preferences": ["general"], "history": "unknown"})
