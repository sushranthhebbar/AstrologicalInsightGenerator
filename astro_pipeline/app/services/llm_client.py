# To use real OpenAI: import openai
import random

class LLMClient:
    async def generate_insight(self, prompt: str) -> str:
        """
        Stub for LLM generation. 
        Replace this with `openai.ChatCompletion.create(...)`
        """
        # simulating network delay
        # await asyncio.sleep(0.5) 
        
        print(f"[LLM] Received Prompt:\n{prompt}\n")
        
        # Mock Response
        return "Based on the alignment of the stars and your career focus, today is an excellent day to take bold risks. Your natural leadership will guide you through uncertainty."
