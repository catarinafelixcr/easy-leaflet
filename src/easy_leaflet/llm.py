from dotenv import load_dotenv
from google import genai
from google.genai import types

# The worker that talks to the LLM
class LLMClient:

    def __init__(self, model="gemini-3.5-flash-lite"):
        # Read the .env file, so the library can find GEMINI_API_KEY
        load_dotenv()
        self.model = model
        # Stop waiting after 60 seconds, so the app never hangs
        self.client = genai.Client(http_options=types.HttpOptions(timeout=60000))

  
    def ask(self, prompt):
        # Send the prompt to the LLM and return the answer as text
        interaction = self.client.interactions.create(  # sends prompt over the internet to Google. We tell it which model and what text.
            model=self.model, input=prompt,
        )
        return interaction.output_text  # is only the answer tex