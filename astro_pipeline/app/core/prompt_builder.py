class PromptBuilder:
    @staticmethod
    def build(name: str, zodiac: str, context: list[str], preferences: dict) -> str:
        """Aggregates all intelligent inputs into a single prompt."""
        
        context_str = "\n".join([f"- {c}" for c in context])
        prefs_str = ", ".join(preferences.get("preferences", []))
        
        prompt = f"""
        Act as a mystical astrologer. 
        User: {name} (Sign: {zodiac})
        
        User Context/Preferences: {prefs_str}
        
        Astrological Knowledge Base (Current Planetary Context):
        {context_str}
        
        Task: Generate a personalized daily insight for this user based on the context above. 
        Keep it uplifting but realistic. Limit to 2 sentences.
        """
        return prompt.strip()
