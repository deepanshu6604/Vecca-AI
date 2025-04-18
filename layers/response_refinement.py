import google.generativeai as genai
from config import GENAI_MODEL_NAME, GENAI_MAX_TOKENS, GENAI_TEMPERATURE

class NLGSecondary:
    def __init__(self):
        self.model = genai.GenerativeModel(GENAI_MODEL_NAME)

    def refine_output(self,response,text):
        """Generates a human-like response using refined insights and factual memory."""
        system_prompt = f"""

        Refine the response to be concise, professional, and exude an alpha-male presence while preserving all key information. 
        Then, humanize it to align naturally with the user's input.

        User Input: {text}
        AI Response: {response}
        Generate a refined, humanized response strictly related to the user's input.
        YOU DON'T HAVE TO INTRODUCE YOURSELF AS AI ,YOU ARE HUMAN'S VIRTUAL BRAIN NAMED AS MR.REX .
        
        humanize response (only related to current user input):
        """

        try:
            response = self.model.generate_content(system_prompt, generation_config=genai.GenerationConfig(
                max_output_tokens=GENAI_MAX_TOKENS,
                temperature=GENAI_TEMPERATURE,
            ))
            response_text = response.text.strip() if hasattr(response, "text") else ""

            # Ensure the text is a valid JSON string
            response_text = response_text.replace("```json", "").replace("```", "").strip()
            return response_text

        except Exception as e:
            return f"NLG secondary Error: {e}"
        
response_refinement = NLGSecondary()        


        