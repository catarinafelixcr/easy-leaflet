from dotenv import load_dotenv
from google import genai


# The worker that talks to the LLM
class LLMClient:

    def __init__(self, model="gemini-3.8-flash"):
        # Read the .env file, so the library can find GEMINI_API_KEY
        load_dotenv()
        self.model = model
        self.client = genai.Client()

    def ask(self, prompt):
        # Send the prompt to the LLM and return the answer as text
        # TODO
        pass